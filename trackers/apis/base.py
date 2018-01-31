from abc import *
from ..utils import Category

"""
Интерфейс (Абстрактный класс) для реализации в адаптерах
"""

class Base(metaclass = ABCMeta):

    @abstractproperty
    def categories(self):
        pass

    def is_support_category(self, category):
        return (category in categories or category == Category.All)

    @abstractmethod
    def is_login(self):
        pass

    @abstractmethod
    def search(self, value, category=Category.All, page=1):
        pass
