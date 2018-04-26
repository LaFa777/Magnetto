from magnetto import ResultParse


def build_data(seeders):
    return ResultParse(
        id='',
        name='',
        url='',
        category='',
        size='',
        seeders=str(seeders),
        leechers='',
        downloads='',
        created='',
        magnet='',
        torrent='')


mock_nozeroseeders_1 = (
    build_data(0),
    build_data(25),
    build_data(0),
    build_data(11),
)
