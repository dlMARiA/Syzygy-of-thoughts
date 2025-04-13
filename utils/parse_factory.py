from interfaces import AnswerParserInterface
import re
import json

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

class AQUAParser(AnswerParserInterface):
    def parse(self, raw_answer):
        try:
            # 尝试将原始答案解析为JSON
            data = json.loads(raw_answer)
            # 直接从JSON数据中提取answer字段
            answer = data.get('answer')
            if answer and isinstance(answer, str) and answer in 'ABCDE':
                return answer
        except json.JSONDecodeError:
            pass

        # 新增逻辑，仿照CLUTRR数据集解析逻辑
        parts = raw_answer.split('####')
        if len(parts) > 1:
            answer_str = parts[1].strip()
            match = re.search(r'([a-zA-Z-]+)', answer_str)
            if match:
                return match.group(1)
        # 如果没有####分隔符，按原逻辑处理
        match = re.search(r'([a-zA-Z-]+)', raw_answer)
        if match:
            return match.group(1)
        # 按原逻辑处理数字
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
        # 处理CLUTRR数据集，提取####后面的关系答案
        parts = raw_answer.split('####')
        if len(parts) > 1:
            answer_str = parts[1].strip()
            match = re.search(r'([a-zA-Z-]+)', answer_str)
            if match:
                return match.group(1)
        # 如果没有####分隔符，按原逻辑处理
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
        # 提取答案中的字母选项
        match = re.search(r'([A-E])', raw_answer)
        if match:
            return match.group(1)
        return "0"

class SVAMPParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现SVAMP数据集答案解析逻辑
        num_str = clean_number_string(raw_answer)
        return convert_to_standard(num_str)


class MultiArithParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现MultiArith数据集答案解析逻辑
        num_str = clean_number_string(raw_answer)
        return convert_to_standard(num_str)


class DataParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现数据类数据集答案解析逻辑
        num_str = clean_number_string(raw_answer)
        return convert_to_standard(num_str)


class SportParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现体育数据集答案解析逻辑
        num_str = clean_number_string(raw_answer)
        return convert_to_standard(num_str)


class StrangeQAParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现StrangeQA数据集答案解析逻辑
        num_str = clean_number_string(raw_answer)
        return convert_to_standard(num_str)


class ASDivParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现ASDiv数据集答案解析逻辑
        num_str = clean_number_string(raw_answer)
        return convert_to_standard(num_str)