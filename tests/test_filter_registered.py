import unittest

from magnetto.filters import Registered
from magnetto.apis import handler_filter_registered

from fixtures import mock_registered_1


class TestFilterRegistered(unittest.TestCase):

    def test_handler_filter_registered_today(self):
        items = handler_filter_registered(mock_registered_1, Registered.TODAY)
        self.assertEqual(len(items), 1)

    def test_handler_filter_registered_yesterday(self):
        items = handler_filter_registered(
            mock_registered_1, Registered.YESTERDAY)
        self.assertEqual(len(items), 2)

    def test_handler_filter_registered_for_3_days(self):
        items = handler_filter_registered(
            mock_registered_1, Registered.FOR_3_DAYS)
        self.assertEqual(len(items), 3)

    def test_handler_filter_registered_for_week(self):
        items = handler_filter_registered(
            mock_registered_1, Registered.FOR_WEEK)
        self.assertEqual(len(items), 4)

    def test_handler_filter_registered_for_month(self):
        items = handler_filter_registered(
            mock_registered_1, Registered.FOR_MONTH)
        self.assertEqual(len(items), 5)

    def test_handler_filter_registered_for_year(self):
        items = handler_filter_registered(
            mock_registered_1, Registered.FOR_YEAR)
        self.assertEqual(len(items), 6)
