from enum import Enum
from collections import UserList
from magnetto import MagnettoMisuseError


class OrderBy(Enum):
    """Колонка для сортировки. !!!Применим только в качестве аргумента фильтра
    Order.

    Attributes:
        CREATE: Дата создания
        NAME: Название темы
        DOWNLOADS: Количество скачиваний
        SEEDERS: Количество сидеров
        LEECHERS: Количество личей
        SIZE: Размер
    """
    CREATE = 1
    NAME = 2
    DOWNLOADS = 3
    SEEDERS = 4
    LEECHERS = 5
    SIZE = 6


class Order:
    """Устанавливает порядок сортировки по убыванию/возрастанию и указывает
    колонку для сортировки

    Example:
        >>> Order(OrderBy.SEEDERS)
        >>> Order(OrderBy.SEEDERS, True)
    """

    def __init__(self, column, asc=False):
        if column not in OrderBy:
            raise MagnettoMisuseError(
                "first arg must be one element from OrderBy."
                "Example: Order(OrderBy.SEEDERS)")

        self.column = column
        self.asc = asc


class Category(Enum):
    """Фильтр по категориям (если указанный фильтр не поддерживается трекером,
    то трекер не выполняет поиск)
    """
    UNDEFINED = 0
    FILMS = 1
    TV_SERIES = 2
    CARTOONS = 3
    MUSICS = 4
    BOOKS = 5
    AUDIOBOOKS = 6
    GAMES = 7
    PROGRAMS = 8


class VideoResolution(Enum):
    """Требуемое разрешение для фильма

    Attributes:
        HD: 720p
        FULLHD: 1080p
        ULTRA_HD: 4k
    """
    HD = "720p"
    FULL_HD = "1080p"
    ULTRA_HD = "2160p"

    def __str__(self):
        return str(self.value)


class VideoSource(Enum):
    """Необходимое качество источника
    """
    TV_RIP = "TVRIP,TV-RIP,SDTV-RIP,SAT-RIP,SATRIP,HDTV-RIP,HDTVRIP"
    WEB_DL_RIP = "WEB-DL,WEBRIP"
    HD_RIP = "HDDVD-RIP,HDDVD-RIP,HDRIP,HD-RIP"
    BD_RIP = "BLU_RAY,BLURAY,BD-RIP,BDRIP"
    VHS_RIP = "VHS-RIP,VHSRIP"
    DVD_RIP = "DVDRIP,DVD-RIP"
    CAM_RIP = "CAMRIP,CAM-RIP"

    def __str__(self):
        return str(self.value)

    def __iter__(self):
        for word in self.value.split(','):
            yield word


class DateRegistered(Enum):
    """Дата регистрации раздачи
    """
    TODAY = 1
    YESTERDAY = 2
    FOR_3_DAYS = 3
    FOR_WEEK = 4
    FOR_MONTH = 5
    FOR_YEAR = 6


class TypeRelease(Enum):
    """Тип раздачи (для сохранения рейтинга на трекерах)

    Attributes:
        SILVER: засчитывается половина рейтинга
        GOLD: рейтинг не считается
    """
    SILVER = 1
    GOLD = 2


class LimitSize:
    """Удаляет раздачи, размер которых больше указанного

    Attributes:
        size (int): размер в мегабайтах. Примеры: [1, "1024", "1024GB", "1024МБ"]
    """

    def __init__(self, size):
        size = str(size)

        # указанная строка содержит только число
        if size.isdigit():
            size += "MB"

        self.size = parse_size(size)

    def __int__(self):
        return int(self.size)


class NoZeroSeeders:
    """Фильтр исключает из конечной выборки раздачи с 0 сидерами
    """
    pass


class NoWords(UserList):
    """Фильтр исключает из конечной выборки раздачи с перечисленными словами.
    Регистронезависимый фильтр.
    """

    def __init__(self, *args):
        """
        Attributes:
            argv (str, ...): Слова для исключения из выдачи
        """
        self.data = args


class NoEqualSize:
    """Исключение раздач с одинаковым размером. По умолчанию разрешается
    расхождение в размере не более 10%.

    Attributes:
        percent(int): Допустимый процент разброса по размеру
    """

    def __init__(self, percent=10):
        """
        Attributes:
            percent (int): Допустимый процент разброса по размеру
        """
        if percent <= 0 or percent >= 100:
            raise MagnettoMisuseError("Arg must be int (0 < x < 100)")

        self.percent = percent

    def __int__(self):
        return int(self.percent)


class Limit:
    """Ограничивает количество результатов

    Attributes:
        limit (int): количество результатов
    """

    def __init__(self, limit):
        self.limit = limit

    def __int__(self):
        return int(self.limit)
