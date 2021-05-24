import copy

class Item:
    """Represents an item for use with Automats"""
    def __init__(self, name: str) -> None:
        self.__itemName = name
    def get_name(self) -> str:
        """Returns item's name."""
        return self.__itemName

class InvalidItemAmountException(Exception):
    """Raised when item amount is less than zero."""
    def __init__(self, amount: float) -> None:
        super().__init__(f"Incorrect amount of items: {amount}")

class InvalidItemPriceException(Exception):
    """Raised when item price is less than 1gr."""
    def __init__(self, price: float) -> None:
        super().__init__(f"Incorrect item price: {price}")

class NoItemsLeftException(Exception):
    """Raised when there are no item copies left."""
    def __init__(self) -> None:
        super().__init__("No items left")

class ItemInfo:
    """Contains information about an item: its price, amount and class instance."""
    def __init__(self, price: float, amount: int, item: Item) -> None:
        self.set_amount(amount)
        self.set_price(price)
        self.__item = item   
    def set_amount(self, amount: int) -> None:
        """Sets how many copies of this items are left."""
        if amount < 0:
            raise InvalidItemAmountException(amount)
        else:
            self.__amount = amount
    def set_price(self, price: float) -> None:
        """Sets price for this item."""
        if price < 0.01:
            raise InvalidItemPriceException(price)
        else:
            self.__price = price  
    def fetch_item(self) -> Item:
        """Decremets item counter and returns a copy of the item instance.
        Raises NoItemsLeftException when the amount of items is 0."""
        if self.__amount == 0:
            raise NoItemsLeftException()
        else:
            self.set_amount(self.__amount - 1)
            return copy.deepcopy(self.__item)
    def get_amount(self) -> int:
        """Returns the current amount of items."""
        return self.__amount
    def get_name(self) -> str:
        """Returns item name."""
        return self.__item.get_name()
    def get_price(self) -> float:
        """Returns item price."""
        return self.__price