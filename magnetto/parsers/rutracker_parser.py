import magnetto
from magnetto.filters import Category
from magnetto.parsers import BaseParser, transformParseError, ResultParse


class RutrackerParser(BaseParser):

    HOME = None

    def __init__(self):
        self.HOME = magnetto.RUTRACKER_URL

    def parse_category(self, doc):
        """Возвращает элемент Category, соответствующий данному элементу
        поиска
        """
        category = {"root": "", "root_forum": "", "forum": ""}

        # заполняем форум из поиска
        category["forum"] = doc.xpath('td[3]/div/a/text()')[0]

        # заполняем корневой форум
        el = doc.xpath('//option[contains(text(), "{}")]'
                       .format(category["forum"]))[0]
        if "root_forum" in el.classes:
            category["root_forum"] = el.text
        else:
            while True:
                el = el.getprevious()
                if el is None:
                    break
                if "root_forum" in el.classes:
                    category["root_forum"] = el.text
                    break

        # заполняем категорию
        category["root"] = el.getparent().get("label")

        # Определяем конечную категорию
        if "Мульфильмы" in category["root_forum"] or \
            "Мультсериалы" in category["root_forum"] or \
                "Аниме" in category["root_forum"]:
            return Category.CARTOONS
        elif "кино" in category["root_forum"].lower() or \
                "Video" in category["root_forum"]:
            return Category.FILMS
        elif "сериалы" in category["root"].lower():
            return Category.TV_SERIES
        elif "книги" in category["root"].lower():
            return Category.BOOKS
        elif "аудиокниги" in category["root"].lower():
            return Category.AUDIOBOOKS
        elif "музыка" in category["root"].lower():
            return Category.MUSICS
        elif "игры" in category["root"].lower():
            return Category.GAMES
        elif "программы" in category["root"].lower():
            return Category.PROGRAMS
        else:
            return Category.UNDEFINED

    @transformParseError
    def parse_search(self, doc):
        result_items = []
        for tr in doc.tree.xpath('//table[@id="tor-tbl"]/tbody/tr'):
            topic_id = tr.xpath('td[4]/div/a/@data-topic_id')[0]
            size_int = int(tr.xpath('td[6]/u')[0].text)
            category = self.parse_category(tr)
            item = ResultParse(
                id=topic_id,
                category=category,
                name=tr.xpath('td[4]/div/a')[0].text,
                url=self.HOME + "viewtopic.php?t=" + str(topic_id),
                size=str(int(size_int/1024/1024)),
                seeders=tr.xpath('td[7]/u')[0].text or '0',
                leechers=tr.xpath('td[8]/b')[0].text or '0',
                downloads=tr.xpath('td[9]')[0].text or '0',
                created=tr.xpath('td[10]/u')[0].text or -1,
                torrent=self.HOME + "dl.php?t=" + str(topic_id),
                magnet=""
            )
            result_items.append(item)
        return result_items

    @transformParseError
    def parse_topic(self, doc):
        # TODO: переделать
        return doc.tree.xpath('//a[contains(@href,"magnet")]/@href')[0]
