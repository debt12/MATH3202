from gurobipy import *

"""
Notes and Assumptions: 

"""

m = Model("ClothCo")

# Sets
Items = ["Shirts", "Shorts", "Pants"]
Resources = ["Labour", "Cloth"]

I = range(len(Items))
R = range(len(Resources))

# Data
p = [12, 8, 15] # profit for item i in I
c = [200, 150, 100] # rental cost for item i in I
u = [[3, 2, 6], [4, 3, 4]] # amount of resources r in R required to build i in I
a = [6, 4, 8] # amount of available resources r in R

# Variables
X = {i: m.addVar(vtype=GRB.INTEGER) for i in I}  # number of items to build.
Y = {i: m.addVar(vtype=GRB.BINARY) for i in I} # if item i in I is built

# Objective Function: Maximise profit
m.setObjective(quicksum(p[i]*X[i] - c[i]*Y[i] for i in I), GRB.MAXIMIZE)

# Constraints

# Available resources
for r in R:
    m.addConstr(quicksum(u[i][r]*X[i] for i in I) <= a[r])

# Non Neg
for i in I:
    m.addConstr(X[i] >= 0)

# Optimise
m.optimize()

# Prints
print("Total profit", m.objVal)


