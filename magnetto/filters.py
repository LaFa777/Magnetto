from enum import Enum
from magnetto import MagnettoMisuseError


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


class Resolution(Enum):
    """Фильтр по разрешениям для фильмов

    Attributes:
        HD: 720p
        FULLHD: 1080p
        ULTRA_HD: 4k
    """
    HD = "720p"
    FULL_HD = "1080p"
    ULTRA_HD = "2160p"


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


class Registered(Enum):
    """Дата регистрации раздачи
    """
    TODAY = 1
    YESTERDAY = 2
    FOR_3_DAYS = 3
    FOR_WEEK = 4
    FOR_MONTH = 5


class TypeRelease(Enum):
    """Тип раздачи (для сохранения рейтинга на трекерах)

    Attributes:
        SILVER: засчитывается половина рейтинга
        GOLD: рейтинг не считается
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
        LARGE: 9.5ГБ - 25ГБ
        HUGE: 25ГБ и выше
    """
    TINY = 1
    SMALL = 2
    MEDIUM = 3
    BIG = 4
    LARGE = 5
    HUGE = 6


class Year:
    """Даты выхода содержимого раздачи (фильм, игра...)
    """

    def __init__(self, year):
        self.year = str(year)

    def __str__(self):
        return str(self.year)


class NoZeroSeeders:
    """Фильтр исключает из конечной выборки раздачи с 0 сидерами
    """
    pass


class NoWords:
    """Фильтр исключает из конечной выборки раздачи данными словами
    """

    def __init__(self, *argv):
        """
        Attributes:
            argv (List[str]): Слова для исключения из выдачи
        """
        self.argv = []
        for arg in argv:
            self.argv.append(arg.lower())

    def __contains__(self, str):
        for arg in self.argv:
            if arg in str.lower():
                return True


class NoEqualSize:
    """Исключение раздач с одинаковым размером. По умолчанию разрешается
    расхождение в размере не более 10%.
    """

    def __init__(self, size=10):
        """
        Attributes:
            size (int): Допустимый процент разброса по размеру
        """
        if size <= 0 or size >= 100:
            raise MagnettoMisuseError("Arg must be int (0 < x < 100)")

        self.size = size

    def __int__(self):
        return int(self.size)
