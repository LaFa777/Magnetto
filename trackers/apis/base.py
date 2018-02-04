from abc import *
import grab
from ..utils import Category

"""
Интерфейс (Абстрактный класс) для реализации в адаптерах
"""

class Base(metaclass = ABCMeta):

    def __init__(self, grab, login=None, password=None):
        self.grab = grab.clone()
        self.authorization(login, password)

    def authorization(self, login, password):
        if(not password):
            login = self.login
            password = self.password
        else:
            self.login = login
            self.password = password

        if (not password):
            raise ValueError("password и login не определены")

        if self.is_login():
            return

        self._authorization_request(login, password)

    @abstractmethod
    def _authorization_request(self, login, password):
        pass

    def is_login(self):
        return bool(self.grab.cookies.items())

    @abstractproperty
    def categories(self):
        pass

    def is_support_category(self, category):
        return (category in categories or category == Category.All)

    @abstractmethod
    def search(self, value, category=Category.All, page=1):
        pass
