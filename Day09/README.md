# Day 09 - Python Bootcamp

### Exercise 00: Still Counts

You have to write a simple calculator module for Python (using Python C API) with four functions:

- `add(a, b)`
- `sub(a, b)`
- `mul(a, b)`
- `div(a, b)`

This module should consist of two files - 'calculator.c' and 'setup.py' for building it.
In regular part of EX00 let's assume the numbers are integers:

```python
>>> import calculator
>>> calculator.add(14.5, 21.87)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: integer argument expected, got float
>>> calculator.add(14, 21)
35
>>> calculator.sub(14, 21)
-7
>>> calculator.mul(14, 21)
294
>>> calculator.div(14, 7)
2
```

Also, your code should handle zero division errors properly, raising a built-in Python exception
from the C code:

```python
>>> import calculator
>>> calculator.by(14, 0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: Cannot divide by zero
```

The module should only include two files mentioned above and be installable using
`python setup.py install`

BONUS: upgrade the code of your calculator so it can handle both int and float values for both 
operands.

### Exercise 01: Split-Second

You need to use a built-in `ctypes` library in Python to implement an interface to a monotonic 
clock in your operating system. Windows, Linux and MacOS have the function as a part of a standard
library. Python [also has it now](https://peps.python.org/pep-0418/#time-monotonic), but you
should write your own version from scratch.

It should be a function `monotonic()` in a file called `monotonic.py` and a returned value should
be in seconds (some OSes also support nanoseconds). 

### Exercise 02: Autopilot

This time you need to use a third way to speed up computation in Python, which is [Cython](https://cython.org/).
We don't go into Data Science, but [multiplying matrices](https://en.wikipedia.org/wiki/Matrix_multiplication) is a pretty easy and
straightforward procedure.

The sample simplified Python code for it may look somewhat similar to this:

```python
from itertools import tee 

def mul(a, b):
    b_iter = tee(zip(*b), len(a))
    return [
        [
            sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b)) 
            for col_b in b_iter[i]
        ] for i, row_a in enumerate(a)
    ]
```

You have to write your own function `mul()` in Cython (filename is `multiply.pyx`) and (as in EX00) 
implement a proper `setup.py` file to make a Python package called 'matrix':

```python
from matrix import mul

x = [[1,2,3],[4,5,6],[7,8,9],[10,11,12]]
y = [[1,2],[1,2],[3,4]]

print(mul(x, y))
"""[[12, 18], [27, 42], [42, 66], [57, 90]]"""
```

For simplicity, let's say your code should only work with integers and matrices are no larger than
100x100. Also, don't use built-in implementation from [Numpy](https://numpy.org/) for this task,
even though in production code that would be probably one of the preferred ways.

BONUS: write a performance test in file `test_mul_perf.py` comparing basic pure Python
implementation with your Cython one. It should be a lot faster.
