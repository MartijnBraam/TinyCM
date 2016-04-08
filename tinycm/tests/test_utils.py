from unittest import TestCase
from tinycm.utils import http_dirname, http_join


class TestUtils(TestCase):
    def test_http_dirname(self):
        tests = [
            ('http://example.com/index.html', 'http://example.com/'),
            ('http://example.com/somewhere/index.html', 'http://example.com/somewhere'),
            ('https://example.com/somewhere/index.html', 'https://example.com/somewhere'),
            ('https://example.com/', 'https://example.com/'),
            ('https://example.com/?timestamp=1234', 'https://example.com/?timestamp=1234'),
            ('https://example.com/index.html?timestamp=1234', 'https://example.com/?timestamp=1234'),
            ('https://example.com/dir/index.html?timestamp=1234', 'https://example.com/dir?timestamp=1234'),
            ('https://user:pass@example.com/dir/index.html', 'https://user:pass@example.com/dir'),
        ]
        for test in tests:
            self.assertEqual(test[1], http_dirname(test[0]))

    def test_http_join(self):
        tests = [
            (
                ["http://example.com", "dir"],
                "http://example.com/dir"
            ),
            (
                ["http://example.com/dir", "foo"],
                "http://example.com/dir/foo"
            ),
            (
                ["http://example.com/dir", "foo.example"],
                "http://example.com/dir/foo.example"
            ),
            (
                ["http://example.com/dir?t=2", "foo.example"],
                "http://example.com/dir/foo.example?t=2"
            ),
        ]
        for test in tests:
            self.assertEqual(test[1], http_join(*test[0]))