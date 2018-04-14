"""Различные примеси для объектов типа :obj:`magnetto.BaseApi`"""

from abc import ABC, abstractmethod, abstractproperty
from magnetto import MagnettoAuthError


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


class CategoryFilterMixin(ABC):
    """Добавляет возможность фильтрации по категориям. В потомках необходимо
    реализовать свойство :obj:`CATEGORIES` и метод
    :obj:`_handle_add_category_filter`.
    """

    @abstractproperty
    def CATEGORIES(self):
        """Словарь типа Dict[:obj:`magnetto.BaseApi`, :obj:`str`].
        """
        pass

    def is_support_category(self, category):
        """Проверяет, поддерживает ли объект переданную категорию

        Args:
            category (:obj:`magnetto.Category`)
        """
        return bool(self.CATEGORIES[category])

    def list_support_categories(self):
        """Возвращает список поддерживаемых категорий.

        Return:
            List[:obj:`magnetto.BaseApi`]
        """
        return self.CATEGORIES.keys()

    def _add_category_filter(self, categories=[]):
        """Выполняет различные проверки на поддерживаемость категории и затем
        вызывает :obj:`_handle_add_category_filter`

        Args:
            categories (List[:obj:`magnetto.Category`])
        """

        # если категорий нет, значит и фильтр настраивать не надо
        if not categories:
            return

        # проверяем, поддерживается ли категория
        diff_categories = set(self.list_support_categories()) & set(categories)
        if not diff_categories:
            return

        # формируем аргументы для фильтра в поиске
        args = []
        for category in diff_categories:
            args.append(self.CATEGORIES[category])

        # делегируем задачу добавления аргументов к запросу
        self._handle_add_category_filter(args)

    @abstractmethod
    def _handle_add_category_filter(self, args):
        """
        Примесь CategoryFilterMixin делегелирует конечную задачу добавления
        аргументов поиска к запросу этому обработчику.

        Args:
            args (List[:obj:`str`]): список аргументов,
                взятых из :obj:`CATEGORIES`
        """
