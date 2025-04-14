import traceback
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
        try:
            settings.set_temperature(temperature)
            # Print current temperature
            # logger.debug(f"Current temperature: {settings.TEMPERATURE}")

            # Initialize the model
            llm = initialize_llm()

            # Building a chain call
            prompt_template = self.prompt_factory.get_prompt_template(method, dataset_type, betti_number, solution_number)
            if prompt_template is None:
                return
            chain = prompt_template | llm

            try:
                # Load the dataset
                logger.info(f"Attempting to load dataset from {dataset_path} with type {dataset_type}")
                dataset = self.dataset_loader.load_dataset(dataset_path, dataset_type)
                logger.info(f"Successfully loaded {len(dataset)} items from the dataset.")
            except Exception as e:
                logger.error(f"Error loading dataset: {str(e)}\n{traceback.format_exc()}")
                return

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
                    if dataset_type == 'aqua':
                        input_dict["options"] = item["options"]

                    # Manually populate the template and print the populated message
                    filled_message = prompt_template.format_messages(**input_dict)[0].content
                    logger.info(f"Message filled with input data for question {idx}/{total}:\n{filled_message}")

                    # Using chained calls to get responses
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
                    logger.error(f"Error processing question {idx}: {str(e)}\n{traceback.format_exc()}")
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
        except Exception as e:
            logger.error(f"An error occurred during the overall test run: {str(e)}\n{traceback.format_exc()}")