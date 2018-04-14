from abc import ABC, abstractproperty, abstractmethod
from magnetto import (OrderBy, Order)


class BaseApi(ABC):

    @abstractproperty
    def HOME(self):
        """Сссылка на главную страницу сайта.
        """
        pass

    @abstractmethod
    def __init__(self, grab):
        """
        Args:
            grab (:obj:`grab.Grab`): Объект
        """
        pass

    @abstractmethod
    def authorization(self, login, password, captcha=None):
        """Выполняет авторизацию на сайте. При нахождении капчи на странице
        сохраняет своё состояние и при повторном вызове метода с введенной
        строкой капчи заполняет старую форму и пробует выполнить ёё отправку на
        сервер.

        Examples:

        >>> rt = RutrackerApi(grab)
        ... try:
        ...     rt.authorization("Masha", "1234")
        ... except MagnettoAuthError:
        ...     print("Некорректные данные для входа")
        ...     exit(1)
        ... except MagnettoCaptchaError as e:
        ...     print("Капча: {url}".format(e))
        ...     captcha = input()
        ...     rt.authorization("Masha", "1234", captcha)

        Raises:
            :obj:`magnetto.MagnettoIncorrectСredentials`: Введены неверные
                данные для входа
            :obj:`magnetto.MagnettoCaptchaError`: На странице обнаружена капча
        """

    @abstractmethod
    def search(self, value, categories=[], page=0, limit=0,
               order_by=OrderBy.DOWNLOADS, order=Order.DESC):
        """Выполняет запрос поиска по трекеру.

        Args:
            value (:obj:`str`): Поисковый запрос
            categories (List[:obj:`magnetto.Category`]): Список категорий для
                поиска
            page (:obj:`int`): Страница поиска
            limit (:obj:`int`): Количество возвращаемых результатов
            order_by (:obj:`magnetto.OrderBy`): Колонка для сортировки
            order (:obj:`magnetto.Order`): Порядок сортировки

        Todo:
            * добавить фильтры на конечную выборку (ненулевые раздачи)
            * (исключение раздач с одинаковым размером)
        """
