import datetime
from pathlib import Path
from typing import List, Type

from luigi import WrapperTask

from live_arbitrage_identificator.backend.pipeline_managers import run_a_pipeline


class AutoResetPipelineFileManager:
    @staticmethod
    def _get_new_filename(new_file: Path, version_number: int) -> Path:
        """
        Generates a new filename by appending the version number before the file extension.
        This ensures that files with the same name don't overwrite each other.
        """
        name = new_file.stem
        ext = new_file.suffix

        new_filename = f"{name}_v{version_number}{ext}"
        return new_file.with_name(new_filename)

    @staticmethod
    def generate_output_paths(old_paths: List[Path], run_time_str: str) -> List[Path]:
        """
        Generates new output paths by modifying the old paths, appending the run time and
        version number if necessary.
        """
        new_paths = []
        for old_path in old_paths:
            new_path = str(old_path).replace("metadata", "metadata/processed/")
            new_path = Path(
                new_path.replace(
                    ".csv",
                    "_at" + str(run_time_str) + "_" + ".csv",
                )
            )

            version_number = 1
            while new_path.exists():
                new_path = AutoResetPipelineFileManager._get_new_filename(new_path, version_number)
                version_number += 1

            new_paths.append(new_path)

        return new_paths


class AutoResetPipeline:
    """
    AutoResetPipeline is an extension of Luigi's WrapperTask that facilitates running the same pipeline
    (with the same inputs) multiple times. It archives the results once the last step is achieved and then
    resets the completion status of the pipeline, allowing it to be run again.

    This class is designed to work with pipelines that need to be executed frequently, such as multiple times
    per day or per minute. By managing the processed results and ensuring unique naming through versioning,
    it prevents overwriting and allows for historical tracking of results, thus keeping the pipeline output clean,
    organized, and easy to access as Luigi does.

    The AutoResetPipeline handles the following key functionalities:
    - Running the pipeline by calling a specified run_a_pipeline function.
    - Resetting the complete status of the pipeline to allow for repeated runs.
    - Moving processed files to a designated directory and managing filenames to avoid conflicts.
    - Keeping track of how many times the pipeline has been run.

    Attributes:
        pipeline (Type[WrapperTask]): The pipeline object that encapsulates the tasks to be run.
        counter (int): A counter to keep track of how many times the pipeline has been run.
        run_timestamps (List[datetime.datetime]): A list of timestamps for each time the pipeline has been run.

    Example usage:
        my_pipeline = MyPipelineTask()
        auto_reset_pipeline = AutoResetPipeline(my_pipeline)
        auto_reset_pipeline.run()  # Run the pipeline and reset its completion status
        auto_reset_pipeline.run()  # Run the pipeline again.
    """

    def __init__(self, pipeline: WrapperTask):
        self.pipeline = pipeline
        self.counter = 0
        self.run_timestamps = []

    def run(self):
        """
        Executes the pipeline by calling run_a_pipeline, resets its completion status,
        increments the counter, and records the run timestamp.
        """
        run_timestamp = datetime.datetime.now()  # Get the current timestamp
        self.run_timestamps.append(run_timestamp)  # Record the run timestamp

        run_a_pipeline(self.pipeline)
        self.reset_complete_status()
        self.counter += 1

    def reset_complete_status(self):
        """
        Resets the complete status of the pipeline to False by moving the
        files to directory `processed` and deleting the old files.
        """
        run_time_str = str(datetime.datetime.now().hour) + "_" + str(datetime.datetime.now().minute)
        old_outputs = self.pipeline.output()
        old_paths = [Path(i.path) for i in old_outputs]
        new_paths = AutoResetPipelineFileManager.generate_output_paths(old_paths, run_time_str)
        self.move_files(old_paths, new_paths)

    @staticmethod
    def _determine_version_number(new_files: list[Path]) -> int:
        """
        Determines the next available version number based on existing files.
        """
        version_number = 0
        for new_file in new_files:
            while (new_file.with_name(f"{new_file.stem}_v{version_number}{new_file.suffix}")).exists():
                version_number += 1
        return version_number

    @staticmethod
    def move_files(old_files: list[Path], new_files: list[Path]):
        """
        Moves the old files to the new files. If any of the new_files already exists,
        uses a version number to avoid overwriting the file while still keeping the old file.
        All files from the same run will share the same version number.
        """
        if not all([old_file.exists() for old_file in old_files]):
            raise FileNotFoundError("Not all old files exist\n" + str(old_files))

        version_number = AutoResetPipeline._determine_version_number(new_files)

        for old_file, new_file in zip(old_files, new_files):
            new_file.parent.mkdir(parents=True, exist_ok=True)
            new_file_with_version = new_file.with_name(f"{new_file.stem}_v{version_number}{new_file.suffix}")
            old_file.rename(new_file_with_version)
