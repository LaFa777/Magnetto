import unittest

from magnetto.filters import NoZeroSeeders
from magnetto.apis import handler_filter_nozeroseeders

from .fixtures import mock_nozeroseeders_1


class TestFilterNoZeroSeeders(unittest.TestCase):

    def test_handler_filter_nozeroseeders(self):
        items = handler_filter_nozeroseeders(
            mock_nozeroseeders_1, NoZeroSeeders)
        self.assertEqual(len(items), 2)
