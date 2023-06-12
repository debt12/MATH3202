from gurobipy import *

# Data
profit = [10, 6, 8, 4, 11, 9, 3]
P = range(len(profit))

Machines = ["Grinding", "VDrilling", "HDrilling", "Boring", "Planing"]
n = [4, 2, 3, 1, 1]
M = range(len(n))

# usage[P][M]
usage = [
    [0.5, 0.1, 0.2, 0.05, 0.00],
    [0.7, 0.2, 0.0, 0.03, 0.00],
    [0.0, 0.0, 0.8, 0.00, 0.01],
    [0.0, 0.3, 0.0, 0.07, 0.00],
    [0.3, 0.0, 0.0, 0.10, 0.05],
    [0.2, 0.6, 0.0, 0.00, 0.00],
    [0.5, 0.0, 0.6, 0.08, 0.05]
]

# months
T = range(6)

# maintenance[T][M]
maint = [
    [1, 0, 0, 0, 0],
    [0, 0, 2, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 1, 0, 1]
]

# market[P][T]
market = [
    [500, 600, 300, 200, 0, 500],
    [1000, 500, 600, 300, 100, 500],
    [300, 200, 0, 400, 500, 100],
    [300, 0, 0, 500, 100, 300],
    [800, 400, 500, 200, 1000, 1100],
    [200, 300, 400, 0, 300, 500],
    [100, 150, 100, 100, 0, 60]
]

maxstore = 100
storecost = 0.5
endstore = 50
monthhours = 16 * 24

fp = Model("Factory Planning")

# X[p,t] is amount produced
X = {(p, t): fp.addVar(vtype=GRB.INTEGER) for p in P for t in T}
# Y[p,t] is amount sold
Y = {(p, t): fp.addVar(vtype=GRB.INTEGER) for p in P for t in T}
# S[p,t] is amount stored at end of month
S = {(p, t): fp.addVar(vtype=GRB.INTEGER) for p in P for t in T}
# Z[t,m] is the number of machine m to maintain in month t
Z = {(t, m): fp.addVar(vtype=GRB.INTEGER) for t in T for m in M}

fp.setObjective(quicksum(profit[p] * Y[p, t] for p in P for t in T) -
                quicksum(storecost * S[p, t] for p in P for t in T), GRB.MAXIMIZE)

for t in T:
    # Usage constraint
    for m in M:
        fp.addConstr(quicksum(usage[p][m] * X[p, t] for p in P) <=
                     monthhours * (n[m] - Z[t, m]))

    for p in P:
        # Marketing
        fp.addConstr(Y[p, t] <= market[p][t])
        # Maximum storage
        fp.addConstr(S[p, t] <= maxstore)
        # Inventory
        if t > 0:
            fp.addConstr(S[p, t] == S[p, t - 1] + X[p, t] - Y[p, t])
        else:
            fp.addConstr(S[p, t] == X[p, t] - Y[p, t])

# Last period inventory
for p in P:
    fp.addConstr(S[p, T[-1]] >= endstore)

# Question 2 - Ensure we still do the same overall maintenance
for m in M:
    fp.addConstr(quicksum(Z[t, m] for t in T) == sum(maint[t][m] for t in T))

# Extension - Smooth the maintenance schedule
for t in T:
    fp.addConstr(quicksum(Z[t, m] for m in M) <= 2)
    fp.addConstr(quicksum(Z[t, m] for m in M) >= 1)

fp.optimize()

print("Profit =", fp.objVal)
print("Production")
for p in P:
    print([round(X[p, t].x) for t in T])
print("Sales")
for p in P:
    print([round(Y[p, t].x) for t in T])
print("Storage")
for p in P:
    print([round(S[p, t].x) for t in T])
print("Maintenance")
for m in M:
    print([round(Z[t, m].x) for t in T], Machines[m])


