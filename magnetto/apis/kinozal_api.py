from urllib.parse import quote_plus

from grab import Grab

import magnetto
from magnetto.errors import (MagnettoIncorrectСredentials, MagnettoMisuseError,
                             MagnettoAuthError)
from magnetto.filters import (Category, OrderBy, Order, Year, Resolution,
                              Registered, TypeRelease, Size, Source)
from magnetto.apis.core import api_filters_method
from magnetto.apis.mixins import LastRequestMixin, CheckAuthMixin
from magnetto.apis import BaseApi
from magnetto.parsers import KinozalParser


class KinozalApi(BaseApi, CheckAuthMixin, LastRequestMixin):

    HOME = None

    def __init__(self, grab=Grab()):
        self._grab = grab.clone()
        self._parser = KinozalParser()
        self._login = ""
        self._password = ""
        self.HOME = magnetto.KINOZAL_URL

    def authorization(self, login, password, captcha=None):
        """
        Note:
            * На сайте нету капчи.
            * Обнаружить что вы залогинены можно только путем запроса на
              главную или просмотром кук
        """
        if not self._login and captcha:
            raise MagnettoMisuseError("Please execute "
                                      ".authorization(login, pass) first")

        self._login = login
        self._password = password

        doc = self._grab.go(self.HOME + "login.php")

        # заполняем форму входа
        doc.set_input('username', login)
        doc.set_input('password', password)

        doc = doc.submit()

        # проверка успешности входа
        if ("login" not in doc.url) and doc.tree.xpath('//*[@class="red"]'):
            raise MagnettoIncorrectСredentials()

        return True

    @api_filters_method
    def search(self, query, filters=[], page=0, limit=999):

        # вход не был выполнен
        if not self._login:
            raise MagnettoAuthError()

        RESULTS_ON_PAGE = 50

        # формируем урл для поиска
        url = "{home}browse.php?page={page}".format(
            home=self.HOME,
            page=RESULTS_ON_PAGE * page
        )

        # таблица соответствий фильтров и модифицируемой переменной
        # 0 - url, 1 - query
        filtersTable = {
            Order.DESC: ["&f=0", ''],
            Order.ASC: ['&f=1', ''],

            Category.TV_SERIES: ['&c=1001', ''],
            Category.FILMS: ['&c=1002', ''],
            Category.CARTOONS: ['&c=1003', ''],
            Category.MUSICS: ['&c=1004', ''],
            Category.AUDIOBOOKS: ['&c=2', ''],
            Category.GAMES: ['&c=23', ''],
            Category.PROGRAMS: ['&c=32', ''],
            Category.BOOKS: ['&c=41', ''],

            Resolution.HD: ['&v=3', ' 720p'],
            Resolution.FULL_HD: ['&v=3', ' 1080p'],
            Resolution.ULTRA_HD: ['&v=7', ' 2160p'],

            Source.TV_RIP: ['&v=5', ''],
            Source.WEB_DL_RIP: ['&v=1', ' WEB-DLRip'],
            Source.HD_RIP: ['&v=1', ' HDRip'],
            Source.BD_RIP: ['&v=1', ' BDRip'],
            Source.VHS_RIP: ['', ' VHSRip'],
            Source.DVD_RIP: ['&v=1', ' DVDRip'],
            Source.CAM_RIP: ['', ''],

            OrderBy.CREATE: ['&t=0', ''],
            OrderBy.NAME: ['', ''],  # не реализуем
            OrderBy.DOWNLOADS: ['&t=5', ''],
            OrderBy.SEEDERS: ['&t=1', ''],
            OrderBy.LEECHERS: ['&t=2', ''],
            OrderBy.MESSAGES: ['&t=4', ''],
            OrderBy.VIEWS: ['', ''],
            OrderBy.SIZE: ['&t=3', ''],
            OrderBy.LAST_MESSAGE: ['&t=6', ''],

            Registered.TODAY: ['&w=1', ''],
            Registered.YESTERDAY: ['&w=2', ''],
            Registered.FOR_3_DAYS: ['&w=3', ''],
            Registered.FOR_WEEK: ['&w=4', ''],
            Registered.FOR_MONTH: ['&w=5', ''],

            TypeRelease.SILVER: ['&w=12', ''],
            TypeRelease.GOLD: ['&w=11', ''],

            Size.TINY: ['&w=6', ''],
            Size.SMALL: ['&w=7', ''],
            Size.MEDIUM: ['&w=8', ''],
            Size.BIG: ['&w=9', ''],
            Size.LARGE: ['&w=10', ''],
        }

        # соотносим фильтры из таблицы их действиям
        for filter in filters:
            url += filtersTable.get(filter, [""])[0]
            query += filtersTable.get(filter, [""])[0]

        # проставляем год
        for filter in filters:
            if type(filter) is Year:
                url += "&d=" + str(filter)

        # добавляем возможно модифицированный поисковый запрос
        url += "&s=" + quote_plus(query)

        # подготавливаем для запроса
        self._grab.setup(url=url)

        # выполняем сам запрос
        self._grab.request()

        # проверяем, что после выполнения запроса мы залогинены
        self.is_logged()

        # разбор страницы
        items = self._parser.parse_search(self._grab.doc)

        return items
