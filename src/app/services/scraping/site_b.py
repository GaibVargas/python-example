from app.services.scraping.base import BaseScraper


class SiteBScraper(BaseScraper):
    def __init__(self, url: str) -> None:
        super().__init__(url)

    def scrape(self) -> str:
        return f"Scraped content from {self.url} of Site type B"

    def transform(self, content: str) -> str:
        return content.upper()
