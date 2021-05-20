#allowed coin values
coin_values = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]

class InvalidCoinValueException(Exception):
    """Signals that the coin had an invalid value passed in the constructor."""
    def __init__(self, value):
        super().__init__(f"Invalid coin value: {value}")

class Coin:
    """Represents a coin for use with Automats."""
    __value = 0
    def __init__(self, value):
        if value in coin_values:
            self.__value = value
        else:
            raise InvalidCoinValueException(value)
    def get_1gr():
        """Creates a new 1gr coin."""
        return Coin(0.01)
    def get_2gr():
        """Creates a new 2gr coin."""
        return Coin(0.02)
    def get_5gr():
        """Creates a new 5gr coin."""
        return Coin(0.05)
    def get_10gr():
        """Creates a new 10gr coin."""
        return Coin(0.1)
    def get_20gr():
        """Creates a new 20gr coin."""
        return Coin(0.2)
    def get_50gr():
        """Creates a new 50gr coin."""
        return Coin(0.5)
    def get_1zl():
        """Creates a new 1zl coin."""
        return Coin(1)
    def get_2zl():
        """Creates a new 2zl coin."""
        return Coin(2)
    def get_5zl():
        """Creates a new 5zl coin."""
        return Coin(5)