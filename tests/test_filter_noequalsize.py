import unittest

from magnetto.filters import NoEqualSize
from magnetto.apis import handler_filter_noequalsize

from fixtures import mock_noequalsize_1, mock_noequalsize_2


class TestFilterNoEqualSize(unittest.TestCase):

    def test_handler_filter_noequalsize_default(self):
        items = handler_filter_noequalsize(
            mock_noequalsize_1, NoEqualSize, [NoEqualSize])
        self.assertEqual(len(items), 4)

    def test_handler_filter_noequalsize_default_obj(self):
        items = handler_filter_noequalsize(
            mock_noequalsize_1, NoEqualSize(), [NoEqualSize()])
        self.assertEqual(len(items), 4)

    def test_handler_filter_noequalsize(self):
        items = handler_filter_noequalsize(
            mock_noequalsize_1, NoEqualSize(50), [NoEqualSize(50)])
        self.assertEqual(len(items), 2)

    # проверка на идентичность сортировки после удаления
    def test_handler_filter_noequalsize_save_sorted(self):
        items = handler_filter_noequalsize(
            mock_noequalsize_1, NoEqualSize(50), [NoEqualSize(50)])
        self.assertEqual(items, mock_noequalsize_2)
