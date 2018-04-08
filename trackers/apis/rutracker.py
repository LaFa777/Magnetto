from .base import *
from ..core import *
from ..categories import Rutracker as RutrackerCategory
from ..parsers.search import Rutracker as RutrackerSearchParser
from ..parsers.topic import Rutracker as RutrackerTopicParser
from urllib.parse import quote_plus
from grab.error import GrabAuthError, DataNotFound
from ..core.errors import TrackersCaptchaError, TrackersAuthError

class Rutracker(Base):
    home_url = "http://rutracker.org/forum/"
    categoryFilter = RutrackerCategory()
    searchParser = RutrackerSearchParser()
    topicParser = RutrackerTopicParser()

    def authorization(self, login:str = None, password:str = None, captcha_str = ""):
        if not password:
            login = self.login
            password = self.password

        # если форме необходим ввод капчи, то выполним ввод в старую форму
        # из прошлого запроса
        if not captcha_str:
            doc = self.grab.go(self.home_url + 'login.php')
        else:
            doc = self.grab.doc

        # проверяем на наличие капчи на странице
        img_captcha = doc.tree.xpath('//img[contains(@src,"/captcha/")]/@src')
        if img_captcha and not captcha_str:
            raise TrackersCaptchaError(img_captcha[0])

        # заполняем форму входа
        try:
            if captcha_str:
                cap_code = doc.set_input_by_xpath('//input[starts-with(@name,"cap_code_")]', captcha_str)

            doc.set_input('login_username', login)
            doc.set_input('login_password', password)
        # вход уже выполнен
        except DataNotFound:
            return

        doc = self.grab.doc.submit()

        # простая проверка на факт успешного входа
        self.check_is_login(doc)

        return

    # информация по поиску по рутрекеру
    # s:2 (убывание) 1 (возрастание)
    # o: 1 (Зарегистрирован) 2 (Название темы) 4 (Количество скачиваний)
    # 10 (количество сидов) 11 (количество личей) 7 (количество сообщений)
    # 8 (последнее сообщение)
    # https://rutracker.org/forum/viewtopic.php?t=101236
    def search(self, value: str, categories=[], page=0, limit=0, order_by=OrderBy.DOWNLOADS, order=Order.DESC):
        RESULTS_ON_PAGE = 50
        # формируем урл для поиска
        url = "{home_url}tracker.php?nm={name}&start={page}".format(
            home_url=self.home_url,
            name=quote_plus(value),
            page=RESULTS_ON_PAGE * page
        )

        # добавляем фильтр для сортировки
        url += "&s="
        url += "2" if (order == Order.DESC) else "1"

        # указываем колонку для сортировки
        url += "&o"
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
        self.grab.setup(url=url)

        # добавляем фильтр по категориям
        if categories:
            self.categoryFilter.add_filter(self.grab, categories)

        # выполняем сам запрос
        doc = self.grab.request()

        # проверяем, что при выполнении запроса мы были залогинены
        try:
            self.check_is_login(doc)
        except TrackersAuthError:
            # попробуем перезайти
            self.authorization(self.login, self.password)
            return search(value, categories, page, limit, order_by, order)

        # забираем метаинфу со страницы
        searchItems = self.searchParser.extract_items(doc)

        # Загружаем limit страниц и парсим их
        for searchItem in searchItems[:limit]:
            full_url = self.home_url + searchItem.url
            doc = self.grab.go(full_url)
            searchItem.magnet = self.topicParser.extract_magnet(doc)

        return searchItems[:limit]
