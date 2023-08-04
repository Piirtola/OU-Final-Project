import datetime
from pathlib import Path

import luigi

from project.src.backend.data_models.enums.sport_types import SportType
from project.src.backend.data_models.scraper_results.metadata_results import RawMetadataCSV
from project.src.backend.drivers.dynamic_driver_pool import DynamicDriverPool
from project.src.backend.scrapers.scraper_factory import ScraperFactory
from project.src.backend.scrapers.scraper_options import SCRAPER_TYPE
from project.src.backend.tasks.base_task import BaseTask
from project.src.backend.utils.path_helpers import get_abs_path_from_relative

driver_pool = None
scraper_factory = None


def get_driver_and_scraper():
    global driver_pool, scraper_factory
    if driver_pool is None:
        driver_pool = DynamicDriverPool(1, 10)
    if scraper_factory is None:
        scraper_factory = ScraperFactory(driver_pool)


class ScrapMd(BaseTask):
    """
    Task for scraping the metadata for a given sport type, date, and scraper type.

    The parameters are needed to create the scraper, the output path is generated from the parameters as well.
    """

    sport_type = luigi.EnumParameter(enum=SportType)
    scraper_type = luigi.EnumParameter(
        enum=SCRAPER_TYPE, default=SCRAPER_TYPE.ODDSPORTAL
    )
    metadata_date = luigi.DateParameter(default=datetime.date.today())

    def requires(self) -> None:
        return

    def run(self):
        get_driver_and_scraper()

        scraper = scraper_factory.create_md_scraper(
            self.scraper_type, self.sport_type, self.metadata_date
        )
        raw_data = scraper.run()
        scraper_factory.driver_pool._return_driver(scraper.driver)
        self.write_to_file(raw_data)

    def write_to_file(self, raw_data: RawMetadataCSV):
        raw_data.write_to_file(self.generate_output_path())

    def generate_output_path(self) -> Path:
        date_str = self.metadata_date.strftime("%Y_%m_%d")
        output_path_end = f"data/metadata/raw/{self.sport_type.value}_{date_str}_{self.scraper_type.value}.csv"
        return get_abs_path_from_relative(Path(output_path_end))
