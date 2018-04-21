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


def parse_size(size_str):
    size_parse = int(re.findall(r'[\d\.]+', size_str)[0])
    size_mb = 0
    if "ГБ" in size_str or "GB" in size_str:
        size_mb = size_parse * 1024
    elif "МБ" in size_str or "MB" in size_str:
        size_mb = size_parse
    # TODO: по умолчанию считать байтами?
    else:
        raise MagnettoParseError("Invalid parse size_str(\"{}\")".format(size_str))

    return str(size_mb)
