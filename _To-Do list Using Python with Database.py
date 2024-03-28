#!/usr/bin/env python
# coding: utf-8

# In[2]:


import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import sqlite3
import re
from tkcalendar import DateEntry

def sanitize_table_name(name):
    return re.sub(r'[^a-zA-Z0-9]', '_', name)

def add_user_name():
    global user_name
    user_name = user_name_entry.get()
    if user_name:
        user_name = sanitize_table_name(user_name)
        welcome_label.config(text=f"Welcome, {user_name}!", bg="#98FB98")
        user_name_entry.delete(0, tk.END)

        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        
        # Modify the CREATE TABLE statement to include user's name in the table name
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {user_name} (task_name TEXT, task_date DATE)')
        
        conn.commit()
        conn.close()
    else:
        messagebox.showwarning("Warning", "Please enter your name.")
line_number = 1  # Initialize line number to 1

def add_task():
    global line_number  # Use the global line_number variable
    task = entry.get()
    date = date_entry.get_date()

    if task:
        is_first_task = not listbox.get(1.0, tk.END).strip()
        if is_first_task:
            listbox.insert(tk.END, f'{line_number}. {task}\n')  # Add line number
        else:
            listbox.insert(tk.END, f'{line_number}. {task}\n')

        line_number += 1  # Increment the line number
        entry.delete(0, tk.END)

        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute(f'INSERT INTO {user_name} (task_name, task_date) VALUES (?, ?)', (task, date))
        conn.commit()
        conn.close()
    else:
        messagebox.showwarning("Warning", "Please enter a task.")

def view_previous_tasks():
    # Get the selected date from the DateEntry widget
    date_to_view = date_view_calendar.get_date()

    if date_to_view:
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute(f'SELECT task_name FROM {user_name} WHERE task_date = ?', (date_to_view,))
        tasks = cursor.fetchall()
        conn.close()

        listbox.delete(1.0, tk.END)
        for i, task in enumerate(tasks, 1):
            listbox.insert(tk.END, f'{i}. {task[0]} ({date_to_view})\n')
    else:
        messagebox.showwarning("Warning", "Please select a date to view tasks for.")

def delete_task():
    try:
        selected_start = listbox.index(tk.SEL_FIRST)
        selected_end = listbox.index(tk.SEL_LAST)
        if selected_start and selected_end:
            listbox.delete(selected_start, selected_end)

            conn = sqlite3.connect('tasks.db')
            cursor = conn.cursor()
            selected_text = listbox.get(selected_start, selected_end)
            cursor.execute(f'DELETE FROM {user_name} WHERE task_name = ?', (selected_text,))
            conn.commit()
            conn.close()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to delete.")

def delete_all_tasks():
    confirmed = messagebox.askyesno("Delete All", "Are you sure you want to delete all tasks?")
    if confirmed:
        listbox.delete(1.0, tk.END)

        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM {user_name}')
        conn.commit()
        conn.close()

def delete_user_account():
    confirmed = messagebox.askyesno("Delete Account", "Are you sure you want to delete your account and all tasks?")
    if confirmed:
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute(f'DROP TABLE IF EXISTS {user_name}')
        conn.commit()
        conn.close()

        welcome_label.config(text="")
        listbox.delete(1.0, tk.END)
        user_name_entry.delete(0, tk.END)

def exit_app():
    root.destroy()

def set_icon():
    global Imageicon
    Imageicon = PhotoImage(file='C:\\Users\\Sis\\OneDrive\\Pictures\\sr tkinter image\\images.png')
    root.iconphoto(False, Imageicon)

root = tk.Tk()
root.title("To-Do List")

root.configure(bg="#000000")
root.geometry("725x550")
root.after(0, set_icon)

frame = tk.Frame(root)
frame.grid(row=0, column=0, columnspan=3, pady=10)

user_name_label = tk.Label(frame, text="Enter Your Name:", font=("Arial", 12))
user_name_label.grid(row=0, column=0, padx=5, pady=5)

user_name_entry = tk.Entry(frame, font=("Arial", 12), width=20)
user_name_entry.grid(row=0, column=1, padx=5, pady=5)

add_user_name_button = tk.Button(frame, text="Add Name", font=("Arial", 12), bg="#98FB98", command=add_user_name)
add_user_name_button.grid(row=0, column=2, padx=5, pady=5)

welcome_label = tk.Label(root, text="", font=("Arial", 12), bg="#98FB98")
welcome_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

entry = tk.Entry(root, font=("Arial", 12), bg="#F0E68C", width=38)
entry.grid(row=2, column=0, padx=5, pady=5)

date_label = tk.Label(root, text="Enter Date (YYYY-MM-DD):", font=("Arial", 12))
date_label.grid(row=2, column=1, padx=5, pady=5)


date_entry = DateEntry(root, font=("Arial", 12), bg="#F0E68C", width=15)
date_entry.grid(row=2, column=2, padx=5, pady=5)

add_button = tk.Button(root, text="Add Task", font=("Arial", 12), bg="#98FB98", command=add_task)
add_button.grid(row=4, column=0, padx=5, pady=5)

date_view_label = tk.Label(root, text="View Tasks for Date:", font=("Arial", 12))
date_view_label.grid(row=3, column=1, padx=5, pady=5)

date_view_calendar = DateEntry(root, font=("Arial", 12), bg="#F0E68C", width=15)
date_view_calendar.grid(row=4, column=2, padx=5, pady=5)


view_button = tk.Button(root, text="View Tasks", font=("Arial", 12), bg="#90EE90", command=view_previous_tasks)
view_button.grid(row=4, column=1, padx=5, pady=5)

listbox = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), bg="#E0FFFF", width=70, height=10)
listbox.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

listbox_scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=listbox.xview)
listbox_scrollbar.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

listbox.config(xscrollcommand=listbox_scrollbar.set)

delete_button = tk.Button(root, text="Delete Task", font=("Arial", 12), bg="#90EE90", command=delete_task)
delete_button.grid(row=7, column=0, columnspan=1, padx=5, pady=5)

delete_all_button = tk.Button(root, text="Delete All Tasks", font=("Arial", 12), bg="#90EE90", command=delete_all_tasks)
delete_all_button.grid(row=7, column=1, columnspan=2, padx=5, pady=5)

delete_account_button = tk.Button(root, text="Delete Account", font=("Arial", 12), bg="#FF6B6B", command=delete_user_account)
delete_account_button.grid(row=9, column=0, columnspan=1, padx=5, pady=5)

exit_button = tk.Button(root, text="Exit", font=("Arial", 12), bg="#90EE90", command=exit_app)
exit_button.grid(row=9, column=1, columnspan=2, padx=5, pady=5)

root.mainloop()


# In[ ]:




