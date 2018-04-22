"""Различные примеси для объектов типа :obj:`magnetto.BaseApi`"""

import time
from magnetto import (MagnettoAuthError, Size, NoZeroSeeders, Category, NoWords,
                      Registred, NoEqualSize)


class LastRequestMixin(object):
    """Функционал для получения последнего запроса
    """

    def get_last_request_data(self):
        """
        Return:
            :obj:`Dict`:
            * :obj:`"url"` последний запрошенный url
            * :obj:`"post"` данные последнего post запроса
        """
        return {
            "url": self._grab.config["url"],
            "post": self._grab.config["post"]
        }


class CheckAuthMixin(object):
    """Добавляет простейший функционал для проверки факта успешного входа
    """

    def is_logged(self):
        """Проверяет на странице наличие имени пользователя.

        Return:
            :obj:`True`: Пользователь авторизован.

        Raises:
            :obj:`magnetto.MagnettoAuthError`
        """
        if not self._grab.doc.text_search(self._login):
            raise MagnettoAuthError("Error authorization")

        return True


class SizeFilterMixin:

    def add_filter_size(self, items, filters):
        """Удаляет раздачи, не соответсвующие переданному фильтру размера
        """
        # устанавливаем фильтр по размеру
        filter_size = None
        if Size.TINY in filters:
            filter_size = range(0, 1300)
        elif Size.SMALL in filters:
            filter_size = range(1300, 2250)
        elif Size.MEDIUM in filters:
            filter_size = range(2250, 4096)
        elif Size.BIG in filters:
            filter_size = range(4096, 9728)
        elif Size.LARGE in filters:
            filter_size = range(9728, 25600)
        elif Size.HUGE in filters:
            filter_size = range(25600, 9999999999)

        # если такой фильтр не был передан, то возвращаем без изменений
        if not filter_size:
            return items

        # убираем не соответствующие фильтру раздачи
        tmp_arr = []
        for item in items:
            if int(item.size) in filter_size:
                tmp_arr.append(item)
        return tmp_arr


class NoZeroSeedersFilterMixin:

    def add_filter_nozeroseeders(self, items, filters):
        """Удаляет раздачи без сидеров
        """

        if NoZeroSeeders not in filters:
            return items

        tmp_arr = []
        for item in items:
            if int(item.seeders) > 0:
                tmp_arr.append(item)
        return tmp_arr


class CategoryFilterMixin:

    def add_filter_category(self, items, filters):
        """Удаляет раздачи, не соответствующие категории
        """
        for filter in filters:
            if filter in Category:
                tmp_arr = []
                for item in items:
                    if item.category is filter:
                        tmp_arr.append(item)
                return tmp_arr
        return items


class NoWordsFilterMixin:

    def add_filter_nowords(self, items, filters):
        """Удаляет раздачи, содержащие указанные в фильтре слова
        """
        for filter in filters:
            if type(filter) is NoWords:
                tmp_arr = []
                for item in items:
                    if item.name not in filter:
                        tmp_arr.append(item)
                return tmp_arr
        return items


class RegistredFilterMixin:

    def add_filter_registred(self, items, filters):
        """Фильтр по дате регистрации раздачи
        """
        current_time = int(time.time())
        filter_time = None

        if Registred.TODAY in filters:
            filter_time = 60 * 60 * 24
        elif Registred.YESTERDAY in filters:
            filter_time = 60 * 60 * 24 * 2
        elif Registred.FOR_3_DAYS in filters:
            filter_time = 60 * 60 * 24 * 3
        elif Registred.FOR_WEEK in filters:
            filter_time = 60 * 60 * 24 * 7
        elif Registred.FOR_MONTH in filters:
            filter_time = 60 * 60 * 24 * 32

        if not filter_time:
            return items

        tmp_arr = []
        for item in items:
            if int(item.created) >= (current_time - filter_time):
                tmp_arr.append(item)
        return tmp_arr


class NoEqualSizeFilterMixin:

    def add_filter_noequalsize(self, items, filters):
        for filter in filters:
            # можно передавать в фильтр просто класс
            if filter is NoEqualSize:
                filter = NoEqualSize()

            if type(filter) is NoEqualSize:
                # сначала необходимо отсортировать items по размеру
                sort_arr = sorted(items, key=lambda item: int(item.size))

                # составляем список раздач не совпадающих по размеру
                # менее чем на filter процент
                tmp_arr = []
                for i, item in enumerate(sort_arr[:-1]):
                    next_size = int(sort_arr[i+1].size)
                    current_size = int(item.size)
                    # если размер текущей раздачи составляет менее filter
                    # процента от размера следующей раздачи, то удаляем
                    if (100-(current_size/next_size*100)) > int(filter):
                        tmp_arr.append(item)
                # т.к. прошли по всем, кроме последнего, то добавляем и его
                tmp_arr.append(sort_arr[len(sort_arr)-1])

                # удаляем из items все раздачи, которые не попали под фильтр
                result_arr = []
                for item in items:
                    if item in tmp_arr:
                        result_arr.append(item)
                return result_arr
        return items
