from user_input import user_input


def test_user_input1(monkeypatch):
    inputs = ["not a number", "20", "0", "-1", "5"]
    input_generator = (i for i in inputs)
    monkeypatch.setattr('builtins.input', lambda x: next(input_generator))
    assert user_input("Enter a number", 1, 10) == 5


def test_user_input2(monkeypatch):
    inputs = ["8"]
    input_generator = (i for i in inputs)
    monkeypatch.setattr('builtins.input', lambda x: next(input_generator))
    assert user_input("Enter a number", 1, 10) == 8
