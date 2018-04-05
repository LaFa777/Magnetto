import settings
import sys
import trackers
import inspect
from grab import Grab
from trackers.core import Category


def init_apis():
    """
    Инициализирует апишки к трекерам
    """
    apis = {}
    for name, obj in inspect.getmembers(sys.modules["trackers.apis"]):
        if inspect.isclass(obj):
            # инициализируем grab объект для каждого трекера
            grab = Grab()
            # TODO: при отсутствии свойства в массиве env вылазит ошибка (заменить на settings.py)
            # Сохранение последней загруженной страницы
            if settings.DEBUG and settings.DEBUG_DIR:
                grab.setup(log_file="{dir}/{class_name}.html".format(
                    dir=settings.DEBUG_DIR,
                    class_name=name
                ))
            # директория для хранения кук
            if settings.trackers[name]["cookies_dir"]:
                grab.setup(cookiefile="{dir}/{class_name}.cookie".format(
                    dir=settings.trackers[name]["cookies_dir"],
                    class_name=name
                ))
            # настройка прокси сервера
            if settings.PROXY and settings.PROXY_TYPE:
                grab.setup(proxy=settings.PROXY,
                           proxy_userpwd=settings.PROXY_USERPWD,
                           proxy_type=settings.PROXY_TYPE)

            # логин и пароль читаем из аргументов
            login = settings.trackers[name]["login"]
            password = settings.trackers[name]["password"]
            if(not login or not password):
                print("Api " + name +
                      " не инициализировано (не установлены логин или пароль)")
            apis[name] = obj(grab, login, password)
    return apis


def main():
    apis = init_apis()
    # проверка работы
    print(vars(apis["Rutracker"].search("Начало", categories=[Category.Film], limit=1)[0]))


if __name__ == '__main__':
    main()
