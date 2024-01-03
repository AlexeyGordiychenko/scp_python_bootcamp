from questionnaire import Questionnaire
import os


def test_questionnaire_correct():
    questionnaire = Questionnaire(os.path.join(
        os.path.dirname(__file__), "..", "questions.json"))
    assert questionnaire.questions is not None
    count = 0
    while questionnaire.next():
        count += 1
    assert count == 10


def test_questionnaire_incorrect1():
    questionnaire = Questionnaire("not_existing.json")
    assert questionnaire.questions == None


def test_questionnaire_incorrect2():
    questionnaire = Questionnaire(os.path.join(
        os.path.dirname(__file__), "test_questions.json"))
    assert questionnaire.questions == None
