from vk_test import VKTest
import os


def test_replicant(monkeypatch):
    inputs = ["1", "12", "70", "3", "4",
              "2", "14", "78", "5", "2",
              "2", "13", "81", "4", "3",
              "1", "12", "89", "4", "2",
              "1", "14", "85", "5", "4",
              "2", "13", "75", "3", "3",
              "3", "13", "69", "4", "2",
              "1", "12", "78", "5", "2",
              "2", "14", "80", "5", "3",
              "3", "13", "85", "3", "3",
              ]
    input_generator = (i for i in inputs)
    monkeypatch.setattr('builtins.input', lambda x: next(input_generator))
    test = VKTest(os.path.join(
        os.path.dirname(__file__), '..', 'questions.json'))
    assert test.run() == True
    assert test.result() == 'replicant'


def test_human(monkeypatch):

    inputs = ["2", "13", "80", "4", "6",
              "2", "12", "92", "6", "3",
              "2", "14", "85", "5", "2",
              "1", "12", "73", "4", "8",
              "2", "13", "65", "3", "3",
              "2", "13", "72", "6", "5",
              "3", "14", "78", "3", "4",
              "1", "12", "90", "6", "3",
              "2", "12", "91", "5", "2",
              "3", "12", "98", "3", "8",
              ]
    input_generator = (i for i in inputs)
    monkeypatch.setattr('builtins.input', lambda x: next(input_generator))
    test = VKTest(os.path.join(
        os.path.dirname(__file__), '..', 'questions.json'))
    assert test.run() == True
    assert test.result() == 'human'


def test_no_questions():
    test = VKTest(os.path.join(
        os.path.dirname(__file__), '..', 'no file.json'))
    assert test.run() == False
    assert test.result() == None
