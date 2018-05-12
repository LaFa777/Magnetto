"""Все классы Api должны наследовать ``BaseApi``"""

from abc import ABC, abstractproperty, abstractmethod
from grab import Grab


class BaseApi(ABC):
    """Все классы Api должны наследовать ``BaseApi``"""

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
            TODO: ошибка сервера
        """

    @abstractmethod
    def search(self, value, filters=None):
        """Выполняет запрос поиска по трекеру.

        Args:
            value (str): Поисковый запрос
            categories (List[filters]): Список категорий для
                фильтрации конечной выборки
            page (int): Страница поиска

        Returns:
            ``List[ResultParsePage]``

        Raises:
            ``MagnettoAuthError``
            TODO: ошибка сервера
            TODO: ошибка парсинга

        Todo:
            * query - \w{3,}*
        """

    def top(self, filters=None):
        pass
