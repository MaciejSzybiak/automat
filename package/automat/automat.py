import random
from typing import NamedTuple
from .coin import *
from .item import *

class InvalidItemNumberException(Exception):
    """Raised when requested item number is not found."""
    def __init__(self) -> None:
        super().__init__("Item number is invalid.")

class NotEnoughMoneyException(Exception):
    """Raised when not enough money is supplied for purchase."""
    def __init__(self, provided: float, required: float) -> None:
        super().__init__(f"Not enough money (provided: {provided}, required: {required}).")

class ExactChangeOnlyException(Exception):
    """Raised when the automat is not able to gice the change."""
    def __init__(self, amount: float) -> None:
        super().__init__(f"Exact change only (left: {amount}")

def get_random_price() -> float:
    """Returns random price inc range of 1.50zl to 7zl."""
    return random.randint(150, 700) / 100

def get_coins_value(coins) -> float:
    """Returns value of the coins in a list."""
    sum = 0
    for c in coins:
        sum += c.get_value()
    return round(sum, 2)

class Automat:
    """Represents a vending machine."""
    def __init__(self, amountOfEachItem: int) -> None:
        if amountOfEachItem < 1:
            raise InvalidItemAmountException()
        #create items and coins dictionaries
        self.__items = { n:ItemInfo(get_random_price(), amountOfEachItem, Item(f"Item {n}")) for n in range(30, 51) }
        self.__coins = { amount:[Coin(amount) for _ in range(0,10)] for amount in coin_values }
    def __fetch_item(self, itemNumber: int) -> Item:
        """Returns the requested item or raises an exception if it's not available."""
        if self.__items[itemNumber] == None:
            raise InvalidItemNumberException()
        try:
            item = self.__items[itemNumber].fetch_item()
            return item
        except NoItemsLeftException:
            pass
    def get_items_list(self) -> "list[tuple[int, str]]":
        """Returns item numbers and names."""
        return [(k, v.get_name()) for k, v in self.__items.items()]
    def get_item_details(self, itemNumber: int) -> "tuple[str, float, int]":
        """Returns name, price and amount of an item."""
        if self.__items[itemNumber] == None:
            raise InvalidItemNumberException()
        itemInfo = self.__items[itemNumber]
        return itemInfo.get_name(), itemInfo.get_price(), itemInfo.get_amount()
    def add_coins(self, coins: "list[Coin]") -> None:
        """Adds coins from the list to automat's coins."""
        for c in coins:
            self.__coins[c.get_value()].append(c)
    def __get_change(self, coinsValue: float, price: float) -> "list[Coin]":
        """Adds coins from the list to automat's coins and returns change to match the amount of money required."""
        amount = coinsValue - price #amount of change left
        coins = []
        for cv in coin_values[::-1]:
            required_coin_count = amount // cv
            available_coin_count = len(self.__coins[cv])
            coin_count = int(min(required_coin_count, available_coin_count))

            #fetch required amount of coins from the automat
            for _ in range(0, coin_count):
                coins.append(self.__coins[cv].pop())
            amount -= coin_count * cv
        if round(amount, 2) > 0:
            raise ExactChangeOnlyException(amount)
        return coins
    def pay_for_item(self, itemNumber: int, coins: "list[Coin]") -> "tuple[list[Coin], Item]":
        """Tries to pay for item. Returns a tuple of change and item if succeeded."""
        coinsValue = get_coins_value(coins)
        itemName, itemPrice, itemAmount = self.get_item_details(itemNumber)
        if coinsValue == itemPrice:
            self.add_coins(coins)
            return [], self.__fetch_item(itemNumber)
        elif coinsValue >= itemPrice:
            self.add_coins(coins)
            return self.__get_change(coinsValue, itemPrice), self.__fetch_item(itemNumber)
        else:
            raise NotEnoughMoneyException(coinsValue, itemPrice)
