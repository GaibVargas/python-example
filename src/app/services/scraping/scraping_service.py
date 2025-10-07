from typing import List

from app.services.scraping.base import BaseScraper


class ScrapingService:
    def __init__(self, scrapers: List[BaseScraper]) -> None:
        self.scrapers = scrapers
        self.content: List[str] = []

    def perform_scraping(self) -> None:
        for scraper in self.scrapers:
            content = scraper.run()
            print(content)
            self.content.append(content)
