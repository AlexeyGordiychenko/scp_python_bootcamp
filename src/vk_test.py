from questionnaire import Questionnaire
from measurements import Measurements
from user_input import user_input

COLOR_GREEN = '\033[33m'
COLOR_RESET = '\033[0m'


class VKTest():
    def __init__(self, filename):
        self.questionnaire = Questionnaire(filename)
        self.measurements = Measurements()
        self.answers = []

    def run(self):
        while self.questionnaire.next():
            if self.questionnaire.choices and self.questionnaire.answer:
                print(f'{COLOR_GREEN}{self.questionnaire.question}{COLOR_RESET}')
                print('\n'.join([f'\t{idx+1}. {choice}' for idx,
                                choice in enumerate(self.questionnaire.choices)]))
                self.answers.append(1 if user_input(
                    "Answer", 1, len(self.questionnaire.choices)) == int(self.questionnaire.answer) else 0)
                self.measurements.measure()

        return len(self.answers) > 0

    def result(self):
        if self.questionnaire.questions is None:
            return
        if sum(self.answers)/len(self.answers) > 0.8\
                and min(self.measurements.respiration) - max(self.measurements.respiration) <= 2\
                and min(self.measurements.heart_rate) - max(self.measurements.heart_rate) <= 20\
                and min(self.measurements.blushing_level) - max(self.measurements.blushing_level) <= 2\
                and min(self.measurements.pupillary_dilation) - max(self.measurements.pupillary_dilation) <= 2:
            return 'replicant'
        return 'human'
