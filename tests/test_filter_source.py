import unittest

from magnetto.filters import Source
from magnetto.apis import handler_filter_source

from fixtures import mock_source_1


class TestFilterSource(unittest.TestCase):

    def test_handler_filter_source_tv_rip(self):
        items = handler_filter_source(
            mock_source_1, Source.TV_RIP, [Source.TV_RIP])
        self.assertEqual(len(items), 1)

    def test_handler_filter_source_web_dl_rip(self):
        items = handler_filter_source(
            mock_source_1, Source.WEB_DL_RIP, [Source.WEB_DL_RIP])
        self.assertEqual(len(items), 1)

    def test_handler_filter_source_bd_rip(self):
        items = handler_filter_source(
            mock_source_1, Source.BD_RIP, [Source.BD_RIP])
        self.assertEqual(len(items), 1)

    def test_handler_filter_source_vhs_rip(self):
        items = handler_filter_source(
            mock_source_1, Source.VHS_RIP, [Source.VHS_RIP])
        self.assertEqual(len(items), 1)

    def test_handler_filter_source_dvd_rip(self):
        items = handler_filter_source(
            mock_source_1, Source.DVD_RIP, [Source.DVD_RIP])
        self.assertEqual(len(items), 1)

    def test_handler_filter_source_cam_rip(self):
        items = handler_filter_source(
            mock_source_1, Source.CAM_RIP, [Source.CAM_RIP])
        self.assertEqual(len(items), 1)

    def test_handler_filter_source_hd_rip(self):
        items = handler_filter_source(
            mock_source_1, Source.HD_RIP, [Source.HD_RIP])
        self.assertEqual(len(items), 1)
