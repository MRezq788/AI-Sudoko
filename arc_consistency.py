puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]



def create_sudoku_csp(grid):

    domains = {}
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                domains[(row, col)] = list(range(1, 10))
            else:
                domains[(row, col)] = [grid[row][col]]

    def get_neighbors(cell):
        r, c = cell
        neighbors = set()

        for row in range(9):
            if row == r:
                continue
            neighbors.add((row, c))

        for col in range(9):
            if col == c:
                continue
            neighbors.add((r, col))

        subgrid_r, subgrid_c = 3 * (r // 3), 3 * (c // 3)
        for row in range(3):
            for col in range(3):
                if subgrid_r + row == r and subgrid_c + col == c:
                    continue
                neighbors.add((subgrid_r + row, subgrid_c + col))
        return neighbors

    arcs = set()
    for row in range(9):
        for col in range(9):
            for neighbor in get_neighbors((row, col)):
                arcs.add(((row, col), neighbor))

    return domains, arcs


def revise(cell1, cell2, domains):
    new_domain = []
    change = False
    for value1 in domains[cell1]:
        change2 = True
        for value2 in domains[cell2]:
            if value1 != value2:
                new_domain.append(value1)
                change2 = False
                break
        change = change or change2
    domains[cell1] = new_domain
    return change


def apply_arc_consistency(domains, arcs):
    change = True
    while change:
        change = False
        for arc in arcs:
            change = revise(arc[0], arc[1], domains)


def solvable(domains):
    for row in range(9):
        for col in range(9):
            if len(domains[(row, col)]) == 0:
                return False
    return True


def arc_consistency_solve(grid):
    domains, arcs = create_sudoku_csp(grid)
    ones1, ones2 = -1, 0

    while solvable(domains) and ones1 != ones2:
        ones1 = ones2
        ones2 = 0
        apply_arc_consistency(domains, arcs)
        for row in range(9):
            for col in range(9):
                if len(domains[(row, col)]) == 1:
                    ones2 += 1
                    grid[row][col] = domains[(row, col)][0]




for row in puzzle:
    print(row)
print("----------------------------------------")
print("----------------------------------------")

arc_consistency_solve(puzzle)

for row in puzzle:
    print(row)
print("----------------------------------------")
print("----------------------------------------")













