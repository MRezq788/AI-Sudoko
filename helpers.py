from tkinter import END

def get_cell_value(cell):
    value = cell.get()
    return int(value) if value.isdigit() else 0

def set_cell_value(cell, value, readonly=False):
    cell.config(state='normal')
    cell.delete(0, END)
    if value != 0:
        cell.insert(0, str(value))
    if readonly:
        cell.config(state='readonly')

