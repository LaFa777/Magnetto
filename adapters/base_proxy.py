from abc import *
from .category import Category

"""
Интерфейс (Абстрактный класс) для реализации в адаптерах
"""

class BaseProxy(metaclass = ABCMeta):

    @abstractproperty
    def categories(self):
        pass

    def isSupportCategory(self, category):
        return (category in categories or category == Category.All)

    @abstractmethod
    def isLogin(self):
        pass

    @abstractmethod
    def search(self, value, category=Category.All, page=1):
        pass
