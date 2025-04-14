from interfaces import DatasetLoaderInterface
import json
from pathlib import Path
from config.settings import settings
from log.logger_utils import Logger

logger = Logger().get_logger()

class DatasetLoader(DatasetLoaderInterface):
    def __init__(self):
        self.loader_mapping = settings.DATASET_LOADER_MAPPING

    def load_math_bbh_mmlu(self, file_path):
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