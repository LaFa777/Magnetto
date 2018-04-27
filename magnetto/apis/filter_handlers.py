import time

import attr

from magnetto.errors import MagnettoMisuseError
from magnetto.apis.core import GlobalFilters
from magnetto.filters import (Size, NoZeroSeeders, Category, NoWords,
                              Registered, NoEqualSize, OrderBy, Order,
                              Resolution, Source)


# TODO: добавить Year, Or

def handler_filter_order(items, filter, arg_filters):
    """Сортирует раздачи по убыванию или возрастанию
    """

    # сначала определим столбец, по которому происходит сортировка
    index = None
    if OrderBy.CREATE in arg_filters:
        index = "created"
    elif OrderBy.NAME in arg_filters:
        index = "name"
    elif OrderBy.DOWNLOADS in arg_filters:
        index = "downloads"
    elif OrderBy.SEEDERS in arg_filters:
        index = "seeders"
    elif OrderBy.LEECHERS in arg_filters:
        index = "leechers"
    elif OrderBy.SIZE in arg_filters:
        index = "size"
    else:
        return items

    # для числовых сортируем предварительно приведя к int
    if "name" in index and filter is Order.DESC:
        return sorted(items, key=lambda item: getattr(item, index), reverse=True)
    elif "name" in index and filter is Order.ASC:
        return sorted(items, key=lambda item: getattr(item, index), reverse=False)
    elif filter is Order.DESC:
        return sorted(items, key=lambda item: int(getattr(item, index)), reverse=True)
    elif filter is Order.ASC:
        return sorted(items, key=lambda item: int(getattr(item, index)), reverse=False)
    else:
        return items


GlobalFilters.append(Order, handler_filter_order)


def handler_filter_size(items, filter, arg_filters):
    """Удаляет раздачи, не соответсвующие переданному фильтру размера
    """
    # устанавливаем фильтр по размеру
    filter_size = None
    if Size.TINY is filter:
        filter_size = range(0, 1301)
    elif Size.SMALL is filter:
        filter_size = range(1301, 2251)
    elif Size.MEDIUM is filter:
        filter_size = range(2251, 4097)
    elif Size.BIG is filter:
        filter_size = range(4097, 9729)
    elif Size.LARGE is filter:
        filter_size = range(9729, 25601)
    elif Size.HUGE is filter:
        filter_size = range(25601, 9999999999)

    # если такой фильтр не был передан, то возвращаем без изменений
    if not filter_size:
        return items

    # убираем не соответствующие фильтру раздачи
    tmp_arr = []
    for item in items:
        if int(item.size) in filter_size:
            tmp_arr.append(item)
    return tmp_arr


GlobalFilters.append(Size, handler_filter_size)


def handler_filter_nozeroseeders(items, filter, arg_filters):
    """Удаляет раздачи без сидеров
    """
    tmp_arr = []
    for item in items:
        if int(item.seeders) > 0:
            tmp_arr.append(item)
    return tmp_arr


GlobalFilters.append(NoZeroSeeders, handler_filter_nozeroseeders)


def handler_filter_category(items, filter, arg_filters):
    """Удаляет раздачи, не соответствующие категории
    """
    tmp_arr = []
    for item in items:
        if item.category is filter:
            tmp_arr.append(item)
    return tmp_arr


GlobalFilters.append(Category, handler_filter_category)


def handler_filter_nowords(items, filter, arg_filters):
    """Удаляет раздачи, содержащие указанные в фильтре слова
    """
    if filter is NoWords:
        raise MagnettoMisuseError("Initialize NoWords filter first. "
                                  "Example: NoWords(\"begin\")")

    tmp_arr = []
    for item in items:
        if item.name not in filter:
            tmp_arr.append(item)
    return tmp_arr


GlobalFilters.append(NoWords, handler_filter_nowords)


def handler_filter_registered(items, filter, arg_filters):
    """Фильтр по дате регистрации раздачи
    """
    current_time = int(float(time.time()))
    filter_time = None

    HOUR = 60 * 60
    DAY = HOUR * 24

    if Registered.TODAY is filter:
        filter_time = DAY
    elif Registered.YESTERDAY is filter:
        filter_time = DAY * 2
    elif Registered.FOR_3_DAYS is filter:
        filter_time = DAY * 3
    elif Registered.FOR_WEEK is filter:
        filter_time = DAY * 7
    elif Registered.FOR_MONTH is filter:
        filter_time = DAY * 32

    if not filter_time:
        return items

    tmp_arr = []
    for item in items:
        if int(float(item.created)) >= (current_time - filter_time):
            tmp_arr.append(item)
    return tmp_arr


GlobalFilters.append(Registered, handler_filter_registered)


def handler_filter_noequalsize(items, filter, arg_filters):
    # можно передавать в фильтр просто класс
    if filter is NoEqualSize:
        filter = NoEqualSize()

    # сначала необходимо отсортировать items по размеру
    sort_arr = sorted(items, key=lambda item: int(item.size))

    # составляем список раздач не совпадающих по размеру
    # менее чем на filter процент
    tmp_arr = []
    for i, item in enumerate(sort_arr[:-1]):
        next_size = int(sort_arr[i+1].size)
        current_size = int(item.size)
        # если размер текущей раздачи составляет менее filter
        # процента от размера следующей раздачи, то удаляем
        if (100-(current_size/next_size*100)) > int(filter):
            tmp_arr.append(item)
    # т.к. итерировались по всем, кроме последнего, то добавляем и его
    tmp_arr.append(sort_arr[len(sort_arr)-1])

    # удаляем из items все раздачи, которые не попали под фильтр
    result_arr = []
    for item in items:
        if item in tmp_arr:
            result_arr.append(item)
    return result_arr


GlobalFilters.append(NoEqualSize, handler_filter_noequalsize)


def handler_filter_resolution(items, filter, arg_filters):
    """Проверяет наличие ключевых слов для разрешения у каждого item
    """
    tmp_arr = []
    for item in items:
        if filter.value.strip() in item.name:
            tmp_arr.append(item)
    return tmp_arr


GlobalFilters.append(Resolution, handler_filter_resolution)


def handler_filter_source(items, filter, arg_filters):
    """Проверяет наличие ключевого слова из Source.ITEM в названии раздачи
    """
    tmp_arr = []
    for item in items:
        is_contain = False
        words = filter.value.strip().split(',')
        for word in words:
            if word and word.lower() in item.name.lower():
                is_contain = True
        if is_contain:
            tmp_arr.append(item)
    return tmp_arr


GlobalFilters.append(Source, handler_filter_resolution)
