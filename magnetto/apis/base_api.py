"""Все классы Api должны наследовать ``BaseApi``"""

from abc import ABC, abstractproperty, abstractmethod
from grab import Grab

from magnetto.filters import OrderBy, Order


class BaseApi(ABC):
    """Все классы Api должны наследовать ``BaseApi``"""

    filters_default = [OrderBy.SEEDERS, Order.DESC]

    def add_filters_default(self, arg_filters):
        """Добавляет фильтр из ``self.filters_default`` в ``arg_filters``
        только в том случае, если фильтр такого же типа отсутствует в
        ``arg_filters``

        Args:
            arg_filters (List[filters]): Массив фильтров
        """
        for def_filter in self.filters_default:
            for arg_filter in arg_filters:
                if type(def_filter) == type(arg_filter):
                    break
            else:
                arg_filters.append(def_filter)
        return arg_filters

    @abstractproperty
    def HOME(self):
        """Сссылка на главную страницу сайта.
        """
        pass

    @abstractmethod
    def __init__(self, grab=Grab()):
        """
        Args:
            grab (grab.Grab): Объект типа ``grab.Grab``
        """
        pass

    @abstractmethod
    def authorization(self, login, password, captcha=None):
        """Выполняет авторизацию на сайте. При нахождении капчи на странице
        сохраняет своё состояние и при повторном вызове метода с введенной
        строкой капчи заполняет старую форму и пробует выполнить ёё отправку на
        сервер.

        Raises:
            ``MagnettoIncorrectСredentials``: Введены неверные
                данные для входа
            ``MagnettoCaptchaError``: На странице обнаружена капча
        """

    @abstractmethod
    def search(self, value, filters=[], page=0, limit=999):
        """Выполняет запрос поиска по трекеру.

        Args:
            value (str): Поисковый запрос
            categories (List[filters]): Список категорий для
                фильтрации конечной выборки
            page (int): Страница поиска
            limit (int): Количество возвращаемых результатов

        Returns:
            ``List[ResultParsePage]``

        Raises:
            ``MagnettoAuthError``
        """
