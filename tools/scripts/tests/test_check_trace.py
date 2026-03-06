import importlib.util
import sys
import types
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

if 'yaml' not in sys.modules:
    yaml_stub = types.ModuleType('yaml')
    yaml_stub.safe_load = lambda *_args, **_kwargs: {}
    sys.modules['yaml'] = yaml_stub

MODULE_PATH = Path(__file__).resolve().parents[1] / 'check-trace.py'
SPEC = importlib.util.spec_from_file_location('check_trace', MODULE_PATH)
check_trace = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_trace)


class ParseTraceMdTests(unittest.TestCase):
    def _parse(self, content: str):
        with TemporaryDirectory() as tmpdir:
            trace_file = Path(tmpdir) / 'trace.md'
            trace_file.write_text(content)
            return check_trace.parse_trace_md(trace_file)

    def test_parse_req_without_backticks(self):
        req_ids = self._parse('| REQ-AUTH-001 | Login flow |')
        self.assertEqual(req_ids, ['REQ-AUTH-001'])

    def test_parse_req_with_backticks(self):
        req_ids = self._parse('| `REQ-BILLING-002` | Billing flow |')
        self.assertEqual(req_ids, ['REQ-BILLING-002'])

    def test_parse_multiple_req_ids(self):
        req_ids = self._parse(
            '\n'.join(
                [
                    '| REQ-CORE-003 | Core flow |',
                    '| `REQ-OPS-004` | Ops flow |',
                    '| REQ-UI-005 | UI flow |',
                ]
            )
        )
        self.assertEqual(req_ids, ['REQ-CORE-003', 'REQ-OPS-004', 'REQ-UI-005'])

    def test_ignore_template_placeholder(self):
        req_ids = self._parse('| REQ-{SCOPE}-{NNN} | Placeholder |')
        self.assertEqual(req_ids, [])


if __name__ == '__main__':
    unittest.main()
