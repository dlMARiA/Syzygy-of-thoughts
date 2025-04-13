from config.settings import settings
from models.openai_client import initialize_llm
from interfaces import PromptTemplateFactoryInterface, DatasetLoaderInterface
from utils.parse_answer import parse_llm_answer, parse_dataset_answer
from utils.answer_validator import validate_response
from log.logger_utils import Logger

logger = Logger().get_logger()


class Runner:
    def __init__(self, prompt_factory: PromptTemplateFactoryInterface, dataset_loader: DatasetLoaderInterface):
        self.prompt_factory = prompt_factory
        self.dataset_loader = dataset_loader

    def run(self, dataset_path: str = settings.RUNNER_DEFAULT_DATASET,
            dataset_type: str = settings.RUNNER_DEFAULT_DATASET_TYPE,
            method: str = settings.RUNNER_DEFAULT_METHOD,
            betti_number: int = settings.RUNNER_DEFAULT_BETTI_NUMBER,
            solution_number: int = settings.RUNNER_DEFAULT_SOLUTION_NUMBER,
            temperature: float = settings.TEMPERATURE):
        settings.set_temperature(temperature)
        # 打印当前温度
        logger.info(f"Current temperature: {settings.TEMPERATURE}")

        # Initialize the model
        llm = initialize_llm()

        # 构建链式调用
        prompt_template = self.prompt_factory.get_prompt_template(method, dataset_type, betti_number, solution_number)
        if prompt_template is None:
            return
        chain = prompt_template | llm

        # Load the dataset
        dataset = self.dataset_loader.load_dataset(dataset_path, dataset_type)
        total = len(dataset)
        correct = 0
        wrong_question_numbers = []

        if total == 0:
            logger.error("Failed to load the dataset. No available questions for testing.")
            return

        for idx, item in enumerate(dataset, 1):
            try:
                input_dict = {
                    "problem": item["problem"],
                    "betti_number": betti_number,
                }
                if dataset_type == 'AQUA':
                    input_dict["options"] = item["options"]

                # 手动填充模板并打印填充后的消息
                filled_message = prompt_template.format_messages(**input_dict)[0].content
                logger.info(f"Message filled with input data for question {idx}/{total}:\n{filled_message}")

                # 使用链式调用获取响应
                response = chain.invoke(input_dict)
                filled_template = response.content

                logger.info(f"Message sent to the LLM for question {idx}/{total}: {input_dict}")
                logger.info(f"Template filled by the LLM for question {idx}/{total}: {filled_template}")

                # Extract the answer calculated by the LLM
                predicted_answer = parse_llm_answer(filled_template)

                # Get the true answer
                true_answer = parse_dataset_answer(item["solution"], dataset_type=dataset_type)

                # Validate the answer
                is_correct = validate_response(filled_template, item["solution"], dataset_type)
                if is_correct:
                    correct += 1
                else:
                    wrong_question_numbers.append(idx)
                logger.info(f"Calculation result of the LLM for question {idx}/{total}: {predicted_answer}, True answer: {true_answer}, Validation result: {'Correct' if is_correct else 'Wrong'}")

            except Exception as e:
                logger.error(f"Processing failed: {str(e)}")
                continue

        # Generate the test report
        logger.info("\n=== Test Report ===")
        logger.info(f"Total number of questions: {total}")
        logger.info(f"Number of correct answers: {correct}")
        if total > 0:
            logger.info(f"Accuracy rate: {correct / total:.2%}")
        else:
            logger.info("Accuracy rate: N/A (The dataset is empty)")
        logger.info(f"Numbers of questions with wrong answers: {wrong_question_numbers}")