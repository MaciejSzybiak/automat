class Item:
    """Represents an item for use with Automats"""
    __itemName = ""
    def __init__(self, name):
        __itemName = name
    def get_name(self):
        """Returns item's name."""
        return self.__itemName