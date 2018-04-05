from abc import *
import inspect
from grab import Grab


class Base(metaclass=ABCMeta):
    def list_self_categories(self):
        """
        Формирует список категорий текущего класса
        """
        categories = set()
        for name, obj in inspect.getmembers(self):
            if not callable(obj) and not name.startswith("_"):
                categories.add(name)
        return categories

    def list_support_categories(self, categories):
        """
        Возвращает список поддерживаемых категорий
        """
        return (set(self.list_self_categories()) & set(categories))

    @abstractmethod
    def add_filter(self, grab: Grab):
        pass
