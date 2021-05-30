from tkinter.constants import BOTH
import package.automat.automat as at
import tkinter as tk
import tkinter.ttk as ttk
from typing import Callable

class AutomatHandler():
    def __init__(self) -> None:
        self.automat = at.Automat(5)
        self.numberText: tk.StringVar
        self.coinText: tk.StringVar
        self.item_number_text = ''

    def display_popup(self, text: str) -> None:
        """Displays a popup window with information string provided by 'text' variable."""
        popup = tk.Toplevel()
        popup.geometry('200x120+400+400')
        popup.wm_title("Info")
        popup.grid_columnconfigure(0, pad=3, weight=1)
        popup.grid_rowconfigure(0, pad=3, weight=1)
        popup.grid_rowconfigure(1, pad=3, weight=1)

        #create label with info
        label = tk.Label(popup, text=text)
        label.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

        #create OK button
        b = ttk.Button(popup, text="OK", command=popup.destroy)
        b.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

    def check_item(self) -> None:
        """Checks if item of the given number exists and tries to buy it.
        Displays apropriate info when the item is not available, the number is
        incorrect, etc."""
        itemNumber = int(self.item_number_text)
        try:
            #get item info
            name, price, amount = self.automat.get_item_details(itemNumber)
        except at.InvalidItemNumberException:
            return
        try:
            #try to buy item
            change, item = self.automat.pay_for_item(itemNumber)
            for c in change:
                self.automat.insert_coin(c)
            self.update_coins_text()
            self.display_popup(f'Bought item: {item.get_name()}\n\nChange was added\nback to your coins')
        except at.NotEnoughMoneyException:
            self.display_popup(f'Selected item: {name}\nPrice: {price}\nAmount: {amount}')
        except at.ExactChangeOnlyException:
            self.display_popup(f'Exact change only!')
        except at.NoItemsLeftException:
            self.display_popup('Item not available')
        finally:
            #clear item number text
            self.item_number_text = ''
            self.update_number_text()

    def update_coins_text(self) -> None:
        """Sets coins display based on the contents of 'coins' list."""
        amount = self.automat.get_inserted_coins_value()
        self.coinText.set(f'{amount}')

    def update_number_text(self) -> None:
        """Sets number text from 'item_number_text' string."""
        self.numberText.set(self.item_number_text)

    def on_coin_btn_click(self, value: float) -> None:
        """Callback for clicking a coin button."""
        self.automat.insert_coin(at.Coin(value))
        self.update_coins_text()

    def on_number_btn_click(self, value: int) -> None:
        """Callback for clicking a number button."""
        self.item_number_text += f'{value}' #append new digit to the number string
        self.update_number_text()
        self.check_item()

    def on_clear_number_btn_click(self) -> None:
        """Clears the entered number."""
        self.item_number_text = ''
        self.update_number_text()

    def on_clear_coins_btn_click(self) -> None:
        """Clears the entered coins. In reality it would
        return the coins to the customer."""
        self.automat.clear_inserted_coins()
        self.update_coins_text()

class Application(tk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.master = master
        self.master.title('Vending machine')
        self.master.geometry('400x300+300+300')
        self.handler = AutomatHandler()
        self.create_widgets()

    def create_widgets(self) -> None:
        """Creates GUI elements."""
        ttk.Style().configure('TButton', padding=(4, 4, 4, 4))
        #create grid layout
        for i in range(0, 6):
            self.grid_columnconfigure(i, pad=3, weight=1)

        self.grid_rowconfigure(0, pad=3, weight=0)
        self.grid_rowconfigure(1, pad=3, weight=0)
        for i in range(2, 6):
            self.grid_rowconfigure(i, pad=3, weight=1)

        #create item number display
        label = tk.Label(self, text="Item number:")
        label.grid(row=0, columnspan=3, rowspan=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        self.handler.numberText = tk.StringVar()
        numberText = tk.Entry(self, justify='right', state=tk.DISABLED, textvariable=self.handler.numberText)
        numberText.grid(row=1, column=0, columnspan=3, rowspan=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        
        #create coins display
        label = tk.Label(self, text="Coins:")
        label.grid(row=0, column=3, columnspan=3, rowspan=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        self.handler.coinText = tk.StringVar()
        coinText = tk.Entry(self, justify='right', state=tk.DISABLED, textvariable=self.handler.coinText)
        coinText.grid(row=1, column=3, columnspan=3, rowspan=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

        #create buttons
        self.create_keypad(2, 0, self.handler.on_number_btn_click, [i for i in range(1, 10)], True)
        self.create_keypad(2, 3, self.handler.on_coin_btn_click, at.coin_values, False)
        button = tk.Button(self, text='CLEAR NUMBER', command=self.handler.on_clear_number_btn_click)
        button.grid(row=5, column=1, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        button = tk.Button(self, text='CLEAR COINS', command=self.handler.on_clear_coins_btn_click)
        button.grid(row=5, column=3, columnspan=3, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

        self.pack(fill="both", expand=True)

    def create_keypad(self, n_row: int, n_column: int, func: Callable, values: list, add_zero: bool) -> None:
        """Creates a 0-9 keypad with specified values and button callback."""
        start_row = n_row + 2
        for i in range(0, 9):
            button = tk.Button(self, text=f'{values[i]}', command=lambda value = values[i]: func(value))
            button.grid(row=start_row - (i // 3), column=i % 3 + n_column, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        if add_zero:
            button = tk.Button(self, text='0', command=lambda: func(0))
            button.grid(row=n_row + 3, column=n_column, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    app.mainloop()