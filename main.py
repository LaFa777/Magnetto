import trackers
import os
import sys
import inspect
from grab import Grab
import os.path

def main():
    apis = {}
    for name, obj in inspect.getmembers(sys.modules["trackers.apis"]):
        if inspect.isclass(obj):
            grab = Grab()
            # Сохранение последней загруженной страницы
            if os.environ['DEBUG'] and os.environ['DEBUG_DIR']:
                grab.setup(log_file="{dir}/{class_name}.html".format(
                    dir = os.environ['DEBUG_DIR'],
                    class_name = name
                    ))
            # директория для хранения кук
            if os.environ['COOKIES_DIR']:
                cookie_file = "{dir}/{class_name}.cookie".format(
                                    dir = os.environ['COOKIES_DIR'],
                                    class_name = name
                                    )
                grab.setup(cookiefile=cookie_file)
                # если кука существует, загрузим её
                if(os.path.isfile(cookie_file)):
                    grab.cookies.load_from_file(cookie_file)
                # grab.load_cookies(cookie_file)
            # настройка прокси сервера
            if os.environ['SOCKS5_PROXY']:
                grab.setup(proxy=os.environ['SOCKS5_PROXY'], proxy_type="socks5")
            login = os.environ[name.upper() + '_LOGIN']
            password = os.environ[name.upper() + '_PASSWORD']
            if(not login or not password):
                print("Api " + name + " не инициализировано (не установлены логин и пароль)")
            api_obj = obj(grab, login, password)
            print(api_obj.is_login())
            apis[name.lower()] = api_obj
    print(apis)

if __name__ == '__main__':
    main()
