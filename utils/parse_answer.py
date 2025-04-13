from config.settings import settings
from log.logger_utils import Logger

logger = Logger().get_logger()


def parse_llm_answer(filled_template):
    """
    解析LLM返回的模板，提取答案
    :param filled_template: LLM填充后的模板
    :return: 解析后的答案
    """
    try:
        # 这里可以根据具体的模板格式进行解析
        # 示例：假设答案在 "final_answer" 字段中
        import json
        template_dict = json.loads(filled_template)
        return template_dict.get("final_answer", "")
    except json.JSONDecodeError:
        logger.error("Failed to parse LLM answer as JSON.")
        return ""


def parse_dataset_answer(raw_answer, dataset_type):
    """
    解析数据集中的答案
    :param raw_answer: 数据集中的原始答案
    :param dataset_type: 数据集类型
    :return: 解析后的答案
    """
    parser_path = settings.ANSWER_PARSER_MAPPING.get(dataset_type)
    if parser_path:
        parts = parser_path.split('.')
        module_name = '.'.join(parts[:-1])
        class_name = parts[-1]
        module = __import__(module_name, fromlist=[class_name])
        parser_class = getattr(module, class_name)
        parser = parser_class()
        return parser.parse(raw_answer)
    logger.error(f"Unsupported dataset type for answer parsing: {dataset_type}")
    return raw_answer