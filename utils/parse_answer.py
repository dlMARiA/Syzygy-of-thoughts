import re
import json
from utils.parse_factory import AQUAParser  # 导入 AQUAParser 类

def clean_number_string(num_str):
    # 移除所有非数字、非符号、非小数点、非逗号、非#字符
    cleaned = re.sub(r'[^0-9eE\+\-\.,%#]', '', num_str.strip())
    return cleaned

def convert_to_standard(num_str):
    try:
        num_str = num_str.strip()
        # 处理空字符串
        if not num_str:
            return "0"
        # 处理科学计数法
        if 'e' in num_str.lower():
            num = float(num_str)
            return str(int(num)) if num.is_integer() else str(num)
        # 处理整数/浮点
        return str(int(float(num_str))) if '.' in num_str and float(num_str).is_integer() else num_str
    except:
        return "0"

def parse_llm_answer(filled_template):
    """
    解析LLM返回的模板，提取答案
    :param filled_template: LLM填充后的模板
    :return: 解析后的答案
    """
    try:
        # 基础清理
        filled_template = filled_template.replace("```json", "").replace("```", "").strip()
        filled_template = re.sub(r'\s+', ' ', filled_template)
        filled_template = re.sub(r'\\([^\\])', r'\\\\\1', filled_template)

        # 尝试使用正则表达式提取 final_answer
        match = re.search(r'"final_answer": "([^"]*)"', filled_template)
        if match:
            final_answer = match.group(1).strip()
        else:
            # 解析 JSON
            try:
                response = json.loads(filled_template)
                final_answer = str(response.get("final_answer", "")).strip()
            except json.JSONDecodeError as e:
                print(f"JSON 解析错误: {e}, 原始答案: {filled_template[:100]}...")
                return "0"

        # 合并日期匹配规则
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

        # 原有数字提取逻辑
        patterns = [
            r'\[([+-]?\d+\.?\d*)\]',
            r'([+-]?\d+\.?\d*)'
        ]
        for pattern in patterns:
            match = re.search(pattern, final_answer)
            if match:
                num_str = match.group(1).replace(',', '')
                return convert_to_standard(num_str)

        # 新增关系类答案提取分支
        relation_match = re.search(r'([a-zA-Z-]+)', final_answer)
        if relation_match:
            return relation_match.group(1)

        # 暴力提取所有数字
        cleaned = re.sub(r'[^0-9]', '', final_answer)
        return convert_to_standard(cleaned)
    except Exception as e:
        print(f"Error: {e}, Raw Answer: {filled_template[:100]}...")
        return "0"

def parse_clutrr_answer(raw_answer):
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
    match = re.search(r'####\s*(\d+)', raw_answer)
    if match:
        return match.group(1)
    num_str = clean_number_string(raw_answer)
    return convert_to_standard(num_str)

def parse_math_answer(raw_answer):
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
    # 统一转换为大写进行匹配
    dataset_type = dataset_type.upper()
    for key in dataset_parsers.keys():
        if key.upper() == dataset_type:
            return dataset_parsers[key](raw_answer)
    print(f"Unsupported dataset type for answer parsing: {dataset_type}")
    return raw_answer

def parse_aqua_jsonl(file_path):
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