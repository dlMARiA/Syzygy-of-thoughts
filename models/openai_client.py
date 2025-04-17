from langchain_openai import ChatOpenAI
from config.sot_settings import settings as sot_settings
from config.diy_settings import settings as diy_settings
from log.logger_utils import Logger
from utils.arg_parser import parse_arguments

logger = Logger().get_logger()


def initialize_llm():
    """
    Initialize and return a configured OpenAI language model client.

    Returns:
    - ChatOpenAI: A configured instance of the language model.

    Error Handling:
    - Catch all initialization exceptions and convert them into meaningful error messages.
    - Ensure the presence of the API key is verified.
    """
    args = parse_arguments()
    if args.prompt_type == 'diy':
        settings = diy_settings
    elif args.prompt_type == 'sot':
        settings = sot_settings
    else:
        raise ValueError(f"Invalid input: {args.prompt_type} (expected 'diy' or 'sot')")

    # Verify if the API key exists
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the configuration.")

    try:
        # Dynamically set max_tokens
        max_tokens = settings.MAX_TOKENS

        return ChatOpenAI(
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE if settings.TEMPERATURE is not None else 0,
            max_tokens=max_tokens,
            timeout=None,
            max_retries=settings.MAX_RETRIES,
            openai_api_key=settings.OPENAI_API_KEY,
            base_url=settings.BASE_URL
        )
    except ValueError as ve:
        # Handle value errors, such as invalid parameters
        logger.error(f"Invalid parameter for ChatOpenAI: {str(ve)}")
        raise ValueError(f"Invalid parameter for ChatOpenAI: {str(ve)}") from ve
    except Exception as e:
        # Handle other exceptions
        logger.error(f"Failed to initialize LLM: {str(e)}")
        raise RuntimeError(f"Failed to initialize LLM: {str(e)}") from e