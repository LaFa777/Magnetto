"""Различные примеси для объектов типа :obj:`magnetto.BaseApi`"""

from magnetto import MagnettoAuthError, Size, NoZeroSeeders, Category


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
        else:
            return items
