Введение в Magnetto
===================

Работа с Api
------------

Основной функционал с которым вам скорее всего придется работать это объекты,
представляющие собой реализацию унифицированного интерфейса для доступа к выбранному сайту.


В самом простом случае использование Magnetto выглядит следующим образом:

.. code-block:: python

  (1) from magnetto import KinozalApi

  (2) api = KinozalApi()
  (3) api.authorization("dima", "1234")
  (4) items = api.search(query="python")
  (5) len(items) and print(items[0].url)

Разберем код более подробно:

``(1)`` является сокращенной формой полного включения ``from magnetto.apis
improt KinozalApi``. Вместо ``KinozalApi`` допускается использование любого
другого класса, реализующего интерфейс ``BaseApi``.

``(3)`` выполняет процедуру входа на сайте, обязательно должен вызываться перед
вызовом остальных методов. Если его не вызвать, то остальные методы будут
поднимать исключение ``MagnettoAuthError``. В случае, если на странице
обнаружена капча, то поднимается исключение ``MagnettoCaptchaError``.

``(4)`` выполняет запрос на сайт по поиску необходимой информации, вызывает
соответствующий Parser объект и возвращает всю необходимую информацию.

``(5)`` выводит url найденной раздачи в терминал

Авторизация
-----------

При вводе некорректных учетных данных поднимается исключение
``MagnettoIncorrectСredentials``

.. code-block:: python

    from magnetto.errors import MagnettoAuthError
    from magnetto import RutrackerApi

    api = RutrackerApi(grab)
    try:
      api.authorization("dima", "1234")
    except MagnettoAuthError:
      print("Некорректные данные для входа")
      exit(1)

Авторизация на сайте выполняется путём заполнения формы входа и отправки её на сервер. В ходе авторизации на сайте может потребоваться ввод капчи с картинки,
в таком случае поднимается исключение ``MagnettoCaptchaError`` содержащее url
картинки, api объект запоминает своё состояние (последний запрошенный документ)
и требует при повторном вызове строку с капчой.

Более наглядно покажу на примере:

.. code-block:: python

  from magnetto.errors import MagnettoCaptchaError
  from magnetto.apis import RutrackerApi

  api = RutrackerApi()
  try:
    api.authorization("dima", "1234")
  except MagnettoCaptchaError as err:
    print("Обнаружена капча: " + err.url)
    print('Ввод распознанной капчи: ', end='')
    captcha = input()
    api.authorization("dima", "1234", captcha)

.. note::

    Более сложные виды капчи (по типу reCAPTCHA) в данный момент не
    обрабатываются. Я просто не сталкивался на трекерах с ней.

Работа с прокси
---------------

Для доступа к сайтам может потребоваться проксирование запросов, в Magnetto
проксирование реализовано при помощи предварительной настройки ``Grab``
объекта. Более подробно вы можете прочитать из документации одноименного
модуля.

Простой пример настройки прокси:

.. code-block:: python

  from grab import Grab
  from magnetto import RutrackerApi

  grab = Grab()
  grab.setup(proxy="ip:port", proxy_userpwd="user:pass",
             proxy_type="socks5")

  api = RutrackerApi(grab=grab)
  ...

Поиск
-----

Функция поиска имеет следующее определение:

.. code-block:: python

  def search(self, query, filters=[], page=0, limit=999):

.. warning::

  Важным ограничением данного метода является невозможность вызова с
  использованием анонимных параметров. При вызове параметры необходимо
  именовать. Данное ограничение связанно с декоратором ``api_filters_method``

Как видно из определения в поиске поддерживается ограничение итоговых
результатов используя аргумент ``limit``.

.. code-block:: python

  api.search(query="python", limit=1)

Сильной стороной поиска в Magnetto являются фильтры, позволяющие уточнять
процедуру поиска.

.. code-block:: python

  from magnetto.filters import Category, Resolution

  ...

  api.search(query="начало", filters=[Category.FILMS, Resolution.FULL_HD])

Подробнее о фильтрах написано в документе :ref:`using_filters`
