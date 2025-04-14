import logging
from utils.parse_answer import parse_dataset_answer, parse_llm_answer

# Configuration log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_response(model_output: str, expected: str, dataset_type: str) -> bool:
    parse_func = {
        'clutrr': lambda: parse_llm_answer(model_output) == parse_dataset_answer(expected, dataset_type='clutrr'),
        'bbh': lambda: parse_llm_answer(model_output) == parse_dataset_answer(expected, dataset_type='bbh'),
        'mmlu': lambda: parse_llm_answer(model_output) == parse_dataset_answer(expected, dataset_type='mmlu'),
        'svamp': lambda: parse_llm_answer(model_output) == parse_dataset_answer(expected, dataset_type='svamp'),
        'aqua': lambda: parse_llm_answer(model_output) == parse_dataset_answer(expected, dataset_type='aqua'),
        'multiarith': lambda: parse_llm_answer(model_output) == parse_dataset_answer(expected, dataset_type='multiarith'),
        'date': lambda: parse_llm_answer(model_output) == parse_dataset_answer(expected, dataset_type='date'),
        'asdiv': lambda: parse_llm_answer(model_output) == parse_dataset_answer(expected, dataset_type='asdiv'),
        'gsm8k': lambda: parse_llm_answer(model_output) == parse_dataset_answer(expected, dataset_type='gsm8k'),
        'math': lambda: parse_llm_answer(model_output) == parse_dataset_answer(expected, dataset_type='math')
    }
    llm_answer = parse_llm_answer(model_output)
    dataset_answer = parse_dataset_answer(expected, dataset_type=dataset_type)
    logger.info(f"Parsed LLM answer: {llm_answer}, Parsed dataset answer: {dataset_answer}")
    return parse_func.get(dataset_type, lambda: False)()