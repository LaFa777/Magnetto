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


mock_noequalsize_1 = (
    build_data('5000'),
    build_data('1024'),
    build_data('1000'),
    build_data('2000'),
    build_data('1500'),
)

mock_noequalsize_2 = [
    build_data('5000'),
    build_data('2000'),
]
