import re
import time
from attr import attrs, attrib, validators
from magnetto.errors import MagnettoParseError
from magnetto.filters import Category
from grab.error import DataNotFound


def check_is_digit(self, attr, value):
    if not value.isdigit():
        raise ValueError("{attr} must be digit".format(attr=attr.name))


@attrs(frozen=True)
class ResultParse:
    """Результат разбора страницы объектами типа ``BaseParser``

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

    id = attrib(validator=[validators.instance_of(str), check_is_digit])
    name = attrib(validator=[validators.instance_of(str), ])
    # TODO: валидация
    url = attrib(validator=[validators.instance_of(str), ])
    size = attrib(validator=[validators.instance_of(str), check_is_digit])
    magnet = attrib(validator=[validators.instance_of(str), ])
    torrent = attrib(validator=[validators.instance_of(str), ])
    # TODO: валидация
    seeders = attrib(default='0', validator=[
                     validators.instance_of(str), check_is_digit])
    leechers = attrib(default='0', validator=[
                      validators.instance_of(str), check_is_digit])
    downloads = attrib(default='0', validator=[
                       validators.instance_of(str), check_is_digit])
    created = attrib(default='0', validator=[
                     validators.instance_of(str), check_is_digit])
    category = attrib(default=Category.UNDEFINED)


def transformParseError(function):
    """Декоратор. Преобразует возможные типы Exception в результате парсинга
    страницы в единый формат - ``MagnettoParseError``.
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
