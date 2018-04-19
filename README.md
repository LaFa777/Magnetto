[![Documentation Status](https://readthedocs.org/projects/magnetto/badge/?version=latest)](http://magnetto.readthedocs.io/ru/latest/?badge=latest)

Библиотека, берущая на себя сложности по работе с торрент-трекерами.

Реализуемый функционал:
- [x] Поиск по трекеру

Поддерживаемые торрент-трекеры:
- [x] Rutracker.org
- [x] Kinozal.guru

Пример использования:
---------------------

```python3
api = KinozalApi()
api.authorization("root", "1234")
print(api.search("python", limit=1))
```

Тестирование
------------

В любом Python 3.4+ окружении:

```bash
pip3 install turq
turq -r routes.py -p 9877 --no-editor
python3 -m unittest tests/test_rutracker_api.py
```

Проверка покрытия проекта тестами:

```bash
pip3 install coverage
coverage run -m unittest tests/test_rutracker_api.py
coverage report
```
