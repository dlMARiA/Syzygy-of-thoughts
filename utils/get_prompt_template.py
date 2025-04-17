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
from prompts.diy_prompt import (
    get_sot_diy_template,
    get_sot_gsm8k_diy_template,
    get_sot_CLUTRR_diy_template,
    get_sot_sport_diy_template,
    get_sot_strangeqa_diy_template,
    get_sot_data_diy_template,
    get_sot_ASDiv_diy_template,
    get_sot_mmlu_diy_template,
    get_sot_AQUA_diy_template,
    get_sot_bbh_diy_template,
    get_sot_SVAMP_diy_template
)
import json
import re
from utils.arg_parser import parse_arguments
from langchain.prompts import ChatPromptTemplate
from config.sot_settings import settings as sot_settings
from config.diy_settings import settings as diy_settings
from log.logger_utils import Logger

logger = Logger().get_logger()


def modify_sot_template(template):
    """
    Modifies a given template string by converting JSON placeholders and formatting it
    to be compatible with a specific prompt template structure.

    The function takes a JSON-like string as input, converts it into a structured dictionary,
    adjusts the formatting of placeholders, and then transforms it into a ChatPromptTemplate object.

    Args:
        template (str): A JSON-like string representing the template to modify.

    Returns:
        ChatPromptTemplate or None: Returns a ChatPromptTemplate object with the modified
        template if successful. If the template cannot be parsed as JSON, the function
        returns None.
    """
    try:
        # Parse template as dictionary
        template_dict = json.loads(template)

        # Simply replace all single curly braces with double curly braces
        modified_template_str = json.dumps(template_dict, indent=4).replace('{', '{{').replace('}', '}}')

        # Replace {{problem}} and {{betti_number}} with {problem} and {betti_number} using regular expression matching
        final_template_str = re.sub(r'{{problem}}', '{problem}', modified_template_str)
        final_template_str = re.sub(r'{{betti_number}}', '{betti_number}', final_template_str)

        # Create a ChatPromptTemplate object
        template_obj = ChatPromptTemplate.from_template(final_template_str)
        return template_obj

    except json.JSONDecodeError:
        # logger.error("Failed to parse the template as JSON.")
        return None

def modify_diy_template(template):
    """
    Modifies a DIY template string to conform to the expected format for a ChatPromptTemplate
    object by replacing specific characters and patterns.

    Args:
        template (str): A string containing the original DIY template to modify.

    Returns:
        ChatPromptTemplate | None: The ChatPromptTemplate object created from the modified
            template string. Returns None if the modified template cannot be parsed.
    """
    try:
        modified_template_str = re.sub(r'^(\s*){', r'\1{{', template)
        modified_template_str = re.sub(r'}(\s*)$', r'}}\1', modified_template_str)
        template_obj = ChatPromptTemplate.from_template(modified_template_str)
        return template_obj
    except json.JSONDecodeError:
        # logger.error("Failed to parse the template as JSON.")
        return None


class PromptTemplateFactory(PromptTemplateFactoryInterface):
    """
    Represents a factory for generating prompt templates based on method type, dataset,
    and additional parameters.

    This class is designed to create prompt templates by allowing dynamic imports and
    template fetching based on a defined mapping. Specifically, it handles "sot" method
    type templates and modifies them accordingly before returning. The class also manages
    invalid method types by logging an error and returning a fallback result.

    Attributes:
        sot_dataset_mapping (dict): A mapping configuration defining the relationship
            between dataset types and their corresponding prompt template function paths.
    """
    def __init__(self):
        args = parse_arguments()
        if args.prompt_type == 'diy':
            settings = diy_settings
        elif args.prompt_type == 'sot':
            settings = sot_settings
        else:
            raise ValueError(f"Invalid input: {args.prompt_type} (expected 'diy' or 'sot')")

        self.dataset_mapping = settings.PROMPT_TEMPLATE_MAPPING

    def get_prompt_template(self, method: str, dataset_type: str, betti_number: int, solution_number: int):
        """
        Retrieves and modifies a prompt template based on the specified method, dataset type,
        Betti number, and solution number. The function dynamically imports the template
        generation function based on the dataset type, then applies modifications to the
        retrieved template. Currently, only the 'sot' method type is supported.

        Args:
            method (str): Specifies the method type for generating the template. Only supports 'sot'.
            dataset_type (str): The type of dataset used to determine the template generation method.
            betti_number (int): The Betti number to be used in the template generation.
            solution_number (int): The solution number to be used in the template generation.

        Returns:
            str or None: Modified prompt template if successful, or None if the method type
            is unsupported or an error occurs.
        """
        if method == 'sot':
            template_path = self.dataset_mapping.get(dataset_type)
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

        if method == 'diy':
            template_path = self.dataset_mapping.get(dataset_type)
            if template_path:
                parts = template_path.split('.')
                module_name = '.'.join(parts[:-1])
                function_name = parts[-1]
                module = __import__(module_name, fromlist=[function_name])
                template_func = getattr(module, function_name)
                template = template_func(betti_number, solution_number)
                logger.info(f"Got diy template for {dataset_type} before modification:\n{template}")
                return modify_diy_template(template)
            else:
                template = get_sot_diy_template(betti_number, solution_number)
                logger.info(f"Got general SOT template before modification:\n{template}")
                return modify_diy_template(template)
        else:
            logger.error(f"Unsupported method type, unable to get the prompt template: {method}")
        return None