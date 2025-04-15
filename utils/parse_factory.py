from interfaces import AnswerParserInterface
import re
import json

def clean_number_string(num_str):
    """
    Removes all non-digit, non-symbol, non-decimal point, non-comma, and non-'#'
    characters from the given string.
    Args:
        num_str (str): The input string containing numeric or mixed characters
            to be cleaned.
    Returns:
        str: A string that contains only the allowed characters after cleaning.
    """
    # Remove all non-digits, non-symbols, non-decimal points, non-commas, and non-# characters
    cleaned = re.sub(r'[^0-9eE\+\-\.,%#]', '', num_str.strip())
    return cleaned

def convert_to_standard(num_str):
    """
    Converts a numerical string into a standardized string representation.
    Args:
        num_str: The input numerical string to be converted.
    Returns:
        A standardized string representation of the input number.
    """
    try:
        num_str = num_str.strip()
        # Handling empty strings
        if not num_str:
            return "0"
        # Handling scientific notation
        if 'e' in num_str.lower():
            num = float(num_str)
            return str(int(num)) if num.is_integer() else str(num)
        # Handling integers/floating points
        return str(int(float(num_str))) if '.' in num_str and float(num_str).is_integer() else num_str
    except:
        return "0"

class AQUAParser(AnswerParserInterface):
    """
    Parses and processes raw answer strings to extract meaningful answers in specific formats.
    Methods:
        parse(raw_answer): Extracts a meaningful and standardized answer from the raw answer
            string input.
    """
    def parse(self, raw_answer):
        """
        Parses the input string to extract a meaningful answer based on certain rules and formats.
        Args:
            raw_answer (str): The raw input string to be parsed and processed.
        Returns:
            str or None: Returns the extracted answer if parsing succeeds based on
            the implemented rules. Returns None if no valid answer is found.
        """
        try:
            # Try parsing the original answer as JSON
            data = json.loads(raw_answer)
            # Extract the answer field directly from the JSON data
            answer = data.get('answer')
            if answer and isinstance(answer, str) and answer in 'ABCDE':
                return answer
        except json.JSONDecodeError:
            pass

        # Added new logic, modeled after the CLUTRR dataset parsing logic
        parts = raw_answer.split('####')
        if len(parts) > 1:
            answer_str = parts[1].strip()
            match = re.search(r'([a-zA-Z-]+)', answer_str)
            if match:
                return match.group(1)
        # If there is no #### separator, the original logic is used.
        match = re.search(r'([a-zA-Z-]+)', raw_answer)
        if match:
            return match.group(1)
        # Process numbers according to original logic
        num_str = clean_number_string(raw_answer)
        return convert_to_standard(num_str)


class MathParser(AnswerParserInterface):
    def parse(self, raw_answer):
        """
        Parses a raw_answer string to extract a numerical value.
        Args:
            raw_answer: The raw input string potentially containing a boxed number or a
                numerical value.
        Returns:
            The numerical value extracted from the raw_answer string and converted to a
            standard format.
        """
        match = re.search(r'\\boxed{([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)', raw_answer)
        if match:
            num_str = match.group(1)
        else:
            num_str = clean_number_string(raw_answer)
        return convert_to_standard(num_str)


class GSM8KParser(AnswerParserInterface):
    def parse(self, raw_answer):
        """
        Parses the input raw answer and extracts a numerical representation.
        Args:
            raw_answer (str): The raw text input potentially containing a number
                pattern or textual representation of a number.
        Returns:
            str: The extracted or converted number as a string.
        """
        match = re.search(r'####\s*(\d+)', raw_answer)
        if match:
            return match.group(1)
        num_str = clean_number_string(raw_answer)
        return convert_to_standard(num_str)


class OBParser(AnswerParserInterface):
    def parse(self, raw_answer):
        """
        Parses and processes a raw answer to clean and convert it to a standard format.
        Args:
            raw_answer: The raw input that needs to be processed and converted. It
                should be provided as a string-compatible format.
        Returs:
            The standardized and converted value based on the processed input.
        """
        num_str = clean_number_string(str(raw_answer))
        return convert_to_standard(num_str)


class CLUTRRParser(AnswerParserInterface):
    def parse(self, raw_answer):
        """
        Processes the CLUTRR dataset's answers and extracts the key relational
        answer detail behind the '####' separator or through raw parsing.
        Args:
            raw_answer (str): The raw answer string, which may or may not contain
                the '####' separator for added detail.
        Returns:
            str: The extracted relevant relational answer, either from the portion
            after the '####' symbol or as directly parsed from the raw answer.
        """
        # Process the CLUTRR dataset and extract the relational answers behind ####
        parts = raw_answer.split('####')
        if len(parts) > 1:
            answer_str = parts[1].strip()
            match = re.search(r'([a-zA-Z-]+)', answer_str)
            if match:
                return match.group(1)
        # If there is no #### separator, the original logic is used.
        match = re.search(r'([a-zA-Z-]+)', raw_answer)
        if match:
            return match.group(1)
        else:
            return raw_answer


class BBHParser(AnswerParserInterface):
    def parse(self, raw_answer):
        return raw_answer.strip()


class MMLUParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # Extract the letter options from the answer
        match = re.search(r'([A-E])', raw_answer)
        if match:
            return match.group(1)
        return "0"

class SVAMPParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # Implement the answer parsing logic for the SVAMP dataset
        num_str = clean_number_string(raw_answer)
        return convert_to_standard(num_str)


class MultiArithParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # Implementing the answer parsing logic for the MultiArith dataset
        num_str = clean_number_string(raw_answer)
        return convert_to_standard(num_str)


class DataParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # Implement the answer parsing logic for data class datasets
        num_str = clean_number_string(raw_answer)
        return convert_to_standard(num_str)


class SportParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # Implementing sports data set answer parsing logic
        num_str = clean_number_string(raw_answer)
        return convert_to_standard(num_str)


class StrangeQAParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # Implementing the answer parsing logic for the StrangeQA dataset
        num_str = clean_number_string(raw_answer)
        return convert_to_standard(num_str)


class ASDivParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # Implement the ASDiv dataset answer parsing logic
        num_str = clean_number_string(raw_answer)
        return convert_to_standard(num_str)