# filePath: dataloader.py
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
        print("load_other_datasets method is called.")  # 添加打印语句
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
                        logger.error(f"Failed to parse JSON line: {str(e)}, line content: {line[:100]}...")
        except Exception as e:
            logger.error(f"Failed to load dataset: {str(e)}")
        return dataset

    def load_dataset(self, file_path: str, dataset_type: str) -> list:
        loader_path = self.loader_mapping.get(dataset_type)
        if loader_path:
            parts = loader_path.split('.')
            module_name = '.'.join(parts[:-1])
            function_name = parts[-1]
            module = __import__(module_name, fromlist=[function_name])
            loader = getattr(module, function_name)
            return loader(file_path)  # 移除 self 参数
        logger.error(f"Unsupported dataset type: {dataset_type}")
        return []