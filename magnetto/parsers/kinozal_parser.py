import re
import magnetto
from magnetto.filters import Category
from magnetto.parsers import BaseParser, transformParseError, ResultParse

from magnetto.utils import parse_size, parse_date


class KinozalParser(BaseParser):

    HOME = None

    def __init__(self):
        self.HOME = magnetto.KINOZAL_URL

    def parse_category(self, doc):
        """Определение категории на основе... картинки в поисковой выдаче
        """
        img_src = doc.xpath('td[1]/img/@src')[0]

        num = re.findall(r'([0-9]+)\.gif', img_src)[0]
        if num in "6,7,8,9,10,11,12,13,14,15,16,17,18,24,33,35,36,39,47,49,50":
            return Category.FILMS
        elif num in "45,46":
            return Category.TV_SERIES
        elif num in "19,20,21,22":
            return Category.CARTOONS
        elif num in "3,4,5,42":
            return Category.MUSICS
        elif num in "41":
            return Category.BOOKS
        elif num in "2":
            return Category.AUDIOBOOKS
        elif num in "23":
            return Category.GAMES
        elif num in "32":
            return Category.PROGRAMS
        else:
            return Category.UNDEFINED

    @transformParseError
    def parse_search(self, doc):
        result_items = []
        for tr in doc.tree.xpath('//table/tr[contains(@class, "bg")]'):
            topic_link = tr.xpath('td[2]/a/@href')[0]
            topic_id = re.findall(r'\d+', topic_link)[0]
            category = self.parse_category(tr)
            item = ResultParse(
                id=topic_id,
                category=category,
                name=tr.xpath('td[2]/a/text()')[0],
                url=self.HOME + topic_link[1:],
                size=parse_size(tr.xpath('td[4]/text()')[0]),
                seeders=tr.xpath('td[5]/text()')[0],
                leechers=tr.xpath('td[6]/text()')[0],
                created=parse_date(tr.xpath('td[7]/text()')[0]),
                torrent=self.HOME + "download.php?id=" + str(topic_id),
                magnet=""
            )
            result_items.append(item)
        return result_items

    @transformParseError
    def parse_topic(self, doc):
        pass
