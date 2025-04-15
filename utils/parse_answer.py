import re
import json
from utils.parse_factory import AQUAParser  # Import the AQUAParser class

def clean_number_string(num_str):
    """
    Cleans a given numeric string by removing all characters that are not digits,
    symbols, decimal points, commas, or the hash (#) symbol. The cleaning process
    ensures that only valid numeric-related characters are retained, making the
    string suitable for further processing or validation.

    Args:
        num_str: A string potentially containing a numeric value with various
            characters that need to be filtered.

    Returns:
        A string containing only the retained numeric-related characters after
        the cleaning process.
    """
    # Remove all non-digits, non-symbols, non-decimal points, non-commas, and non-# characters
    cleaned = re.sub(r'[^0-9eE\+\-\.,%#]', '', num_str.strip())
    return cleaned

def convert_to_standard(num_str):
    """
    Converts a numeric string to its standard representation. The function processes strings
    that may contain numbers in scientific notation, integers, or floating-point formats. It
    also handles empty strings and invalid inputs gracefully, returning "0" in such cases.

    Args:
        num_str (str): The numeric string to be converted to its standard representation.

    Returns:
        str: The converted standard representation of the numeric string. Returns "0" for
        empty or invalid inputs.
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

def parse_llm_answer(filled_template):
    """
    Parses the LLM-generated answer from a filled template string to extract the desired
    information such as dates, numbers, or other patterns.

    Args:
        filled_template (str): The template string containing the LLM answer to parse.

    Returns:
        str: A formatted string representing the extracted answer, based on the detected
        patterns in the input. Defaults to "0" if unable to process the input correctly.
    """
    try:
        # Basic cleaning
        filled_template = filled_template.replace("```json", "").replace("```", "").strip()
        filled_template = re.sub(r'\s+', ' ', filled_template)
        filled_template = re.sub(r'\\([^\\])', r'\\\\\1', filled_template)

        # Try using regular expression to extract final_answer
        match = re.search(r'"final_answer": "([^"]*)"', filled_template)
        if match:
            final_answer = match.group(1).strip()
        else:
            # Parse JSON
            try:
                response = json.loads(filled_template)
                final_answer = str(response.get("final_answer", "")).strip()
            except json.JSONDecodeError as e:
                print(f"JSON 解析错误: {e}, 原始答案: {filled_template[:100]}...")
                return "0"

        # Merge date matching rules
        date_patterns = [
            r'(\d{2})/(\d{2})/(\d{4})',
            r'\[(\d{2}/\d{2}/\d{4})\]',
            r'(\d{4})-(\d{2})-(\d{2})'
        ]
        for pattern in date_patterns:
            date_match = re.match(pattern, final_answer)
            if date_match:
                if pattern == r'(\d{2})/(\d{2})/(\d{4})':
                    month = date_match.group(1)
                    day = date_match.group(2)
                    year = date_match.group(3)
                    return f"{month}{day}{year}"
                elif pattern == r'\[(\d{2}/\d{2}/\d{4})\]':
                    date_str = date_match.group(1)
                    parts = date_str.split('/')
                    if len(parts) == 3:
                        return f"{parts[0]}{parts[1]}{parts[2]}"
                    else:
                        return ''.join(re.findall(r'\d+', date_str))
                elif pattern == r'(\d{4})-(\d{2})-(\d{2})':
                    year = date_match.group(1)
                    month = date_match.group(2)
                    day = date_match.group(3)
                    return f"{month}{day}{year}"

        # Original digital extraction logic
        patterns = [
            r'\[([+-]?\d+\.?\d*)\]',
            r'([+-]?\d+\.?\d*)'
        ]
        for pattern in patterns:
            match = re.search(pattern, final_answer)
            if match:
                num_str = match.group(1).replace(',', '')
                return convert_to_standard(num_str)

        # Added a new branch for relationship-based answer extraction
        relation_match = re.search(r'([a-zA-Z-]+)', final_answer)
        if relation_match:
            return relation_match.group(1)

        # Brute force extraction of all numbers
        cleaned = re.sub(r'[^0-9]', '', final_answer)
        return convert_to_standard(cleaned)
    except Exception as e:
        print(f"Error: {e}, Raw Answer: {filled_template[:100]}...")
        return "0"

def parse_clutrr_answer(raw_answer):
    """
    Parses the provided raw answer string, extracting the first occurrence 
    of an alphabetic sequence. Supports specific formatting with delimiter 
    and fallback for directly extracting sequences.

    Args:
        raw_answer: str
            The raw input string, potentially containing a formatted answer 
            with a '####' delimiter or alphabetic sequences to be parsed.

    Returns:
        str: The extracted alphabetic sequence if found, otherwise returns 
        the raw input string unchanged.
    """
    parts = raw_answer.split('####')
    if len(parts) > 1:
        answer_str = parts[1].strip()
        match = re.search(r'([a-zA-Z-]+)', answer_str)
        if match:
            return match.group(1)
    match = re.search(r'([a-zA-Z-]+)', raw_answer)
    if match:
        return match.group(1)
    else:
        return raw_answer

def parse_gsm8k_answer(raw_answer):
    """
    Parses an answer from the GSM8K dataset format. This function extracts a properly formatted
    answer from the input string using specified patterns. It checks for exact matches based on 
    a regex pattern and provides a fallback mechanism to clean and convert the raw input.

    Args:
        raw_answer (str): The raw input string containing the answer to be extracted and processed.

    Returns:
        str: A formatted and standardized answer string. If no exact match is found via the 
        regex pattern, the function attempts to clean and standardize the input.
    """
    match = re.search(r'####\s*(\d+)', raw_answer)
    if match:
        return match.group(1)
    num_str = clean_number_string(raw_answer)
    return convert_to_standard(num_str)

def parse_math_answer(raw_answer):
    """
    Parses a given raw mathematics answer for a numerical value enclosed in a LaTeX \boxed{}
    expression and converts it to a standard numerical format.

    The function attempts to locate and extract a number enclosed in a \boxed{} LaTeX expression.
    If no such expression is found in the input, it falls back on cleaning and parsing the raw
    input as a numerical string. Once extracted, the numerical string is converted and returned
    in a standard numerical format.

    Args:
        raw_answer (str): A string representation of a raw answer, which may include LaTeX \boxed{}
            notations or a numerical representation.

    Returns:
        float: The numerical value extracted and converted from the raw answer.
    """
    match = re.search(r'\\boxed{([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)', raw_answer)
    if match:
        num_str = match.group(1)
    else:
        num_str = clean_number_string(raw_answer)
    return convert_to_standard(num_str)

dataset_parsers = {
    'CLUTRR': parse_clutrr_answer,
    'bbh': lambda x: x.strip(),
    'mmlu': lambda x: re.search(r'([A-E])', x).group(1) if re.search(r'([A-E])', x) else "0",
    'SVAMP': lambda x: convert_to_standard(clean_number_string(x)),
    'AQUA': lambda x: AQUAParser().parse(x),
    'MultiArith': lambda x: convert_to_standard(clean_number_string(x)),
    'date': lambda x: convert_to_standard(clean_number_string(x)),
    'ASDiv': lambda x: convert_to_standard(clean_number_string(x)),
    'gsm8k': parse_gsm8k_answer,
    'math': parse_math_answer
}

def parse_dataset_answer(raw_answer, dataset_type):
    """
    Parses the raw dataset answer based on the provided dataset type. The function
    utilizes a dictionary of dataset parsers to dynamically invoke the appropriate
    parser function based on the case-insensitive match to the dataset type. If no
    matching parser is found, the raw answer is returned, and a message is printed
    indicating the unsupported dataset type.

    Args:
        raw_answer: The raw answer data to be parsed.
        dataset_type: The type of the dataset as a string. It determines which
            parser function to invoke.

    Returns:
        The parsed answer if a matching parser is found; otherwise, the raw answer
        is returned unchanged.
    """
    # Convert to uppercase for matching
    dataset_type = dataset_type.upper()
    for key in dataset_parsers.keys():
        if key.upper() == dataset_type:
            return dataset_parsers[key](raw_answer)
    print(f"Unsupported dataset type for answer parsing: {dataset_type}")
    return raw_answer

def parse_aqua_jsonl(file_path):
    """
    Parses a JSONL file containing AQUA dataset answers, processes each line to extract the final answer, and
    converts raw answers into the desired format.

    Args:
        file_path (str): Path to the JSONL file containing AQUA dataset answers.

    Returns:
        list: A list containing parsed answers, where each answer is processed into the required format.

    Raises:
        FileNotFoundError: If the specified file path does not exist or cannot be opened.
        json.JSONDecodeError: If a line in the file is not a valid JSON object.
    """
    parsed_answers = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data = json.loads(line)
                raw_answer = json.dumps({"final_answer": data.get('answer')})
                parsed_answer = parse_dataset_answer(raw_answer, 'AQUA')
                parsed_answers.append(parsed_answer)
            except json.JSONDecodeError:
                print(f"Error decoding JSON line: {line[:100]}...")
    return parsed_answers