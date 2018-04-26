from magnetto import ResultParse, Category


def build_data(category):
    return ResultParse(
        id='',
        name='',
        url='',
        category=category,
        size='',
        seeders='',
        leechers='',
        downloads='',
        created='',
        magnet='',
        torrent='')


mock_category_1 = (
    build_data(Category.UNDEFINED),
    build_data(Category.FILMS),
    build_data(Category.TV_SERIES),
    build_data(Category.CARTOONS),
    build_data(Category.MUSICS),
    build_data(Category.BOOKS),
    build_data(Category.AUDIOBOOKS),
    build_data(Category.GAMES),
    build_data(Category.PROGRAMS),
)
