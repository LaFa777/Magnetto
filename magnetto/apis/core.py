class GlobalFilters:
    """Класс для хранения обработчиков конечной выборки.
    """
    handlers = {}

    @classmethod
    def append(cls, filter_type, handler):
        """Для указанного типа фильтра добавляет функцию - обработчик.

        Attributes:
            filter_type: тип, наличие которого проверяется в переданных
                аргументах метода апи. Если соответствие найдено, то
                запускается каждый обработчик из ``GlobalFilters.handlers``
            handler: указатель на функцию типа ``func(items, filter)``
        """
        cls.handlers[filter_type] = cls.handlers.get(filter_type, [])
        cls.handlers[filter_type].append(handler)


def api_filters_method(function):
    """Декоратор. Выполняет запуск всех фильтров влияющих на конечную выборку.
    Должен декорировать только методы класса типа ``BaseApi``.
    """

    def handle_items(self, **kwargs):
        kwargs['filters'] = kwargs.get('filters', self.filters_default)

        # TODO: проверять что не был передан второй фильтр из одной и той же
        # категории

        # добавляем отсутствующие фильтры
        kwargs['filters'] = self.add_filters_default(kwargs['filters'])

        # вызываем декорируемую функцию api
        result_items = function(self, **kwargs)

        # вызываем необходимые обработчики для переданных фильтров
        for filter in kwargs['filters']:
            for filter_type, handlers in GlobalFilters.handlers.items():
                if filter is filter_type or \
                   type(filter) is filter_type:
                    for func in handlers:
                        result_items = func(result_items, filter,
                                            kwargs['filters'])

        # ограничиваем количество возвращаемых значений
        return result_items[:int(kwargs.get('limit', 999))]
    return handle_items
