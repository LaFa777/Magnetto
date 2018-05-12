from collections import UserList

from .manager import FiltersManager


class FilterHandlersManager(UserList):
    """Выполняет фильтрацию выборки с трекера после выполнения запроса.
    Инициализируется элементами типа: [тип фильтра, ссылка на
    функцию-обработчик].

    Example:
        >>> filters = FilterHandlers([
        >>>                 (Limit, handler_filter_order),
        >>> ])
        >>> filters.handle(items, filters)
    """

    def handle(self, items, filters):
        """Вызывает обработчики для соответствующего типа фильтра.
        """
        if not isinstance(filters, FiltersManager):
            filters_manager = FiltersManager(filters)
        else:
            filters_manager = filters

        for filter_type, handler in self.data:
            filter = filters_manager.get(filter_type)
            if filter:
                items = handler(items, filter)

        return items
