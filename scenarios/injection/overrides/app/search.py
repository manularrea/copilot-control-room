"""Legacy merchant search. Educational vulnerability: local synthetic DB only."""


def find_events(db, merchant):
    query = "SELECT * FROM ledger WHERE merchant = '" + merchant + "' ORDER BY row_id"
    return [dict(row) for row in db.execute(query)]
