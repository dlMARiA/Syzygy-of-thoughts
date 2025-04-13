from interfaces import AnswerParserInterface


class GPQAParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现GPQA数据集答案解析逻辑
        return raw_answer


class MathParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现数学数据集答案解析逻辑
        return raw_answer


class GSM8KParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现GSM8K数据集答案解析逻辑
        return raw_answer


class OBParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现OB数据集答案解析逻辑
        return raw_answer


class CLUTRRParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现CLUTRR数据集答案解析逻辑
        return raw_answer


class BBHParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现BBH数据集答案解析逻辑
        return raw_answer


class MMLUParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现MMLU数据集答案解析逻辑
        return raw_answer


class SVAMPParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现SVAMP数据集答案解析逻辑
        return raw_answer


class AQUAParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现AQUA数据集答案解析逻辑
        return raw_answer


class MultiArithParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现MultiArith数据集答案解析逻辑
        return raw_answer


class DataParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现数据类数据集答案解析逻辑
        return raw_answer


class SportParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现体育数据集答案解析逻辑
        return raw_answer


class StrangeQAParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现StrangeQA数据集答案解析逻辑
        return raw_answer


class ASDivParser(AnswerParserInterface):
    def parse(self, raw_answer):
        # 实现ASDiv数据集答案解析逻辑
        return raw_answer