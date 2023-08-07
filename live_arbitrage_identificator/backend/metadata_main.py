import asyncio
import datetime

from live_arbitrage_identificator.backend.data_models.enums.sport_types import SportType
from live_arbitrage_identificator.backend.scrapers.scraper_options import SCRAPER_TYPE
from live_arbitrage_identificator.utils.config_manager import ConfigManager
from live_arbitrage_identificator.utils.logger import Logger, logging

# from project.src.backend.managers.job_factory import JobFactory
# from project.src.backend.managers.md_job_manager import MdJobManager


logger = Logger(log_dir="../logs/metadata", log_file="metadata_main.log", log_level=logging.INFO)


@logger.log_timing
async def main():
    """
    Main function for the metadata collection software.
    This function uses ConfigManager to create metadata jobs and adds them to the MdJobManager.
    MdJobManager is responsible for running and scheduling these jobs and their pipelines.
    """

    config_manager = ConfigManager()
    job_factory = JobFactory()
    md_job_manager = MdJobManager()

    metadata_scrapers = config_manager.get_config("available_metadata_scrapers")
    for scraper in metadata_scrapers:
        scraper_type = SCRAPER_TYPE(scraper["site"].upper())
        for sport in scraper["sports"]:
            sport_type = SportType(sport.upper())

            for date in [None, datetime.date.today() + datetime.timedelta(days=1)]:
                pipeline = job_factory.create_metadata_pipeline_task(scraper_type, sport_type, date)
                md_job_manager.add_pipeline_as_job(pipeline, interval_seconds=60 * 60)

    while True:
        try:
            await asyncio.sleep(5)
        except Exception as e:
            logger.log(logging.ERROR, f"Exception occurred: {e}")


if __name__ == "__main__":
    logger.log(logging.INFO, "Starting metadata collection software")
    asyncio.run(main())
