from gurobipy import *

m = Model("Set Covering")

# Sets
Towns = [1, 2, 3, 4, 5, 6]
T = range(len(Towns))

# Data
w = [(1, 2), (1, 2, 6), (3, 4), (3, 4, 5), (4, 5, 6), (2, 5, 6)]

# Variables
X = {t: m.addVar(vtype=GRB.BINARY) for t in T}

# Objective Function
m.setObjective(quicksum(X[t] for t in T), GRB.MINIMIZE)

# Constraints
for t in T:
    m.addConstr(quicksum(X[q-1] for q in w[t]) >= 1)

# Optimise
m.optimize()

# Prints
print("Total profit", m.objVal)