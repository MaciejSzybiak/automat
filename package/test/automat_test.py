import unittest
from ..automat.automat import *
from ..automat.coin import *

def sum_coins(coins: "list[Coin]") -> float:
    sum = 0
    for c in coins:
        sum = round(sum + c.get_value(), 2)
    return sum

class TestAutomatMethods(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.itemAmount = 5
        self.a = Automat(self.itemAmount)
        self.itemNumber = 30
        self.itemPrice = 3
        self.a._Automat__items[self.itemNumber].set_price(self.itemPrice)

    def test_returnsItemsList(self) -> None:
        items = self.a.get_items_list()

        self.assertEqual(len(items), 21)

    def test_returnsItemDetails(self) -> None:
        itemName, itemPrice, itemAmount = self.a.get_item_details(30)

        self.assertGreater(len(itemName), 0)
        self.assertEqual(itemPrice, self.itemPrice)
        self.assertEqual(itemAmount, self.itemAmount)

    def test_addsCoins(self) -> None:
        amountOf5zl = len(self.a._Automat__coins[5])
        amountOf20gr = len(self.a._Automat__coins[0.2])
        coins_to_add = [Coin(5), Coin(5), Coin(0.2)]

        self.a.add_coins(coins_to_add)

        self.assertEqual(len(self.a._Automat__coins[5]), amountOf5zl + 2)
        self.assertEqual(len(self.a._Automat__coins[0.2]), amountOf20gr + 1)

    def test_returnsChange(self) -> None:
        coinsValue = 17.37
        price = 10
        expected = round(coinsValue - price, 2)

        change = self.a._Automat__get_change(coinsValue, price)
        sum = sum_coins(change)

        self.assertEqual(sum, expected)

    def test_returnsNoCoinsWhenRequiredAmountPaid(self) -> None:
        testCoins = [Coin(2), Coin(1)]

        for c in testCoins:
            self.a.insert_coin(c)

        coins, item = self.a.pay_for_item(self.itemNumber)

        self.assertListEqual(coins, [])

    def test_consumesCoinsWhenRequiredAmountPaid(self) -> None:
        testCoins = [Coin(2), Coin(1)]

        for c in testCoins:
            self.a.insert_coin(c)

        coins, item = self.a.pay_for_item(self.itemNumber)

        self.assertEqual(self.a.get_inserted_coins_value(), 0)

    def test_returnsCoinsWhenPaidTooMuch(self) -> None:
        testCoins = [Coin(2), Coin(2)]

        for c in testCoins:
            self.a.insert_coin(c)

        coins, item = self.a.pay_for_item(self.itemNumber)
        sum = sum_coins(coins)

        self.assertEqual(sum, 1)

    def test_insertsCoins(self) -> None:
        coinToAdd = Coin(5)

        self.a.insert_coin(coinToAdd)

        self.assertListEqual(self.a._Automat__inserted_coins, [coinToAdd])

    def test_returnsInsertedCoinsValue(self) -> None:
        coinValue = 5
        coinToAdd = Coin(coinValue)

        self.a.insert_coin(coinToAdd)

        self.assertEqual(self.a.get_inserted_coins_value(), coinValue)

    def test_clearsInsertedCoins(self) -> None:
        coinValue = 5
        coinToAdd = Coin(coinValue)

        self.a._Automat__inserted_coins.append(coinToAdd)
        self.a.clear_inserted_coins()

        self.assertEqual(self.a._Automat__inserted_coins, [])

    def test_getCoinsValue(self) -> None:
        coins = [Coin(5), Coin(0.1), Coin(0.02)]

        value = get_coins_value(coins)

        self.assertEqual(value, 5.12)

if __name__ == '__main__':
    unittest.main()