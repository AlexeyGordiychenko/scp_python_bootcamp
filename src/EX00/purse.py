import unittest
from typing import Dict


def ingot_decorator(func):
    def wrapper(purse: Dict[str, int]):
        amount = func(purse.get('gold_ingots', 0))
        return {} if amount == 0 else {'gold_ingots': amount}
    return wrapper


@ingot_decorator
def add_ingot(amount):
    return amount + 1


@ingot_decorator
def get_ingot(amount):
    return max(0, amount - 1)


def empty(purse: Dict[str, int]):
    return {}


class PurseTests(unittest.TestCase):

    def test_purse_empty(self):
        purse = {'gold_ingots': 6}
        self.assertEqual(empty(purse), {})
        self.assertEqual(purse, {'gold_ingots': 6})

    def test_purse_empty_on_empty(self):
        purse = {}
        self.assertEqual(empty(purse), {})
        self.assertEqual(purse, {})

    def test_add_ingot(self):
        purse = {'gold_ingots': 9}
        self.assertEqual(add_ingot(purse), {'gold_ingots': 10})
        self.assertEqual(purse, {'gold_ingots': 9})

    def test_get_ingot(self):
        purse = {'gold_ingots': 9}
        self.assertEqual(get_ingot(purse), {'gold_ingots': 8})
        self.assertEqual(purse, {'gold_ingots': 9})

    def test_add_ingot_in_empty(self):
        purse = {'gold_ingots': 9}
        self.assertEqual(add_ingot(empty(purse)), {'gold_ingots': 1})
        self.assertEqual(purse, {'gold_ingots': 9})

    def test_get_ingot_from_empty(self):
        purse = {'gold_ingots': 9}
        self.assertEqual(get_ingot(empty(purse)), {})
        self.assertEqual(purse, {'gold_ingots': 9})

    def test_get_ingot_from_zero(self):
        purse = {'gold_ingots': 0}
        self.assertEqual(get_ingot(purse), {})
        self.assertEqual(purse, {'gold_ingots': 0})

    def test_empty_stones(self):
        purse = {'stones': 5}
        self.assertEqual(empty(purse), {})
        self.assertEqual(purse, {'stones': 5})

    def test_get_ingot_stones(self):
        purse = {'stones': 5}
        self.assertEqual(get_ingot(purse), {})
        self.assertEqual(purse, {'stones': 5})

    def test_add_ingot_stones(self):
        purse = {'stones': 5}
        self.assertEqual(add_ingot(purse), {'gold_ingots': 1})
        self.assertEqual(purse, {'stones': 5})


if __name__ == "__main__":
    unittest.main()
