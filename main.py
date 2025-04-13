from utils.runner import Runner
from utils.get_prompt_template import PromptTemplateFactory
from utils.dataloader import DatasetLoader
from log.logger_utils import Logger

logger = Logger().get_logger()

if __name__ == "__main__":
    try:
        logger.info("Starting the test...")
        prompt_factory = PromptTemplateFactory()
        dataset_loader = DatasetLoader()
        runner = Runner(prompt_factory, dataset_loader)
        runner.run()
        logger.info("Test completed.")
    except Exception as e:
        logger.error(f"Program terminated abnormally: {str(e)}")
        exit(1)