from collections import Counter, UserDict

from magnetto.errors import MagnettoMisuseError


class FiltersManager(UserDict):
    """Удобный способ работы с массивом фильтров.
    """

    def __init__(self, filters, defaults=[]):
        self._defaults = defaults
        self.data = []

        self.appends(filters)

    def appends(self, filters):
        """Соединяет указанные фильтры с default_filters.
        Дополнительно проверяет, что передан только 1 фильтр одного типа.
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
        counter = Counter(filters)
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
