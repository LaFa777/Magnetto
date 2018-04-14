from enum import Enum


class Category(Enum):
    """Фильтр для вызова Api методов. Уточняет поиск по категории.

    Attributes:
        FILMS: Фильмы
    """
    FILMS = 1


class Order(Enum):
    """Фильтр для вызова Api методов. Указывает вид сортировки.

    Attributes:
        DESC: По убыванию
        ASC: По возрастанию
    """
    DESC = 1
    ASC = 2


class OrderBy(Enum):
    """Фильтр для вызова Api методов. Указывает колонку для сортировки.

    Attributes:
        CREATE: Дата создания
        NAME: Название темы
        DOWNLOADS: Количество скачиваний
        SEEDER: Количество сидеров
        LEECHER: Количество личей
        MESSAGES: Количество сообщений в топике
        LAST_MESSAGE: Последнее сообщение
    """
    CREATE = 1
    NAME = 2
    DOWNLOADS = 3
    SEEDER = 4
    LEECHER = 5
    MESSAGES = 6
    LAST_MESSAGE = 7
