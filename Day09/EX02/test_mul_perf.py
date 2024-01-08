import time
from itertools import tee
from random import randint
from matrix import mul as cy_mul


def py_mul(a, b):
    b_iter = tee(zip(*b), len(a))
    return [
        [
            sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b))
            for col_b in b_iter[i]
        ] for i, row_a in enumerate(a)
    ]


def generate_matrices():
    m1 = [[randint(-1000, 1000) for _ in range(100)] for _ in range(100)]
    m2 = [[randint(-1000, 1000) for _ in range(100)] for _ in range(100)]
    return m1, m2


def time_functions():
    X, Y = generate_matrices()

    start = time.time()
    py_mul(X, Y)
    py_time = time.time() - start

    start = time.time()
    cy_mul(X, Y)
    cy_time = time.time() - start

    return py_time, cy_time


if __name__ == "__main__":
    py_time_res, cy_time_res = 0, 0
    for _ in range(20):
        py_time, cy_time = time_functions()
        py_time_res += py_time
        cy_time_res += cy_time
    print(f"Python time = {py_time_res}")
    print(f"Cython time = {cy_time_res}")
