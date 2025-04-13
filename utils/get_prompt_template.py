from interfaces import PromptTemplateFactoryInterface
from prompts.sot_prompt import (
    get_sot_template,
    get_sot_gsm8k_template,
    get_sot_CLUTRR_template,
    get_sot_sport_template,
    get_sot_strangeqa_template,
    get_sot_data_template,
    get_sot_ASDiv_template,
    get_sot_mmlu_template,
    get_sot_AQUA_template,
    get_sot_bbh_template,
    get_sot_SVAMP_template
)
import json
import re
from langchain.prompts import ChatPromptTemplate
from config.settings import settings
from log.logger_utils import Logger

logger = Logger().get_logger()


def modify_sot_template(template):
    try:
        # 解析模板为字典
        template_dict = json.loads(template)

        # 直接将所有单大括号替换为双大括号
        modified_template_str = json.dumps(template_dict, indent=4).replace('{', '{{').replace('}', '}}')

        # 用正则匹配替换 {{problem}} 和 {{betti_number}} 为 {problem} 和 {betti_number}
        final_template_str = re.sub(r'{{problem}}', '{problem}', modified_template_str)
        final_template_str = re.sub(r'{{betti_number}}', '{betti_number}', final_template_str)

        # 创建 ChatPromptTemplate 对象
        template_obj = ChatPromptTemplate.from_template(final_template_str)
        return template_obj

    except json.JSONDecodeError:
        logger.error("Failed to parse the template as JSON.")
        return None


class PromptTemplateFactory(PromptTemplateFactoryInterface):
    def __init__(self):
        self.sot_dataset_mapping = settings.PROMPT_TEMPLATE_MAPPING

    def get_prompt_template(self, method: str, dataset_type: str, betti_number: int, solution_number: int):
        if method == 'sot':
            template_path = self.sot_dataset_mapping.get(dataset_type)
            if template_path:
                parts = template_path.split('.')
                module_name = '.'.join(parts[:-1])
                function_name = parts[-1]
                module = __import__(module_name, fromlist=[function_name])
                template_func = getattr(module, function_name)
                template = template_func(betti_number, solution_number)
                logger.info(f"Got SOT template for {dataset_type} before modification:\n{template}")
                return modify_sot_template(template)
            else:
                template = get_sot_template(betti_number, solution_number)
                logger.info(f"Got general SOT template before modification:\n{template}")
                return modify_sot_template(template)
        else:
            logger.error(f"Unsupported method type, unable to get the prompt template: {method}")
            return None


class PromptTemplateFactory(PromptTemplateFactoryInterface):
    def __init__(self):
        self.sot_dataset_mapping = settings.PROMPT_TEMPLATE_MAPPING

    def get_prompt_template(self, method: str, dataset_type: str, betti_number: int, solution_number: int):
        if method == 'sot':
            template_path = self.sot_dataset_mapping.get(dataset_type)
            if template_path:
                parts = template_path.split('.')
                module_name = '.'.join(parts[:-1])
                function_name = parts[-1]
                module = __import__(module_name, fromlist=[function_name])
                template_func = getattr(module, function_name)
                template = template_func(betti_number, solution_number)
                logger.info(f"Got SOT template for {dataset_type} before modification:\n{template}")
                return modify_sot_template(template)
            else:
                template = get_sot_template(betti_number, solution_number)
                logger.info(f"Got general SOT template before modification:\n{template}")
                return modify_sot_template(template)
        else:
            logger.error(f"Unsupported method type, unable to get the prompt template: {method}")
            return None


class PromptTemplateFactory(PromptTemplateFactoryInterface):
    def __init__(self):
        self.sot_dataset_mapping = settings.PROMPT_TEMPLATE_MAPPING

    def get_prompt_template(self, method: str, dataset_type: str, betti_number: int, solution_number: int):
        if method == 'sot':
            template_path = self.sot_dataset_mapping.get(dataset_type)
            if template_path:
                parts = template_path.split('.')
                module_name = '.'.join(parts[:-1])
                function_name = parts[-1]
                module = __import__(module_name, fromlist=[function_name])
                template_func = getattr(module, function_name)
                template = template_func(betti_number, solution_number)
                logger.info(f"Got SOT template for {dataset_type} before modification:\n{template}")
                return modify_sot_template(template)
            else:
                template = get_sot_template(betti_number, solution_number)
                logger.info(f"Got general SOT template before modification:\n{template}")
                return modify_sot_template(template)
        else:
            logger.error(f"Unsupported method type, unable to get the prompt template: {method}")
            return None