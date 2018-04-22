import magnetto
from magnetto import (OrderBy, Order, BaseApi, RutrackerParser,
                      MagnettoCaptchaError, MagnettoMisuseError,
                      MagnettoAuthError, MagnettoIncorrectСredentials,
                      CheckAuthMixin, LastRequestMixin, Resolution, Source,
                      Registred, Year, SizeFilterMixin, CategoryFilterMixin,
                      NoZeroSeedersFilterMixin, NoWordsFilterMixin)
from urllib.parse import quote_plus
from grab.error import DataNotFound
from grab import Grab


class RutrackerApi(BaseApi, CheckAuthMixin, LastRequestMixin, SizeFilterMixin,
                   NoZeroSeedersFilterMixin, CategoryFilterMixin, NoWordsFilterMixin):

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
    def search(self, value, filters=[OrderBy.DOWNLOADS, Order.DESC], page=0,
               limit=999):

        # вход не был выполнен
        if not self._login:
            raise MagnettoAuthError()

        RESULTS_ON_PAGE = 50

        # формируем урл для поиска
        url = "{home}tracker.php?start={page}".format(
            home=self.HOME,
            page=RESULTS_ON_PAGE * page
        )

        # Сортировать выдачу по:
        if Order.DESC in filters:
            url += "&s=2"
        elif Order.ASC in filters:
            url += "&s=1"

        # Упорядочить выдачу результатов по критерию:
        # дата регистрации
        if OrderBy.CREATE in filters:
            url += "&o=1"
        # название темы
        elif OrderBy.NAME in filters:
            url += "&o=2"
        # Количество скачиваний
        elif OrderBy.DOWNLOADS in filters:
            url += "&o=4"
        # количество сидов
        elif OrderBy.SEEDERS in filters:
            url += "&o=10"
        # количество личей
        elif OrderBy.LEECHERS in filters:
            url += "&o=11"
        # количество сообщений
        elif OrderBy.MESSAGES:
            url += "&o=5"
        # количество просмотров
        elif OrderBy.VIEWS:
            url += "&o=6"
        # размер раздачи
        elif OrderBy.SIZE:
            url += "&o=7"
        # последнее сообщение
        elif OrderBy.LAST_MESSAGE:
            url += "&o=8"

        # Выбор качества
        if Resolution.HD in filters:
            value += " 720p"
        elif Resolution.FULL_HD in filters:
            value += " 1080p"
        elif Resolution.ULTRA_HD in filters:
            url += " 2160p"

        # выбор формата
        if Source.TV_RIP in filters:
            rips = Source.TV_RIP.value.split(',')
            value += ' | '.join(rips)
        elif Source.WEB_DL_RIP in filters:
            rips = Source.WEB_DL_RIP.value.split(',')
            value += ' | '.join(rips)
        elif Source.HD_RIP in filters:
            rips = Source.HD_RIP.value.split(',')
            value += ' | '.join(rips)
        elif Source.BD_RIP in filters:
            rips = Source.BD_RIP.value.split(',')
            value += ' | '.join(rips)
        elif Source.VHS_RIP in filters:
            rips = Source.VHS_RIP.value.split(',')
            value += ' | '.join(rips)
        elif Source.DVD_RIP in filters:
            rips = Source.DVD_RIP.value.split(',')
            value += ' | '.join(rips)
        elif Source.CAM_RIP in filters:
            rips = Source.CAM_RIP.value.split(',')
            value += ' | '.join(rips)

        # Фильтр по дате регистрации раздачи
        if Registred.TODAY in filters:
            url += "&w=1"
        elif Registred.YESTERDAY in filters:
            url += "&w=2"
        elif Registred.FOR_3_DAYS in filters:
            url += "&w=3"
        elif Registred.FOR_WEEK in filters:
            url += "&w=4"
        elif Registred.FOR_MONTH in filters:
            url += "&w=5"

        # добавляем год
        for year in filters:
            if type(year) is Year:
                value += " " + str(year)

        url += "&nm=" + quote_plus(value)

        # подготавливаем для запроса
        self._grab.setup(url=url)

        # выполняем сам запрос
        self._grab.request()

        # проверяем, что после выполнения запроса мы залогинены
        self.is_logged()

        # разбор страницы
        items = self._parser.parse_search(self._grab.doc)

        items = self.add_filter_size(items, filters)
        items = self.add_filter_nozeroseeders(items, filters)
        items = self.add_filter_category(items, filters)
        items = self.add_filter_nowords(items, filters)

        return items[:limit]
