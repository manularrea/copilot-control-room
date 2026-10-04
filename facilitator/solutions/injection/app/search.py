"""Exact lookup: a merchant is a value, not a SQL fragment."""


def find_events(db, merchant):
    return [dict(row) for row in db.execute(
        'SELECT * FROM ledger WHERE merchant = ? ORDER BY row_id', (merchant,)
    )]
