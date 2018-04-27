import unittest

from magnetto.filters import Order, OrderBy
from magnetto.apis import handler_filter_order

from fixtures import (mock_order_created_raw, mock_order_created_asc,
                      mock_order_created_desc, mock_order_name_raw,
                      mock_order_name_asc, mock_order_name_desc,
                      mock_order_downloads_raw, mock_order_downloads_asc,
                      mock_order_downloads_desc, mock_order_seeders_raw,
                      mock_order_seeders_asc, mock_order_seeders_desc,
                      mock_order_leechers_raw, mock_order_leechers_asc,
                      mock_order_leechers_desc, mock_order_size_raw,
                      mock_order_size_asc, mock_order_size_desc)


class TestFilterOrder(unittest.TestCase):

    def test_handler_filter_order_created_asc(self):
        items = handler_filter_order(mock_order_created_raw,
                                     Order.ASC,
                                     [OrderBy.CREATE])
        self.assertEqual(items, mock_order_created_asc)

    def test_handler_filter_order_created_desc(self):
        items = handler_filter_order(mock_order_created_raw,
                                     Order.DESC,
                                     [OrderBy.CREATE])
        self.assertEqual(items, mock_order_created_desc)

    def test_handler_filter_order_name_asc(self):
        items = handler_filter_order(mock_order_name_raw,
                                     Order.ASC,
                                     [OrderBy.NAME])
        self.assertEqual(items, mock_order_name_asc)

    def test_handler_filter_order_name_desc(self):
        items = handler_filter_order(mock_order_name_raw,
                                     Order.DESC,
                                     [OrderBy.NAME])
        self.assertEqual(items, mock_order_name_desc)

    def test_handler_filter_order_downloads_asc(self):
        items = handler_filter_order(mock_order_downloads_raw,
                                     Order.ASC,
                                     [OrderBy.DOWNLOADS])
        self.assertEqual(items, mock_order_downloads_asc)

    def test_handler_filter_order_downloads_desc(self):
        items = handler_filter_order(mock_order_downloads_raw,
                                     Order.DESC,
                                     [OrderBy.DOWNLOADS])
        self.assertEqual(items, mock_order_downloads_desc)

    def test_handler_filter_order_seeders_asc(self):
        items = handler_filter_order(mock_order_seeders_raw,
                                     Order.ASC,
                                     [OrderBy.SEEDERS])
        self.assertEqual(items, mock_order_seeders_asc)

    def test_handler_filter_order_seeders_desc(self):
        items = handler_filter_order(mock_order_seeders_raw,
                                     Order.DESC,
                                     [OrderBy.SEEDERS])
        self.assertEqual(items, mock_order_seeders_desc)

    def test_handler_filter_order_leechers_asc(self):
        items = handler_filter_order(mock_order_leechers_raw,
                                     Order.ASC,
                                     [OrderBy.LEECHERS])
        self.assertEqual(items, mock_order_leechers_asc)

    def test_handler_filter_order_leechers_desc(self):
        items = handler_filter_order(mock_order_leechers_raw,
                                     Order.DESC,
                                     [OrderBy.LEECHERS])
        self.assertEqual(items, mock_order_leechers_desc)

    def test_handler_filter_order_size_asc(self):
        items = handler_filter_order(mock_order_size_raw,
                                     Order.ASC,
                                     [OrderBy.SIZE])
        self.assertEqual(items, mock_order_size_asc)

    def test_handler_filter_order_size_desc(self):
        items = handler_filter_order(mock_order_size_raw,
                                     Order.DESC,
                                     [OrderBy.SIZE])
        self.assertEqual(items, mock_order_size_desc)
