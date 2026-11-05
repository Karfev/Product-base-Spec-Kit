import importlib.util
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

MODULE_PATH = Path(__file__).resolve().parents[1] / 'check-trace.py'
SPEC = importlib.util.spec_from_file_location('check_trace', MODULE_PATH)
check_trace = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_trace)

INIT = 'INIT-2026-010-demo'
REQ_ID = 'REQ-DEMO-001'


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


class RepositoryTestCase(unittest.TestCase):
    """Builds a temporary repository with one initiative."""

    def setUp(self):
        tmpdir = TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        self.root = Path(tmpdir.name)
        self.init_dir = self.root / 'initiatives' / INIT

    def write(self, relative_path: str, content: str) -> None:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def write_initiative(self, trace, status='proposed', profile='standard', parent=None, req_id=REQ_ID):
        directory = parent or self.init_dir
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'requirements.yml').write_text(yaml.safe_dump({
            'metadata': {'product': 'platform', 'profile': profile},
            'requirements': [{'id': req_id, 'status': status, 'trace': trace}],
        }))

    def write_trace_md(self, req_id=REQ_ID):
        (self.init_dir / 'trace.md').write_text(f'| {req_id} | link |\n')

    def run_checks(self, strict=False):
        errors, warnings, _, _ = check_trace.run_checks(self.root, strict)
        return errors, warnings


class SeverityTests(RepositoryTestCase):
    MISSING_TEST = {'tests': [f'tests/missing.spec.ts::{REQ_ID}']}

    def test_broken_link_is_error_for_implemented(self):
        self.write_initiative(self.MISSING_TEST, status='implemented')
        self.write_trace_md()
        errors, _ = self.run_checks()
        self.assertEqual(len(errors), 1)
        self.assertIn('test file not found', errors[0])

    def test_broken_link_is_error_for_verified(self):
        self.write_initiative(self.MISSING_TEST, status='verified')
        self.write_trace_md()
        self.assertEqual(len(self.run_checks()[0]), 1)

    def test_broken_link_is_warning_for_proposed(self):
        self.write_initiative(self.MISSING_TEST)
        self.write_trace_md()
        errors, warnings = self.run_checks()
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)

    def test_strict_turns_broken_link_into_error(self):
        self.write_initiative(self.MISSING_TEST)
        self.write_trace_md()
        self.assertEqual(len(self.run_checks(strict=True)[0]), 1)

    def test_empty_evidence_is_error_for_implemented(self):
        self.write_initiative({}, status='implemented')
        self.write_trace_md()
        errors, _ = self.run_checks()
        self.assertEqual(len(errors), 1)
        self.assertIn('no trace evidence', errors[0])

    def test_empty_evidence_is_warning_for_draft_even_when_strict(self):
        self.write_initiative({}, status='draft')
        self.write_trace_md()
        errors, warnings = self.run_checks(strict=True)
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)

    def test_deprecated_needs_no_evidence_or_trace_row(self):
        self.write_initiative({}, status='deprecated')
        self.assertEqual(self.run_checks(), ([], []))

    def test_missing_trace_row_is_error_for_implemented_standard(self):
        self.write('initiatives/%s/tests/a.spec.ts' % INIT, REQ_ID)
        self.write_initiative({'tests': [f'tests/a.spec.ts::{REQ_ID}']}, status='implemented')
        errors, _ = self.run_checks()
        self.assertEqual(len(errors), 1)
        self.assertIn('no entry in a trace.md of this initiative', errors[0])

    def test_missing_trace_row_is_warning_for_implemented_minimal(self):
        self.write('initiatives/%s/tests/a.spec.ts' % INIT, REQ_ID)
        self.write_initiative({'tests': [f'tests/a.spec.ts::{REQ_ID}']}, status='implemented', profile='minimal')
        errors, warnings = self.run_checks()
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)

    def test_unknown_req_id_in_trace_md_is_error(self):
        self.write_initiative({})
        self.write_trace_md('REQ-OTHER-001')
        self.assertIn('not found', self.run_checks()[0][0])

    def test_archived_initiative_is_skipped(self):
        self.init_dir.mkdir(parents=True)
        (self.init_dir / 'requirements.yml').write_text(yaml.safe_dump({
            'metadata': {'initiative_status': 'archived'},
            'requirements': [{'id': REQ_ID, 'status': 'implemented', 'trace': {}}],
        }))
        self.assertEqual(self.run_checks(), ([], []))

    def test_template_initiative_is_skipped(self):
        self.write_initiative({}, status='implemented', parent=self.root / 'initiatives' / '{INIT-YYYY-NNN-slug}')
        self.assertEqual(self.run_checks(), ([], []))

    def test_examples_are_checked_but_do_not_join_registry(self):
        example = self.root / 'examples' / 'INIT-2026-099-demo'
        self.write_initiative(
            {'tests': ['tests/missing.spec.ts::REQ-DEMO-002']}, parent=example, req_id='REQ-DEMO-002'
        )
        self.write_initiative({})
        self.write_trace_md('REQ-DEMO-002')
        errors, warnings = self.run_checks()
        self.assertTrue(any('REQ-DEMO-002' in e and 'not found in any' in e for e in errors))
        self.assertTrue(any('examples' in w and 'test file not found' in w for w in warnings))


class PerInitiativeCoverageTests(RepositoryTestCase):
    OTHER = 'INIT-2026-011-other'
    EVIDENCE = {'tests': [f'ext:other/test.ts::{REQ_ID}']}

    def write_other(self, trace_row=True, status='implemented'):
        self.write(f'initiatives/{self.OTHER}/requirements.yml', yaml.safe_dump({
            'metadata': {'initiative': self.OTHER, 'product': 'platform', 'profile': 'standard'},
            'requirements': [{'id': REQ_ID, 'status': status, 'delta': 'modified', 'base_rev': 1, 'trace': self.EVIDENCE}],
        }))
        if trace_row:
            self.write(f'initiatives/{self.OTHER}/trace.md', f'| {REQ_ID} | row |')

    def test_row_of_another_initiative_does_not_count(self):
        self.write_initiative(self.EVIDENCE, status='implemented')
        self.write_trace_md()
        self.write_other(trace_row=False)
        errors, _ = self.run_checks()
        self.assertEqual(len(errors), 1)
        self.assertIn(self.OTHER, errors[0])

    def test_each_initiative_has_its_own_row(self):
        self.write_initiative(self.EVIDENCE, status='implemented')
        self.write_trace_md()
        self.write_other()
        self.assertEqual(self.run_checks(), ([], []))

    def test_l4_row_counts_for_the_initiative_named_in_the_spec(self):
        self.write_initiative(self.EVIDENCE, status='implemented')
        self.write_trace_md()
        self.write_other(trace_row=False)
        self.write('.specify/specs/011-other/spec.md', f'**Initiative:** {self.OTHER}\n')
        self.write('.specify/specs/011-other/trace.md', f'| {REQ_ID} | row |')
        self.assertEqual(self.run_checks()[0], [])

    def test_l4_row_of_another_initiative_does_not_count(self):
        self.write_initiative(self.EVIDENCE, status='implemented')
        self.write_trace_md()
        self.write_other(trace_row=False)
        self.write('.specify/specs/010-demo/spec.md', f'**Initiative:** {INIT}\n')
        self.write('.specify/specs/010-demo/trace.md', f'| {REQ_ID} | row |')
        errors, _ = self.run_checks()
        self.assertEqual(len(errors), 1)
        self.assertIn(self.OTHER, errors[0])

    def test_l4_row_without_named_initiative_counts_for_all(self):
        self.write_initiative(self.EVIDENCE, status='implemented')
        self.write_other(trace_row=False)
        self.write('.specify/specs/010-demo/trace.md', f'| {REQ_ID} | row |')
        self.assertEqual(self.run_checks()[0], [])


class LinkResolutionTests(RepositoryTestCase):
    """A requirement in implemented status turns every broken link into an error."""

    def problems(self, trace):
        self.write_initiative(trace, status='implemented')
        self.write_trace_md()
        return self.run_checks()[0]

    def test_test_resolves_relative_to_initiative(self):
        self.write(f'initiatives/{INIT}/tests/a.spec.ts', f'// {REQ_ID}')
        self.assertEqual(self.problems({'tests': [f'tests/a.spec.ts::{REQ_ID}']}), [])

    def test_test_resolves_relative_to_root(self):
        self.write('tests/a.spec.ts', f'// {REQ_ID}')
        self.assertEqual(self.problems({'tests': [f'tests/a.spec.ts::{REQ_ID}']}), [])

    def test_test_tag_must_be_in_file(self):
        self.write('tests/a.spec.ts', '// nothing here')
        self.assertIn('not found in test file', self.problems({'tests': [f'tests/a.spec.ts::{REQ_ID}']})[0])

    def test_test_tag_must_match_requirement(self):
        self.write('tests/a.spec.ts', '// REQ-OTHER-001')
        self.assertIn('tagged for REQ-OTHER-001', self.problems({'tests': ['tests/a.spec.ts::REQ-OTHER-001']})[0])

    def test_external_test_is_accepted_without_a_file(self):
        self.assertEqual(self.problems({'tests': [f'ext:billing-api/tests/a.spec.ts::{REQ_ID}']}), [])

    def test_external_test_requires_matching_req_id(self):
        problems = self.problems({'tests': ['ext:billing-api/tests/a.spec.ts::REQ-OTHER-001']})
        self.assertIn('tagged for REQ-OTHER-001', problems[0])

    def test_external_test_requires_repo_and_path(self):
        self.assertIn('must look like', self.problems({'tests': [f'ext:billing-api::{REQ_ID}']})[0])

    def test_contract_pointer_resolves(self):
        self.write(f'initiatives/{INIT}/contracts/openapi.yaml', yaml.safe_dump({
            'paths': {'/keys/{id}': {'delete': {'responses': {204: {'description': 'ok'}}}}}
        }))
        trace = {'contracts': ['contracts/openapi.yaml#/paths/~1keys~1{id}/delete/responses/204']}
        self.assertEqual(self.problems(trace), [])

    def test_contract_fragment_without_leading_slash(self):
        self.write('contracts/asyncapi.yaml', yaml.safe_dump({'channels': {'assets.updated': {}}}))
        self.assertEqual(self.problems({'contracts': ['contracts/asyncapi.yaml#channels/assets.updated']}), [])

    def test_contract_pointer_missing(self):
        self.write('contracts/openapi.yaml', yaml.safe_dump({'paths': {}}))
        problems = self.problems({'contracts': ['contracts/openapi.yaml#/paths/~1ghost/post']})
        self.assertIn('fragment', problems[0])

    def test_contract_file_missing(self):
        self.assertIn('contract file not found', self.problems({'contracts': ['contracts/none.yaml']})[0])

    def test_contract_fragment_in_non_yaml_file_is_not_parsed(self):
        self.write('contracts/api.proto', 'message Ping {}')
        self.assertEqual(self.problems({'contracts': ['contracts/api.proto#Ping']}), [])

    def test_schema_and_view_files(self):
        self.write('contracts/a.schema.json', '{}')
        self.write('views/a.md', 'view')
        self.assertEqual(self.problems({
            'contracts': ['contracts/a.schema.json'],
            'schemas': ['contracts/a.schema.json'],
            'architecture_views': ['views/a.md#section'],
        }), [])

    def test_missing_schema_file(self):
        problems = self.problems({'tests': [f'ext:r/t.py::{REQ_ID}'], 'schemas': ['contracts/none.json']})
        self.assertIn('file not found', problems[0])

    def test_slo_in_multi_document_openslo(self):
        self.write('ops/slo.yaml', '---\nkind: SLI\nmetadata:\n  name: other\n---\nkind: SLO\nmetadata:\n  name: latency\n')
        self.assertEqual(self.problems({'slo': 'ops/slo.yaml#latency'}), [])

    def test_slo_name_of_non_slo_document_does_not_match(self):
        self.write('ops/slo.yaml', '---\nkind: SLI\nmetadata:\n  name: latency\n---\nkind: SLO\nmetadata:\n  name: other\n')
        self.assertIn("SLO 'latency' not found", self.problems({'slo': 'ops/slo.yaml#latency'})[0])

    def test_slo_in_slos_list(self):
        self.write('ops/slo.yaml', 'kind: SLO\nmetadata:\n  name: bundle\nslos:\n  - name: latency\n')
        self.assertEqual(self.problems({'slo': 'ops/slo.yaml#latency'}), [])

    def test_slo_file_missing(self):
        self.assertIn('SLO file not found', self.problems({'slo': 'ops/none.yaml#latency'})[0])

    def test_adr_by_full_id_in_initiative_product_and_root(self):
        self.write(f'initiatives/{INIT}/decisions/INIT-ADR-0001-a.md', 'adr')
        self.write('products/platform/decisions/PLAT-0003-b.md', 'adr')
        self.write('decisions/PLAT-0002-c.md', 'adr')
        self.assertEqual(self.problems({
            'tests': [f'ext:r/t.py::{REQ_ID}'],
            'adr': ['INIT-ADR-0001-a', 'PLAT-0003-b', 'PLAT-0002-c'],
        }), [])

    def test_adr_by_path(self):
        self.write(f'initiatives/{INIT}/decisions/a.md', 'adr')
        self.assertEqual(self.problems({
            'tests': [f'ext:r/t.py::{REQ_ID}'],
            'adr': [f'initiatives/{INIT}/decisions/a.md'],
        }), [])

    def test_adr_short_id_does_not_match_full_slug(self):
        self.write('decisions/PLAT-0002-c.md', 'adr')
        problems = self.problems({'tests': [f'ext:r/t.py::{REQ_ID}'], 'adr': ['PLAT-0002']})
        self.assertIn('ADR not found', problems[0])

    def test_prd_and_components_are_not_links(self):
        self.assertEqual(self.problems({
            'tests': [f'ext:r/t.py::{REQ_ID}'],
            'prd': 'prd.md#none',
            'components': ['service-a'],
        }), [])


if __name__ == '__main__':
    unittest.main()
