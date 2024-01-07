import calculator_float
import pytest


def compare_doubles(a, b):
    assert a == pytest.approx(b, abs=1e-12)


def test_add():
    compare_doubles(calculator_float.add(5.1, 0), 5.1)
    compare_doubles(calculator_float.add(0, 5.2), 5.2)
    compare_doubles(calculator_float.add(-30, 50.1), 20.1)
    compare_doubles(calculator_float.add(0, 0), 0)
    compare_doubles(calculator_float.add(1, -2.2), -1.2)
    compare_doubles(calculator_float.add(-10, -2), -12)
    compare_doubles(calculator_float.add(37, 3.3), 40.3)


def test_sub():
    compare_doubles(calculator_float.sub(5.1, 0), 5.1)
    compare_doubles(calculator_float.sub(0, 5.2), -5.2)
    compare_doubles(calculator_float.sub(-30, 50.1), -80.1)
    compare_doubles(calculator_float.sub(0, 0), 0)
    compare_doubles(calculator_float.sub(1, -2.2), 3.2)
    compare_doubles(calculator_float.sub(-10, -2), -8)
    compare_doubles(calculator_float.sub(37, 3.3), 33.7)


def test_mul():
    compare_doubles(calculator_float.mul(5.1, 0), 0)
    compare_doubles(calculator_float.mul(0, 5.2), 0)
    compare_doubles(calculator_float.mul(-30, 50.1), -1503)
    compare_doubles(calculator_float.mul(0, 0), 0)
    compare_doubles(calculator_float.mul(1, -2.2), -2.2)
    compare_doubles(calculator_float.mul(-10, -2), 20)
    compare_doubles(calculator_float.mul(37, 3.3), 122.1)


def test_div():
    with pytest.raises(ZeroDivisionError):
        calculator_float.div(5.1, 0)
    compare_doubles(calculator_float.div(0, 5.2), 0)
    compare_doubles(calculator_float.div(-92.4, 3), -30.8)
    with pytest.raises(ZeroDivisionError):
        calculator_float.div(0, 0)
    compare_doubles(calculator_float.div(1, -2.5), -0.4)
    compare_doubles(calculator_float.div(-10, -2), 5)
    compare_doubles(calculator_float.div(37, 3.2), 11.5625)
