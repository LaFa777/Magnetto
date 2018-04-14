from grab import Grab
from magnetto import (Order, OrderBy, BaseApi, MagnettoCaptchaError)


class ApiDispatcher(object):
    """Диспетчер, абстрагирующий от работы с множественными апи трекера. Умеет
    выполнять инициализацию переданных Api, в том числе проставляет
    соответствующие настройки :obj:`grab.Grab` объекту (пример: coockie файл,
    log файл). Делегирует вызовы одноименным вызовам апи.

    Examples:

        Пример инициализации с одним объектом

    >>> api = RutrackerApi("Roland", "1234")
    ... dispatcher = ApiDispatcher([api, ])
    ... print(dispatcher.search("Начало"))
    """

    def __init__(self, grab=Grab(), objs=[], log_dir=None, coockie_dir=None):
        """
        Args:
            objs (List[:obj:`magnetto.BaseApi`]): Массив Api объектов
            grab (:obj:`grab.Grab`, optional): Экземпляр Grab объекта.
                Используется для указания своих типов настроек (пример:
                настройки прокси).
            log_dir (:obj:`str`, optional): В данную директорию помещается
                результат выполнения запроса
            coockie_dir (:obj:`str`, optional): Директория, для сохранения
                coockie файлов
        """
        self._grab = grab.clone()
        self._log_dir = log_dir
        self._coockie_dir = coockie_dir
        self._apis = objs
        self._fail_apis = {}

    def add_obj(self, obj):
        """Добавляет api объект

        Args:
            obj (:obj:`magnetto.BaseApi`): Api объект

        Return:
            :obj:`True` - объект добавлен
            :obj:`False` - такой объект уже существует
        """
        if isinstance(obj, BaseApi) and obj not in self._apis:
            self._apis.append(obj)
            return True
        else:
            return False

    def get_obj(self, cls):
        """Возвращает соответствующий экземпляр Api объекта

        Args:
            cls (:obj:`magnetto.BaseApi`): Api класс

        Return:
            :obj:`magnetto.BaseApi` Соответствущий классу объект
            :obj:`None` Соответствущего объекта не найдено
        """
        for obj in self._apis:
            if isinstance(obj, cls):
                return obj
        return None

    def del_cls(self, cls):
        """Удаляет объект данного типа из обработки (нужен например при
        изменении формы входа и невозможности повторной авторизации)

        Args:
            cls (:obj:`magnetto.BaseApi`): Api класс
        """
        for obj in self._apis:
            if isinstance(obj, cls):
                self._apis.remove(obj)

    def del_obj(self, obj):
        """Удаляет переданный объект из обработки

        Args:
            obj (:obj:`magnetto.BaseApi`): Api объект
        """
        if obj in self._apis:
            self._apis.remove(obj)

    def authorization(self, cls, login, password, captcha=None):
        """Выполняет процедуру авторизации для укзанного Api класса и сохраняет
        объект методом add_obj. Проставляет в grab объекте параметры log_file
        и cookiefile

        Args:
            cls (:obj:`magnetto.BaseApi`): Инициализирует переданный cls и
                выполняет :obj:`BaseApi.authorization()`
            login (:obj:`str`): Логин для входа
            password (:obj:`str`): Пароль для входа
            captcha (:obj:`str`): Введенная капча (нужна только при ошибке
                предыдущей авторизации)

        Return:
            :obj:`True`: успешная авторизация

        Raises:
            :obj:`magnetto.MagnettoIncorrectСredentials`: введены неверные
                данные для входа
            :obj:`magnetto.MagnettoCaptchaError`: на странице обнаружена капча
        """
        if not (captcha and cls in self._fail_apis):

            # подстройка grab объекта под cls
            grab = self._grab.clone()
            grab.setup(log_file="{dir}/{cls}.html".format(
                dir=self._log_dir,
                cls=cls.__name__))
            grab.setup(cookiefile="{dir}/{cls}.cookie".format(
                dir=self._coockie_dir,
                cls=cls.__name__))

            obj = cls(grab)
        else:
            # берем уже проицициализированный объект, для ввода капчи
            # (отправки ранее используемой формы)
            obj = self._fail_apis[cls]

        try:
            obj.authorization(login, password, captcha)
        except MagnettoCaptchaError as e:
            # сохраняем экземпляр объекта, чтобы в дальнейшем иметь возможность
            # ввести капчу и отправить запрос повторно
            self._fail_apis[cls] = obj
            raise

        # сохранять объект больше нет необходимости
        if cls in self._fail_apis:
            del self._fail_apis[cls]

        # сохраняем объект в случае успешной авторизации
        self.add_obj(obj)

        return True

    def search(self, value, categories=[], page=0, limit=0,
               order_by=OrderBy.DOWNLOADS, order=Order.DESC):
        """
        Todo:
            * фильтры
        """
        if not self._apis:
            raise Exception("ApiDispather has no Api objects")

        results = {}
        for obj in self._apis:
            results[obj.__class__] = obj.search(
                value, categories, page, limit, order_by, order)

        # TODO: всякие разные фильтры

        return results
