from magnetto import RutrackerApi

LOG_DIR = "/tmp"  # директория, с результатами выполнения запросов (html файлы)
COOCKIE_DIR = "/tmp"  # директория для coockie файлов

PROXY = ""  # url:port
PROXY_USERPWD = ""  # user:password
PROXY_TYPE = ""  # socks5, socks4, http

trackers = {
    RutrackerApi: {
        "login": "",
        "password": ""
    },
}
