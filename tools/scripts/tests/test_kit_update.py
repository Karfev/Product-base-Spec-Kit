import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = REPO_ROOT / 'tools' / 'kit-update.sh'
TAG = 'kit-v1.0.0'


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


if __name__ == '__main__':
    unittest.main()
