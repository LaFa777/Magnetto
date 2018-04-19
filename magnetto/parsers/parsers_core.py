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
