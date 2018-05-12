from collections import Counter, UserList

from magnetto.errors import MagnettoMisuseError


class FiltersManager(UserList):
    """Удобный способ работы с массивом фильтров. Выполняет проверки на
    единственность переданного типа фильтра. Объединяет фильтры с фильтрами по
    умолчанию.
    """

    def __init__(self, filters, defaults=[]):
        """
        Attributes:
            filters (List[filter]): массив фильтров
            defaults (List[filter]): массив фильтров, которые будут обединены с
                filters в случае отсутствия таковых.
        """
        self._defaults = defaults
        self.data = []

        self.appends(filters)

    def appends(self, filters):
        """Проверяет, что передан только 1 фильтр одного типа. Дополняет
        filters фильтрами по умолчанию, в случае отсутствия фильтра такого же
        типа.
        """
        # сначала добавим фильтры по умолчанию (если такие отсутствуют)
        for default in self._defaults:
            for filter in filters:
                # если идентичны cls или type(obj)
                if default == filter or \
                   type(default) == type(filter):
                    break
            else:
                filters.append(default)

        # не должно быть одинаковых типов фильтров
        keys = [type(filter) for filter in filters]
        counter = Counter(keys)
        if max(counter.values()) > 1:
            raise MagnettoMisuseError(
                "Передано несколько фильтров одного типа")

        self.data = filters

        return self.data

    def get(self, filter_type):
        """Возвращает фильтр указанного типа.
        """
        if not self.data:
            raise MagnettoMisuseError("No initialize instance")

        for filter in self.data:
            if filter_type == filter or \
               filter_type == type(filter):
                return filter

        # не нашли фильтр такого типа
        return None

    def __contains__(self, filter_type):
        return bool(self.get(filter_type))
