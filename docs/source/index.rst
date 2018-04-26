.. Magnetto documentation master file, created by
   sphinx-quickstart on Wed Apr 11 12:51:50 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Magnetto - простой поиск по торрентам!
======================================

Magnetto предназначен для унификации работы с сайтами торрент трекеров, в частности
предоставляет программный интефейс позволяющий:

  * производить разбор(парсинг) страницы с заранее известной формой ответа
  * выполнять удаленные запросы к сайтам в удобной для описания форме

Описанный функционал в Magnetto реализуется двумя обширными подмодулями:

  * ``magnetto.apis`` - содержит определения Api классов для каждого из трекера.
    Реализует функционал для унификации и упрощения написания конечного Апи для
    нового сайта.
  * ``magnetto.parser`` - разбирает (парсит) страницы трекера и возвращает результат
    в уницифицированной, заранее определенной форме.


Документация Magnetto
---------------------

.. toctree::
  :maxdepth: 1

  tutorial
  using_filters

Разработчику
------------

.. toctree::
  :maxdepth: 1

  dev_testing
  dev_apis
  dev_parsers
  dev_filters

Подробное описание частей модуля
--------------------------------

.. toctree::
   magnetto

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
