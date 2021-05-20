import random
import copy
from typing import NamedTuple
from automat.coin import Coin
from automat.coin import coin_values
from automat.coin import InvalidCoinValueException
from automat.item import Item

class InvalidItemAmountException(Exception):
    """Raised when item amount is a decimal or less than zero."""
    def __init__(self, amount):
        super().__init__(f"Incorrect amount of items: {amount}")

class InvalidItemPriceException(Exception):
    """Raised when item price is less than 1gr."""
    def __init__(self, price):
        super().__init__(f"Incorrect item price: {price}")

class NoItemsLeftException(Exception):
    """Raised when there are no item copies left in ItemInfo class."""
    def __init__(self):
        super().__init__("No items left")

class ItemInfo:
    """Contains information about an item: its price, amount and class instance."""
    __price = 0
    __amount = 0
    __item = None
    def __init__(self, price, amount, item):
        self.set_amount(amount)
        self.set_price(price)
        self.__item = item   
    def set_amount(self, amount):
        """Sets how many copies of this items are left."""
        if amount < 0 or amount % 1 != 0:
            raise InvalidItemAmountException(amount)
        else:
            __amount = amount
    def set_price(self, price):
        """Sets price for this item."""
        if price < 0.01:
            raise InvalidItemPriceException(price)
        else:
            __price = price  
    def fetch_item(self):
        """Decremets item counter and returns a copy of the item instance.
        Raises NoItemsLeftException when the amount of items is 0."""
        if self.__amount == 0:
            raise NoItemsLeftException()
        else:
            return copy.deepcopy(self.__item)
    def get_amount(self):
        """Returns the current amount of items."""
        return self.__amount


def get_random_price():
    """Returns random price in range of 1.50zl to 7zl."""
    return random.randint(150, 700) / 100

class Automat:
    __items = {} #dictionary: item_number(30 to 50):ItemInfo
    __coins = {} #dictionary: Coin:amount
    def __init__(self, amountOfEachItem):
        if amountOfEachItem < 1:
            raise InvalidItemAmountException()
        #create items and coins dictionaries
        __items = { n:ItemInfo(get_random_price(), amountOfEachItem, Item(f"Item {n}")) for n in range(30, 51) }
        __coins = { Coin(amount):10 for amount in coin_values }

