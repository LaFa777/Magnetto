"""Различные примеси для объектов типа ``BaseApi``"""

from magnetto.errors import MagnettoAuthError


class LastRequestMixin:
    """Функционал для получения последнего запроса
    """

    def get_last_request_data(self):
        """
        Return:
            ``Dict``:
            * ``Dict["url"]`` последний запрошенный url
            * ``Dict["post"]`` данные последнего post запроса
        """
        return {
            "url": self._grab.config["url"],
            "post": self._grab.config["post"]
        }


class CheckAuthMixin:
    """Добавляет простейший функционал для проверки факта успешного входа
    """

    def is_logged(self):
        """Проверяет на странице наличие имени пользователя.

        Return:
            ``True``: Пользователь авторизован.

        Raises:
            ``MagnettoAuthError``
        """
        if not self._grab.doc.text_search(self._login):
            raise MagnettoAuthError("Error authorization")

        return True
