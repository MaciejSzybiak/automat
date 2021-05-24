import unittest
from ..automat.coin import *

class TestCoinMethods(unittest.TestCase):
    def test_eqOperatorFalse(self) -> None:
        c1 = Coin(0.01)
        c2 = Coin(0.2)

        self.assertFalse(c1 == c2)

    def test_eqOperatorTrue(self) -> None:
        c1 = Coin(0.2)
        c2 = Coin(0.2)

        self.assertTrue(c1 == c2)

    def test_returnsValue(self) -> None:
        coinValue = 2
        c = Coin(coinValue)

        self.assertEqual(c.get_value(), coinValue)

    def test_raisesInvalidCoinValueException(self) -> None:
        with self.assertRaises(InvalidCoinValueException):
            coin = Coin(0.88)

if __name__ == '__main__':
    unittest.main()