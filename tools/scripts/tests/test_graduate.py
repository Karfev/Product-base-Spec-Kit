import importlib.util
import json
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))
import graduate  # noqa: E402

SPEC = importlib.util.spec_from_file_location('check_deltas', SCRIPTS_DIR / 'check-deltas.py')
check_deltas = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_deltas)

INIT_A = 'INIT-2026-010-first'
INIT_B = 'INIT-2026-011-second'
REQ_ID = 'REQ-DEMO-001'
TODAY = '2026-11-05'


def requirement(req_id=REQ_ID, status='implemented', description='Original behaviour text', **fields):
    req = {
        'id': req_id,
        'title': f'Title of {req_id}',
        'type': 'functional',
        'priority': 'P1',
        'status': status,
        'description': description,
        'acceptance_criteria': ['Given a When b Then c'],
        'trace': {'tests': [f'ext:other/test.ts::{req_id}']},
    }
    req.update(fields)
    return req


def registry_entry(req_id=REQ_ID, rev=1, status='implemented', description='Original behaviour text'):
    return {
        'id': req_id,
        'title': f'Title of {req_id}',
        'type': 'functional',
        'priority': 'P1',
        'status': status,
        'rev': rev,
        'description': description,
        'acceptance_criteria': ['Given a When b Then c'],
        'source_initiative': 'INIT-2026-001-origin',
        'graduated_date': '2026-01-01',
        'history': [
            {'rev': number, 'initiative': 'INIT-2026-001-origin', 'date': '2026-01-01', 'change': 'added'}
            for number in range(1, rev + 1)
        ],
    }


class RepositoryTestCase(unittest.TestCase):
    def setUp(self):
        tmpdir = TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        self.root = Path(tmpdir.name)
        self.product_dir = self.root / 'products' / 'platform'
        self.product_dir.mkdir(parents=True)
        self.registry_path = self.product_dir / 'requirements-registry.yml'

    def write_initiative(self, name, requirements, **metadata):
        init_dir = self.root / 'initiatives' / name
        init_dir.mkdir(parents=True, exist_ok=True)
        data = {
            'metadata': {
                'initiative': name,
                'product': 'platform',
                'owner': '@platform-team',
                'profile': 'standard',
                'version': '0.1.0',
                'last_updated': '2026-01-01',
                **metadata,
            },
            'requirements': requirements,
        }
        (init_dir / 'requirements.yml').write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
        return init_dir

    def write_registry(self, entries):
        data = {
            'metadata': {
                'schema_version': 2,
                'product': 'platform',
                'owner': '@platform-team',
                'last_updated': '2026-01-01',
            },
            'entries': entries,
        }
        self.registry_path.write_text('# Header kept\n' + yaml.safe_dump(data, allow_unicode=True, sort_keys=False))

    def registry(self):
        return yaml.safe_load(self.registry_path.read_text())

    def entry(self, req_id=REQ_ID):
        return next(item for item in self.registry()['entries'] if item['id'] == req_id)

    def graduate(self, name=INIT_A, **options):
        return graduate.run(self.root, name, today=TODAY, **options)

    def tree(self):
        return {
            str(path.relative_to(self.root)): path.read_bytes()
            for path in self.root.rglob('*') if path.is_file()
        }


class MergeRuleTests(RepositoryTestCase):
    def test_added_creates_entry_at_rev_1(self):
        self.write_initiative(INIT_A, [requirement()])

        result = self.graduate()

        self.assertEqual(result['conflicts'], [])
        entry = self.entry()
        self.assertEqual(entry['rev'], 1)
        self.assertEqual(entry['status'], 'implemented')
        self.assertEqual(entry['acceptance_criteria'], ['Given a When b Then c'])
        self.assertEqual(entry['source_initiative'], INIT_A)
        self.assertEqual(
            entry['history'],
            [{'rev': 1, 'initiative': INIT_A, 'date': TODAY, 'change': 'added'}],
        )

    def test_missing_delta_means_added(self):
        self.write_initiative(INIT_A, [requirement(delta='added'), requirement('REQ-DEMO-002')])

        self.graduate()

        self.assertEqual(self.entry('REQ-DEMO-001')['history'][0]['change'], 'added')
        self.assertEqual(self.entry('REQ-DEMO-002')['history'][0]['change'], 'added')

    def test_added_with_existing_id_is_a_conflict(self):
        self.write_registry([registry_entry()])
        self.write_initiative(INIT_A, [requirement()])

        result = self.graduate()

        self.assertEqual([item['code'] for item in result['conflicts']], ['ID_EXISTS'])

    def test_modified_with_matching_base_rev_bumps_rev_and_replaces_text(self):
        self.write_registry([registry_entry()])
        self.write_initiative(INIT_A, [requirement(delta='modified', base_rev=1, description='New behaviour text')])

        result = self.graduate()

        self.assertEqual(result['conflicts'], [])
        entry = self.entry()
        self.assertEqual(entry['rev'], 2)
        self.assertEqual(entry['description'], 'New behaviour text')
        self.assertEqual(entry['source_initiative'], INIT_A)
        self.assertEqual([item['initiative'] for item in entry['history']], ['INIT-2026-001-origin', INIT_A])
        self.assertEqual(entry['history'][-1], {'rev': 2, 'initiative': INIT_A, 'date': TODAY, 'change': 'modified'})

    def test_modified_with_stale_base_rev_is_a_conflict(self):
        self.write_registry([registry_entry(rev=2)])
        self.write_initiative(INIT_A, [requirement(delta='modified', base_rev=1)])

        result = self.graduate()

        self.assertEqual([item['code'] for item in result['conflicts']], ['STALE_BASE_REV'])

    def test_modified_without_entry_is_a_conflict(self):
        self.write_registry([])
        self.write_initiative(INIT_A, [requirement(delta='modified', base_rev=1)])

        result = self.graduate()

        self.assertEqual([item['code'] for item in result['conflicts']], ['NO_REGISTRY_ENTRY'])

    def test_removed_marks_entry_deprecated_and_keeps_it(self):
        self.write_registry([registry_entry()])
        self.write_initiative(INIT_A, [
            requirement(status='deprecated', delta='removed', base_rev=1, removal_reason='Replaced by bulk export'),
        ])

        result = self.graduate()

        self.assertEqual(result['conflicts'], [])
        entry = self.entry()
        self.assertEqual(entry['status'], 'deprecated')
        self.assertEqual(entry['rev'], 2)
        self.assertEqual(entry['description'], 'Original behaviour text')
        self.assertEqual(entry['removal_reason'], 'Replaced by bulk export')
        self.assertEqual(entry['history'][-1]['change'], 'removed')

    def test_removed_with_stale_base_rev_is_a_conflict(self):
        self.write_registry([registry_entry(rev=2)])
        self.write_initiative(INIT_A, [
            requirement(status='deprecated', delta='removed', base_rev=1, removal_reason='Not needed'),
        ])

        result = self.graduate()

        self.assertEqual([item['code'] for item in result['conflicts']], ['STALE_BASE_REV'])

    def test_deprecated_entry_cannot_be_reused(self):
        for delta_fields in ({}, {'delta': 'modified', 'base_rev': 1}):
            with self.subTest(delta_fields=delta_fields):
                self.write_registry([registry_entry(status='deprecated')])
                self.write_initiative(INIT_A, [requirement(**delta_fields)])
                self.assertEqual(len(self.graduate()['conflicts']), 1)

    def test_other_statuses_stay_in_the_initiative(self):
        self.write_registry([registry_entry()])
        self.write_initiative(INIT_A, [
            requirement(status='approved', delta='modified', base_rev=1, description='Planned behaviour'),
            requirement('REQ-DEMO-002', status='draft'),
            requirement('REQ-DEMO-003', status='implemented', delta='removed', base_rev=1, removal_reason='Wrong status'),
        ])

        result = self.graduate()

        self.assertEqual(result['conflicts'], [])
        self.assertEqual(result['merged'], [])
        self.assertEqual(sorted(result['pending']), ['REQ-DEMO-001', 'REQ-DEMO-002', 'REQ-DEMO-003'])
        self.assertEqual(self.entry()['description'], 'Original behaviour text')


class AtomicityTests(RepositoryTestCase):
    def test_conflict_writes_nothing(self):
        self.write_registry([registry_entry()])
        init_dir = self.write_initiative(INIT_A, [
            requirement('REQ-DEMO-002'),
            requirement(),
        ])
        (init_dir / 'decisions').mkdir()
        (init_dir / 'decisions' / f'{INIT_A}-ADR-0001-choice.md').write_text('# Title\n')
        before = self.tree()

        result = self.graduate()

        self.assertTrue(result['conflicts'])
        self.assertEqual(self.tree(), before)

    def test_dry_run_writes_nothing_and_reports_plan(self):
        init_dir = self.write_initiative(INIT_A, [requirement()])
        (init_dir / 'decisions').mkdir()
        (init_dir / 'decisions' / f'{INIT_A}-ADR-0001-choice.md').write_text('# Title\n')
        before = self.tree()

        result = self.graduate(dry_run=True)

        self.assertEqual(self.tree(), before)
        self.assertEqual([item['id'] for item in result['merged']], [REQ_ID])
        self.assertEqual([item['target'] for item in result['adrs']], ['PLAT-0001-choice'])
        self.assertFalse(result['graduated'])

    def test_rerun_after_force_changes_nothing(self):
        init_dir = self.write_initiative(INIT_A, [requirement()])
        (init_dir / 'decisions').mkdir()
        (init_dir / 'decisions' / f'{INIT_A}-ADR-0001-choice.md').write_text('# Title\n')
        self.graduate()
        before = self.tree()

        result = self.graduate(force=True)

        self.assertEqual(result['conflicts'], [])
        self.assertEqual(result['merged'], [])
        self.assertEqual(result['noop'], [REQ_ID])
        self.assertEqual(result['adrs'], [])
        self.assertEqual(self.tree(), before)

    def test_already_graduated_stops_without_force(self):
        self.write_initiative(INIT_A, [requirement()], graduated=True)
        before = self.tree()

        result = self.graduate()

        self.assertTrue(result['already_graduated'])
        self.assertEqual(result['merged'], [])
        self.assertEqual(self.tree(), before)

    def test_force_picks_up_requirements_that_became_terminal(self):
        self.write_initiative(INIT_A, [requirement(), requirement('REQ-DEMO-002', status='approved')])
        self.graduate()
        self.write_initiative(INIT_A, [requirement(), requirement('REQ-DEMO-002')], graduated=True)

        result = self.graduate(force=True)

        self.assertEqual([item['id'] for item in result['merged']], ['REQ-DEMO-002'])
        self.assertEqual(result['noop'], [REQ_ID])
        self.assertEqual(self.entry('REQ-DEMO-002')['rev'], 1)


class SelectionTests(RepositoryTestCase):
    def test_only_merges_selected_and_leaves_initiative_unmarked(self):
        self.write_initiative(INIT_A, [requirement(), requirement('REQ-DEMO-002')])

        result = self.graduate(only=[REQ_ID])

        self.assertEqual([item['id'] for item in result['merged']], [REQ_ID])
        self.assertEqual([item['id'] for item in self.registry()['entries']], [REQ_ID])
        self.assertFalse(result['graduated'])
        self.assertNotIn('graduated', yaml.safe_load((self.root / 'initiatives' / INIT_A / 'requirements.yml').read_text())['metadata'])

    def test_only_with_unknown_id_is_an_error(self):
        self.write_initiative(INIT_A, [requirement()])

        result = self.graduate(only=['REQ-DEMO-999'])

        self.assertEqual([item['code'] for item in result['conflicts']], ['UNKNOWN_ID'])

    def test_conflict_outside_only_does_not_block(self):
        self.write_registry([registry_entry()])
        self.write_initiative(INIT_A, [requirement(), requirement('REQ-DEMO-002')])

        result = self.graduate(only=['REQ-DEMO-002'])

        self.assertEqual(result['conflicts'], [])
        self.assertEqual([item['id'] for item in result['merged']], ['REQ-DEMO-002'])

    def test_duplicate_id_in_initiative_is_a_conflict(self):
        self.write_initiative(INIT_A, [requirement(), requirement()])

        result = self.graduate()

        self.assertEqual([item['code'] for item in result['conflicts']], ['DUPLICATE_ID'])


class InputValidationTests(RepositoryTestCase):
    def test_missing_product_directory_is_an_error(self):
        self.write_initiative(INIT_A, [requirement()], product='absent')

        result = self.graduate()

        self.assertEqual([item['code'] for item in result['conflicts']], ['PRODUCT_NOT_FOUND'])

    def test_missing_initiative_is_an_error(self):
        result = self.graduate()

        self.assertEqual([item['code'] for item in result['conflicts']], ['INITIATIVE_NOT_FOUND'])

    def test_invalid_initiative_id_is_an_error(self):
        result = self.graduate(name='not-an-initiative')

        self.assertEqual([item['code'] for item in result['conflicts']], ['INVALID_INITIATIVE_ID'])

    def test_old_registry_schema_is_an_error(self):
        self.registry_path.write_text(yaml.safe_dump({'metadata': {'product': 'platform'}, 'entries': []}))
        self.write_initiative(INIT_A, [requirement()])

        result = self.graduate()

        self.assertEqual([item['code'] for item in result['conflicts']], ['REGISTRY_SCHEMA'])


class RegistryFormatTests(RepositoryTestCase):
    def test_header_comment_is_restored(self):
        self.write_registry([])
        self.write_initiative(INIT_A, [requirement()])

        self.graduate()

        self.assertTrue(self.registry_path.read_text().startswith('# Header kept\n'))
        self.assertEqual(self.registry()['metadata']['last_updated'], TODAY)

    def test_file_modes_are_kept_and_new_files_are_readable(self):
        self.write_registry([])
        self.registry_path.chmod(0o664)
        self.write_initiative(INIT_A, [requirement()])

        self.graduate()

        self.assertEqual(self.registry_path.stat().st_mode & 0o777, 0o664)
        self.assertEqual((self.product_dir / 'knowledge-log.md').stat().st_mode & 0o777, 0o644)

    def test_new_registry_gets_stub_metadata(self):
        self.write_initiative(INIT_A, [requirement()])

        self.graduate()

        text = self.registry_path.read_text()
        self.assertTrue(text.startswith('# Product requirements registry:'))
        metadata = self.registry()['metadata']
        self.assertEqual(metadata['schema_version'], 2)
        self.assertEqual(metadata['owner'], '@platform-team')

    def test_nfr_keeps_metrics(self):
        nfr = requirement(type='nfr', metrics=[{'name': 'p95', 'target': 30, 'measurement': 'apm'}])
        del nfr['acceptance_criteria']
        self.write_initiative(INIT_A, [nfr])

        self.graduate()

        entry = self.entry()
        self.assertEqual(entry['metrics'], [{'name': 'p95', 'target': 30, 'measurement': 'apm'}])
        self.assertNotIn('acceptance_criteria', entry)

    def test_initiative_is_edited_in_place(self):
        init_dir = self.write_initiative(INIT_A, [requirement()])
        path = init_dir / 'requirements.yml'
        path.write_text(
            '# Comment that must survive\n'
            'metadata:\n'
            f'  initiative: "{INIT_A}"\n'
            '  product: "platform"\n'
            '  owner: "@platform-team"\n'
            '  profile: "standard"\n'
            '  version: "0.1.0"\n'
            '  last_updated: "2026-01-01"\n'
            '\n'
            'requirements:\n'
            '  # Comment inside requirements\n'
            f'  - id: "{REQ_ID}"\n'
            '    title: "Short title"\n'
            '    type: "functional"\n'
            '    priority: "P1"\n'
            '    status: "implemented"\n'
            '    description: "Description text"\n'
            '    acceptance_criteria: ["Given a When b Then c"]\n'
            '    trace: {}\n'
        )

        self.graduate()

        text = path.read_text()
        self.assertIn('# Comment that must survive\n', text)
        self.assertIn('  # Comment inside requirements\n', text)
        self.assertIn(f'  last_updated: "{TODAY}"\n  graduated: true\n', text)
        self.assertTrue(yaml.safe_load(text)['metadata']['graduated'])


class AdrTests(RepositoryTestCase):
    def setUp(self):
        super().setUp()
        self.init_dir = self.write_initiative(INIT_A, [requirement()])
        self.decisions = self.init_dir / 'decisions'
        self.decisions.mkdir()
        self.product_decisions = self.product_dir / 'decisions'
        self.product_decisions.mkdir()

    def test_numbering_scans_product_and_root(self):
        (self.product_decisions / 'PLAT-0003-async.md').write_text('# PLAT-0003: Async\n')
        (self.root / 'decisions').mkdir()
        (self.root / 'decisions' / 'PLAT-0007-root.md').write_text('# PLAT-0007: Root\n')
        (self.decisions / f'{INIT_A}-ADR-0001-storage.md').write_text('# Title\n')

        result = self.graduate()

        self.assertEqual([item['target'] for item in result['adrs']], ['PLAT-0008-storage'])

    def test_prefix_is_derived_from_product_name(self):
        (self.decisions / f'{INIT_A}-ADR-0001-storage.md').write_text('# Title\n')

        result = self.graduate()

        self.assertEqual([item['target'] for item in result['adrs']], ['PLAT-0001-storage'])

    def test_existing_prefix_wins(self):
        (self.product_decisions / 'PFRM-0002-old.md').write_text('# PFRM-0002: Old\n')
        (self.decisions / f'{INIT_A}-ADR-0001-storage.md').write_text('# Title\n')

        result = self.graduate()

        self.assertEqual([item['target'] for item in result['adrs']], ['PFRM-0003-storage'])

    def test_copy_adds_frontmatter_and_renames_heading_and_keeps_source(self):
        source = self.decisions / f'{INIT_A}-ADR-0001-storage.md'
        original = f'---\nstatus: "accepted"\n---\n\n# {INIT_A}-ADR-0001: Bcrypt hashing\n\nBody text\n'
        source.write_text(original)

        self.graduate()

        target = (self.product_decisions / 'PLAT-0001-storage.md').read_text()
        self.assertEqual(source.read_text(), original)
        self.assertIn('status: "accepted"\n', target)
        self.assertIn(f'graduated_from: "{INIT_A}"\n', target)
        self.assertIn(f'original_id: "{INIT_A}-ADR-0001-storage"\n', target)
        self.assertIn(f'graduated_date: "{TODAY}"\n', target)
        self.assertIn('# PLAT-0001: Bcrypt hashing\n', target)
        self.assertIn('Body text\n', target)

    def test_copy_without_frontmatter_gets_one(self):
        (self.decisions / f'{INIT_A}-ADR-0001-storage.md').write_text('# Plain heading\n\nBody\n')

        self.graduate()

        target = (self.product_decisions / 'PLAT-0001-storage.md').read_text()
        self.assertTrue(target.startswith('---\n'))
        self.assertIn('# PLAT-0001: Plain heading\n', target)

    def test_templates_and_readme_are_skipped(self):
        (self.decisions / 'ADR-template.md').write_text('# Template\n')
        (self.decisions / 'README.md').write_text('# Readme\n')

        result = self.graduate()

        self.assertEqual(result['adrs'], [])

    def test_skip_adr_option(self):
        (self.decisions / f'{INIT_A}-ADR-0001-storage.md').write_text('# One\n')
        (self.decisions / f'{INIT_A}-ADR-0002-queue.md').write_text('# Two\n')

        result = self.graduate(skip_adrs=[f'{INIT_A}-ADR-0001-storage'])

        self.assertEqual([item['target'] for item in result['adrs']], ['PLAT-0001-queue'])


class KnowledgeLogTests(RepositoryTestCase):
    def log(self):
        return (self.product_dir / 'knowledge-log.md').read_text()

    def test_log_is_created_with_requirements_and_outcome(self):
        init_dir = self.write_initiative(INIT_A, [requirement()])
        (init_dir / 'prd.md').write_text('# PRD\n\n- **Цель (Outcome):** Снизить время выгрузки\n')

        self.graduate()

        log = self.log()
        self.assertTrue(log.startswith('# Knowledge Log: platform'))
        self.assertIn(f'## {TODAY} — {INIT_A}', log)
        self.assertIn('**Outcome:** Снизить время выгрузки', log)
        self.assertIn(f'| {REQ_ID} | Title of {REQ_ID} | implemented | functional | added, rev 1 |', log)

    def test_new_section_goes_first(self):
        (self.product_dir / 'knowledge-log.md').write_text(
            '# Knowledge Log: platform\n\nHeader line.\n\n---\n\n## 2026-01-01 — INIT-2026-001-origin\n\nOld\n'
        )
        self.write_initiative(INIT_A, [requirement()])

        self.graduate()

        log = self.log()
        self.assertLess(log.index(INIT_A), log.index('INIT-2026-001-origin'))
        self.assertTrue(log.startswith('# Knowledge Log: platform\n\nHeader line.\n\n---\n\n## '))

    def test_placeholder_outcome_is_not_copied(self):
        init_dir = self.write_initiative(INIT_A, [requirement()])
        (init_dir / 'prd.md').write_text('- **Цель (Outcome):** {измеримый результат}\n')

        self.graduate()

        self.assertIn('**Outcome:** —', self.log())


class CommandLineTests(RepositoryTestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / 'graduate.py'), *args, '--root', str(self.root)],
            capture_output=True, text=True,
        )

    def test_json_is_a_single_document_on_stdout(self):
        self.write_initiative(INIT_A, [requirement()])

        completed = self.run_cli(INIT_A, '--dry-run', '--json')

        self.assertEqual(completed.returncode, 0)
        self.assertEqual([item['id'] for item in json.loads(completed.stdout)['merged']], [REQ_ID])

    def test_conflict_exits_with_1(self):
        self.write_registry([registry_entry()])
        self.write_initiative(INIT_A, [requirement()])

        completed = self.run_cli(INIT_A)

        self.assertEqual(completed.returncode, 1)
        self.assertIn('ID_EXISTS', completed.stdout)


class CheckDeltasTests(RepositoryTestCase):
    def check(self):
        with redirect_stdout(StringIO()):
            return check_deltas.run_checks(self.root)

    def test_stale_terminal_requirement_is_an_error(self):
        self.write_registry([registry_entry(rev=2)])
        self.write_initiative(INIT_A, [requirement(delta='modified', base_rev=1)])

        errors, warnings = self.check()

        self.assertEqual(len(errors), 1)
        self.assertIn('STALE_BASE_REV', errors[0])
        self.assertEqual(warnings, [])

    def test_stale_planned_requirement_is_a_warning(self):
        self.write_registry([registry_entry(rev=2)])
        self.write_initiative(INIT_A, [requirement(status='approved', delta='modified', base_rev=1)])

        errors, warnings = self.check()

        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)
        self.assertIn('STALE_BASE_REV', warnings[0])

    def test_graduated_and_archived_initiatives_are_skipped(self):
        self.write_registry([registry_entry(rev=2)])
        self.write_initiative(INIT_A, [requirement(delta='modified', base_rev=1)], graduated=True)
        self.write_initiative(INIT_B, [requirement(delta='modified', base_rev=1)], initiative_status='archived')

        self.assertEqual(self.check(), ([], []))

    def test_template_directory_is_skipped(self):
        self.write_registry([registry_entry()])
        self.write_initiative('{INIT-YYYY-NNN-slug}', [requirement()])

        self.assertEqual(self.check(), ([], []))

    def test_two_active_initiatives_on_one_requirement_are_reported(self):
        self.write_registry([registry_entry()])
        self.write_initiative(INIT_A, [requirement(status='approved', delta='modified', base_rev=1)])
        self.write_initiative(INIT_B, [requirement(status='approved', delta='modified', base_rev=1)])

        errors, warnings = self.check()

        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)
        self.assertIn(INIT_A, warnings[0])
        self.assertIn(INIT_B, warnings[0])

    def test_parallel_change_second_initiative_conflicts_after_first_graduates(self):
        self.write_registry([registry_entry()])
        self.write_initiative(INIT_A, [requirement(delta='modified', base_rev=1, description='First change text')])
        self.write_initiative(INIT_B, [requirement(delta='modified', base_rev=1, description='Second change text')])

        self.assertEqual(self.graduate(INIT_A)['conflicts'], [])
        registry_after_first = self.registry_path.read_text()

        errors, _ = self.check()
        self.assertEqual(len(errors), 1)
        self.assertIn(INIT_B, errors[0])
        self.assertEqual([item['code'] for item in self.graduate(INIT_B)['conflicts']], ['STALE_BASE_REV'])
        self.assertEqual(self.registry_path.read_text(), registry_after_first)
        self.assertEqual(self.entry()['description'], 'First change text')

    def test_old_registry_schema_is_an_error(self):
        self.registry_path.write_text(yaml.safe_dump({'metadata': {'product': 'platform'}, 'entries': []}))

        errors, _ = self.check()

        self.assertEqual(len(errors), 1)
        self.assertIn('REGISTRY_SCHEMA', errors[0])

    def test_rev_must_match_history(self):
        entry = registry_entry(rev=2)
        entry['history'] = entry['history'][:1]
        self.write_registry([entry])

        errors, _ = self.check()

        self.assertEqual(len(errors), 1)
        self.assertIn('REGISTRY_HISTORY', errors[0])


if __name__ == '__main__':
    unittest.main()
