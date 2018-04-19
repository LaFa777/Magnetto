import re
import magnetto
from magnetto import (BaseParser, transformParseError, ResultParseSearchPage)


class KinozalParser(BaseParser):

    HOME = None

    def __init__(self):
        self.HOME = magnetto.KINOZAL_URL

    @transformParseError
    def parse_search(self, doc):
        result_items = []
        for tr in doc.tree.xpath('//table/tr[contains(@class, "bg")]'):
            topic_link = tr.xpath('td[2]/a/@href')[0]
            topic_id = re.findall(r'\d+', topic_link)[0]
            item = ResultParseSearchPage(
                id=topic_id,
                category="",  # TODO:
                name=tr.xpath('td[2]/a/text()')[0],
                url=self.HOME + topic_link[1:],
                size=tr.xpath('td[4]/text()')[0], # разбор размера в машинный формат
                seeders=tr.xpath('td[5]/text()')[0],
                leechers=tr.xpath('td[6]/text()')[0],
                downloads="",  # TODO:
                created=tr.xpath('td[7]/text()')[0], # преобразование в unix time
                torrent=self.HOME + "download.php?id=" + str(topic_id),
                magnet=""  # TODO:
            )
            result_items.append(item)
        return tuple(result_items)

    @transformParseError
    def parse_topic(self, doc):
        pass
