from app.services.scraping.base import BaseScraper


class SiteAScraper(BaseScraper):
    def __init__(self, url: str) -> None:
        super().__init__(url)

    def scrape(self) -> str:
        return f"Scraped content from {self.url} of Site type A"

    def transform(self, content: str) -> str:
        return content.upper()
