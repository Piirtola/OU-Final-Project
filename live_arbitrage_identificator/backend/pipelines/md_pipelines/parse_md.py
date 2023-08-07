import datetime
from pathlib import Path

import luigi

from project.src.backend.data_models.enums.sport_types import SportType
from project.src.backend.data_models.scraper_results.metadata_results import MetadataResults, read_raw_metadata_csv
from project.src.backend.parsers.parser_factory import ParserFactory
from project.src.backend.scrapers.scraper_options import SCRAPER_TYPE
from project.src.backend.tasks.base_task import BaseTask
from project.src.backend.tasks.metadata_tasks.scrap_md import ScrapMd
from project.src.backend.utils.path_helpers import get_abs_path_from_relative


class ParseMd(BaseTask):
    sport_type = luigi.EnumParameter(enum=SportType)
    scraper_type = luigi.EnumParameter(enum=SCRAPER_TYPE, default=SCRAPER_TYPE.ODDSPORTAL)
    metadata_date = luigi.DateParameter(default=datetime.date.today())

    def requires(self) -> ScrapMd:
        return ScrapMd(
            scraper_type=self.scraper_type,
            sport_type=self.sport_type,
            metadata_date=self.metadata_date,
        )

    def run(self):
        parser = ParserFactory().create_md_parser(self.scraper_type, self.sport_type)
        raw_data = read_raw_metadata_csv(Path(self.input().path))
        parsed_data = parser.parse(raw_data)
        self.write_to_file(parsed_data)

    def write_to_file(self, parsed_data: MetadataResults):
        output_path = self.generate_output_path()
        parsed_data.write_to_file(output_path)

    def generate_output_path(self) -> str:
        date_str = self.metadata_date.strftime("%Y_%m_%d")
        output_path_end = f"data/metadata/parsed/{self.sport_type.value}_{date_str}_{self.scraper_type.value}.csv"
        return get_abs_path_from_relative(Path(output_path_end))
