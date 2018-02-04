import requests
from .base import Base
from ..utils import Category
import os

# TODO: реагировать на капчуху
class Rutracker(Base):

    categories = ["All"]
    results_on_page = 50

    def _authorization_request(self, login, password):
        self.grab.go('http://rutracker.org/forum/login.php')
        self.grab.doc.set_input('login_username', login)
        self.grab.doc.set_input('login_password', password)
        self.grab.doc.submit()

    def search(value, category='All', page=1):
        pass
        #self.grab.go("https://rutracker.org/forum/tracker.php?nm={value}".format({
        #    value: value,
        #}))
