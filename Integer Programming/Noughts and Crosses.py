import math
import random
from gurobipy import *

# Sets
N = range(9)
Lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
L = range(len(Lines))

# Data
numcrosses = 1

# Model
m = Model("Noughts and Crosses")

#Variables
X = [m.addVar(vtype=GRB.BINARY) for i in N]
Y = [m.addVar(vtype=GRB.BINARY) for l in L]

# Objective
m.setObjective(quicksum(Y))

# Constraints
[m.addConstr(quicksum(X[i] for i in Lines[l]) + Y[l] >= 1) for l in L]
[m.addConstr(quicksum(X[i] for i in Lines[l]) - Y[l] <= 1) for l in L]
[m.addConstr(quicksum(X) == numcrosses)]

# Optimise
m.optimize()

# Prints
for i in range(3):
    lstr = ''
    for j in range(3):
        lstr += "X" if X[i*3+j].x > 0.99 else "O"
    print(lstr)