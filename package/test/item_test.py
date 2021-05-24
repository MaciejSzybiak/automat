import unittest
from ..automat.automat import *
from ..automat.coin import *
from ..automat.item import *

class TestItemMethods(unittest.TestCase):
    def test_returnsItemName(self) -> None:
        name = "item_test_name"
        item = Item(name)

        self.assertEqual(item.get_name(), name)

class TestItemInfoMethods(unittest.TestCase):
    def test_returnsPrice(self) -> None:
        price = 5.01
        info = ItemInfo(price, 1, Item("a"))

        self.assertEqual(info.get_price(), price)

    def test_returnsAmount(self) -> None:
        amount = 3
        info = ItemInfo(1, amount, Item("a"))
        
        self.assertEqual(info.get_amount(), amount)

    def test_returnsItemName(self) -> None:
        testName = "test_name"
        info = ItemInfo(1, 1, Item(testName))

        self.assertEqual(info.get_name(), testName)

    def test_raisesExceptionWhenInvalidAmountIsSet(self) -> None:
        info = ItemInfo(1, 1, Item("a"))
        with self.assertRaises(InvalidItemAmountException):
            info.set_amount(-2)

    def test_raisesExceptionWhenInvalidPriceIsSet(self) -> None:
        info = ItemInfo(1, 1, Item("a"))
        with self.assertRaises(InvalidItemPriceException):
            info.set_price(-0.7)

    def test_returnsItem(self) -> None:
        info = ItemInfo(1, 1, Item("a"))

        item = info.fetch_item()

        self.assertIsInstance(item, Item)

    def test_raisesNoItemsLeftException(self) -> None:
        info = ItemInfo(1, 0, Item("a"))

        with self.assertRaises(NoItemsLeftException):
            item = info.fetch_item()

if __name__ == '__main__':
    unittest.main()