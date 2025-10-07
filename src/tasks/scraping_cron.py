from apscheduler.schedulers.blocking import BlockingScheduler

from app.services.scraping.scraping_service import ScrapingService
from app.services.scraping.site_a import SiteAScraper
from app.services.scraping.site_b import SiteBScraper


def main() -> None:
    site1 = SiteAScraper("http://example.com/a")
    site2 = SiteBScraper("http://example.com/b")
    site3 = SiteAScraper("http://example.com/a.2")
    service = ScrapingService([site1, site2, site3])
    service.perform_scraping()


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(main, "interval", seconds=10)
    print("Scheduler iniciado. Pressione Ctrl+C para encerrar.")
    scheduler.start()
