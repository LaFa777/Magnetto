import unittest

from magnetto.filters import Category
from magnetto.apis import handler_filter_category

from fixtures import mock_category_1


class TestFilterCategory(unittest.TestCase):

    def test_handler_filter_category_undefined(self):
        items = handler_filter_category(
            mock_category_1, Category.UNDEFINED)
        self.assertEqual(len(items), 1)

    def test_handler_filter_category_films(self):
        items = handler_filter_category(
            mock_category_1, Category.FILMS)
        self.assertEqual(len(items), 1)

    def test_handler_filter_category_tv_series(self):
        items = handler_filter_category(
            mock_category_1, Category.TV_SERIES)
        self.assertEqual(len(items), 1)

    def test_handler_filter_category_cartoons(self):
        items = handler_filter_category(
            mock_category_1, Category.CARTOONS)
        self.assertEqual(len(items), 1)

    def test_handler_filter_category_musics(self):
        items = handler_filter_category(
            mock_category_1, Category.MUSICS)
        self.assertEqual(len(items), 1)

    def test_handler_filter_category_books(self):
        items = handler_filter_category(
            mock_category_1, Category.BOOKS)
        self.assertEqual(len(items), 1)

    def test_handler_filter_category_audiobooks(self):
        items = handler_filter_category(
            mock_category_1, Category.AUDIOBOOKS)
        self.assertEqual(len(items), 1)

    def test_handler_filter_category_games(self):
        items = handler_filter_category(
            mock_category_1, Category.GAMES)
        self.assertEqual(len(items), 1)

    def test_handler_filter_category_programs(self):
        items = handler_filter_category(
            mock_category_1, Category.PROGRAMS)
        self.assertEqual(len(items), 1)
