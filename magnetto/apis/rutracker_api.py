from magnetto import (Category, OrderBy, Order, BaseApi, RutrackerParser,
                      RUTRACKER_URL, MagnettoCaptchaError, MagnettoAuthError,
                      MagnettoIncorrectСredentials, CheckAuthMixin,
                      CategoryFilterMixin, LastRequestMixin)
from urllib.parse import quote_plus
from grab.error import DataNotFound


class RutrackerApi(BaseApi, CheckAuthMixin, CategoryFilterMixin, LastRequestMixin):

    HOME = RUTRACKER_URL

    CATEGORIES = {
        Category.FILMS: "1105,1165,124,1245,1246,1247,1248,1250,1390,140,1543,"
        "1577,1642,1666,187,1900,194,1950,1991,208,209,2090,2091,2092,"
        "2093,2198,2199,22,2200,2201,2221,2258,2339,2343,2365,2540,312,"
        "313,33,376,4,404,484,505,521,539,7,709,893,921,922,923,924,925,"
        "926,927,928,930,934,941"
    }

    def __init__(self, grab):
        self._grab = grab.clone()
        self._parser = RutrackerParser()
        self._login = ""
        self._password = ""

    def authorization(self, login, password, captcha=None):
        # NOTE: Добавить возможность при повторном запросе передавать только
        # капчу?
        self._login = login
        self._password = password

        # если форме необходим ввод капчи, то выполним ввод в старую форму
        # из прошлого запроса
        if not captcha:
            doc = self._grab.go(self.HOME + "login.php")
        else:
            doc = self._grab.doc

        # проверяем наличие капчи на странице
        img_captcha = doc.tree.xpath('//img[contains(@src,"/captcha/")]/@src')
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

        self._grab.doc.submit()

        # проверка на факт успешного входа
        if self._grab.doc.tree.xpath(
                '//*[@id="login-form-full"]/table/tbody/tr[2]/td/h4'):
            raise MagnettoIncorrectСredentials()

        return True

    # доп инфа: https://rutracker.org/forum/viewtopic.php?t=101236
    def search(self, value, categories=[], page=0, limit=0,
               order_by=OrderBy.DOWNLOADS, order=Order.DESC):

        # вход не был выполнен
        if not self._login:
            raise MagnettoAuthError()

        RESULTS_ON_PAGE = 50
        # формируем урл для поиска
        url = "{home}tracker.php?nm={name}&start={page}".format(
            home=self.HOME,
            name=quote_plus(value),
            page=RESULTS_ON_PAGE * page
        )

        # добавляем фильтр для сортировки
        # s:2 (убывание) 1 (возрастание)
        url += "&s="
        url += "2" if (order == Order.DESC) else "1"

        # добавляем колонку для сортировки
        # o: 1 (Зарегистрирован) 2 (Название темы) 4 (Количество скачиваний)
        # 10 (количество сидов) 11 (количество личей) 7 (количество сообщений)
        # 8 (последнее сообщение)
        url += "&o="
        # зарегистрирован
        if (order_by == OrderBy.CREATE):
            url += "1"
        # название темы
        elif (order_by == OrderBy.NAME):
            url += "2"
        # Количество скачиваний
        elif (order_by == OrderBy.DOWNLOADS):
            url += "4"
        # количество сидов
        elif (order_by == OrderBy.SEEDER):
            url += "10"
        # количество личей
        elif (order_by == OrderBy.LEECHER):
            url += "11"
        # количество сообщений
        elif (order_by == OrderBy.MESSAGES):
            url += "7"
        # последнее сообщение
        else:
            url += "8"

        # подготавливаем для запроса
        self._grab.setup(url=url)

        # добавляем фильтр по категориям
        if categories:
            self._add_category_filter(categories)

        # выполняем сам запрос
        self._grab.request()

        # проверяем, что после выполнения запроса мы залогинены
        self.is_logged()

        # разбор страницы
        searchItems = self._parser.parse_search_page(self._grab.doc)

        return searchItems[:limit]

    def _handle_add_category_filter(self, args):
        url = "{url}&f={param}".format(
            url=self._grab.config["url"],
            param=','.join(args)
        )
        self._grab.setup(url=url)
