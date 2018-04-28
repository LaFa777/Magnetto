import unittest

from magnetto.filters import Size
from magnetto.apis import handler_filter_size

from fixtures import mock_size_1


class TestFilterSize(unittest.TestCase):

    def test_handler_filter_size_tyny(self):
        items = handler_filter_size(mock_size_1, Size.TINY, [Size.TINY])
        self.assertEqual(len(items), 2)

    def test_handler_filter_size_small(self):
        items = handler_filter_size(mock_size_1, Size.SMALL, [Size.SMALL])
        self.assertEqual(len(items), 1)

    def test_handler_filter_size_medium(self):
        items = handler_filter_size(mock_size_1, Size.MEDIUM, [Size.MEDIUM])
        self.assertEqual(len(items), 1)

    def test_handler_filter_size_big(self):
        items = handler_filter_size(mock_size_1, Size.BIG, [Size.BIG])
        self.assertEqual(len(items), 1)

    def test_handler_filter_size_large(self):
        items = handler_filter_size(mock_size_1, Size.LARGE, [Size.LARGE])
        self.assertEqual(len(items), 1)

    def test_handler_filter_size_huge(self):
        items = handler_filter_size(mock_size_1, Size.HUGE, [Size.HUGE])
        self.assertEqual(len(items), 1)
