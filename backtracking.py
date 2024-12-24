import random
from helpers import get_cell_value, set_cell_value, is_valid
import copy

#generates a solved board
def backtrack_solve(board, row=0, col=0):
    if col == 9:
        row += 1
        col = 0
    if row == 9:
        return True
        
    if board[row][col] != 0:
        return backtrack_solve(board, row, col + 1)
        
    nums = list(range(1, 10))
    random.shuffle(nums)
    for num in nums:
        if is_valid(board, row, col, num):
            board[row][col] = num
            if backtrack_solve(board, row, col + 1):
                return True
            board[row][col] = 0
    
    return False

#generates a puzzle
def generate_puzzle(cells):
    board = [[0] * 9 for _ in range(9)]
    _generate_filled(board)
    _remove_numbers(board, cells)

#fills the board with a solved board
def _generate_filled(board):
    backtrack_solve(board)
    return board

#removes random 45 numbers from the board
def _remove_numbers(board, cells):
    for i in range(9):
        for j in range(9):
            set_cell_value(cells[i][j], board[i][j])
    
    positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(positions)
    
    for pos in positions[:45]:
        row, col = pos
        temp = board[row][col]
        board[row][col] = 0
        
        board_copy = copy.deepcopy(board)
        if not _is_unique(board_copy):
            board[row][col] = temp
            set_cell_value(cells[row][col], temp, True)
        else:
            set_cell_value(cells[row][col], 0)
            cells[row][col].config(state='normal')

#checks if the board has a unique solution
def _is_unique(board):
    solutions = []
    
    def solve(b):
        if len(solutions) > 1:
            return
        if not any(0 in row for row in b):
            solutions.append([row[:] for row in b])
            return
        
        row, col = next((i, j) for i in range(9) for j in range(9) if b[i][j] == 0)
        for num in range(1, 10):
            if is_valid(b, row, col, num):
                b[row][col] = num
                solve(b)
                b[row][col] = 0
    
    solve(board)
    return len(solutions) == 1

#checks if a move is valid
def is_valid_move(cells, row, col, num):
    for j in range(9):
        if j != col and get_cell_value(cells[row][j]) == num:
            return False
    
    for i in range(9):
        if i != row and get_cell_value(cells[i][col]) == num:
            return False
    
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if (i != row or j != col) and get_cell_value(cells[i][j]) == num:
                return False
    
    return True
