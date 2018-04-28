import unittest

from magnetto.filters import Resolution
from magnetto.apis import handler_filter_resolution

from fixtures import mock_resolution_1


class TestFilterResolution(unittest.TestCase):

    def test_handler_filter_resolution_hd(self):
        items = handler_filter_resolution(
            mock_resolution_1, Resolution.HD, [Resolution.HD])
        self.assertEqual(len(items), 1)

    def test_handler_filter_resolution_full_hd(self):
        items = handler_filter_resolution(
            mock_resolution_1, Resolution.FULL_HD, [Resolution.FULL_HD])
        self.assertEqual(len(items), 1)

    def test_handler_filter_resolution_ultra_hd(self):
        items = handler_filter_resolution(
            mock_resolution_1, Resolution.ULTRA_HD, [Resolution.ULTRA_HD])
        self.assertEqual(len(items), 1)
