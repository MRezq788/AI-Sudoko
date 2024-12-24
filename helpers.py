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


def is_valid(board, row, col, num):
    for j in range(9):
        if board[row][j] == num and j != col:
            return False

    for i in range(9):
        if board[i][col] == num and i != row:
            return False

    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num and (i != row or j != col):
                return False

    return True

