import tkinter as tk
from tkinter import messagebox, ttk
from arc_consistency import arc_consistency_solve
from backtracking import generate_puzzle, is_valid_move
from helpers import get_cell_value, set_cell_value

def create_cell(frame, row, col, validate_callback):
    cell = tk.Entry(frame, width=2, justify='center')
    cell.grid(row=row+1, column=col, padx=1, pady=1)
    cell.bind('<KeyRelease>', lambda e, r=row, c=col: validate_callback(e, r, c))
    
    if row % 3 == 0 and row != 0:
        cell.grid(pady=(3, 1))
    if col % 3 == 0 and col != 0:
        cell.grid(padx=(3, 1))
    
    return cell

def setup_gui(root):
    root.title("Sudoku Solver")
    cells = [[None for _ in range(9)] for _ in range(9)]
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0)
    
    mode_frame = ttk.Frame(main_frame)
    mode_frame.grid(row=0, column=0, columnspan=9, pady=(0, 10))
    ttk.Label(mode_frame, text="Mode:").pack(side=tk.LEFT)
    mode_var = tk.StringVar(value="1")  # AI mode by default
    
    # Create solve button here so we can reference it
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=10, column=0, columnspan=9, pady=(10, 0))
    solve_button = ttk.Button(button_frame, text="Solve")
    
    def mode_changed(*args):
        if mode_var.get() == "1":  # AI mode
            solve_button.config(state='normal')
        else:  # User mode
            solve_button.config(state='disabled')
    
    mode_var.trace('w', mode_changed)  # Track mode changes
    
    ttk.Radiobutton(mode_frame, text="AI Solver", variable=mode_var, 
                   value="1").pack(side=tk.LEFT)
    ttk.Radiobutton(mode_frame, text="User Input", variable=mode_var, 
                   value="2").pack(side=tk.LEFT)
    
    def validate_input(event, row, col):
        if mode_var.get() == "1":  # Disable input in AI mode
            return False
        cell = cells[row][col]
        value = cell.get()
        if value == '':
            return True
        try:
            num = int(value)
            if num < 1 or num > 9:
                raise ValueError
            if not is_valid_move(cells, row, col, num):
                messagebox.showerror("Invalid Move", 
                                   "This number violates Sudoku constraints!")
                cell.delete(0, tk.END)
                return False
        except ValueError:
            cell.delete(0, tk.END)
            return False
        return True
    
    for i in range(9):
        for j in range(9):
            cells[i][j] = create_cell(main_frame, i, j, validate_input)
    
    def clear_board():
        for i in range(9):
            for j in range(9):
                cells[i][j].config(state='normal')
                cells[i][j].delete(0, tk.END)
    
    def solve_board():
        board = [[get_cell_value(cells[i][j]) for j in range(9)] 
                for i in range(9)]
        if arc_consistency_solve(board):
            for i in range(9):
                for j in range(9):
                    if get_cell_value(cells[i][j]) == 0:
                        set_cell_value(cells[i][j], board[i][j])
        else:
            messagebox.showerror("Error", "No solution exists!")
    
    ttk.Button(button_frame, text="Generate", 
              command=lambda: generate_puzzle(cells)).pack(side=tk.LEFT, padx=5)
    solve_button.config(command=solve_board)
    solve_button.pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Clear", 
              command=clear_board).pack(side=tk.LEFT, padx=5)
    
    return cells