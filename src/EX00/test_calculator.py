import calculator
import pytest


def test_add():
    assert calculator.add(5, 0) == 5
    assert calculator.add(0, 5) == 5
    assert calculator.add(-30, 50) == 20
    assert calculator.add(0, 0) == 0
    assert calculator.add(1, -2) == -1
    assert calculator.add(-10, -2) == -12
    with pytest.raises(TypeError):
        calculator.add(37, 3.3) == 40.3


def test_sub():
    assert calculator.sub(5, 0) == 5
    assert calculator.sub(0, 5) == -5
    assert calculator.sub(-30, 50) == -80
    assert calculator.sub(0, 0) == 0
    assert calculator.sub(1, -2) == 3
    assert calculator.sub(-10, -2) == -8
    with pytest.raises(TypeError):
        calculator.sub(37, 3.3) == 33.7


def test_mul():
    assert calculator.mul(5, 0) == 0
    assert calculator.mul(0, 5) == 0
    assert calculator.mul(-30, 50) == -1500
    assert calculator.mul(0, 0) == 0
    assert calculator.mul(1, -2) == -2
    assert calculator.mul(-10, -2) == 20
    with pytest.raises(TypeError):
        calculator.add(37, 3.3) == 122.1


def test_div():
    with pytest.raises(ZeroDivisionError):
        assert calculator.div(5, 0) == 0
    assert calculator.div(0, 5) == 0
    assert calculator.div(-60, 30) == -2
    with pytest.raises(ZeroDivisionError):
        assert calculator.div(0, 0) == 0
    assert calculator.div(-10, -2) == 5
    with pytest.raises(TypeError):
        calculator.div(37, 3.2) == 11.5625
