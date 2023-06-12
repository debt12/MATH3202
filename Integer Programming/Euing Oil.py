from gurobipy import *

m = Model("Euing Oil")

# Sets
J = [0, 1]
I = [0, 1]
B = [0, 1, 2]

# Data
r = [1.2, 1.4]
c = [2.5, 2, 1.5]

# Variables
X11 = m.addVar(name = "X11")
X12 = m.addVar(name = "X12")
X21 = m.addVar(name = "X21")
X22 = m.addVar(name = "X22")

Y1 = m.addVar(ub = 500, name = "Y1")
Y2 = m.addVar(ub = 500, name = "Y2")
Y3 = m.addVar(ub = 500, name = "Y3")

Z1 = m.addVar(vtype=GRB.BINARY, name = "Z1")
Z2 = m.addVar(vtype=GRB.BINARY, name = "Z2")
Z3 = m.addVar(vtype=GRB.BINARY, name = "Z3")

# Objective Function
m.setObjective(r[0] * (X11 + X12) + r[1] * (X21 + X22) -
               c[0] * Y1 - c[1] * Y2 - c[2] * Y3, GRB.MAXIMIZE)

# Constraints
m.addConstr(X11 >= 0.5 * (X11 + X12))
m.addConstr(X21 >= 0.6 * (X21 + X22))
m.addConstr(Y1 >= 500 * Z1)
m.addConstr(Y2 <= 500 * Z1)
m.addConstr(Y2 >= 500 * Z2)
m.addConstr(Y3 <= 500 * Z2)
m.addConstr(Y3 >= 500 * Z3)
m.addConstr(X11 + X21 <= 500 + Y1 + Y2 + Y3)
m.addConstr(X12 + X22 <= 1000)


# Optimise
m.optimize()

# Prints
print("Total profit", m.objVal)
for v in m.getVars():
    print(v.VarName, round(v.x, 2))

