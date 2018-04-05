from abc import *
from grab import Grab
from grab.error import GrabAuthError
from ..core import *


class Base(metaclass=ABCMeta):

    def __init__(self, grab: Grab, login: str, password: str):
        self.grab = grab.clone()
        self.login = login
        self.password = password
        self.authorization(self.login, self.password)

    @abstractmethod
    def authorization(self, login: str, password: str):
        pass

    # простая проверка на факт успешного логина
    def check_is_login(self, doc):
        if not doc.text_search(self.login):
            raise GrabAuthError

    @abstractmethod
    def search(self, value: str, cats=None, page=0, limit=0, order_by=OrderBy.DOWNLOADS, order=Order.DESC):
        pass
