class SOTTemplate:
    def __init__(self, betti_number, solution_number):
        self.tip = '"tip": "!! You must answer in JSON format!!"'
        self.module = '"module": "{problem}"'
        self.betti_numbers = '"betti_numbers": "{betti_number}"'
        self.auxiliary_condition = '"Describe auxiliary conditions added to solve the problem"'
        self.free_conditions_base = {
            f'"condition{i}"': '""' for i in range(1, betti_number + 1)
        }
        self.explanation = '"<Generate multiple solution processes step by step using auxiliary conditions. Ensure that each process solves the problem from start to finish.>"'
        self.solutions_base = {
            f'"solution{i}"': '""' for i in range(1, solution_number + 1)
        }
        self.optimality_analysis = '"optimality_analysis": "<Evaluate and examine all the solutions mentioned above, and select the best solution.>"'
        self.optimal_solution = '"optimal_solution": ""'
        self.final_answer_format = ""

    def get_template(self):
        """
        Generates a formatted template string based on the specified conditions, solutions, and analysis
        properties. The template includes details such as the analysis module, Betti numbers, free
        conditions, mappings, minimality analysis, and the final answer format, and structures this
        information in JSON-like formatting.

        Returns:
            str: A formatted string representing the template with all embedded data.
        """
        free_conditions = {
            **{"\"auxiliary_condition\"": self.auxiliary_condition},
            **self.free_conditions_base
        }
        free_conditions_str = ",\n            ".join([f'{k}: {v}' for k, v in free_conditions.items()])

        solutions = {
            **{"\"explanation\"": self.explanation},
            **self.solutions_base
        }
        solutions_str = ",\n            ".join([f'{k}: {v}' for k, v in solutions.items()])

        template = f"""
{{
    {self.tip},
    "analysis": {{
        {self.module},
        {self.betti_numbers},
        "free_conditions": {{
            {free_conditions_str}
        }},
        "mapping": {{
            {solutions_str}
        }},
        "minimality": {{
            {self.optimality_analysis},
            {self.optimal_solution}
        }}
    }},
    "final_answer": "{self.final_answer_format}"
}}
"""
        return template


class SOTGeneralTemplate(SOTTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [Pure Number]>"


class SOTAQUATemplate(SOTTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [option]e.g., A,B,C,D>"


class SOTBBHTemplate(SOTTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [option]e.g., A,B,C,D>"


class SOTDataTemplate(SOTTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [standard answer],such as[05/31/2021]>"


class SOTCLUTRRTemplate(SOTTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [relationship]e.g., grandson, father, brother>"


class SOTSportTemplate(SOTTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [Pure Number]>"


class SOTStrangeQATemplate(SOTTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [Pure Number]>"


class SOTGSM8KTemplate(SOTTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [Pure Number]>"


class SOTASDivTemplate(SOTTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [Pure Number]>"


class SOTMMLUTemplate(SOTTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [option]e.g., A,B,C,D>"


class SOTSVAMPTemplate(SOTTemplate):
    def __init__(self, betti_number, solution_number):
        super().__init__(betti_number, solution_number)
        self.final_answer_format = "<Must use the following format: [Pure Number]>"


def get_sot_template(betti_number, solution_number):
    return SOTGeneralTemplate(betti_number, solution_number).get_template()


def get_sot_gsm8k_template(betti_number, solution_number):
    return SOTGSM8KTemplate(betti_number, solution_number).get_template()


def get_sot_CLUTRR_template(betti_number, solution_number):
    return SOTCLUTRRTemplate(betti_number, solution_number).get_template()


def get_sot_sport_template(betti_number, solution_number):
    return SOTSportTemplate(betti_number, solution_number).get_template()


def get_sot_strangeqa_template(betti_number, solution_number):
    return SOTStrangeQATemplate(betti_number, solution_number).get_template()


def get_sot_data_template(betti_number, solution_number):
    return SOTDataTemplate(betti_number, solution_number).get_template()


def get_sot_ASDiv_template(betti_number, solution_number):
    return SOTASDivTemplate(betti_number, solution_number).get_template()


def get_sot_mmlu_template(betti_number, solution_number):
    return SOTMMLUTemplate(betti_number, solution_number).get_template()


def get_sot_AQUA_template(betti_number, solution_number):
    return SOTAQUATemplate(betti_number, solution_number).get_template()


def get_sot_bbh_template(betti_number, solution_number):
    return SOTBBHTemplate(betti_number, solution_number).get_template()


def get_sot_SVAMP_template(betti_number, solution_number):
    return SOTSVAMPTemplate(betti_number, solution_number).get_template()