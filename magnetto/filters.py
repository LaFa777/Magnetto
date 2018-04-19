from enum import Enum


class Category(Enum):
    """Фильтр по категориям (если указанный фильтр не поддерживается трекером,
    то трекер не Выполняет поиск)
    """
    FILMS = 1
    TV_SERIES = 2
    CARTOONS = 3
    MUSICS = 4
    BOOKS = 5
    AUDIOBOOKS = 6
    GAMES = 7
    PROGRAMS = 8


class Resolution(Enum):
    """Фильтр по разрешениям для фильмов

    Attributes:
        HD: 720p
        FULLHD: 1080p
        ULTRA_HD: 4k
    """
    HD = 1
    FULL_HD = 2
    ULTRA_HD = 3


class Source(Enum):
    """Фильтры по качеству источника
    """
    TV_RIP = "TVRIP,TV-RIP,SDTV-RIP,SAT-RIP,SATRIP,HDTV-RIP,HDTVRIP"
    WEB_DL_RIP = "WEB-DL,WEBRIP"
    HD_RIP = "HDDVD-RIP,HDDVD-RIP,HDRIP,HD-RIP"
    BD_RIP = "BLU_RAY,BLURAY,BD-RIP,BDRIP"
    VHS_RIP = "VHS-RIP,VHSRIP"
    DVD_RIP = "DVDRIP,DVD-RIP"
    CAM_RIP = "CAMRIP,CAM-RIP"


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
        SIZE: Размер
        MESSAGES: Количество сообщений в топике
        LAST_MESSAGE: Последнее сообщение
    """
    CREATE = 1
    NAME = 2
    DOWNLOADS = 3
    SEEDERS = 4
    LEECHERS = 5
    SIZE = 6
    MESSAGES = 7
    LAST_MESSAGE = 8
    VIEWS = 9


class Registred(Enum):
    """Дата регистрации раздачи
    """
    TODAY = 1
    YESTERDAY = 2
    FOR_3_DAYS = 3
    FOR_WEEK = 4
    FOR_MONTH = 5


class TypeRelease(Enum):
    """Тип раздачи (для сохранения рейтинга на трекерах)
    """
    SILVER = 1
    GOLD = 2


class Size(Enum):
    """Размер  раздачи (в основном применим для фильмов).

    Attributes:
        TINY: меньше 1.3ГБ
        SMALL: 1.3ГБ - 2.2ГБ
        MEDIUM: 2.2ГБ - 4.0ГБ
        BIG: 4.0ГБ - 9.5ГБ
        HUGE: 9.5ГБ и выше
    """
    TINY = 1
    SMALL = 2
    MEDIUM = 3
    BIG = 4
    HUGE = 5


class Year:
    """Даты выхода содержимого раздачи (фильм, игра...)
    """

    def __init__(self, year):
        self.year = year

    def __str__(self):
        return self.year
