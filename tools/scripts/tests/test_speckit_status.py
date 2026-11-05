import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

SCRIPT = Path(__file__).resolve().parents[1] / 'speckit-status.py'
SPEC = importlib.util.spec_from_file_location('speckit_status', SCRIPT)
speckit_status = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(speckit_status)

INIT = 'INIT-2026-010-demo'
SPEC_SLUG = '010-demo'
REQ_ID = 'REQ-DEMO-001'
TEMPLATE_TASK = '- [ ] **T1:** Добавить контракт'


class StatusTestCase(unittest.TestCase):
    def setUp(self):
        tmpdir = TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        self.root = Path(tmpdir.name)
        self.init_dir = self.root / 'initiatives' / INIT
        self.write('.specify/specs/{NNN}-{slug}/tasks.md', f'{TEMPLATE_TASK}\n')

    def write(self, relative_path: str, content: str) -> None:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def write_initiative(self, profile='standard', status='approved', requirements=None, **metadata):
        if requirements is None:
            requirements = [{'id': REQ_ID, 'status': status}]
        self.write(f'initiatives/{INIT}/requirements.yml', yaml.safe_dump({
            'metadata': {'product': 'platform', 'profile': profile, **metadata},
            'requirements': requirements,
        }))

    def write_prd(self):
        self.write(f'initiatives/{INIT}/prd.md', '# PRD\n\nFilled text.\n')

    def write_contracts(self):
        self.write(f'initiatives/{INIT}/contracts/openapi.yaml', 'openapi: 3.1.0\npaths:\n  /things/{id}: {}\n')

    def write_spec(self, slug=SPEC_SLUG, initiative=INIT, files=('spec', 'plan', 'tasks')):
        base = f'.specify/specs/{slug}'
        if 'spec' in files:
            self.write(f'{base}/spec.md', f'**Initiative:** {initiative}\n\nCovers {REQ_ID}.\n')
        if 'plan' in files:
            self.write(f'{base}/plan.md', 'Plan text.\n')
        if 'tasks' in files:
            self.write(f'{base}/tasks.md', f'- [ ] **T1:** Real task for {REQ_ID}\n')

    def status(self):
        return speckit_status.run(self.root, INIT)

    def states(self):
        return {step['id']: step['state'] for step in self.status()['steps']}


class StepTests(StatusTestCase):
    def test_fresh_initiative_is_ready_for_prd(self):
        self.write_initiative(requirements=[])
        result = self.status()
        self.assertEqual(result['next'], {'id': 'prd', 'command': f'/speckit-prd {INIT}'})
        states = self.states()
        self.assertEqual(states['prd'], 'ready')
        self.assertEqual(states['requirements'], 'blocked')

    def test_blocked_step_names_what_blocks_it(self):
        self.write_initiative(requirements=[])
        step = next(item for item in self.status()['steps'] if item['id'] == 'requirements')
        self.assertEqual(step['blocked_by'], ['prd'])

    def test_placeholder_keeps_step_open_and_is_reported(self):
        self.write_initiative(requirements=[])
        self.write(f'initiatives/{INIT}/prd.md', '# {Название инициативы}\n')
        result = self.status()
        self.assertEqual(result['next']['id'], 'prd')
        self.assertEqual([item['code'] for item in result['diagnostics']], ['UNFILLED_PLACEHOLDER'])
        self.assertEqual(set(result['diagnostics'][0]), {'severity', 'code', 'message', 'fix'})

    def test_next_moves_along_the_lifecycle(self):
        self.write_initiative()
        self.write_prd()
        self.assertEqual(self.status()['next']['id'], 'contracts')
        self.write_contracts()
        self.assertEqual(self.status()['next']['id'], 'specify')
        self.write_spec(files=('spec',))
        self.assertEqual(self.status()['next'], {'id': 'plan', 'command': f'/speckit-plan {SPEC_SLUG}'})
        self.write_spec(files=('plan',))
        self.assertEqual(self.status()['next'], {'id': 'tasks', 'command': f'/speckit-tasks {SPEC_SLUG}'})
        self.write_spec(files=('tasks',))
        self.assertEqual(self.status()['next']['id'], 'implement')

    def test_template_task_list_is_not_done(self):
        self.write_initiative()
        self.write_prd()
        self.write_contracts()
        self.write_spec(files=('spec', 'plan'))
        self.write(f'.specify/specs/{SPEC_SLUG}/tasks.md', f'{TEMPLATE_TASK}\n')
        result = self.status()
        self.assertEqual(result['next']['id'], 'tasks')
        self.assertIn('UNFILLED_TASKS', [item['code'] for item in result['diagnostics']])

    def test_implement_needs_terminal_statuses_and_ignores_deprecated(self):
        self.write_initiative(requirements=[
            {'id': REQ_ID, 'status': 'implemented'},
            {'id': 'REQ-DEMO-002', 'status': 'deprecated'},
        ])
        self.assertEqual(self.states()['implement'], 'done')
        self.write_initiative(requirements=[{'id': REQ_ID, 'status': 'approved'}])
        self.assertNotEqual(self.states()['implement'], 'done')

    def test_rtm_needs_every_requirement(self):
        self.write_initiative(requirements=[{'id': REQ_ID, 'status': 'implemented'}, {'id': 'REQ-DEMO-002', 'status': 'implemented'}])
        self.write(f'initiatives/{INIT}/trace.md', f'| {REQ_ID} | row |\n')
        self.assertNotEqual(self.states()['rtm'], 'done')
        self.write(f'initiatives/{INIT}/trace.md', f'| {REQ_ID} | row |\n| REQ-DEMO-002 | row |\n')
        self.assertEqual(self.states()['rtm'], 'done')

    def test_graduate_reads_metadata(self):
        self.write_initiative(graduated=True)
        self.assertEqual(self.states()['graduate'], 'done')

    def test_all_done_has_no_next(self):
        self.write_initiative(status='implemented', graduated=True)
        self.write_prd()
        self.write_contracts()
        self.write_spec()
        self.write(f'.specify/specs/{SPEC_SLUG}/trace.md', f'| {REQ_ID} | row |\n')
        self.write(f'initiatives/{INIT}/trace.md', f'| {REQ_ID} | row |\n')
        self.write(f'initiatives/{INIT}/delivery/rollout.md', 'Rollout text.\n')
        result = self.status()
        self.assertEqual(set(self.states().values()), {'done'})
        self.assertIsNone(result['next'])


class ProfileTests(StatusTestCase):
    def test_minimal_has_no_contracts_or_rollout(self):
        self.write_initiative(profile='minimal', requirements=[])
        ids = {step['id'] for step in self.status()['steps']}
        self.assertNotIn('contracts', ids)
        self.assertNotIn('release-rollout', ids)

    def consilium_hint(self, profile):
        self.write_initiative(profile=profile, status='implemented')
        self.write_prd()
        self.write_contracts()
        self.write_spec()
        self.write(f'.specify/specs/{SPEC_SLUG}/trace.md', f'| {REQ_ID} | row |\n')
        self.write(f'initiatives/{INIT}/trace.md', f'| {REQ_ID} | row |\n')
        return self.status()['next']

    def test_consilium_is_suggested_before_graduation_for_standard(self):
        hint = self.consilium_hint('standard')
        self.assertEqual(hint['id'], 'graduate')
        self.assertEqual(hint['also_consider'], ['/speckit-consilium'])

    def test_consilium_is_not_suggested_for_minimal(self):
        hint = self.consilium_hint('minimal')
        self.assertEqual(hint['id'], 'graduate')
        self.assertNotIn('also_consider', hint)


class SpecLinkTests(StatusTestCase):
    def test_spec_of_another_initiative_does_not_count(self):
        self.write_initiative()
        self.write_spec(initiative='INIT-2026-011-other')
        self.assertNotEqual(self.states()['specify'], 'done')

    def test_every_linked_spec_must_have_the_file(self):
        self.write_initiative()
        self.write_prd()
        self.write_contracts()
        self.write_spec()
        self.write_spec(slug='011-second', files=('spec',))
        self.assertEqual(self.status()['next'], {'id': 'plan', 'command': '/speckit-plan 011-second'})

    def test_l4_steps_are_skipped_when_work_is_done_without_a_spec(self):
        self.write_initiative(status='implemented')
        self.write_prd()
        self.write_contracts()
        states = self.states()
        for step in ('specify', 'plan', 'tasks', 'trace'):
            self.assertEqual(states[step], 'skipped')
        self.assertEqual(self.status()['next']['id'], 'rtm')


class EdgeCaseTests(StatusTestCase):
    def test_archived_initiative(self):
        self.write(f'archive/{INIT}/requirements.yml', yaml.safe_dump({'metadata': {'product': 'platform'}, 'requirements': []}))
        result = self.status()
        self.assertEqual(result['initiative_status'], 'archived')
        self.assertEqual(result['steps'], [])
        self.assertEqual(result['diagnostics'][0]['code'], 'ARCHIVED')

    def test_missing_initiative(self):
        self.assertEqual(self.status()['diagnostics'][0]['code'], 'INITIATIVE_NOT_FOUND')

    def test_invalid_id(self):
        result = speckit_status.run(self.root, 'bad-id')
        self.assertEqual(result['diagnostics'][0]['code'], 'INVALID_INITIATIVE_ID')

    def test_placeholder_rules_keep_expressions_with_a_colon(self):
        self.assertEqual(speckit_status.quality.find_placeholders('metric{result: ok|failed}'), [])
        self.assertEqual(speckit_status.quality.find_placeholders('{canary | blue-green}'), [(1, 'canary | blue-green')])


class CommandLineTests(StatusTestCase):
    def run_cli(self, name=INIT, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), name, '--root', str(self.root), *args],
            capture_output=True, text=True,
        )

    def test_json_is_one_document_on_stdout(self):
        self.write_initiative(requirements=[])
        completed = self.run_cli(INIT, '--json')
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(json.loads(completed.stdout)['next']['id'], 'prd')

    def test_error_exits_with_1(self):
        completed = self.run_cli(INIT, '--json')
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(json.loads(completed.stdout)['diagnostics'][0]['severity'], 'error')


if __name__ == '__main__':
    unittest.main()
