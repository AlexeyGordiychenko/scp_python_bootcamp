import pytest
from matrix import mul


def matrices_equal(a: list[list[int]], b: list[list[int]]) -> bool:
    assert len(a) == len(b)
    for row_a, row_b in zip(a, b):
        assert len(row_a) == len(row_b)

        for ele_a, ele_b in zip(row_a, row_b):
            assert ele_a == ele_b


def test_correct():
    matrices_equal(mul(
        [[1, 2], [3, 4]],
        [[5, 6], [7, 8]]
    ),
        [[19, 22], [43, 50]]
    )


def test_incorrect_matrices():
    with pytest.raises(TypeError):
        mul([1, 1], [1, 1])


def test_incorrect_dimensions():
    a = [[1, 2, 3], [4, 5, 6]]
    b = [[7, 8], [9, 10]]
    with pytest.raises(ValueError):
        mul(a, b)


def test_incorrect_value_str():
    a = [[1, 2], [3, 4]]
    b = [[5, '6'], [7, 8]]
    with pytest.raises(TypeError):
        mul(a, b)


def test_incorrect_value_float():
    a = [[1, 2], [3, 4]]
    b = [[5, 6.6], [7, 8]]
    with pytest.raises(TypeError):
        mul(a, b)
