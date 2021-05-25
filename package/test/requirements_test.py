import unittest
import copy
from ..automat.automat import *
from ..automat.coin import *

class TestProjectRequirements(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.automat = Automat(5)
        self.itemNumber = 30
        #set constant item price for itemNumber
        self.itemPrice = 5.2
        self.automat._Automat__items[self.itemNumber].set_price(self.itemPrice)

    def test_returnsItemPrice(self) -> None:
        """Test requirement #1"""
        #get item info
        name, price, amount = self.automat.get_item_details(self.itemNumber)

        #price must be a float number and greater than 0
        self.assertIsInstance(price, float)
        self.assertGreater(price, 0)

    def test_returnsItemWithNoChangeWhenExactPriceMatched(self) -> None:
        """Test requirement #2"""
        coins = [Coin(2), Coin(2), Coin(1), Coin(0.2)]

        #try to buy the item with coins
        change, item = self.automat.pay_for_item(self.itemNumber, coins)

        #machine should return no change and a valid item
        self.assertListEqual(change, [])
        self.assertIsInstance(item, Item)
        #coins should be consumed by the machine
        self.assertListEqual(coins, [])

    def test_returnsItemAndChangeWhenTooMuchMoneyPaid(self) -> None:
        """Test requirement #3"""
        coins = [Coin(2), Coin(2), Coin(2), Coin(0.5)]
        expected_change = 1.3

        change, item = self.automat.pay_for_item(self.itemNumber, coins)

        #machine should return correct amount of change and a valid item
        self.assertEqual(get_coins_value(change), expected_change)
        self.assertIsInstance(item, Item)
        #coins should be consumed by the machine
        self.assertListEqual(coins, [])

    def test_raisesExceptionWhenBuyingUnavailableItem(self) -> None:
        """Test requirement #4"""
        coins = [Coin(2), Coin(2), Coin(1), Coin(0.2)]
        #check how many items are available right now
        name, price, available = self.automat.get_item_details(self.itemNumber)

        #buy all items
        for _ in range(0, available):
            #coins are copied to avoid being consumed
            self.automat.pay_for_item(self.itemNumber, copy.deepcopy(coins))

        #NoItemsLeftException is the expected messsage
        with self.assertRaises(NoItemsLeftException):
            self.automat.pay_for_item(self.itemNumber, coins)

        #coins should not be consumed by the machine
        self.assertEqual(len(coins), 4)

    def test_raisesExceptionWhenCheckingInvalidItemNumber(self) -> None:
        """Test requirement #5"""
        #InvalidItemNumberException is the expected message
        with self.assertRaises(InvalidItemNumberException):
            name, price, amount = self.automat.get_item_details(55)

    def test_raisesExceptionWhenNotEnoughMoneyPaid(self) -> None:
        """Test requirement #6"""
        coins = [Coin(1)]

        #NotEnoughMoneyException is the expected message
        with self.assertRaises(NotEnoughMoneyException):
            self.automat.pay_for_item(self.itemNumber, coins)

        #coins should not be consumed by the machine
        self.assertEqual(len(coins), 1)

    def test_retryBuyingAfterAddingMoreMoney(self) -> None:
        """Test requirement #7"""
        coins = [Coin(2), Coin(2), Coin(1)]

        #pay not enough money - expected to raise NotEnoughMoneyException
        with self.assertRaises(NotEnoughMoneyException):
            self.automat.pay_for_item(self.itemNumber, coins)

        #add more money and pay again
        coins.append(Coin(0.2))
        change, item = self.automat.pay_for_item(self.itemNumber, coins)

        #returned change list should be empty and the item should be valid
        self.assertListEqual(change, [])
        self.assertIsInstance(item, Item)
        #coins should be consumed by the machine
        self.assertListEqual(coins, [])

    def test_payingWith1grCoins(self) -> None:
        """Test requirement #8"""
        #520 1gr coins
        coins = [Coin(0.01) for _ in range(0, 520)]

        #use the coins to buy the item
        change, item = self.automat.pay_for_item(self.itemNumber, coins)

        #returned change list should be empty and the item should be valid
        self.assertListEqual(change, [])
        self.assertIsInstance(item, Item)
        #coins should be consumed by the machine
        self.assertListEqual(coins, [])

if __name__ == '__main__':
    unittest.main()