from .utils import build_data
from magnetto import Category


mock_category_1 = (
    build_data(category=Category.UNDEFINED),
    build_data(category=Category.FILMS),
    build_data(category=Category.TV_SERIES),
    build_data(category=Category.CARTOONS),
    build_data(category=Category.MUSICS),
    build_data(category=Category.BOOKS),
    build_data(category=Category.AUDIOBOOKS),
    build_data(category=Category.GAMES),
    build_data(category=Category.PROGRAMS),
)
