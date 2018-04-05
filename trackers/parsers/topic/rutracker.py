from .base import *
from grab.document import Document


class Rutracker(Base):
    def extract_magnet(self, doc: Document):
        return doc.tree.xpath('//a[contains(@href,"magnet")]/@href')[0]
