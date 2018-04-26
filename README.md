[![Documentation Status](https://readthedocs.org/projects/magnetto/badge/?version=latest)](http://magnetto.readthedocs.io/ru/latest/?badge=latest)

Библиотека, которая позволяет забыть про сложности поиска необходимого торрент файла по трекерам.

Реализовано:
- [x] Поиск по трекеру
- [x] Фильтрация поисковой выдачи (Фильмы, Размер, Качество видео и т.д.)
- [x] Разбор(парсинг) страницы поиска

Поддерживаемые торрент-трекеры:
- [x] Rutracker.org
- [x] Kinozal.guru
- [ ] lostfilm
- [ ] NNM-Club

TODO:
- [ ] Разбор страницы с раздачей
- [ ] Получение списка новых раздач
- [ ] Добавление фильтра по игровым категориям
- [ ] Обработка "падения" сайта (по таймауту и по редиректу и по non 200 статусу)

Пример использования:
---------------------

Простой поиск:
```python3
>>> from magnetto import KinozalApi
>>> api = KinozalApi()
>>> api.authorization("root", "1234")
True
>>> api.search(query="python", limit=1)
[ResultParseSearchPage(id='292975', name='Монти Пайтон и Священный Грааль / Monty Python and the Holy Grail / 1975 / ПМ, ПД, ЛО / DVDRip', url='http://kinozal.guru/details.php?id=292975', category=<Category.FILMS: 1>, size='1024', seeders='11', leechers='0', downloads='', created='1491728940', magnet='', torrent='http://kinozal.guru/download.php?id=292975')]
```

Сложный поиск с применением фильтров:
```python3
>>> from magnetto import KinozalApi, Category, Resolution
>>> api = KinozalApi()
>>> api.authorization("root", "1234")
>>> api.search(query="начало", filters=[Category.FILMS, Resolution.FULL_HD], limit=1)
```
