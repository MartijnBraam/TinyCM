from unittest import TestCase
from tinycm.definitions.file import FileDefinition


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