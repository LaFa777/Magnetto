import requests
from .base_proxy import BaseProxy

# TODO: Минимальное логгирование успешной авторизации
# TODO: кукисы из файла
# TODO: реагировать на капчуху
class RutrackerProxy(BaseProxy):

    categories = ["All"]
    results_on_page = 50

    def __init__(self, login, password, proxies=None):
        self.rs = requests.Session()
        rq = self.rs.post('http://rutracker.org/forum/login.php', {
            'login_username' : login,
            'login_password' : password,
            'login' : '%D0%92%D1%85%D0%BE%D0%B4'
            }, proxies=proxies)

    def isLogin(self):
        return bool(self.rs.cookies)

    def search(value, category='All', page=1):
        pass

if __name__ == '__main__':
    import os
    proxy = RutrackerProxy(os.environ['LOGIN'], os.environ['PASSWORD'])
    print(proxy.isLogin())
