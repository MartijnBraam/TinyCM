from unittest import TestCase
from tinycm.definitions.file import FileDefinition
import tempfile
import os


class TestFileDefinition(TestCase):
    def test__merge_permission_mask(self):
        d = FileDefinition('file::/tmp/test', {'name': '/tmp/test', 'type': 'constant', 'contents': ''}, 'unittest', [],
                           {})
        self.assertEqual(d._merge_permission_mask('000', 'xxx'), '000')
        self.assertEqual(d._merge_permission_mask('000', '1xx'), '100')
        self.assertEqual(d._merge_permission_mask('000', '11x'), '110')
        self.assertEqual(d._merge_permission_mask('000', '111'), '111')

    def test__oct_to_dec(self):
        d = FileDefinition('file::/tmp/test', {'name': '/tmp/test', 'type': 'constant', 'contents': ''}, 'unittest', [],
                           {})
        self.assertEqual(d._oct_to_dec(0), 0)
        self.assertEqual(d._oct_to_dec(1), 1)
        self.assertEqual(d._oct_to_dec(2), 2)
        self.assertEqual(d._oct_to_dec(4), 4)
        self.assertEqual(d._oct_to_dec(10), 8)
        self.assertEqual(d._oct_to_dec(20), 16)
        self.assertEqual(d._oct_to_dec(30), 24)

    def test_global(self):
        with tempfile.TemporaryDirectory(prefix='unittest-tinycm-') as tempdir:
            testfile = os.path.join(tempdir, 'testfile')

            d = FileDefinition('file::{}'.format(testfile), {
                'name': testfile,
                'type': 'constant',
                'contents': 'test {constant}'
            }, 'unittest', [], {})

            result = d.verify()
            self.assertFalse(result.success)
            self.assertIn('does not exist', result.message)

            with open(testfile, 'w') as handle:
                handle.write('test')

            result = d.verify()
            self.assertFalse(result.success)
            self.assertIn('File contents incorrect', result.message)

            d.execute()

            result = d.verify()
            self.assertTrue(result.success)

    def test_permissions(self):
        with tempfile.TemporaryDirectory(prefix='unittest-tinycm-') as tempdir:
            testfile = os.path.join(tempdir, 'testfile')

            d = FileDefinition('file::{}'.format(testfile), {
                'name': testfile,
                'type': 'constant',
                'contents': 'test',
                'owner': 1000,
                'group': 1000,
                'permission-mask': '777'
            }, 'unittest', [], {})

            result = d.verify()
            self.assertFalse(result.success)
            self.assertIn('does not exist', result.message)

            d.execute()

            result = d.verify()
            self.assertTrue(result.success)

    def test_remove(self):
        with tempfile.TemporaryDirectory(prefix='unittest-tinycm-') as tempdir:
            testfile = os.path.join(tempdir, 'testfile')

            d = FileDefinition('file::{}'.format(testfile), {
                'name': testfile,
                'type': 'constant',
                'contents': 'test',
            }, 'unittest', [], {})

            result = d.verify()
            self.assertFalse(result.success)
            self.assertIn('does not exist', result.message)

            d.execute()

            result = d.verify()
            self.assertTrue(result.success)

            d = FileDefinition('file::{}'.format(testfile), {
                'name': testfile,
                'type': 'constant',
                'contents': 'test',
                'ensure': 'removed'
            }, 'unittest', [], {})

            result = d.verify()
            self.assertFalse(result.success)

            d.execute()

            result = d.verify()
            self.assertTrue(result.success)

    def test_ensure_exists(self):
        with tempfile.TemporaryDirectory(prefix='unittest-tinycm-') as tempdir:
            testfile = os.path.join(tempdir, 'testfile')

            d = FileDefinition('file::{}'.format(testfile), {
                'name': testfile,
                'type': 'constant',
                'contents': 'test',
                'ensure': 'exists'
            }, 'unittest', [], {})

            result = d.verify()
            self.assertFalse(result.success)
            self.assertIn('does not exist', result.message)

            d.execute()

            result = d.verify()
            self.assertTrue(result.success)

            # Changing the file contents after creation should not matter
            with open(testfile, "w") as handle:
                handle.write("Completely different contents")

            result = d.verify()
            self.assertTrue(result.success)
