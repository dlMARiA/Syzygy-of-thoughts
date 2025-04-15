from interfaces import DatasetLoaderInterface
import json
from pathlib import Path
from config.settings import settings
from log.logger_utils import Logger

logger = Logger().get_logger()

class DatasetLoader(DatasetLoaderInterface):
    """
    Handles the loading of datasets in various formats, providing specific processing
    logic for different dataset types.

    Attributes:
        loader_mapping (dict): A mapping of dataset types to their respective
            loader functions as configured in the settings.
    """
    def __init__(self):
        self.loader_mapping = settings.DATASET_LOADER_MAPPING

    def load_math_bbh_mmlu(self, file_path):
        """
        Loads and processes a dataset from a specified JSON file path. The dataset can be in the form
        of a single JSON structure containing multiple items, or a JSON Lines format where each line is
        an independent JSON object. Processes each dataset item, ensuring consistent attribute names
        for `problem` and `solution` based on available keys.

        Args:
            file_path (str): Path to the JSON file containing the dataset.

        Returns:
            list: A list of processed dataset items. Each item is a dictionary with keys `problem`
            and `solution`.

        Raises:
            Exception: If there is an error opening or reading the file.
            json.JSONDecodeError: If the JSON content or individual JSON lines cannot be parsed.

        """
        dataset = []
        try:
            with Path(file_path).open("r", encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    for item in data:
                        item["problem"] = item.get("problem", "") if 'problem' in item else item.get("input", "")
                        item["solution"] = item.get("solution", "") if 'solution' in item else item.get("answer", "")
                        dataset.append(item)
                except json.JSONDecodeError:
                    f.seek(0)
                    for line in f:
                        try:
                            item = json.loads(line)
                            item["problem"] = item.get("problem", "") if 'problem' in item else item.get("input", "")
                            item["solution"] = item.get("solution", "") if 'solution' in item else item.get("answer", "")
                            dataset.append(item)
                        except json.JSONDecodeError as e:
                            logger.error(f"Failed to parse JSON line: {str(e)}, line content: {line[:100]}...")
        except Exception as e:
            logger.error(f"Failed to load dataset: {str(e)}")
        return dataset

    def load_other_datasets(self, file_path):
        """
        Loads datasets from a specified file, parses each line as JSON, and extracts required fields
        to create a unified dataset format.

        Args:
            file_path (str): The path to the file containing the dataset in JSON line format.

        Returns:
            list[dict]: A list of dictionaries where each dictionary contains the fields "problem"
            and "solution". Lines that could not be processed are excluded from the returned dataset.
        """
        print("load_other_datasets method is called.")  # Add print statement
        dataset = []
        try:
            with Path(file_path).open("r", encoding='utf-8') as f:
                for line in f:
                    try:
                        item = json.loads(line)
                        item["problem"] = item.get("question", "")
                        item["solution"] = item.get("answer", "")
                        dataset.append(item)
                    except json.JSONDecodeError as e:
                        # logger.error(f"Failed to parse JSON line: {str(e)}, line content: {line[:100]}...")
                        pass
        except Exception as e:
            # logger.error(f"Failed to load dataset: {str(e)}")
            pass
        return dataset

    def load_dataset(self, file_path: str, dataset_type: str) -> list:
        """
        Loads and processes a dataset based on the specified file path and dataset type.

        This function selects the appropriate loader function based on the `dataset_type` and
        uses it to process the dataset located at the provided `file_path`. If the `dataset_type`
        is not supported, an error message is logged, and an empty list is returned.

        Args:
            file_path: Path to the dataset file to load.
            dataset_type: Type of the dataset to load. Supported types include "math", "bbh",
                "mmlu", "gsm8k", "clutrr", "svamp", "aqua", "multiarith", "date", and "asdiv".

        Returns:
            A list containing the processed dataset. Returns an empty list if the dataset type
            is unsupported.
        """
        # Make sure keys are capitalized consistently
        loader_function = {
            'math': self.load_math_bbh_mmlu,
            'bbh': self.load_math_bbh_mmlu,
            'mmlu': self.load_math_bbh_mmlu,
            'gsm8k': self.load_other_datasets,
            'clutrr': self.load_other_datasets,
            'svamp': self.load_other_datasets,
            'aqua': self.load_other_datasets,
            'multiarith': self.load_other_datasets,
            'date': self.load_other_datasets,
            'asdiv': self.load_other_datasets
        }
        loader = loader_function.get(dataset_type.lower())
        if loader:
            return loader(file_path)
        logger.error(f"Unsupported dataset type: {dataset_type}")
        return []