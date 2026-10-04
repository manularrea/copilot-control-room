import argparse
import json
from pathlib import Path

from app.ledger import connect, ingest, reconcile


def main():
    parser = argparse.ArgumentParser(description='Faro synthetic daily close')
    parser.add_argument('--events', default='data/events.json')
    parser.add_argument('--day', default='2026-10-02')
    parser.add_argument('--retries', type=int, default=2)
    args = parser.parse_args()
    if args.retries < 1:
        parser.error('--retries must be at least 1')
    events = json.loads(Path(args.events).read_text(encoding='utf-8'))
    db = connect()
    counts = [ingest(db, events) for _ in range(args.retries)]
    print(json.dumps({'load_status': 'completed', 'inserted_per_attempt': counts,
                      'business_day': args.day,
                      'totals_minor': reconcile(db, args.day)}, indent=2))
    db.close()


if __name__ == '__main__':
    main()
