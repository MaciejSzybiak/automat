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
        sum = round(sum + c.get_value(), 2)
    return sum

class Automat:
    """Represents a vending machine."""
    def __init__(self, amountOfEachItem: int) -> None:
        if amountOfEachItem < 1:
            raise InvalidItemAmountException()
        #create items and coins dictionaries
        self.__items = { n:ItemInfo(get_random_price(), amountOfEachItem, Item(f"Item {n}")) for n in range(30, 51) }
        self.__coins = { amount:[Coin(amount) for _ in range(0,10)] for amount in coin_values }
        self.__inserted_coins: "list[Coin]" = []
    def __fetch_item(self, itemNumber: int) -> Item:
        """Returns the requested item or raises an exception if it's not available."""
        try:
            item = self.__items[itemNumber].fetch_item()
            return item
        except NoItemsLeftException as e:
            raise e
        except KeyError:
            raise InvalidItemNumberException()
    def get_items_list(self) -> "list[tuple[int, str]]":
        """Returns item numbers and names."""
        return [(k, v.get_name()) for k, v in self.__items.items()]
    def get_item_details(self, itemNumber: int) -> "tuple[str, float, int]":
        """Returns name, price and amount of an item."""
        try:
            itemInfo = self.__items[itemNumber]
        except KeyError:
            raise InvalidItemNumberException()
        return itemInfo.get_name(), itemInfo.get_price(), itemInfo.get_amount()
    def insert_coin(self, coin: Coin) -> None:
        """Insert a coin from the customer."""
        self.__inserted_coins.append(coin)
    def clear_inserted_coins(self) -> None:
        """Clears inserted coins list."""
        self.__inserted_coins.clear()
    def get_inserted_coins_value(self) -> float:
        """Returns value of the inserted coins."""
        return get_coins_value(self.__inserted_coins)
    def add_coins(self, coins: "list[Coin]") -> None:
        """Adds coins from the list to automat's coins."""
        #add coins to the machine
        for c in coins:
            self.__coins[c.get_value()].append(c)
        coins.clear() #clear the list of coins passed to the machine
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
            amount = round(amount - coin_count * cv, 2)
        if amount > 0:
            raise ExactChangeOnlyException(amount)
        return coins
    def pay_for_item(self, itemNumber: int) -> "tuple[list[Coin], Item]":
        """Tries to pay for item with the inserted coins. Returns a tuple of change and item if succeeded."""
        coinsValue = self.get_inserted_coins_value()
        itemName, itemPrice, itemAmount = self.get_item_details(itemNumber)
        if coinsValue == itemPrice:
            try:
                item = self.__fetch_item(itemNumber)
                self.add_coins(self.__inserted_coins)
                return [], item
            except NoItemsLeftException as e:
                raise e
        elif coinsValue >= itemPrice:
            self.add_coins(self.__inserted_coins)
            return self.__get_change(coinsValue, itemPrice), self.__fetch_item(itemNumber)
        else:
            raise NotEnoughMoneyException(coinsValue, itemPrice)
