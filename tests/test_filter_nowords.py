import unittest

from magnetto.errors import MagnettoMisuseError
from magnetto.filters import NoWords
from magnetto.apis import handler_filter_nowords

from fixtures import mock_nowords_1


class TestFilterNoWords(unittest.TestCase):

    def test_handler_filter_nowords_misuseerror(self):
        with self.assertRaises(MagnettoMisuseError):
            handler_filter_nowords(mock_nowords_1, NoWords)

    def test_handler_filter_nowords(self):
        items = handler_filter_nowords(mock_nowords_1, NoWords("ведение"))
        self.assertEqual(len(items), 2)
