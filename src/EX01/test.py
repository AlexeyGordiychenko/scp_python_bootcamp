import unittest
from decypher import decypher


class DecypherTests(unittest.TestCase):

    def test_decypher_empty(self):
        self.assertEqual(decypher(''), '')

    def test_decypher_towerbridge(self):
        self.assertEqual(decypher(
            'The only way everyone reaches Brenda rapidly is delivering groceries explicitly'), 'towerbridge')

    def test_decypher_bigben(self):
        self.assertEqual(decypher(
            'Britain is Great because everyone necessitates'), 'bigben')

    def test_decypher_hydepark(self):
        self.assertEqual(decypher(
            'Have you delivered eggplant pizza at restored keep?'), 'hydepark')


if __name__ == '__main__':
    unittest.main()
