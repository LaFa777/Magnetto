import re
import time
from collections import namedtuple
from magnetto import MagnettoParseError
from grab.error import DataNotFound

ResultParseSearchPage = namedtuple("ResultParseSearchPage", [
    "id",
    "name",
    "url",
    "category",
    "size",
    "seeders",
    "leechers",
    "downloads",
    "created",
    "magnet",
    "torrent"
])
"""Результат разбора страницы объектами типа :obj:`magnetto.BaseParser`

Attributes:
    id (str): id раздачи
    name (str): название раздачи
    url (str): ссылка на страницу с раздачей
    category (str): категория
    size (str): размер (в байтах)
    seeders (str): количество раздающих
    leechers (str): количество скачивающих
    downloads (str): количество скачиваний
    created (str): дата создания
    magnet (str): magnet ссылка
    torrent (str): ссылка на торрент файл
"""


def transformParseError(function):
    """Декоратор. Преобразует возможные типы Exception в результате парсинга
    страницы в единый формат - :obj:`magnetto.MagnettoParseError`.
    """

    def handleErrors(self, doc):
        try:
            return function(self, doc)
        except (DataNotFound, IndexError):
            raise MagnettoParseError
    return handleErrors


def parse_date(str):
    unix = 0

    time_str = re.findall(r'\d{1,2}:\d{2}', str)[0]
    date_str = re.findall(r'\d{1,2}\.\d{1,2}\.\d{4}', str)[0]

    datetime_str = "{} {}".format(date_str, time_str)

    unix = time.strptime(datetime_str, "%d.%m.%Y %H:%M")

    # переводим в timestamp
    return repr(time.mktime(unix))


def parse_size(str):
    size_str = re.findall(r'[\d\.]+', str)[0]
    size_int = int(float(size_str))
    size_mb = 0
    if "ГБ" in str or "GB" in str:
        size_mb = size_int * 1024
    elif "МБ" in str or "MB" in str:
        size_mb = size_int
    # TODO: по умолчанию считать байтами?
    else:
        raise MagnettoParseError(
            "Invalid parse size_str(\"{}\")".format(size_str))

    return repr(size_mb)
