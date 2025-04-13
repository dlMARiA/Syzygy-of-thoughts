import os
import yaml

# 读取 sot.yaml 文件
config_path = os.path.join(os.path.dirname(__file__), 'sot.yaml')
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)


class Settings:
    OPENAI_API_KEY = config['openai']['api_key']
    MODEL_NAME = config['openai']['model_name']
    BASE_URL = config['openai']['base_url']
    MAX_TOKENS = config['openai']['max_tokens']
    MAX_RETRIES = config['openai']['max_retries']
    TEMPERATURE = None
    RUNNER_DEFAULT_DATASET = config['runner']['default_dataset']
    RUNNER_DEFAULT_DATASET_TYPE = config['runner']['default_dataset_type']
    RUNNER_DEFAULT_METHOD = config['runner']['default_method']
    RUNNER_DEFAULT_BETTI_NUMBER = config['runner']['default_betti_number']
    RUNNER_DEFAULT_SOLUTION_NUMBER = config['runner']['default_solution_number']
    DATASET_LOADER_MAPPING = config.get('dataset_loader_mapping', {})
    PROMPT_TEMPLATE_MAPPING = config.get('prompt_template_mapping', {})
    ANSWER_PARSER_MAPPING = config.get('answer_parser_mapping', {})

    @classmethod
    def dynamic_max_tokens(cls, question: str) -> int:
        """按问题长度动态计算最大令牌数"""
        base_length = 512
        question_length = len(question.split())
        return min(base_length + question_length * 2, 4096)

    @classmethod
    def set_temperature(cls, temperature: float):
        cls.TEMPERATURE = temperature if temperature is not None else config['openai']['temperature']


settings = Settings()