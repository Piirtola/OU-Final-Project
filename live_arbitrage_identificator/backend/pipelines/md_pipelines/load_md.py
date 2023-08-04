import datetime
import time
from pathlib import Path

import luigi
import pandas as pd

from live_arbitrage_identificator.backend.data_models.enums.sport_types import SportType


from live_arbitrage_identificator.backend.database.database_helper import DBHelper
from live_arbitrage_identificator.backend.database.database_manager import DatabaseManagerConfig, DBManager
from live_arbitrage_identificator.backend.scrapers.scraper_options import SCRAPER_TYPE
from live_arbitrage_identificator.backend.tasks.base_task import BaseTask
from live_arbitrage_identificator.backend.tasks.metadata_tasks.transform_md import TransformMd
from live_arbitrage_identificator.backend.transformers.oddsportal.op_md_transformer import sport_type_option_map
from live_arbitrage_identificator.backend.utils.load_env import load_db_env
from live_arbitrage_identificator.backend.utils.path_helpers import get_abs_path_from_relative
from live_arbitrage_identificator.backend.utils.read_file_to_df import read_file_to_df

db_manager = DBManager(DatabaseManagerConfig(**load_db_env()))
db_helper = DBHelper(db_manager)

scraper_type_id_map = {
    SCRAPER_TYPE.ODDSPORTAL.value: 1,
}


class LoadMd(BaseTask):
    scraper_type = luigi.EnumParameter(enum=SCRAPER_TYPE)
    sport_type = luigi.EnumParameter(enum=SportType)
    metadata_date = luigi.DateParameter(default=datetime.date.today())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.write_attempts = 0

    def requires(self):
        return TransformMd(
            scraper_type=self.scraper_type,
            sport_type=self.sport_type,
            metadata_date=self.metadata_date,
        )

    def run(self):
        formatted_data_df = read_file_to_df(self.input().path, ",")
        # TODO: Change this to a new version (still taking in a DF) but using the new RDB Schema
        db_helper.insert_pre_scrap_metadata_df(formatted_data_df)
        self.write_to_file(formatted_data_df)

    def write_to_file(self, formatted_data_df: pd.DataFrame):
        filepath = self.generate_output_path()
        filepath.parent.mkdir(parents=True, exist_ok=True)

        scraper_type_id = scraper_type_id_map[self.scraper_type.value]
        sport_type_id = sport_type_option_map[self.sport_type.value]

        query = f"SELECT * FROM pre_scrap_metadata WHERE match_date = '{self.metadata_date}' AND sport_type_id = '{sport_type_id}' AND scraper_type_id = '{scraper_type_id}'"
        df = db_helper.fetch_query_as_df(query)

        # The query sometimes returns an empty dataframe as the data is not yet in the database for some reason.
        if df.empty:
            if self.write_attempts < 3:
                print("Sleeping for 5 seconds and trying again.")
                time.sleep(5)
                self.write_attempts += 1
                self.write_to_file(formatted_data_df)
            df = db_helper.fetch_query_as_df(query)
            if df.empty:
                print("Error incoming")
                print(df)
                print(db_helper.fetch_query_as_df(query))
                raise ValueError(f"No data found for query:" + str(query))
        else:
            df.to_csv(self.output().path, index=False)

    def generate_output_path(self) -> Path:
        date_str = self.metadata_date.strftime("%Y_%m_%d")
        output_path_end = f"data/metadata/loaded/{self.sport_type.value}_{date_str}_{self.scraper_type.value}.csv"
        return get_abs_path_from_relative(Path(output_path_end))
