from gurobipy import *

# Sets
Items = ["Chair", "Table"]  # Items from given table
Resources = ["Labour", "Wood"]  # Resources from given table
I = range(len(Items))
R = range(len(Resources))

# Data
p = [8, 5]  # Profit from selling a table and a chair
pRange = range(len(p))
u = [[1, 9], [1, 5]]  # Resources to build [chair, table] in terms of [[labour, wood]]
a = [6, 45]  # quantity of available resources [labour, wood]
aRange = range(len(a))
LB = [0, 0]
UB = [1000, 1000]

# Model
m = Model("Telfa")

# Variables
X = {pr: m.addVar(lb = LB[pr], ub = UB[pr], name = Items[pr]) for pr in pRange}  # number of items to build.

# Objective: Maximise profit
m.setObjective(quicksum(p[pr] * X[pr] for pr in pRange), GRB.MAXIMIZE)  # Maximise profit from building item i in Items

# Constraints

# Available Resources
for ar in aRange:
    m.addConstr(quicksum(X[pr] * u[pr][ar] for pr in pRange) <= a[ar])

# Optimise
m.optimize()

# Prints
print("Total profit", m.objVal)
