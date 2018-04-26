import unittest

from magnetto.filters import Registred
from magnetto.apis import handler_filter_registred

from .fixtures import mock_registred_1


class TestFilterRegistred(unittest.TestCase):

    def test_handler_filter_registred_today(self):
        items = handler_filter_registred(mock_registred_1, Registred.TODAY)
        self.assertEqual(len(items), 1)

    def test_handler_filter_registred_yesterday(self):
        items = handler_filter_registred(mock_registred_1, Registred.YESTERDAY)
        self.assertEqual(len(items), 2)

    def test_handler_filter_registred_for_3_days(self):
        items = handler_filter_registred(
            mock_registred_1, Registred.FOR_3_DAYS)
        self.assertEqual(len(items), 3)

    def test_handler_filter_registred_for_week(self):
        items = handler_filter_registred(mock_registred_1, Registred.FOR_WEEK)
        self.assertEqual(len(items), 4)

    def test_handler_filter_registred_for_month(self):
        items = handler_filter_registred(mock_registred_1, Registred.FOR_MONTH)
        self.assertEqual(len(items), 5)
