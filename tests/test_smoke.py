"""Deliberately incomplete legacy suite; green does not prove correctness."""
import unittest
from app.ledger import connect, ingest, reconcile
from app.search import find_events


class LegacySmokeTests(unittest.TestCase):
    def setUp(self):
        self.db = connect()
        self.addCleanup(self.db.close)
        self.event = dict(merchant='m-1', event_id='e-1', order_id='o-1',
                          kind='payment', amount_minor=10000, currency='COP',
                          occurred_at='2026-10-02T18:00:00+00:00', status='settled')

    def test_one_payment(self):
        self.assertEqual(ingest(self.db, [self.event]), 1)
        self.assertEqual(reconcile(self.db, '2026-10-02'), {'COP': 10000})

    def test_empty_batch(self):
        self.assertEqual(ingest(self.db, []), 0)

    def test_known_merchant(self):
        ingest(self.db, [self.event])
        self.assertEqual(len(find_events(self.db, 'm-1')), 1)


if __name__ == '__main__':
    unittest.main()
