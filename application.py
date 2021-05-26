from tkinter.constants import BOTH
import package.automat.automat as at
import tkinter as tk
import tkinter.ttk as ttk
from typing import Callable

class AutomatHandler():
    def __init__(self) -> None:
        self.automat = at.Automat(5)
        self.numberText = None
        self.coinText = None

    def on_coin_btn_click(self, value: int) -> None:
        print(f'Coin: {value}')
    def on_number_btn_click(self, value: int) -> None:
        print(f'Number: {value}')
    def on_clear_number_btn_click(self) -> None:
        print('Clear number')
    def on_clear_coins_btn_click(self) -> None:
        print('Clear coins')


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
        self.grid_columnconfigure(0, pad=3, weight=1)
        self.grid_columnconfigure(1, pad=3, weight=1)
        self.grid_columnconfigure(2, pad=3, weight=1)
        self.grid_columnconfigure(3, pad=3, weight=1)
        self.grid_columnconfigure(4, pad=3, weight=1)
        self.grid_columnconfigure(5, pad=3, weight=1)

        self.grid_rowconfigure(0, pad=3, weight=0)
        self.grid_rowconfigure(1, pad=3, weight=0)
        self.grid_rowconfigure(2, pad=3, weight=1)
        self.grid_rowconfigure(3, pad=3, weight=1)
        self.grid_rowconfigure(4, pad=3, weight=1)
        self.grid_rowconfigure(5, pad=3, weight=1)

        #create item number display
        label = tk.Label(self, text="Item number:")
        label.grid(row=0, columnspan=3, rowspan=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        self.handler.numberText = tk.Entry(self, justify='right', state=tk.DISABLED)
        self.handler.numberText.grid(row=1, column=0, columnspan=3, rowspan=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        
        #create coins display
        label = tk.Label(self, text="Coins:")
        label.grid(row=0, column=3, columnspan=3, rowspan=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        self.handler.coinText = tk.Entry(self, justify='right', state=tk.DISABLED)
        self.handler.coinText.grid(row=1, column=3, columnspan=3, rowspan=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

        #create buttons
        self.createKeypad(2, 0, self.handler.on_number_btn_click, [i for i in range(1, 10)], True)
        self.createKeypad(2, 3, self.handler.on_coin_btn_click, at.coin_values, False)
        button = tk.Button(self, text='CLEAR NUMBER', command=self.handler.on_clear_number_btn_click)
        button.grid(row=5, column=1, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        button = tk.Button(self, text='CLEAR COINS', command=self.handler.on_clear_coins_btn_click)
        button.grid(row=5, column=3, columnspan=3, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

        self.pack(fill="both", expand=True)

    def createKeypad(self, n_row: int, n_column: int, func: Callable, values: list, add_zero: bool) -> None:
        """Creates a 0-9 keypad with specified values and button callback."""
        start_row = n_row + 2
        for i in range(1, 10):
            button = tk.Button(self, text=f'{values[i - 1]}', command=lambda value = values[i - 1]: func(value))
            button.grid(row=start_row - ((i-1) // 3), column=(i - 1) % 3 + n_column, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        if add_zero:
            button = tk.Button(self, text='0', command=lambda: func(0))
            button.grid(row=n_row + 3, column=n_column, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    app.mainloop()