#allowed coin values
coin_values = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]

class InvalidCoinValueException(Exception):
    """Signals that the coin had an invalid value passed in the constructor."""
    def __init__(self, value: float) -> None:
        super().__init__(f"Invalid coin value: {value}")

class Coin:
    """Represents a coin for use with Automats."""
    def __init__(self, value: float) -> None:
        if value in coin_values:
            self.__value = value
        else:
            raise InvalidCoinValueException(value)
    def get_value(self) -> float:
        """Returns the value of a coin."""
        return self.__value
    def __eq__(self, other: object) -> bool:
        """Compares coin values."""
        return isinstance(other, Coin) and self.__value == other._Coin__value