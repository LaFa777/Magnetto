from grab import Grab
import settings
from magnetto import ApiDispatcher, Category, MagnettoCaptchaError


def main():
    # настраиваем граб объект с прокси
    grab = Grab()
    grab.setup(proxy=settings.PROXY, proxy_userpwd=settings.PROXY_USERPWD,
               proxy_type=settings.PROXY_TYPE)

    dp = ApiDispatcher(grab=grab, log_dir=settings.LOG_DIR,
                       coockie_dir=settings.COOCKIE_DIR)

    # проинициализируем каждый трекер из настроек
    for api, conf in settings.trackers.items():
        try:
            dp.authorization(api, conf["login"], conf["password"])
        except MagnettoCaptchaError as err:
            print("Woop woop! Captcha is here: " + err.url)
            print('Please input catpcha: ', end='')
            captcha = input()
            # попробуем снова...
            dp.authorization(api, conf["login"], conf["password"], captcha)

    # проверим работоспособносить поиска
    print(dp.search("приключения капитана врунгеля",
                    categories=[Category.FILMS], limit=1))


if __name__ == '__main__':
    main()
