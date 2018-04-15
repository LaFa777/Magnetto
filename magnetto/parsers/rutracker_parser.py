from magnetto import (BaseParser, transformParseError, ResultParseSearchPage,
                      RUTRACKER_URL)


class RutrackerParser(BaseParser):

    HOME = RUTRACKER_URL

    @transformParseError
    def parse_search(self, doc):
        result_items = []
        for tr in doc.tree.xpath('//table[@id="tor-tbl"]/tbody/tr'):
            topic_id = tr.xpath('td[4]/div/a/@data-topic_id')[0]
            item = ResultParseSearchPage(
                id=topic_id,
                category=tr.xpath('td[3]/div/a/text()')[0],
                name=tr.xpath('td[4]/div/a/text()')[0],
                url=self.HOME + "viewtopic.php?t=" + str(topic_id),
                author=tr.xpath('td[5]/div/a/text()')[0],
                size=tr.xpath('td[6]/u/text()')[0],
                seeders=tr.xpath('td[7]/u/text()')[0],
                leechers=tr.xpath('td[8]/b/text()')[0],
                downloads=tr.xpath('td[9]/text()')[0],
                created=tr.xpath('td[10]/u/text()')[0],
                torrent=self.HOME + "dl.php?t=" + str(topic_id),
                magnet=""  # TODO:
            )
            result_items.append(item)
        return tuple(result_items)

    @transformParseError
    def parse_topic(self, doc):
        # TODO: переделать
        return doc.tree.xpath('//a[contains(@href,"magnet")]/@href')[0]
