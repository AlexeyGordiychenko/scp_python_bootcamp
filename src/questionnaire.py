import json


class Questionnaire:
    """
    The purpose of this class is to parse questions from json file and yield one
    question at the time. A question includes a question, choices, and the
    answer.
    """

    def __init__(self, filename):
        """
        Initializes a new instance of the class with a list of questions parsed
        from json file. Current question is set to None.

        :parameters:
            filename (str): The name of the file to parse.
        """
        self.questions = None
        self.current_question = None
        try:
            with open(filename, "r") as f:
                self.questions = iter(json.load(f))
        except:
            pass

    def next(self):
        """
        Advances to the next question in the list of questions.

        :returns:
            The next question in the list or None if there are no more
            questions.
        """
        if self.questions:
            try:
                self.current_question = next(self.questions)
            except StopIteration:
                self.current_question = None
        return self.current_question

    @property
    def question(self):
        """
        :returns: The current question string.
        """
        return self.current_question.get('question', '') if self.current_question else None

    @property
    def choices(self):
        """
        :returns:
            list: The choices for the current question.
        """
        return self.current_question.get('choices', []) if self.current_question else None

    @property
    def answer(self):
        """
        :returns:
            int: The answer for the current question.
        """
        return self.current_question.get('answer', 0) if self.current_question else None
