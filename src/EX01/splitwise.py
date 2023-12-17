import unittest
from typing import Dict, Tuple


def distribute(total: int, count: int):
    for i in range(count):
        part = total // (count - i)
        total -= part
        yield {'gold_ingots': part}


def split_booty(*args: Dict[str, int]) -> Tuple[Dict[str, int], Dict[str, int], Dict[str, int]]:
    total = sum([p.get('gold_ingots', 0) for p in args])
    return tuple(distribute(total, 3))


class SplitTests(unittest.TestCase):

    def check(self, purses_in):
        purses_in_copy = purses_in.copy()
        total_in = sum([p.get('gold_ingots', 0) for p in purses_in])
        ingots = [p.get('gold_ingots', 0) for p in split_booty(*purses_in)]
        # check that the number of ingots is the same
        self.assertEqual(total_in, sum(ingots))
        # the difference between the number of ingots is no larger than 1
        self.assertEqual((max(ingots) - min(ingots)) <= 1, True)
        # check that the input list is not modified
        self.assertEqual(purses_in, purses_in_copy)

    def test_split_readme(self):
        purses_in = [{"gold_ingots": 3}, {"gold_ingots": 2}, {"apples": 10}]
        self.check(purses_in)

    def test_split_zero(self):
        purses_in = [{"gold_ingots": 0}]
        self.check(purses_in)

    def test_split_one(self):
        purses_in = [{"gold_ingots": 1}]
        self.check(purses_in)

    def test_split_two(self):
        purses_in = [{"gold_ingots": 2}]
        self.check(purses_in)

    def test_split_three(self):
        purses_in = [{"gold_ingots": 3}]
        self.check(purses_in)

    def test_split_common_1(self):
        purses_in = [{"gold_ingots": 1}, {
            "gold_ingots": 1}, {"gold_ingots": 1}]
        self.check(purses_in)

    def test_split_common_2(self):
        purses_in = [{"gold_ingots": 13}, {"gold_ingots": 8},
                     {"gold_ingots": 0}, {"gold_ingots": 5}]
        self.check(purses_in)


if __name__ == "__main__":
    unittest.main()
