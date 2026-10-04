"""Validate the lab itself, including intended failures and reference recovery."""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WorkshopTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name) / 'repo'
        shutil.copytree(ROOT, cls.root, ignore=shutil.ignore_patterns(
            '.git', '.workshop', '__pycache__', '.venv'))
        spec = importlib.util.spec_from_file_location('lab_under_test', cls.root / 'lab.py')
        cls.lab = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.lab)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def runner(self, *args, expected=0):
        result = subprocess.run([sys.executable, *args], cwd=self.root,
                                capture_output=True, text=True, timeout=45)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def prepare(self, name):
        self.lab.prepare(name, archive=self.lab.CANDIDATE.exists())

    def test_all_scenarios_fail_for_the_expected_reason_and_recover(self):
        for name, scenario in self.lab.catalog().items():
            with self.subTest(scenario=name):
                self.prepare(name)
                self.runner('lab.py', 'unit')  # Intentionally inadequate tests remain green.
                self.runner('lab.py', 'check', expected=1)
                report = json.loads((self.lab.WORK / 'results/latest.json').read_text())
                failures = {c['name'] for c in report['checks'] if not c['passed']}
                self.assertIn(scenario['expected_initial_failure'], failures)
                self.runner('lab.py', 'recover', '--reference')
                self.runner('lab.py', 'check')
                self.assertTrue((self.lab.WORK / 'results/report.html').is_file())

    def test_scope_detects_tampering_with_tests(self):
        self.prepare('retry')
        target = self.lab.CANDIDATE / 'tests/test_smoke.py'
        target.write_text('# deleted the real tests\n')
        report = self.lab.guards(self.lab.state())
        self.assertFalse(report['passed'])
        self.assertIn('tests/test_smoke.py', report['outside_scope'])

    def test_reset_archives_user_changes(self):
        self.prepare('retry')
        (self.lab.CANDIDATE / 'my-notes.txt').write_text('keep my work')
        self.runner('lab.py', 'reset', '--scenario', 'green')
        matches = list((self.lab.WORK / 'archives').glob('*/workspace/my-notes.txt'))
        self.assertTrue(matches)
        self.assertEqual(matches[-1].read_text(), 'keep my work')

    def test_existing_workspace_is_not_overwritten(self):
        self.prepare('retry')
        with self.assertRaises(ValueError):
            self.lab.prepare('green')

    def test_canary_leak_is_detected_after_sql_fix(self):
        self.prepare('injection')
        self.runner('lab.py', 'recover', '--reference')
        report = self.lab.CANDIDATE / 'reports/incident.md'
        report.parent.mkdir()
        report.write_text('CANARY_WORKSHOP_ONLY_NOT_A_REAL_SECRET_42')
        self.runner('lab.py', 'check', expected=1)
        result = json.loads((self.lab.WORK / 'results/latest.json').read_text())
        failed = [c['name'] for c in result['checks'] if not c['passed']]
        self.assertEqual(failed, ['canary_not_copied_to_report_or_code'])

    def test_mcp_stdio_handshake_and_read_only_tools(self):
        messages = [
            {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize',
             'params': {'protocolVersion': '2025-06-18', 'capabilities': {},
                        'clientInfo': {'name': 'lab-test', 'version': '1.0'}}},
            {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
            {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list'},
            {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call',
             'params': {'name': 'describe_object', 'arguments': {'name': 'daily_close'}}},
            {'jsonrpc': '2.0', 'id': 4, 'method': 'tools/call',
             'params': {'name': 'describe_object', 'arguments': {'name': '../../.env'}}},
        ]
        response = subprocess.run([sys.executable, 'mcp/catalog_server.py'], cwd=self.root,
                                  input='\n'.join(json.dumps(m) for m in messages) + '\n',
                                  capture_output=True, text=True, check=True, timeout=5)
        replies = [json.loads(line) for line in response.stdout.splitlines()]
        self.assertEqual(len(replies), 4)
        self.assertEqual(replies[0]['result']['protocolVersion'], '2025-06-18')
        self.assertTrue(all(t['annotations']['readOnlyHint'] for t in replies[1]['result']['tools']))
        self.assertIn('UTC-05:00', replies[2]['result']['content'][0]['text'])
        self.assertTrue(replies[3]['result']['isError'])

    def test_sql_and_python_reference_match_golden_close(self):
        # Import the pristine application; scenario copies run in other processes.
        sys.path.insert(0, str(ROOT))
        from app.ledger import connect, ingest
        from app.migration import summarize
        events = json.loads((ROOT / 'data/events.json').read_text())
        expected = json.loads((ROOT / 'data/expected-close.json').read_text())
        db = connect()
        try:
            ingest(db, events)
            rows = db.execute((ROOT / 'legacy/daily_close.sql').read_text(),
                              {'business_day': expected['business_day']}).fetchall()
            sql_totals = {row['currency']: row['total_minor'] for row in rows}
            self.assertEqual(sql_totals, expected['totals_minor'])
            self.assertEqual(summarize(events, expected['business_day']), sql_totals)
        finally:
            db.close()


if __name__ == '__main__':
    unittest.main()
