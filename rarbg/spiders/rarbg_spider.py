import csv

from pathlib import Path

import scrapy
import logging
from urllib.parse import parse_qs
from ..items import Torrent


LOGGER = logging.getLogger(__name__)


class TorrentSpider(scrapy.Spider):
    name = "rarbg"

    def __init__(self, search_term: str = None):
        # if search_term != None, then ensure this string is in titles
        # self.search_term = 'MP3-daily-2019-January-26'
        self.search_term = search_term
        if search_term == "ignore":
            self.search_term = None
        # search_term = 'MP3-daily-2022-February-05'
        if self.search_term:
            pass
            # Search only music
            start_url = f"https://rarbg.to/torrents.php?search={search_term}&category%5B%5D=23&category%5B%5D=25"
            # Search all categories
            # start_url = f"https://rarbg.to/torrents.php?search={search_term}"
        else:
            # URL of movie torrents sorted by seeders descending order
            start_url = "http://rarbg.to/torrents.php?category=44&page=1"
            # 4K.HDR Movies
            # start_url = f"https://rarbg.to/torrents.php?category=52&page=120"
        self.start_urls = [start_url]

        # Figure out how to determine where we are writing
        self.already_have = set()
        target_file = Path("/home/xjjk/scrapers/rarbg/None.auto.csv")
        if not target_file.exists():
            return
        already_have = set()
        with target_file.open() as csvfile:
            reader = csv.DictReader(csvfile)
            for r in reader:
                title = r["title"]
                magnet = r["magnet"]
                if not magnet.startswith("magnet"):
                    continue
                already_have.add(title)
        self.already_have = already_have
        self.logger.info(f"Already have: ", already_have)

    def parse(self, response):
        #        self.logger.info(response)

        # Determine page of going through search results
        page = None
        url_components = parse_qs(response.url)
        if "page" in url_components:
            page = int(url_components["page"][0])

        self.logger.info(f"Processing {response.url}, page={page}")

        # Torrents on this page first
        for tr in response.css("tr.lista2"):
            tds = tr.css("td")
            title = tds[1].css("a")[0].css("::attr(title)").get()

            if title in self.already_have:
                self.logger.info(f"Skipping {title}, already fetched")
                continue

            if not title:
                self.logger.error(tr)
            search_term = self.search_term
            if search_term and search_term not in title:
                self.logger.info(f"Skipping {title} as does not match {search_term}")
                continue

            self.logger.info(f"Found {title}")
            t = Torrent(
                title=tds[1].css("a")[0].css("::attr(title)").get(),
                url=response.urljoin(tds[1].css("a")[0].css("::attr(href)").get()),
                upload_date=tds[2].css("::text").get(),
                size=tds[3].css("::text").get(),
                seeders=int(tds[4].css("::text").get()),
                leechers=int(tds[5].css("::text").get()),
                uploader=tds[7].css("::text").get(),
            )

            torrent_info_request = scrapy.Request(
                t["url"],
                callback=self.parse_torrent_info,
                cb_kwargs=dict(torrent=t),
                priority=1,
            )
            yield torrent_info_request

        MAX_PAGES: int | None = 40
        # Crawl next pages
        for page_url in response.css("#pager_links > a::attr(href)").extract():
            page_url = response.urljoin(page_url)

            if page:
                url_components = parse_qs(page_url)
                next_page = int(url_components["page"][0])

                self.logger.debug(f"{next_page=}")

                if next_page < page:
                    self.logger.info(f"Skipping search results page={next_page}, url={page_url}")
                    continue

                if MAX_PAGES and next_page >= MAX_PAGES:
                    continue

            yield scrapy.Request(url=page_url, callback=self.parse)

    def parse_torrent_info(self, response, torrent: Torrent):
        magnet_link = response.css(
            "tr:nth-child(1) > td:nth-child(2) > a:nth-child(3)::attr(href)"
        ).get()
        if magnet_link is None:
            self.logger.debug(response)
        self.logger.info(magnet_link)
        torrent["magnet"] = magnet_link
        yield torrent
