from urllib.parse import quote_plus

from grab import Grab
from grab.error import DataNotFound

import magnetto
from magnetto.errors import (MagnettoCaptchaError, MagnettoMisuseError,
                             MagnettoIncorrectСredentials)
from magnetto.filters import (FiltersManager, filter_handlers_manager,
                              OrderBy, Order, VideoResolution, VideoSource,
                              NoWords, NoZeroSeeders)

from magnetto.apis import BaseApi
from magnetto.apis.mixins import CheckAuthMixin, LastRequestMixin

from magnetto.parsers import RutrackerParser


class RutrackerApi(BaseApi, CheckAuthMixin, LastRequestMixin):

    def __init__(self,
                 grab=Grab(),
                 parser=RutrackerParser(),
                 filter_handlers=filter_handlers_manager):
        self._grab = grab.clone()
        self._parser = parser
        self._filter_handlers = filter_handlers
        self._login = ""
        self._password = ""

    def authorization(self, login, password, captcha=None):

        # если передан только 1 параметр, то скорее всего это была капча
        if self._login and self._password and login and not password:
            captcha = login
        else:
            self._login = login
            self._password = password

        # если передана капча и функция ранее не вызывалась
        if captcha and not self._grab.doc.body:
            raise MagnettoMisuseError(
                "Please execute .authorization(login, pass) first")

        # если форме необходим ввод капчи, то выполним ввод в старую форму
        # из прошлого запроса
        if not captcha:
            doc = self._grab.go(magnetto.RUTRACKER_URL + "login.php")
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

            doc.set_input('login_username', self._login)
            doc.set_input('login_password', self._password)
        # вход уже выполнен
        except DataNotFound:
            return True

        doc = doc.submit()

        # проверка правильности данных
        if doc.tree.xpath(
                '//*[@id="login-form-full"]//h4[contains(@class, "warn")]'):
            raise MagnettoIncorrectСredentials()

        return True

    # доп инфа: https://rutracker.org/forum/viewtopic.php?t=101236
    # TODO: уточнение поиска для категорий (необходимо т.к. не всегда поиск
    # возращает то что нужно)
    def search(self, query, filters=[]):

        self.is_logged()

        filters = FiltersManager(filters, [Order(OrderBy.SEEDERS)])

        # формируем урл для поиска
        url = "{home}tracker.php?".format(
            home=magnetto.RUTRACKER_URL
        )

        # направление сортировки
        if filters.get(Order).asc:
            url += "&s=1"
        else:
            url += "&s=2"

        # столбец для сортировки
        orderByTable = {
            OrderBy.CREATE: "&o=1",
            OrderBy.NAME: "&o=2",
            OrderBy.DOWNLOADS: "&o=4",
            OrderBy.SEEDERS: "&o=10",
            OrderBy.LEECHERS: "&o=11",
            OrderBy.SIZE: "&o=7",
        }
        for column, param in orderByTable.items():
            if filters.get(Order).column == column:
                url += param

        # Выбор качества
        if VideoResolution in filters:
            query += ' ' + str(filters.get(VideoResolution))

        # выбор формата
        if VideoSource in filters:
            query += ' ' + str(filters.get(VideoSource)).replace(',', ' | ')

        # добавляем каждое слово из фильтра NoWords в запрос
        if NoWords in filters:
            for word in filters.get(NoWords):
                query += " -" + str(word)

        # убираем раздачи без сидеров
        if NoZeroSeeders in filters:
            url += "&sd=1"

        url += "&nm=" + quote_plus(query)

        self._grab.request(url=url)

        self.is_logged()

        # разбор страницы
        items = self._parser.parse_search(self._grab.doc)

        # выполним пост обработку
        items = self._filter_handlers.handle(items, filters)

        return items
