import magnetto
from magnetto import (BaseApi, Category,
                      MagnettoIncorrectСredentials, MagnettoMisuseError,
                      MagnettoAuthError,
                      LastRequestMixin, OrderBy, Order, Year, Resolution,
                      Registred, TypeRelease, Size, Source, CheckAuthMixin,
                      KinozalParser,
                      SizeFilterMixin, CategoryFilterMixin,
                      NoZeroSeedersFilterMixin)
from grab import Grab
from urllib.parse import quote_plus


class KinozalApi(BaseApi, CheckAuthMixin, LastRequestMixin, SizeFilterMixin,
                 CategoryFilterMixin, NoZeroSeedersFilterMixin):

    HOME = None

    CATEGORIES = {
        Category.FILMS: ""
    }

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

    def search(self, value, filters=[OrderBy.DOWNLOADS, Order.DESC], page=0,
               limit=999):
        """
        Note:
            * поддеживает фильтры только в единичном варианте (последнее
              сработавшее условие)
        """

        # вход не был выполнен
        if not self._login:
            raise MagnettoAuthError()

        RESULTS_ON_PAGE = 50

        # формируем урл для поиска
        url = "{home}browse.php?page={page}".format(
            home=self.HOME,
            page=RESULTS_ON_PAGE * page
        )

        # Сортировать выдачу по:
        if Order.DESC in filters:
            url += "&f=0"
        elif Order.ASC in filters:
            url += "&f=1"

        # категории
        # все сериалы 1001
        if Category.TV_SERIES in filters:
            url += "&c=1001"
        # все Фильмы 1002
        elif Category.FILMS in filters:
            url += "&c=1002"
        # все мульты 1003
        elif Category.CARTOONS in filters:
            url += "&c=1003"
        # вся музыка 1004
        elif Category.MUSICS in filters:
            url += "&c=1004"
        # аудиокниги 2
        elif Category.AUDIOBOOKS in filters:
            url += "&c=2"
        # видеоклипы 1 ???
        # игры 23
        elif Category.GAMES in filters:
            url += "&c=23"
        # программы 32
        elif Category.PROGRAMS in filters:
            url += "&c=32"
        # дизайн графика 40 ???
        # библиотека (книги) 41
        elif Category.BOOKS in filters:
            url += "&c=41"

        # проставляем год
        for filter in filters:
            if filter.__class__ == Year:
                url += "&d=" + str(filter)

        # Выбор качества
        if Resolution.HD in filters and Resolution.FULL_HD in filters:
            url += "&v=3"
        elif Resolution.HD in filters:
            value += " 720p"
        elif Resolution.FULL_HD in filters:
            value += " 1080p"
        elif Resolution.ULTRA_HD in filters:
            url += "&v=7"

        # выбор формата
        if Source.TV_RIP in filters:
            url += "&v=5"
        elif Source.WEB_DL_RIP in filters:
            url += "&v=1"
            value += " WEB-DLRip"
        elif Source.HD_RIP in filters:
            value += " HDRip"
            url += "&v=1"
        elif Source.BD_RIP in filters:
            value += " BDRip"
            url += "&v=1"
        elif Source.VHS_RIP in filters:
            value += " VHSRip"
        elif Source.DVD_RIP in filters:
            url += "&v=1"
            value += " DVDRip"
        # CAM_RIP на этом трекере нит
        elif Source.CAM_RIP in filters:
            return []

        # Сортировка результата по:
        # дата регистрации
        if OrderBy.CREATE in filters:
            url += "&t=0"
        # название темы (не реализован (можно фильтровать выдачу ниже))
        # elif OrderBy.NAME in filters:
        #    url += "&t="
        # Количество скачиваний
        elif OrderBy.DOWNLOADS in filters:
            url += "&t=5"
        # количество сидов
        elif OrderBy.SEEDERS in filters:
            url += "&t=1"
        # количество личей
        elif OrderBy.LEECHERS in filters:
            url += "&t=2"
        # количество сообщений
        elif OrderBy.MESSAGES:
            url += "&t=4"
        # количество просмотров (игнорируем)
        # elif OrderBy.VIEWS:
        #     url += "&t="
        # размер раздачи
        elif OrderBy.SIZE:
            url += "&t=3"
        # последнее сообщение
        elif OrderBy.LAST_MESSAGE:
            url += "&t=6"

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

        # Фильтр по типу релиза
        if TypeRelease.SILVER in filters:
            url += "&w=12"
        elif TypeRelease.GOLD in filters:
            url += "&w=11"

        # Фильтр по размеру
        if Size.TINY in filters:
            url += "&w=6"
        elif Size.SMALL in filters:
            url += "&w=7"
        elif Size.MEDIUM in filters:
            url += "&w=8"
        elif Size.BIG in filters:
            url += "&w=9"
        elif Size.LARGE in filters:
            url += "&w=10"

        # добавляем возможно модифицированный поисковый запрос
        url += "&s=" + quote_plus(value)

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

        return items[:limit]
