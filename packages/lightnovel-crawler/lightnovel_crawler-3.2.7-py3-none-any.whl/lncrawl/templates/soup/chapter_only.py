from abc import abstractmethod
from typing import Generator

from bs4 import BeautifulSoup, Tag

from ...models import Chapter
from .general import GeneralSoupTemplate


class ChapterOnlySoupTemplate(GeneralSoupTemplate):
    def parse_chapter_list(self, soup: BeautifulSoup) -> Generator[Chapter, None, None]:
        chap_id = 0
        for tag in self.select_chapter_tags(soup):
            if not isinstance(tag, Tag):
                continue
            chap_id += 1
            yield self.parse_chapter_item(tag, chap_id)

    @abstractmethod
    def select_chapter_tags(self, soup: BeautifulSoup) -> Generator[Tag, None, None]:
        """Select chapter list item tags from the page soup"""
        raise NotImplementedError()

    @abstractmethod
    def parse_chapter_item(self, tag: Tag, id: int) -> Chapter:
        """Parse a single chapter from chapter list item tag"""
        raise NotImplementedError()
