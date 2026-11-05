import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = REPO_ROOT / 'tools' / 'kit-update.sh'
TAG = 'kit-v1.0.0'
TEMPLATE_DIR = 'initiatives/{INIT-YYYY-NNN-slug}'


def git(cwd: Path, *args) -> str:
    return subprocess.run(['git', *args], cwd=cwd, check=True, capture_output=True, text=True).stdout


def init_repo(path: Path) -> None:
    path.mkdir(parents=True)
    git(path, 'init', '-q')
    git(path, 'config', 'user.name', 'test')
    git(path, 'config', 'user.email', 'test@example.invalid')


def write_files(root: Path, files: dict) -> None:
    for relative_path, content in files.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


def commit_all(path: Path) -> None:
    git(path, 'add', '-A')
    git(path, 'commit', '-q', '-m', 'commit')


class KitUpdateTests(unittest.TestCase):
    def setUp(self):
        tmpdir = TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        base = Path(tmpdir.name)
        self.kit = base / 'kit'
        self.fork = base / 'fork'
        init_repo(self.kit)
        write_files(self.kit, {
            'VERSION': '1.0.0\n',
            'tools/kit-paths.txt': '# comment\nVERSION\ntools\ninitiatives/{INIT-YYYY-NNN-slug}\nabsent/path\n\n',
            'tools/check.py': 'new check\n',
            'tools/sub/nested.py': 'kit nested\n',
            'tools-extra/note.md': 'not a listed path\n',
            'initiatives/{INIT-YYYY-NNN-slug}/prd.md': 'new template\n',
            'initiatives/INIT-2026-000-golden/prd.md': 'kit content\n',
            'README.md': 'kit readme\n',
        })
        commit_all(self.kit)
        git(self.kit, 'tag', '-a', TAG, '-m', 'release')
        init_repo(self.fork)
        write_files(self.fork, {
            'VERSION': '0.9.0\n',
            'tools/check.py': 'old check with a local change\n',
            'tools/fork-only.py': 'fork tool\n',
            'initiatives/{INIT-YYYY-NNN-slug}/prd.md': 'old template\n',
            'initiatives/INIT-2026-100-fork/prd.md': 'fork content\n',
            'README.md': 'fork readme\n',
        })
        commit_all(self.fork)

    def run_update(self, source=None, tag=TAG):
        return subprocess.run(
            ['bash', str(SCRIPT), str(source or self.kit), tag],
            cwd=self.fork, capture_output=True, text=True,
        )

    def read(self, relative_path: str) -> str:
        return (self.fork / relative_path).read_text()

    def exclude(self, content: str) -> None:
        (self.fork / '.kit-exclude').write_bytes(content.encode())
        commit_all(self.fork)

    def test_updates_listed_paths_only(self):
        completed = self.run_update()
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(self.read('tools/check.py'), 'new check\n')
        self.assertEqual(self.read('initiatives/{INIT-YYYY-NNN-slug}/prd.md'), 'new template\n')
        self.assertEqual(self.read('VERSION'), '1.0.0\n')
        self.assertEqual(self.read('README.md'), 'fork readme\n')
        self.assertEqual(self.read('initiatives/INIT-2026-100-fork/prd.md'), 'fork content\n')
        self.assertFalse((self.fork / 'initiatives/INIT-2026-000-golden').exists())

    def test_result_stays_uncommitted_and_local_change_is_in_the_diff(self):
        head = git(self.fork, 'rev-parse', 'HEAD')
        self.run_update()
        self.assertEqual(git(self.fork, 'rev-parse', 'HEAD'), head)
        self.assertIn('-old check with a local change', git(self.fork, 'diff', '--cached', '--', 'tools/check.py'))

    def test_file_only_in_the_fork_is_kept_and_listed(self):
        completed = self.run_update()
        self.assertEqual(self.read('tools/fork-only.py'), 'fork tool\n')
        self.assertIn('tools/fork-only.py', completed.stdout)

    def test_reports_versions_and_missing_paths(self):
        completed = self.run_update()
        self.assertIn('0.9.0 -> 1.0.0', completed.stdout)
        self.assertIn("'absent/path' is not in", completed.stdout)

    def test_dirty_tree_is_refused(self):
        write_files(self.fork, {'README.md': 'unsaved\n'})
        completed = self.run_update()
        self.assertEqual(completed.returncode, 1)
        self.assertIn('not clean', completed.stdout)
        self.assertEqual(self.read('tools/check.py'), 'old check with a local change\n')

    def test_untracked_file_is_refused(self):
        write_files(self.fork, {'tools/new.py': 'untracked\n'})
        self.assertEqual(self.run_update().returncode, 1)

    def test_missing_tag_is_an_error(self):
        completed = self.run_update(tag='kit-v9.9.9')
        self.assertEqual(completed.returncode, 1)
        self.assertIn('cannot fetch', completed.stdout)
        self.assertEqual(git(self.fork, 'status', '--porcelain'), '')

    def test_tag_without_path_list_is_an_error(self):
        git(self.kit, 'rm', '-q', 'tools/kit-paths.txt')
        commit_all(self.kit) if git(self.kit, 'status', '--porcelain') else None
        git(self.kit, 'tag', 'old-tag')
        completed = self.run_update(tag='old-tag')
        self.assertEqual(completed.returncode, 1)
        self.assertIn('no tools/kit-paths.txt', completed.stdout)

    def test_second_run_after_commit_is_up_to_date(self):
        self.run_update()
        commit_all(self.fork)
        completed = self.run_update()
        self.assertEqual(completed.returncode, 0)
        self.assertIn('Already up to date', completed.stdout)

    def test_no_tags_are_copied_into_the_fork(self):
        self.run_update()
        self.assertEqual(git(self.fork, 'tag'), '')

    def test_paths_are_taken_from_the_new_version(self):
        write_files(self.kit, {'tools/kit-paths.txt': 'VERSION\ntools\ndocs\n', 'docs/guide.md': 'guide\n'})
        commit_all(self.kit)
        git(self.kit, 'tag', 'kit-v1.1.0')
        self.run_update(tag='kit-v1.1.0')
        self.assertEqual(self.read('docs/guide.md'), 'guide\n')

    def test_works_when_piped_into_bash_for_the_first_update(self):
        completed = subprocess.run(
            ['bash', '-s', '--', str(self.kit), TAG],
            cwd=self.fork, input=SCRIPT.read_text(), capture_output=True, text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(self.read('tools/check.py'), 'new check\n')

    def test_excluded_path_removed_by_the_fork_stays_removed(self):
        git(self.fork, 'rm', '-rq', TEMPLATE_DIR)
        self.exclude(f'{TEMPLATE_DIR}\n')
        completed = self.run_update()
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertFalse((self.fork / TEMPLATE_DIR).exists())
        self.assertEqual(self.read('tools/check.py'), 'new check\n')
        self.assertIn(f'  {TEMPLATE_DIR}\n', completed.stdout)

    def test_excluded_path_keeps_the_local_content(self):
        self.exclude(f'{TEMPLATE_DIR}\n')
        self.run_update()
        self.assertEqual(self.read(f'{TEMPLATE_DIR}/prd.md'), 'old template\n')
        self.assertEqual(git(self.fork, 'diff', '--cached', '--', TEMPLATE_DIR), '')

    def test_listed_path_inside_an_excluded_directory_is_skipped(self):
        self.exclude('initiatives\n')
        completed = self.run_update()
        self.assertEqual(self.read(f'{TEMPLATE_DIR}/prd.md'), 'old template\n')
        self.assertIn(f'  {TEMPLATE_DIR}\n', completed.stdout)

    def test_file_inside_a_listed_directory_can_be_excluded(self):
        self.exclude('tools/check.py\n')
        completed = self.run_update()
        self.assertEqual(self.read('tools/check.py'), 'old check with a local change\n')
        self.assertEqual(self.read('tools/sub/nested.py'), 'kit nested\n')
        self.assertIn('  tools/check.py\n', completed.stdout)

    def test_directory_inside_a_listed_directory_can_be_excluded(self):
        self.exclude('tools/sub\n')
        completed = self.run_update()
        self.assertFalse((self.fork / 'tools/sub').exists())
        self.assertEqual(self.read('tools/check.py'), 'new check\n')
        self.assertIn('  tools/sub\n', completed.stdout)

    def test_excluding_everything_inside_a_listed_path_is_not_an_error(self):
        self.exclude(f'{TEMPLATE_DIR}/prd.md\n')
        completed = self.run_update()
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(self.read(f'{TEMPLATE_DIR}/prd.md'), 'old template\n')
        self.assertIn(f'  {TEMPLATE_DIR}/prd.md\n', completed.stdout)

    def test_entry_covers_whole_path_components_only(self):
        self.exclude(f'tool\ntools/che\n{TEMPLATE_DIR[:-1]}\n')
        completed = self.run_update()
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(self.read('tools/check.py'), 'new check\n')
        self.assertEqual(self.read(f'{TEMPLATE_DIR}/prd.md'), 'new template\n')

    def test_entry_next_to_a_listed_directory_is_not_reported_as_skipped(self):
        self.exclude('tools-extra/note.md\n')
        completed = self.run_update()
        self.assertNotIn('Skipped', completed.stdout)
        self.assertIn("'tools-extra/note.md'", completed.stdout)

    def test_entry_is_a_path_and_not_a_pattern(self):
        self.exclude('tools/*\n*\n')
        self.run_update()
        self.assertEqual(self.read('tools/check.py'), 'new check\n')
        self.assertEqual(self.read(f'{TEMPLATE_DIR}/prd.md'), 'new template\n')

    def test_exclude_file_format(self):
        self.exclude(f'# comment\n\ntools/check.py\r\n./tools/sub/\n{TEMPLATE_DIR}')
        completed = self.run_update()
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(self.read('tools/check.py'), 'old check with a local change\n')
        self.assertFalse((self.fork / 'tools/sub').exists())
        self.assertEqual(self.read(f'{TEMPLATE_DIR}/prd.md'), 'old template\n')
        self.assertEqual(self.read('VERSION'), '1.0.0\n')

    def test_skipped_paths_are_reported_when_already_up_to_date(self):
        self.exclude('tools/sub\n')
        self.run_update()
        commit_all(self.fork)
        completed = self.run_update()
        self.assertIn('Already up to date', completed.stdout)
        self.assertIn('  tools/sub\n', completed.stdout)

    def test_no_report_without_an_exclude_file(self):
        self.assertNotIn('Skipped', self.run_update().stdout)

    def test_entry_that_matches_nothing_is_reported(self):
        self.exclude('no/such/path\n')
        completed = self.run_update()
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("'no/such/path'", completed.stdout)

    def test_excluded_file_only_in_the_fork_is_not_reported(self):
        self.exclude('tools/fork-only.py\n')
        completed = self.run_update()
        self.assertEqual(self.read('tools/fork-only.py'), 'fork tool\n')
        self.assertNotIn('tools/fork-only.py', completed.stdout)

    def test_exclude_file_is_not_replaced_by_the_kit(self):
        kit_paths = (REPO_ROOT / 'tools' / 'kit-paths.txt').read_text().splitlines()
        self.assertNotIn('.kit-exclude', kit_paths)
        self.exclude('tools/sub\n')
        self.run_update()
        self.assertEqual(git(self.fork, 'diff', '--cached', '--', '.kit-exclude'), '')
        self.assertEqual(self.read('.kit-exclude'), 'tools/sub\n')

    def test_exclude_file_is_used_when_piped_into_bash(self):
        self.exclude(f'{TEMPLATE_DIR}\ntools/sub\n')
        completed = subprocess.run(
            ['bash', '-s', '--', str(self.kit), TAG],
            cwd=self.fork, input=SCRIPT.read_text(), capture_output=True, text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(self.read(f'{TEMPLATE_DIR}/prd.md'), 'old template\n')
        self.assertFalse((self.fork / 'tools/sub').exists())
        self.assertEqual(self.read('tools/check.py'), 'new check\n')
        self.assertIn('Nothing is committed', completed.stdout)


if __name__ == '__main__':
    unittest.main()
