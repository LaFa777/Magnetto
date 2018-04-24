[![Documentation Status](https://readthedocs.org/projects/magnetto/badge/?version=latest)](http://magnetto.readthedocs.io/ru/latest/?badge=latest)

Библиотека, которая позволяет забыть про сложности поиска необходимого торрент файла по трекерам.

Реализовано:
- [x] Поиск по трекеру
- [x] Фильтрация поисковой выдачи (Фильмы, Размер, Качество видео и т.д.)
- [x] Разбор(парсинг) страницы поиска
- [ ] Разбор топика с раздачей

Поддерживаемые торрент-трекеры:
- [x] Rutracker.org
- [x] Kinozal.guru
- [ ] lostfilm
- [ ] NNM-Club

Пример использования:
---------------------

Простой поиск:
```python3
>>> from magnetto import KinozalApi
>>> api = KinozalApi()
>>> api.authorization("root", "1234")
True
>>> api.search("python", limit=1)
[ResultParseSearchPage(id='292975', name='Монти Пайтон и Священный Грааль / Monty Python and the Holy Grail / 1975 / ПМ, ПД, ЛО / DVDRip', url='http://kinozal.guru/details.php?id=292975', category=<Category.FILMS: 1>, size='1024', seeders='11', leechers='0', downloads='', created='1491728940', magnet='', torrent='http://kinozal.guru/download.php?id=292975')]
```

Сложный поиск с применением фильтров:
```python3
>>> from magnetto import KinozalApi, Category
>>> api = KinozalApi()
>>> api.authorization("root", "1234")
True
>>> api.search("python", filters=[Category.BOOKS], limit=1)
[ResultParseSearchPage(id='934418', name='Марк Лутц - Программирование на Python (2 тома из 2) / Учебная / 2011 / PDF', url='http://kinozal.guru/details.php?id=934418', category=<Category.BOOKS: 5>, size='68', seeders='6', leechers='0', downloads='', created='1330258320.0', magnet='', torrent='http://kinozal.guru/download.php?id=934418')]
```
Более подробно про фильтры написано в документации.


Тестирование
------------

В любом Python 3.4+ окружении:

```bash
pip3 install turq
cd tests
turq -r routes.py -p 9877 --no-editor
```

```bash
python3 -m unittest tests/test_rutracker_api.py tests/test_rutracker_parser.py
```

Проверка покрытия проекта тестами:

```bash
pip3 install coverage
coverage run -m unittest tests/test_rutracker_api.py tests/test_rutracker_parser.py
coverage report
```
