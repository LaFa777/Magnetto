from abc import ABC, abstractmethod


class BaseParser(ABC):
    """Все парсеры должны реализовывать данный интерфейс
    """

    @abstractmethod
    def parse_search_page(self, doc):
        """Разбирает страницу поиска

        Args:
            doc (:obj:`grab.Document`): Страница поиска

        Return:
            List[:obj:`magnetto.ResultParsePage`]: Результаты поиска

        Raises:
            :obj:`magnetto.MagnettoParseError`: Неудачный разбор страницы
        """

    @abstractmethod
    def parse_topic_page(self, doc):
        """Разбирает страницу с топиком

        Args:
            doc (:obj:`grab.Document`): Топик страницы

        Return:
            :obj:`magnetto.ResultParsePage`

        Raises:
            :obj:`magnetto.MagnettoParseError`: Неудачный разбор страницы
        """
