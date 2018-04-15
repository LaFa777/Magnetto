import unittest
from grab import Grab
from magnetto import RutrackerParser
from .fixtures import mock_search_1


def buildGrab(filename):
    """Создает Grab объект с проинициализированным grab.doc
    """
    file = open("./tests/htmls/" + filename)
    str = file.read().encode("utf-8")
    file.close()
    return Grab(document_body=str)


class TestRutrackerParser(unittest.TestCase):

    def setUp(self):
        self.parser = RutrackerParser()

    def test_parser_search(self):
        grab = buildGrab('rutracker_search.html')
        result = self.parser.parse_search(grab.doc)

        self.assertEqual(result, mock_search_1)
