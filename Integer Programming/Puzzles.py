from gurobipy import *

R = range(9)
C = range(9)
N = range(9)

# Data for "Tough Puzzle" on sudoku.com.au 2023-03-28
puzzle = [
    [0, 0, 6], [0, 5, 2],
    [1, 0, 7], [1, 5, 3],
    [2, 4, 8], [2, 6, 9], [2, 7, 3],
    [3, 1, 2], [3, 5, 8],
    [4, 0, 1], [4, 2, 8], [4, 6, 6], [4, 8, 4],
    [5, 3, 9], [5, 7, 2],
    [6, 1, 5], [6, 2, 3], [6, 4, 4],
    [7, 3, 8], [7, 8, 2],
    [8, 3, 6], [8, 8, 7]
]

m = Model("Sudoku")

X = {(i, j, k): m.addVar(vtype=GRB.BINARY) for i in R for j in C for k in N}

# only once per row
for i in R:
    for k in N:
        m.addConstr(quicksum(X[i, j, k] for j in C) == 1)

# only once per column
for j in C:
    for k in N:
        m.addConstr(quicksum(X[i, j, k] for i in R) == 1)

# only once per square
for a in range(3):
    for b in range(3):
        for k in N:
            m.addConstr(quicksum(X[i, j, k] for j in range(3 * b, 3 * (b + 1)) for i in range(3 * a, 3 * (a + 1))) == 1)

# only one digit per cell
for i in R:
    for j in C:
        m.addConstr(quicksum(X[i, j, k] for k in N) == 1)

# satisfy puzzle data
for p in puzzle:
    m.addConstr(X[p[0], p[1], p[2] - 1] == 1)

m.optimize()

for i in R:
    for j in C:
        for k in N:
            if X[i, j, k].x > 0.99:
                print(k + 1, end='')
    print()


