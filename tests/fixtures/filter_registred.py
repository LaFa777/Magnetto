from time import time
from magnetto import ResultParse


def build_data(time):
    return ResultParse(
        id='',
        name='',
        url='',
        category='',
        size='',
        seeders='',
        leechers='',
        downloads='',
        created=str(int(float(time))),
        magnet='',
        torrent='')


HOUR = 60 * 60
DAY = HOUR * 24

mock_registred_1 = (
    build_data(time() - HOUR),  # TODAY
    build_data(time() - DAY * 2 + HOUR),  # YESTERDAY
    build_data(time() - DAY * 3 + HOUR),  # FOR_3_DAYS
    build_data(time() - DAY * 7 + HOUR),  # FOR_WEEK
    build_data(time() - DAY * 32 + HOUR),  # FOR_MONTH
    build_data(time() - DAY * 367 + HOUR),  # FOR_YEAR
)
