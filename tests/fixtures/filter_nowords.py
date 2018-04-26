from magnetto import ResultParse


def build_data(name):
    return ResultParse(
        id='',
        name=str(name),
        url='',
        category='',
        size='',
        seeders='',
        leechers='',
        downloads='',
        created='',
        magnet='',
        torrent='')


mock_nowords_1 = (
    build_data("python books 12"),
    build_data("best modules"),
    build_data("Введение в Magnetto"),
)
