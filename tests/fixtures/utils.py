from magnetto import ResultParse
from magnetto.filters import Category


def build_data(id='1234', name='test', url='http://localhost:80', size='0',
               magnet='hd4G', torrent="http://localhost:80", created="12",
               category=Category.UNDEFINED, seeders='0', leechers='0',
               downloads='0'):
    return ResultParse(
        id=str(id),
        name=name,
        url=url,
        category=category,
        size=str(size),
        seeders=str(seeders),
        leechers=str(leechers),
        downloads=str(downloads),
        created=str(int(float(created))),
        magnet=magnet,
        torrent=torrent)
