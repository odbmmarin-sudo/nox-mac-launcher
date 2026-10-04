import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('builder', ROOT / 'build.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ImportTests(unittest.TestCase):
    def test_personal_save_link_is_not_imported(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'source'
            source.mkdir()
            personal = root / 'personal'
            personal.mkdir()
            (personal / 'save.dat').write_text('private')
            (source / 'Save').symlink_to(personal, target_is_directory=True)
            (source / 'Game.exe').write_bytes(b'test fixture')
            builder.copy_game(source, root / 'target')
            self.assertEqual(list((root / 'target/Save').iterdir()), [])
            self.assertEqual((personal / 'save.dat').read_text(), 'private')

    def test_other_external_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'source'
            source.mkdir()
            (source / 'escape').symlink_to(root)
            with self.assertRaises(ValueError):
                builder.copy_game(source, root / 'target')
            self.assertFalse((root / 'target').exists())

    def test_display_patch_preserves_compatibility_and_comments(self):
        ini = '[ddraw]\n; renderer=auto is supported\nrenderer=auto\nwindowed=false\n[Game/2]\nmaxgameticks=125\nwindowed=false\n'
        changed = builder.configure(ini)
        self.assertIn('; renderer=auto is supported', changed)
        self.assertIn('windowed=true', changed)
        self.assertIn('[Game/2]\nmaxgameticks=125\nwindowed=false', changed)

    def test_checksum_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'bad.zip'
            path.write_bytes(b'wrong archive')
            with self.assertRaises(ValueError):
                builder.verify(path, '0' * 64)


if __name__ == '__main__':
    unittest.main()
