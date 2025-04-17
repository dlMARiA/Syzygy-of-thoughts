import os
import yaml

# Read the sot.yaml file
config_path = os.path.join(os.path.dirname(__file__), 'diy.yaml')
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)


class Settings:
    """
    Encapsulates application settings and configurations, including OpenAI API
    settings, runner defaults, and mappings for dataset loaders, prompt templates,
    and answer parsers. Class methods allow for calculation and adjustment of
    specific settings dynamically.
    """
    OPENAI_API_KEY = config['openai']['api_key']
    MODEL_NAME = config['openai']['model_name']
    BASE_URL = config['openai']['base_url']
    MAX_TOKENS = config['openai']['max_tokens']
    MAX_RETRIES = config['openai']['max_retries']
    TEMPERATURE = None
    RUNNER_DEFAULT_DATASET = config['runner']['default_dataset']
    # Convert the default dataset type to lowercase
    RUNNER_DEFAULT_DATASET_TYPE = config['runner']['default_dataset_type'].lower()
    RUNNER_DEFAULT_METHOD = config['runner']['default_method']
    RUNNER_DEFAULT_BETTI_NUMBER = config['runner']['default_betti_number']
    RUNNER_DEFAULT_SOLUTION_NUMBER = config['runner']['default_solution_number']
    DATASET_LOADER_MAPPING = {k.lower(): v for k, v in config.get('dataset_loader_mapping', {}).items()}
    PROMPT_TEMPLATE_MAPPING = {k.lower(): v for k, v in config.get('prompt_template_mapping', {}).items()}
    ANSWER_PARSER_MAPPING = {k.lower(): v for k, v in config.get('answer_parser_mapping', {}).items()}
    TIP = config['runner']['tip']
    DEFAULT_TIP = config['runner']['default_tip']

    @classmethod
    def dynamic_max_tokens(cls, question: str) -> int:
        """
        Dynamically calculate the maximum number of tokens based on question length
        """
        base_length = 512
        question_length = len(question.split())
        return min(base_length + question_length * 2, 4096)

    @classmethod
    def set_temperature(cls, temperature: float):
        """
        Sets the class-level temperature to the specified value or to the default value
        from the configuration if the provided value is None.
        """
        cls.TEMPERATURE = temperature if temperature is not None else config['openai']['temperature']


settings = Settings()
