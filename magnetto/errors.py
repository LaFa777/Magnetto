class MagnettoError(Exception):
    """Базовый класс в иерархии исключений модуля ``magnetto``
    """


class MagnettoMisuseError(MagnettoError):
    """Неправильное использование метода
    """


class MagnettoIncorrectСredentials(MagnettoError):
    """Неправильные пароль или логин. Вызывается при неудачной попытке
    авторизации.
    """


class MagnettoAuthError(MagnettoError):
    """Истек срок действия coockie файлов или найден признак необходимости
    авторизации.
    """


class MagnettoCaptchaError(MagnettoError):
    """Обнаружена капча на странице. Необходимо повторно произвести авторизацию
    с передачей распознанной капчи.
    """

    def __init__(self, obj, url):
        """
        Attributes:
            obj (BaseApi): объект, вызвавший исключительную ситацию
            url (str): ссылка на картинку с капчой
        """
        self.url = url
        self.obj = obj

    def __str__(self):
        """
        Return:
            ``str``: ссылка на картинку с капчой
        """
        return repr(self.url)


class MagnettoParseError(MagnettoError):
    """Неудачная попытка разбора страницы
    """
