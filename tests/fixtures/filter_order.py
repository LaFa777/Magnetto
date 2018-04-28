from time import time

from .utils import build_data


def filter_asc(items):
    return [
        items[0],
        items[2],
        items[1],
        items[3],
    ]


def filter_desc(items):
    return filter_asc(items)[::-1]


HOUR = 60 * 60
DAY = HOUR * 24


mock_order_created_raw = [
    build_data(created=(time() + HOUR)),
    build_data(created=(time() + HOUR * 5)),
    build_data(created=(time() + HOUR * 3)),
    build_data(created=(time() + HOUR * 10)),
]
mock_order_created_asc = filter_asc(mock_order_created_raw)
mock_order_created_desc = filter_desc(mock_order_created_raw)

mock_order_name_raw = [
    build_data(name="aaa a"),
    build_data(name="aca a"),
    build_data(name="aaa b"),
    build_data(name="yip"),
]
mock_order_name_asc = filter_asc(mock_order_name_raw)
mock_order_name_desc = filter_desc(mock_order_name_raw)

mock_order_downloads_raw = [
    build_data(downloads=1),
    build_data(downloads=50),
    build_data(downloads=3),
    build_data(downloads=4000),
]
mock_order_downloads_asc = filter_asc(mock_order_downloads_raw)
mock_order_downloads_desc = filter_desc(mock_order_downloads_raw)

mock_order_seeders_raw = [
    build_data(seeders=1),
    build_data(seeders=50),
    build_data(seeders=3),
    build_data(seeders=4000),
]
mock_order_seeders_asc = filter_asc(mock_order_seeders_raw)
mock_order_seeders_desc = filter_desc(mock_order_seeders_raw)

mock_order_leechers_raw = [
    build_data(leechers=1),
    build_data(leechers=50),
    build_data(leechers=3),
    build_data(leechers=4000),
]
mock_order_leechers_asc = filter_asc(mock_order_leechers_raw)
mock_order_leechers_desc = filter_desc(mock_order_leechers_raw)

mock_order_size_raw = [
    build_data(size=1),
    build_data(size=50),
    build_data(size=3),
    build_data(size=4000),
]
mock_order_size_asc = filter_asc(mock_order_size_raw)
mock_order_size_desc = filter_desc(mock_order_size_raw)
