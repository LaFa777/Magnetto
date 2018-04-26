from magnetto import ResultParse


def build_data(size):
    return ResultParse(
        id='',
        name='',
        url='',
        category='',
        size=str(size),
        seeders='',
        leechers='',
        downloads='',
        created='',
        magnet='',
        torrent='')


mock_size_1 = (
    build_data('1024'),
    build_data('1300'),
    build_data('2000'),
    build_data('4000'),
    build_data('5000'),
    build_data('10000'),
    build_data('30000'),
)
