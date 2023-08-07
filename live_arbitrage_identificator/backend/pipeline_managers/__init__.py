import logging

import luigi

logging.basicConfig(level=logging.WARNING)


def run_a_pipeline(pipeline: luigi.WrapperTask):
    """Runs a pipeline by building it and running it."""
    luigi.build([pipeline], local_scheduler=True)
