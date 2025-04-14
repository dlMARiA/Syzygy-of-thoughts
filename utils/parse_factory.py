from interfaces import AnswerParserInterface
import re
import json

def clean_number_string(num_str):
    # Remove all non-digits, non-symbols, non-decimal points, non-commas, and non-# characters
    cleaned = re.sub(r'[^0-9eE\+\-\.,%#]', '', num_str.strip())
    return cleaned

def convert_to_standard(num_str):
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
    def parse(self, raw_answer):
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
        match = re.search(r'\\boxed{([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)', raw_answer)
        if match:
            num_str = match.group(1)
        else:
            num_str = clean_number_string(raw_answer)
        return convert_to_standard(num_str)


class GSM8KParser(AnswerParserInterface):
    def parse(self, raw_answer):
        match = re.search(r'####\s*(\d+)', raw_answer)
        if match:
            return match.group(1)
        num_str = clean_number_string(raw_answer)
        return convert_to_standard(num_str)


class OBParser(AnswerParserInterface):
    def parse(self, raw_answer):
        num_str = clean_number_string(str(raw_answer))
        return convert_to_standard(num_str)


class CLUTRRParser(AnswerParserInterface):
    def parse(self, raw_answer):
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