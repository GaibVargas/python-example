from typing import List

from app.services.scraping.base import BaseScraper
from infra.logger.logger_manager import LoggingManager

logger = LoggingManager.get_logger(__name__)


class ScrapingService:
    def __init__(self, scrapers: List[BaseScraper]) -> None:
        self.scrapers = scrapers
        self.content: List[str] = []

    def start_scraping(self) -> None:
        for scraper in self.scrapers:
            content = scraper.run()
            logger.info(content)
            self.content.append(content)
