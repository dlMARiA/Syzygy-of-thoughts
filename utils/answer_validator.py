from config.settings import settings
from log.logger_utils import Logger

logger = Logger().get_logger()


def validate_response(filled_template, true_answer, dataset_type):
    """
    验证LLM返回的结果是否正确
    :param filled_template: LLM填充后的模板
    :param true_answer: 真实答案
    :param dataset_type: 数据集类型
    :return: 验证结果（True 或 False）
    """
    try:
        # 解析LLM答案
        from parse_answer import parse_llm_answer
        predicted_answer = parse_llm_answer(filled_template)

        # 解析真实答案
        from parse_answer import parse_dataset_answer
        parsed_true_answer = parse_dataset_answer(true_answer, dataset_type)

        # 简单示例：直接比较答案
        return predicted_answer == parsed_true_answer
    except Exception as e:
        logger.error(f"Validation failed: {str(e)}")
        return False