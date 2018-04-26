Тестирование Magnetto
=====================

.. warning::

  В разработке

В любом Python 3.4+ окружении:

.. code-block:: bash

    pip3 install turq
    cd tests
    turq -r routes.py -p 9877 --no-editor


.. code-block:: bash

  python3 -m unittest tests/test_rutracker_api.py tests/test_rutracker_parser.py


Проверка покрытия проекта тестами:

.. code-block:: bash

  pip3 install coverage
  coverage run -m unittest tests/test_rutracker_api.py tests/test_rutracker_parser.py
  coverage report
