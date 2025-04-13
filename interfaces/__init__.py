from abc import ABC, abstractmethod


class PromptTemplateFactoryInterface(ABC):
    @abstractmethod
    def get_prompt_template(self, method: str, dataset_type: str, betti_number: int, solution_number: int):
        pass


class DatasetLoaderInterface(ABC):
    @abstractmethod
    def load_dataset(self, file_path: str, dataset_type: str) -> list:
        pass


class AnswerParserInterface(ABC):
    @abstractmethod
    def parse(self, raw_answer):
        pass