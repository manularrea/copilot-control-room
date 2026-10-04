"""Port of legacy/daily_close.sql; preserve the business calendar."""
from app.ledger import business_day


def summarize(events, day):
    totals = {}
    for event in events:
        if event['status'] != 'settled' or event['occurred_at'][:10] != day:
            continue
        sign = -1 if event['kind'] == 'refund' else 1
        currency = event['currency']
        totals[currency] = totals.get(currency, 0) + sign * event['amount_minor']
    return dict(sorted(totals.items()))
