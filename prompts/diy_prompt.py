from config.diy_settings import settings
class DIYTemplate:
    def __init__(self, betti_number, solution_number):
        self.tip = f'"tip1": "{settings.TIP}"'
        self.default_tip = f'"tip2": "{settings.DEFAULT_TIP}"'
        self.module = '"module": "{problem}"'
        self.final_answer_format = ""

    def get_template(self):
        """
        Generates a formatted template string containing various components.

        Returns:
            str: The formatted string template including the specified attributes.
        """
        template = f"""
        {{
            {self.tip},
            {self.default_tip},
            {self.module},
            "final_answer": "{self.final_answer_format}"
        }}
        """
        return template


class SOTGeneralTemplate(DIYTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [Pure Number]>"


class SOTAQUATemplate(DIYTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [option]e.g., A,B,C,D>"


class SOTBBHTemplate(DIYTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [option]e.g., A,B,C,D>"


class SOTDataTemplate(DIYTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [standard answer],such as[05/31/2021]>"


class SOTCLUTRRTemplate(DIYTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [relationship]e.g., grandson, father, brother>"


class SOTSportTemplate(DIYTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [Pure Number]>"


class SOTStrangeQATemplate(DIYTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [Pure Number]>"


class SOTGSM8KTemplate(DIYTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [Pure Number]>"


class SOTASDivTemplate(DIYTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [Pure Number]>"


class SOTMMLUTemplate(DIYTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [option]e.g., A,B,C,D>"


class SOTSVAMPTemplate(DIYTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [Pure Number]>"


def get_sot_diy_template(betti_number, solution_number):
    return SOTGeneralTemplate(betti_number, solution_number).get_template()


def get_sot_gsm8k_diy_template(betti_number, solution_number):
    return SOTGSM8KTemplate(betti_number, solution_number).get_template()


def get_sot_CLUTRR_diy_template(betti_number, solution_number):
    return SOTCLUTRRTemplate(betti_number, solution_number).get_template()


def get_sot_sport_diy_template(betti_number, solution_number):
    return SOTSportTemplate(betti_number, solution_number).get_template()


def get_sot_strangeqa_diy_template(betti_number, solution_number):
    return SOTStrangeQATemplate(betti_number, solution_number).get_template()


def get_sot_data_diy_template(betti_number, solution_number):
    return SOTDataTemplate(betti_number, solution_number).get_template()


def get_sot_ASDiv_diy_template(betti_number, solution_number):
    return SOTASDivTemplate(betti_number, solution_number).get_template()


def get_sot_mmlu_diy_template(betti_number, solution_number):
    return SOTMMLUTemplate(betti_number, solution_number).get_template()


def get_sot_AQUA_diy_template(betti_number, solution_number):
    return SOTAQUATemplate(betti_number, solution_number).get_template()


def get_sot_bbh_diy_template(betti_number, solution_number):
    return SOTBBHTemplate(betti_number, solution_number).get_template()


def get_sot_SVAMP_diy_template(betti_number, solution_number):
    return SOTSVAMPTemplate(betti_number, solution_number).get_template()