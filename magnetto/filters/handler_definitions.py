import time

import attr

from magnetto.errors import MagnettoMisuseError

from .core import OrderBy, DateRegistered


def handler_filter_order(items, filter):
    """Сортирует раздачи по убыванию или возрастанию
    """

    # сначала определим столбец, по которому происходит сортировка
    index = None
    if OrderBy.CREATE is filter.column:
        index = "created"
    elif OrderBy.NAME is filter.column:
        index = "name"
    elif OrderBy.DOWNLOADS is filter.column:
        index = "downloads"
    elif OrderBy.SEEDERS is filter.column:
        index = "seeders"
    elif OrderBy.LEECHERS is filter.column:
        index = "leechers"
    elif OrderBy.SIZE is filter.column:
        index = "size"
    else:
        return items

    # для числовых сортируем предварительно приведя к int
    # изменить как в книжке getattr
    if "name" in index and filter.asc is False:
        return sorted(items,
                      key=lambda item: getattr(item, index),
                      reverse=True)
    elif "name" in index and filter.asc is True:
        return sorted(items,
                      key=lambda item: getattr(item, index),
                      reverse=False)
    elif filter.asc is False:
        return sorted(items,
                      key=lambda item: int(getattr(item, index)),
                      reverse=True)
    elif filter.asc is True:
        return sorted(items,
                      key=lambda item: int(getattr(item, index)),
                      reverse=False)
    else:
        return items


def handler_filter_limitsize(items, filter):
    """Удаляет раздачи, не соответсвующие переданному фильтру размера
    """
    # убираем не соответствующие фильтру раздачи
    tmp_arr = []
    for item in items:
        if int(item.size) <= filter_size:
            tmp_arr.append(item)
    return tmp_arr


def handler_filter_nozeroseeders(items, filter):
    """Удаляет раздачи без сидеров
    """
    tmp_arr = []
    for item in items:
        if int(item.seeders) > 0:
            tmp_arr.append(item)
    return tmp_arr


def handler_filter_category(items, filter):
    """Удаляет раздачи, не соответствующие категории
    """
    tmp_arr = []
    for item in items:
        if item.category is filter:
            tmp_arr.append(item)
    return tmp_arr


def handler_filter_nowords(items, filter):
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


def handler_filter_dateregistered(items, filter):
    """Фильтр по дате регистрации раздачи
    """
    current_time = int(float(time.time()))
    filter_time = None

    HOUR = 60 * 60
    DAY = HOUR * 24

    if DateRegistered.TODAY is filter:
        filter_time = DAY
    elif DateRegistered.YESTERDAY is filter:
        filter_time = DAY * 2
    elif DateRegistered.FOR_3_DAYS is filter:
        filter_time = DAY * 3
    elif DateRegistered.FOR_WEEK is filter:
        filter_time = DAY * 7
    elif DateRegistered.FOR_MONTH is filter:
        filter_time = DAY * 32

    if not filter_time:
        return items

    tmp_arr = []
    for item in items:
        if int(float(item.created)) >= (current_time - filter_time):
            tmp_arr.append(item)
    return tmp_arr


def handler_filter_noequalsize(items, filter):
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


def handler_filter_videoresolution(items, filter):
    """Проверяет наличие ключевых слов для разрешения у каждого item
    """
    tmp_arr = []
    for item in items:
        if filter.value.strip().lower() in item.name.lower():
            tmp_arr.append(item)
    return tmp_arr


def handler_filter_videosource(items, filter):
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


def handler_filter_limit(items, filter):
    return items[:int(filter)]
