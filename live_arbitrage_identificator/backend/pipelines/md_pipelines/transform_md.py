import datetime
from pathlib import Path

import luigi
import pandas as pd

from project.src.backend.data_models.enums.sport_types import SportType
from project.src.backend.data_models.scraper_results.metadata_results import read_metadata_results
from project.src.backend.scrapers.scraper_options import SCRAPER_TYPE
from project.src.backend.tasks.base_task import BaseTask
from project.src.backend.tasks.metadata_tasks.parse_md import ParseMd
from project.src.backend.transformers.transformer_factory import TransformerFactory
from project.src.backend.utils.path_helpers import get_abs_path_from_relative


class TransformMd(BaseTask):
    """
    A task that transforms metadata to RDB friendly format.
    """

    scraper_type = luigi.EnumParameter(enum=SCRAPER_TYPE)
    sport_type = luigi.EnumParameter(enum=SportType)
    metadata_date: datetime.date = luigi.DateParameter(default=datetime.date.today())

    def requires(self) -> luigi.Task:
        return ParseMd(
            scraper_type=self.scraper_type,
            sport_type=self.sport_type,
            metadata_date=self.metadata_date,
        )

    def run(self):
        transformer = TransformerFactory().create_md_transformer(self.scraper_type, self.sport_type)
        parsed_data = read_metadata_results(Path(self.input().path))
        transformed_data = transformer.transform()
        self.write_to_file(transformed_data)

    def write_to_file(self, transformed_data: pd.DataFrame):
        filepath = self.generate_output_path()
        filepath.parent.mkdir(parents=True, exist_ok=True)
        transformed_data.to_csv(filepath, index=False)

    def generate_input_path(self) -> str:
        return self.input().path

    def generate_output_path(self) -> str:
        date_str = self.metadata_date.strftime("%Y_%m_%d")
        output_path_end = f"data/metadata/transformed/{self.sport_type.value}_{date_str}_{self.scraper_type.value}.csv"
        return get_abs_path_from_relative(Path(output_path_end))
