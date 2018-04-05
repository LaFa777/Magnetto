from .base import Base
from grab import Grab


class Rutracker(Base):
    film = "1105,1165,124,1245,1246,1247,1248,1250,1390,140,1543,1577,1642,1666,"\
        "187,1900,194,1950,1991,208,209,2090,2091,2092,2093,2198,2199,22,2200,"\
        "2201,2221,2258,2339,2343,2365,2540,312,313,33,376,4,404,484,505,521,"\
        "539,7,709,893,921,922,923,924,925,926,927,928,930,934,941"
    tv_series = ""

    def add_filter(self, grab: Grab, categories: list):
        """
        Формирует запрос типа https://rutracker.org/forum/tracker.php?f={список категорий}
        """
        # получаем список поддерживаемых категорий
        diff_categories = self.list_support_categories(categories)
        if not diff_categories:
            return

        # составляем list аргументов
        args = []
        for category in diff_categories:
            args.append(getattr(self, category))

        # формируем окончательный url
        url = "{url}&{param}".format(
            url=grab.config["url"],
            param=','.join(args)
        )

        # и устанавливаем его
        grab.setup(url=url)
