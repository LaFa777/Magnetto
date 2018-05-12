from magnetto.filters import core, handler_definitions, FilterHandlersManager

filter_handlers_manager = FilterHandlersManager((
    (core.Order, handler_definitions.handler_filter_order),
    (core.LimitSize, handler_definitions.handler_filter_limitsize),
    (core.NoZeroSeeders, handler_definitions.handler_filter_nozeroseeders),
    (core.Category, handler_definitions.handler_filter_category),
    (core.NoWords, handler_definitions.handler_filter_nowords),
    (core.DateRegistered, handler_definitions.handler_filter_dateregistered),
    (core.NoEqualSize, handler_definitions.handler_filter_noequalsize),
    (core.VideoResolution, handler_definitions.handler_filter_videoresolution),
    (core.VideoSource, handler_definitions.handler_filter_videosource),
    (core.Limit, handler_definitions.handler_filter_limit),
))
"""Глобальный объект, для хранения всех функций-обработчиков.
Фильтры указываются в порядке их вызова.
"""
