import json


class Questionnaire:
    def __init__(self, filename):
        self.questions = None
        self.current_question = None
        try:
            with open(filename, "r") as f:
                self.questions = iter(json.load(f))
        except:
            pass

    def next(self):
        if self.questions:
            try:
                self.current_question = next(self.questions)
            except StopIteration:
                self.current_question = None
        return self.current_question

    @property
    def question(self):
        return self.current_question.get('question', '') if self.current_question else None

    @property
    def choices(self):
        return self.current_question.get('choices', []) if self.current_question else None

    @property
    def answer(self):
        return self.current_question.get('answer', 0) if self.current_question else None


if __name__ == "__main__":
    questionnaire = Questionnaire('questions.json')
    while questionnaire.next():
        print(questionnaire.question)
        print('\n'.join([f'\t{idx+1}. {choice}' for idx,
                        choice in enumerate(questionnaire.choices)]))
        # print(questionnaire.answer)
