from urllib.parse import quote_plus

from grab import Grab
from grab.error import DataNotFound

import magnetto
from magnetto.errors import (MagnettoCaptchaError, MagnettoMisuseError,
                             MagnettoAuthError, MagnettoIncorrectСredentials)
from magnetto.filters import OrderBy, Order, Resolution, Source, Year

from magnetto.apis.core import api_filters_method
from magnetto.apis import BaseApi
from magnetto.apis.mixins import CheckAuthMixin, LastRequestMixin

from magnetto.parsers import RutrackerParser


class RutrackerApi(BaseApi, CheckAuthMixin, LastRequestMixin):

    HOME = None

    def __init__(self, grab=Grab()):
        self._grab = grab.clone()
        self._parser = RutrackerParser()
        self._login = ""
        self._password = ""
        self.HOME = magnetto.RUTRACKER_URL

    def authorization(self, login, password, captcha=None):
        # NOTE: Добавить возможность при повторном запросе передавать только
        # капчу?
        self._login = login
        self._password = password

        if captcha and not self._grab.doc.body:
            raise MagnettoMisuseError(
                "Please execute .authorization(login, pass) first")

        # если форме необходим ввод капчи, то выполним ввод в старую форму
        # из прошлого запроса
        if not captcha:
            doc = self._grab.go(self.HOME + "login.php")
        else:
            doc = self._grab.doc

        # проверяем наличие капчи на странице
        img_captcha = doc.tree.xpath(
            '//img[contains(@src,"/captcha/")]/@src')
        if img_captcha and not captcha:
            raise MagnettoCaptchaError(self, img_captcha[0])

        # заполняем форму входа
        try:
            if captcha:
                doc.set_input_by_xpath(
                    '//input[starts-with(@name,"cap_code_")]', captcha)

            doc.set_input('login_username', login)
            doc.set_input('login_password', password)
        # вход уже выполнен
        except DataNotFound:
            return True

        doc = doc.submit()

        # проверка правильности данных
        if doc.tree.xpath(
                '//*[@id="login-form-full"]//h4[contains(@class, "warn")]'):
            raise MagnettoIncorrectСredentials()

        return True

    # TODO: реализовать вспомогательные элементы поиска (* часть текста, +СЛОВО
    # раздача должна содержать это слово, -СЛОВО исключить слово,
    # СЛОВО | СЛОВО или)
    # доп инфа: https://rutracker.org/forum/viewtopic.php?t=101236
    @api_filters_method
    def search(self, query, filters=[], page=0, limit=999):

        # вход не был выполнен
        if not self._login:
            raise MagnettoAuthError()

        # добавляем отсутствующие фильтры
        filters = self.add_filters_default(filters)

        RESULTS_ON_PAGE = 50

        # формируем урл для поиска
        url = "{home}tracker.php?start={page}".format(
            home=self.HOME,
            page=RESULTS_ON_PAGE * page
        )

        filtersTable = {
            Order.DESC: "&s=2",
            Order.ASC: "&s=1",

            OrderBy.CREATE: "&o=1",
            OrderBy.NAME: "&o=2",
            OrderBy.DOWNLOADS: "&o=4",
            OrderBy.SEEDERS: "&o=10",
            OrderBy.LEECHERS: "&o=11",
            OrderBy.MESSAGES: "&o=5",
            OrderBy.VIEWS: "&o=6",
            OrderBy.SIZE: "&o=7",
            OrderBy.LAST_MESSAGE: "&o=8"
        }

        # соотносим фильтры из таблицы их действиям
        for filter in filters:
            url += filtersTable[filter]

        # Выбор качества
        for filter in filters:
            if type(filter) is Resolution:
                query += " " + filter.value

        # выбор формата
        for filter in filters:
            if type(filter) is Source:
                query += ' ' + filter.value.replace(',', ' | ')

        # добавляем год
        for year in filters:
            if type(year) is Year:
                query += " " + str(year)

        url += "&nm=" + quote_plus(query)

        # подготавливаем для запроса
        self._grab.setup(url=url)

        # выполняем сам запрос
        self._grab.request()

        # проверяем, что после выполнения запроса мы залогинены
        self.is_logged()

        # разбор страницы
        items = self._parser.parse_search(self._grab.doc)

        # нужно возвращать ВСЕ элементы. Фильтрация происходит в декораторе
        return items
