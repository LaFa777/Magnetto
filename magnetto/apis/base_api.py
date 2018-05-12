"""Все классы Api должны наследоваться от ``BaseApi``"""

from abc import ABCMeta, abstractmethod
from grab import Grab


class BaseApi(metaclass=ABCMeta):
    """Все классы Api должны наследоваться от ``BaseApi``"""

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

        Example:
            >>> try:
            >>>    api.authorization(login, password)
            >>> except MagnettoCaptchaError as err:
            >>>    print("Captcha url: " + err.url)
            >>>    captcha = input()
            >>>    api.authorization(captcha)

        Raises:
            ``MagnettoIncorrectСredentials``: Введены неверные
                данные для входа
            ``MagnettoCaptchaError``: На странице обнаружена капча
            TODO: ошибка сервера
        """

    @abstractmethod
    def search(self, query, filters=[]):
        """Выполняет запрос поиска по трекеру.

        Args:
            query (str): Поисковый запрос.
            filters (List[filter]): фильтры, для уточнения поиска

        Returns:
            ``List[ResultParsePage]``

        Raises:
            ``MagnettoAuthError``
            ``MagnettoParseError``

        Todo:
            * query - \w{3,}*
        """

    def top(self, filters=[]):
        pass
