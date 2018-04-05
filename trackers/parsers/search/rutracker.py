from .base import *
from ...core import SearchItem
from grab.document import Document


class Rutracker(Base):
    def extract_items(self, doc: Document):
        items = []
        for tr in doc.tree.xpath('//table[@id="tor-tbl"]/tbody/tr'):
            item = SearchItem()
            item.category = tr.xpath('td[3]/div/a/text()')[0]
            item.name = tr.xpath('td[4]/div/a/text()')[0]
            item.url = tr.xpath('td[4]/div/a/@href')[0]
            item.author = tr.xpath('td[5]/div/a/text()')[0]
            item.size = tr.xpath('td[6]/u/text()')[0]
            item.seeders = tr.xpath('td[7]/u/text()')[0]
            item.leechers = tr.xpath('td[8]/b/text()')[0]
            item.downloads = tr.xpath('td[9]/text()')[0]
            item.created = tr.xpath('td[10]/u/text()')[0]
            items.append(item)
        return items
