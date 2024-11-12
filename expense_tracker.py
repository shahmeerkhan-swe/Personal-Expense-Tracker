import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime

conn = sqlite3.connect('expense_tracker.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    date TEXT, 
    category TEXT,
    amount REAL,
    description TEXT
)
''')

conn.commit() 

root = tk.Tk()
root.title("Expense Tracker")

tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
date_entry = tk.Entry(root) 
date_entry.grid(row=0, column=1)
date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

tk.Label(root, text="Category:").grid(row=1, column=0)
category_entry = tk.Entry(root) 
category_entry.grid(row=1, column=1)

tk.Label(root, text="Amount:").grid(row=2, column=0)    
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1)  

tk.Label(root, text="Description:").grid(row=3, column=0)
description_entry = tk.Entry(root)
description_entry.grid(row=3, column=1)

def add_expense(): 
    date = date_entry.get()
    category = category_entry.get() 
    amount = amount_entry.get()
    description = description_entry.get()

    if not date or not category or not amount:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return
    
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showwarning("Warning", "Amount must be a number.")
        return
    
    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                    (date, category, amount, description))
    
    conn.commit()

    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    
    date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
    messagebox.showinfo("Success", "Expense added successfully.")

add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.grid(row=4, column=0, columnspan=2)


def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    view_window = tk.Toplevel(root)
    view_window.title("View Expenses")

    total_amount = sum(expense[3] for expense in expenses)
    tk.Label(view_window, text=f"Total amount: {total_amount:.2f}").pack()

    for expense in expenses:
        tk.Label(view_window, text=f"Date: {expense[1]}, Category: {expense[2]}, Amount: {expense[3]}, Description: {expense[4]}").pack()

view_button = tk.Button(root, text="View Expenses", command=view_expenses)
view_button.grid(row=5, column=0, columnspan=2)

root.mainloop()

conn.close() 




