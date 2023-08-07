import unittest
from pathlib import Path
from unittest.mock import MagicMock

import luigi

from live_arbitrage_identificator.backend.pipelines.auto_reset_pipeline import (
    AutoResetPipeline,
    AutoResetPipelineFileManager,
)


class DummyTask(luigi.Task):
    def run(self):
        pass

    def output(self):
        return [luigi.LocalTarget(Path("/tmp/old_file.txt"))]  # Return a list


class TestAutoResetPipelineFileManager(unittest.TestCase):
    def test_get_new_filename(self):
        filename = Path("file.txt")
        new_filename = AutoResetPipelineFileManager._get_new_filename(filename, 2)
        self.assertEqual(new_filename, Path("file_v2.txt"))

    def test_generate_output_paths(self):
        old_paths = [Path("metadata/file.csv")]
        run_time_str = "12_30"
        new_paths = AutoResetPipelineFileManager.generate_output_paths(old_paths, run_time_str)
        self.assertEqual(new_paths, [Path("metadata/processed/file_at12_30_.csv")])


class TestAutoResetPipeline(unittest.TestCase):
    def setUp(self) -> None:
        self.old_file = Path("/tmp/old_file.txt")
        if not self.old_file.parent.exists():
            self.old_file.parent.mkdir(parents=True)

    def test_move_files(self):
        old_file = self.old_file
        new_file = Path(str(self.old_file).replace("old", "new"))
        versioned_new_file = new_file.with_name(f"{new_file.stem}_v0{new_file.suffix}")

        # Clean up any existing test files
        if versioned_new_file.exists():
            versioned_new_file.unlink()

        old_file.touch()
        AutoResetPipeline.move_files([old_file], [new_file])

        self.assertFalse(old_file.exists())
        self.assertTrue(versioned_new_file.exists())

        # Clean up after test
        versioned_new_file.unlink()

    def test_reset_complete_status_dummy(self):
        pipeline_task = DummyTask()
        auto_reset_pipeline = AutoResetPipeline(pipeline_task)
        auto_reset_pipeline.move_files = MagicMock()
        auto_reset_pipeline.reset_complete_status()
        auto_reset_pipeline.move_files.assert_called_once()

    def test_reset_complete_status_mock(self):
        pipeline_mock = MagicMock()
        pipeline_mock.output.return_value = [MagicMock(path=str(Path("/tmp/old_file.txt")))]
        auto_reset_pipeline = AutoResetPipeline(pipeline_mock)
        auto_reset_pipeline.move_files = MagicMock()
        auto_reset_pipeline.reset_complete_status()
        auto_reset_pipeline.move_files.assert_called_once()


if __name__ == "__main__":
    unittest.main()
