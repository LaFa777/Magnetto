from abc import *
from grab.document import Document


class Base(metaclass=ABCMeta):
    @abstractmethod
    def extract_magnet(self, doc: Document):
        pass
