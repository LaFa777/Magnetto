from abc import ABC, abstractmethod


class BaseParser(ABC):
    """Все парсеры должны реализовывать данный интерфейс
    """

    @abstractmethod
    def parse_search(self, doc):
        """Разбирает страницу поиска

        Args:
            doc (``grab.Document``): Страница поиска

        Return:
            ``ResultParsePage``

        Raises:
            ``MagnettoParseError``
        """

    @abstractmethod
    def parse_topic(self, doc):
        """Разбирает страницу с топиком

        Args:
            doc (``grab.Document``): Топик страницы

        Return:
            ``ResultParsePage``

        Raises:
            ``MagnettoParseError``
        """
