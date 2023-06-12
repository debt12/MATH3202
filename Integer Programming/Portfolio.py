from gurobipy import *

# Part 1

# This is an example of using a dictionary to define a set and associated data
Products = {
    'Cars (Germany)': 10.3,
    'Cars (Japan)': 10.1,
    'Computers (USA)': 11.8,
    'Computers (Singapore)': 11.4,
    'Appliances (Europe)': 12.7,
    'Appliances (Asia)': 12.2,
    'Insurance (Germany)': 9.5,
    'Insurance (USA)': 9.9,
    'Short-term bonds': 3.6,
    'Medium-term bonds': 4.2
}

m = Model('Portfolio optimisation')

X = {p: m.addVar() for p in Products}

m.setObjective(quicksum(Products[p] * X[p] / 100 for p in Products), GRB.MAXIMIZE)
Constraints = {
    "Total": m.addConstr(quicksum(X[p] for p in Products) == 100000),
    "C1": m.addConstr(X['Cars (Germany)'] + X['Cars (Japan)'] <= 30000),
    "C2": m.addConstr(X['Computers (USA)'] + X['Computers (Singapore)'] <= 30000),
    "C3": m.addConstr(X['Appliances (Europe)'] + X['Appliances (Asia)'] <= 20000),
    "C4": m.addConstr(X['Insurance (Germany)'] + X['Insurance (USA)'] >= 20000),
    "C5": m.addConstr(X['Short-term bonds'] + X['Medium-term bonds'] >= 25000),
    "C6": m.addConstr(X['Short-term bonds'] - 0.4 * X['Medium-term bonds'] >= 0),
    "C7": m.addConstr(X['Cars (Germany)'] + X['Insurance (Germany)'] <= 50000),
    "C8": m.addConstr(X['Computers (USA)'] + X['Insurance (USA)'] <= 40000)
}
m.optimize()

print('Return is:', m.objVal)
for p in Products:
    print(p, round(X[p].x, 2))
    # , round(X[p].SAOBJLow,3),round(X[p].Obj,3),
    # round(X[p].SAOBJUp,3))

# for c in Constraints:
#     print(c, round(Constraints[c].slack,1), round(100*Constraints[c].pi,2),
#           round(Constraints[c].SARHSLow,1),Constraints[c].RHS,round(Constraints[c].SARHSUp,1))

# Part 2

# Business as usual, downturn, upturn, crash
ScenarioProb = [0.8, 0.15, 0.04, 0.01]
S = range(len(ScenarioProb))

Year2Return = {
    'Cars (Germany)': [10.3, 5.1, 11.8, -30.0],
    'Cars (Japan)': [10.1, 4.4, 12.0, -35.0],
    'Computers (USA)': [11.8, 10.0, 12.5, 1.0],
    'Computers (Singapore)': [11.4, 11.0, 11.8, 2.0],
    'Appliances (Europe)': [12.7, 8.2, 13.4, -10.0],
    'Appliances (Asia)': [12.2, 8.0, 13.0, -12.0],
    'Insurance (Germany)': [9.5, 2.0, 14.7, -5.4],
    'Insurance (USA)': [9.9, 3.0, 12.9, -4.6],
    'Short-term bonds': [3.6, 4.2, 3.1, 5.9],
    'Medium-term bonds': [4.2, 4.7, 3.5, 6.3]
}

Y = {(p, s): m.addVar() for p in Products for s in S}

m.setObjective(quicksum(Products[p] * X[p] / 100 for p in Products) +
               quicksum(ScenarioProb[s] * Year2Return[p][s] * Y[p, s] / 100
                        for p in Products for s in S), GRB.MAXIMIZE)

for s in S:
    m.addConstr(quicksum(Y[p, s] for p in Products) <= 100000)
    for p in Products:
        m.addConstr(Y[p, s] <= 10000 + X[p])
        m.addConstr(Y[p, s] >= X[p] - 10000)

m.optimize()

print('First year return is:', sum(Products[p] * X[p].x / 100 for p in Products))
for p in Products:
    print('    ', p, round(X[p].x, 2))
for s in S:
    print('Second year', s, 'return:', sum(Year2Return[p][s] * Y[p, s].x / 100 for p in Products))
    for p in Products:
        print('    ', p, round(Y[p, s].x, 2))

W = {p: m.addVar(vtype=GRB.BINARY) for p in Products}
Z = {(p, s): m.addVar(vtype=GRB.BINARY) for p in Products for s in S}

for p in Products:
    m.addConstr(X[p] <= 100000 * W[p])
    m.addConstr(X[p] >= 10000 * W[p])
    for s in S:
        m.addConstr(Y[p, s] <= 100000 * Z[p, s])
        m.addConstr(Y[p, s] >= 10000 * Z[p, s])

m.optimize()

print('First year return is:', sum(Products[p] * X[p].x / 100 for p in Products))
for p in Products:
    print('    ', p, round(X[p].x, 2))
for s in S:
    print('Second year', s, 'return:', sum(Year2Return[p][s] * Y[p, s].x / 100 for p in Products))
    for p in Products:
        print('    ', p, round(Y[p, s].x, 2))


