from enum import Enum


class Category(Enum):
    Film = 1
    # Game = 2


class Order(Enum):
    DESC = 1  # по убыванию
    ASC = 2  # по возрастанию


class OrderBy(Enum):
    CREATE = 1  # зарегистрирован
    NAME = 2  # название темы
    DOWNLOADS = 3  # Количество скачиваний
    SEEDER = 4  # количество сидов
    LEECHER = 5  # количество личей
    MESSAGES = 6  # количество сообщений
    LAST_MESSAGE = 7  # последнее сообщение


class SearchItem(object):
    category = ""
    name = ""
    url = ""
    author = ""
    size = ""
    seeders = ""
    leechers = ""
    downloads = ""
    created = ""
    magnet = ""
