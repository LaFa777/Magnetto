import unittest

from magnetto.errors import MagnettoMisuseError
from magnetto.filters import Year
from magnetto.apis import handler_filter_year

from fixtures import mock_year_1


class TestFilterYear(unittest.TestCase):

    def test_handler_filter_year(self):
        items = handler_filter_year(
            mock_year_1, Year(2015), [Year(2015)])
        self.assertEqual(len(items), 1)

    def test_handler_filter_year_str(self):
        items = handler_filter_year(
            mock_year_1, Year('2014'), [Year('2014')])
        self.assertEqual(len(items), 2)

    def test_handler_filter_year_misuse(self):
        with self.assertRaises(MagnettoMisuseError):
            handler_filter_year(mock_year_1, Year("Test"), [Year("Test")])
        with self.assertRaises(MagnettoMisuseError):
            handler_filter_year(mock_year_1, Year, [Year])
