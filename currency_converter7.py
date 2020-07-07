# Python program to convert the currency
# of one country to that of another country: NIDHI SHARMA

# Import the modules needed
import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

one_year_from_now = datetime.now() + relativedelta(years=1)
date_formated = one_year_from_now.strftime("%d/%m/%Y")


def callback(input):
    if input == "":
        return True
    try:
        input = float(input)
    except ValueError:
        return False
    else:
        return True

    
def convert1(from_country_var, to_country_var, amount=1.0):
    c_amount = c.convert(from_country_var, to_country_var, amount)
    tk.Label(root1, fg="DeepPink2", bg="misty rose",
             text=f" {amount} {from_country_var} equals ", width=30, font=("Courier", 15)).grid(row=0, column=0)
    tk.Label(root1, fg="DeepPink2", bg="misty rose",
             text=f" {c_amount} {to_country_var}", width=30, font=("Courier", 20)).grid(row=1, column=0)
    return c_amount


def convert(event):
    from_country_var = codes[names.index(from_country.get())]
    to_country_var = codes[names.index(to_country.get())]
    convert1(from_country_var, to_country_var)
    converted_amount_entry.delete(0, tk.END)
    converted_amount_entry.insert(0, "")
    if from_country_var == to_country_var:
        mb.showerror("ERROR", "FROM COUNTRY AND TO COUNTRY CAN'T HAVE SAME VALUE")
    else:
        if amount_var.get() == '':
            pass
        else:
            amount = float(amount_var.get())
            converted_amount = convert1(from_country_var, to_country_var, amount)
            converted_amount_entry.insert(0, str(converted_amount))


class Currency_convertor:
    # empty dict to store the conversion rates
    rates = {}
    symbol = {}

    def __init__(self, url, url2):
        data = requests.get(url).json()
        data2 = requests.get(url2).json()
        # Extracting only the rates from the json data
        self.rates = data["rates"]
        self.symbol = data2["symbols"]

    # function to do a simple cross multiplication between the amount and the conversion rates
    def convert(self, from_currency, to_currency, amount):
        if from_currency != 'EUR':
            amount = amount / self.rates[from_currency]
        # limiting the precision to 4 decimal places
        amount = round(amount * self.rates[to_currency], 4)
        return amount


# Driver code

if __name__ == "__main__":
    url = str.__add__('http://data.fixer.io/api/latest?access_key=', 'b63cf4a76e5fbd36f0a024fb92028ef2')
    url2 = str.__add__('http://data.fixer.io/api/symbols?access_key=', 'b63cf4a76e5fbd36f0a024fb92028ef2')

    c = Currency_convertor(url, url2)

    names = list(c.symbol.values())
    codes = list(c.symbol.keys())

    # creating window
    root = tk.Tk()
    root1 = tk.Frame(root, background="misty rose")
    # root1.config(background='misty rose')
    reg = root.register(callback)

    root1.grid(row=7, columnspan=5)
    convert1("USD", "INR")
    root.title("CURRENCY CONVERTER")
    root.configure(background='lavender blush')

    from_country_label = tk.Label(root, text="From Currency: ", bg="misty rose", fg="DeepPink2")

    to_country_label = tk.Label(root, text="To Currency: ", bg="misty rose", fg="DeepPink2")

    amount_label = tk.Label(root, text="Actual Amount: ", bg="misty rose", fg="DeepPink2")

    converted_amount_label = tk.Label(root, text="Converted Amount: ", bg="misty rose", fg="DeepPink2")

    # from country variable: stores full currency name
    from_country = tk.StringVar()

    # from country drop-down
    from_country_entry = ttk.Combobox(root, width=30, textvariable=from_country, state="readonly")
    from_country_entry['values'] = names  # names: list of names of all currencies
    from_country_entry.set("United States Dollar")

    # to country variable: stores full currency name
    to_country = tk.StringVar()
    to_country_entry = ttk.Combobox(root, width=30, textvariable=to_country, state="readonly")
    to_country_entry['values'] = names  # names: list of names of all currencies
    to_country_entry.set("Indian Rupee")

    # amount variable: stores amount to be changed in string
    amount_var = tk.StringVar()

    # entry box for amount
    amount_entry = ttk.Entry(root, width=33, textvariable=amount_var)

    amount_entry.focus()  # the app starts, focus automatically moves to amount entry box
    amount_entry.config(validate="key", validatecommand=(reg, '%P'))
    # Entry box for converted amount
    converted_amount_entry = ttk.Entry(root, width=33)
    #  creating gui
    tk.Label(root, text="REAL TIME CURRENCY CONVERTER", fg="magenta4", bg="plum1",
             font=("Courier", 20)).grid(row=0, columnspan=5, padx=25, pady=5)
    tk.Label(root, text="DATE: " + str(date_formated) + "        " + "TIME: " + str(time.strftime("%H:%M:%S")),
             fg="maroon4",
             bg="pink").grid(row=1, columnspan=5, padx=25, pady=4)
    from_country_label.grid(row=3, column=0, columnspan=2, padx=25, pady=4)
    to_country_label.grid(row=3, column=3, columnspan=2, padx=25, pady=4)
    from_country_entry.grid(row=4, column=0, columnspan=2, padx=25, pady=4)
    to_country_entry.grid(row=4, column=3, columnspan=2, padx=25, pady=4)
    amount_label.grid(row=5, column=0, columnspan=2, padx=25, pady=4)
    converted_amount_label.grid(row=5, column=3, columnspan=2, padx=25, pady=4)
    amount_entry.grid(row=6, column=0, columnspan=2, padx=25, pady=4)
    converted_amount_entry.grid(row=6, column=3, columnspan=2, padx=25, pady=4)
    # binding combobox with convert and any button pressed in window
    root.bind_all("<Key>", convert)
    to_country_entry.bind("<<ComboboxSelected>>", convert)
    from_country_entry.bind("<<ComboboxSelected>>", convert)

    root.mainloop()
# End of code
