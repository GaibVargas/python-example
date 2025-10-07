from abc import ABC, abstractmethod


class BaseScraper(ABC):
    def __init__(self, url: str) -> None:
        self.url = url

    @abstractmethod
    def scrape(self) -> str:
        pass

    @abstractmethod
    def transform(self, content: str) -> str:
        pass

    def run(self) -> str:
        content = self.scrape()
        return self.transform(content)
