from apscheduler.schedulers.blocking import BlockingScheduler

from app.services.scraping.scraping_service import ScrapingService
from app.services.scraping.site_a import SiteAScraper
from app.services.scraping.site_b import SiteBScraper
from infra.logger.logger_manager import LoggingManager

logger = LoggingManager.get_logger(__name__)

def main() -> None:
    site1 = SiteAScraper("http://example.com/a")
    site2 = SiteBScraper("http://example.com/b")
    site3 = SiteAScraper("http://example.com/a.2")
    service = ScrapingService([site1, site2, site3])
    service.start_scraping()


if __name__ == "__main__":
    try:
        logger.debug("Debug message")
        logger.info("info message")
        logger.warning("warning message")
        logger.error("error message")
        try:
            1 / 0
        except ZeroDivisionError:
            logger.exception("exception message")

        scheduler = BlockingScheduler()
        scheduler.add_job(main, "interval", seconds=10)
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Process ended by user.")