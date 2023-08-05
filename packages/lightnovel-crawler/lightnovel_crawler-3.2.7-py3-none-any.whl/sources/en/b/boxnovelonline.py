# -*- coding: utf-8 -*-
import logging
from lncrawl.core.crawler import Crawler

logger = logging.getLogger(__name__)
search_url = "https://boxnovel.online/?s=%s&post_type=wp-manga&author=&artist=&release="


class BoxNovelOnline(Crawler):
    base_url = "https://boxnovel.online/"

    def search_novel(self, query):
        query = query.lower().replace(" ", "+")
        soup = self.get_soup(search_url % query)

        results = []
        for tab in soup.select(".c-tabs-item__content"):
            a = tab.select_one(".post-title h3 a")
            latest = tab.select_one(".latest-chap .chapter a").text
            results.append(
                {
                    "title": a.text.strip(),
                    "url": self.absolute_url(a["href"]),
                    "info": "%s" % (latest),
                }
            )

        return results

    def read_novel_info(self):
        logger.debug("Visiting %s", self.novel_url)
        soup = self.get_soup(self.novel_url)

        self.novel_title = " ".join(
            [str(x) for x in soup.select_one(".post-title h1").contents if not x.name]
        ).strip()
        logger.info("Novel title: %s", self.novel_title)

        probable_img = soup.select_one(".summary_image img")
        if probable_img:
            self.novel_cover = self.absolute_url(probable_img["data-src"])
        logger.info("Novel cover: %s", self.novel_cover)

        author = soup.select(".author-content a")
        if len(author) == 2:
            self.novel_author = author[0].text + " (" + author[1].text + ")"
        else:
            self.novel_author = author[0].text
        logger.info("Novel author: %s", self.novel_author)

        volumes = set()
        chapters = soup.select("ul.main li.wp-manga-chapter a")
        for a in reversed(chapters):
            chap_id = len(self.chapters) + 1
            vol_id = (chap_id - 1) // 100 + 1
            volumes.add(vol_id)
            self.chapters.append(
                {
                    "id": chap_id,
                    "volume": vol_id,
                    "url": self.absolute_url(a["href"]),
                    "title": a.text.strip() or ("Chapter %d" % chap_id),
                }
            )

        self.volumes = [{"id": x} for x in volumes]

    def download_chapter_body(self, chapter):
        soup = self.get_soup(chapter["url"])

        contents = soup.select_one("div.text-left")
        for bad in contents.select("h3, .code-block, script, .adsbygoogle"):
            bad.extract()

        return str(contents)
