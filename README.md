[![Documentation Status](https://readthedocs.org/projects/magnetto/badge/?version=latest)](http://magnetto.readthedocs.io/ru/latest/?badge=latest)


Абстрагирующая от сложностей работы по парсингу и поиску по торрент трекерам библиотека.

Тестирование
------------

В любом Python 3.4+ окружении::

    $ pip3 install turq
    $ turq -r routes.py -p 9877 --no-editor
    $ python3 -m unittest tests/test_rutracker_api.py
