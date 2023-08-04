import logging

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.job import Job
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from luigi import WrapperTask

from live_arbitrage_identificator.backend.pipelines.auto_reset_pipeline import AutoResetPipeline


class MdPipelineManager:
    """
    Class that manages the metadata pipelines and their concurrent execution utilizing APScheduler and
    its ProcessPoolExecutor, MemoryJob, and BackgroundScheduler.
    """

    def __init__(self):
        executors = {"processpool": ProcessPoolExecutor()}
        self.scheduler = BackgroundScheduler(executors=executors)
        self.scheduler.start()
        self.scheduler.add_jobstore(MemoryJobStore(), alias="default_job-store")
        self.pipelines = []
        logging.info("MdPipelineManager initialized.")

    def add_pipeline(self, pipeline: WrapperTask | AutoResetPipeline, interval_seconds: int = 10800):
        """
        Adds a Luigi.WrapperTask pipeline to the manager, by wrapping it into an AutoResetPipeline.
        Then schedules it to run every interval_seconds using the BackgroundScheduler.

        Args:
            pipeline (WrapperTask | AutoResetPipeline): The pipeline to be added to the manager.
            interval_seconds (int, optional): The interval in seconds between each pipeline run. Defaults to 10800s = 3h.
        """
        job_instance = AutoResetPipeline(pipeline)
        job = self.scheduler.add_job(
            job_instance.run,
            "interval",
            seconds=interval_seconds,
            jobstore="default_jobstore",
            executor="processpool",
            misfire_grace_time=60,
        )
        self.pipelines.append(job)
        logging.info(f"Pipeline {pipeline.__annotations__} added. Scheduled to run every {interval_seconds} seconds.")

    def add_and_run_pipeline(self, pipeline: WrapperTask | AutoResetPipeline, interval_seconds: int = 10800):
        """
        Adds a Luigi.WrapperTask pipeline to the manager, by wrapping it into an AutoResetPipeline.
        Then schedules it to run every interval_seconds. Finally, runs the pipeline immediately.

        Args:
            pipeline (WrapperTask | AutoResetPipeline): The pipeline to be added to the manager.
            interval_seconds (int, optional): The interval in seconds between each pipeline run. Defaults to 10800s = 3h.
        """
        self.add_pipeline(pipeline, interval_seconds)
        pipeline.run()
        logging.info(f"Pipeline {pipeline.__annotations__} run.")

    def remove_pipeline(self, job):
        """
        Removes a pipeline from the manager.

        Args:
            job: The job representing the pipeline to be removed.
        """
        if job in self.pipelines:
            self.scheduler.remove_job(job.id)
            self.pipelines.remove(job)
            logging.info(f"Pipeline removed. Job ID: {job.id}")
        else:
            logging.warning("Attempted to remove a non-existent pipeline.")

    def pause_pipeline(self, job):
        """
        Pauses a pipeline in the manager.

        Args:
            job: The job representing the pipeline to be paused.
        """
        if job in self.pipelines:
            self.scheduler.pause_job(job.id)
            logging.info(f"Pipeline paused. Job ID: {job.id}")
        else:
            logging.warning("Attempted to pause a non-existent pipeline.")

    def resume_pipeline(self, job):
        """
        Resumes a paused pipeline in the manager.

        Args:
            job: The job representing the pipeline to be resumed.
        """
        if job in self.pipelines:
            self.scheduler.resume_job(job.id)
            logging.info(f"Pipeline resumed. Job ID: {job.id}")
        else:
            logging.warning("Attempted to resume a non-existent pipeline.")
