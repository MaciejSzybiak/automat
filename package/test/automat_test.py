import unittest
from ..automat.automat import *
from ..automat.coin import *

class TestAutomatMethods(unittest.TestCase):
    def test_returnsItemsList(self) -> None:
        a = Automat(5)
        
        items = a.get_items_list()

        self.assertEqual(len(items), 21)

    def test_returnsItemDetails(self) -> None:
        a = Automat(5)

        itemName, itemPrice, itemAmount = a.get_item_details(30)

        self.assertGreater(len(itemName), 0)
        self.assertGreater(itemPrice, 0)
        self.assertEqual(itemAmount, 5)

    def test_addsCoins(self) -> None:
        a = Automat(5)
        amountOf5zl = len(a._Automat__coins[5])
        amountOf20gr = len(a._Automat__coins[0.2])
        coins_to_add = [Coin(5), Coin(5), Coin(0.2)]

        a.add_coins(coins_to_add)

        self.assertEqual(len(a._Automat__coins[5]), amountOf5zl + 2)
        self.assertEqual(len(a._Automat__coins[0.2]), amountOf20gr + 1)

    def test_returnsChange(self) -> None:
        a = Automat(5)
        coinsValue = 17.37
        price = 10

        change = a._Automat__get_change(coinsValue, price)
        sum = 0
        for c in change:
            sum += c.get_value()

        self.assertAlmostEqual(sum, coinsValue - price, places=2)

    def test_returnsNoCoinsWhenRequiredAmountPaid(self) -> None:
        a = Automat(5)
        a._Automat__items[30].set_price(5)
        testCoins = [Coin(5)]

        coins, item = a.pay_for_item(30, testCoins)

        self.assertListEqual(coins, [])

    def test_returnsCoinsWhenPaidTooMuch(self) -> None:
        a = Automat(5)
        a._Automat__items[30].set_price(5)
        testCoins = [Coin(2), Coin(2), Coin(2)]

        itemName, itemPrice, itemAmount = a.get_item_details(30)

        coins, item = a.pay_for_item(30, testCoins)
        sum = 0
        for c in coins:
            sum += c.get_value()
            
        self.assertListEqual(coins, [Coin(1)])

    def test_getCoinsValue(self) -> None:
        coins = [Coin(5), Coin(0.1), Coin(0.02)]

        self.assertEqual(get_coins_value(coins), 5.12)

if __name__ == '__main__':
    unittest.main()