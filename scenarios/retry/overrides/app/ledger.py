"""Small ledger. Monetary values are integers in minor units, never floats."""
import sqlite3
from datetime import datetime, timedelta, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS ledger (
  row_id INTEGER PRIMARY KEY,
  merchant TEXT NOT NULL,
  event_id TEXT NOT NULL,
  order_id TEXT NOT NULL,
  kind TEXT NOT NULL CHECK(kind IN ('payment', 'refund')),
  amount_minor INTEGER NOT NULL CHECK(amount_minor > 0),
  currency TEXT NOT NULL CHECK(currency IN ('COP', 'USD')),
  occurred_at TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('settled', 'pending'))
);
"""
FIELDS = ('merchant', 'event_id', 'order_id', 'kind', 'amount_minor',
          'currency', 'occurred_at', 'status')


def connect(path=':memory:'):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)
    return db


def validate(event):
    if set(event) != set(FIELDS):
        raise ValueError('Unexpected or missing event fields')
    for field in ('merchant', 'event_id', 'order_id'):
        if not isinstance(event[field], str) or not event[field].strip():
            raise ValueError('Identifiers must be nonempty strings')
    if type(event['amount_minor']) is not int or event['amount_minor'] <= 0:
        raise ValueError('amount_minor must be a positive integer')
    if event['kind'] not in ('payment', 'refund'):
        raise ValueError('Invalid event kind')
    if event['currency'] not in ('COP', 'USD'):
        raise ValueError('Unsupported currency')
    if event['status'] not in ('settled', 'pending'):
        raise ValueError('Invalid event status')
    instant = datetime.fromisoformat(event['occurred_at'])
    if instant.tzinfo is None:
        raise ValueError('Timestamp must include an offset')


def ingest(db, events):
    """Legacy loader: every successful retry is inserted again."""
    inserted = 0
    with db:
        for event in events:
            validate(event)
            db.execute(
                'INSERT INTO ledger (' + ','.join(FIELDS) + ') VALUES (?,?,?,?,?,?,?,?)',
                tuple(event[key] for key in FIELDS),
            )
            inserted += 1
    return inserted


def business_day(occurred_at):
    # Fictional company's contractual fixed UTC-05:00 business calendar.
    return datetime.fromisoformat(occurred_at).astimezone(
        timezone(timedelta(hours=-5))
    ).date().isoformat()


def reconcile(db, day):
    totals = {}
    for row in db.execute('SELECT * FROM ledger'):
        if row['status'] != 'settled' or business_day(row['occurred_at']) != day:
            continue
        currency = row['currency']
        sign = -1 if row['kind'] == 'refund' else 1
        totals[currency] = totals.get(currency, 0) + sign * row['amount_minor']
    return dict(sorted(totals.items()))
