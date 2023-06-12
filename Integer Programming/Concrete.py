from gurobipy import *
import math
import random
import pylab

"""
Notes and Assumptions: 

"""

m = Model("Concrete")

def Distance(p1, p2):
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

# Sets
Num = 50
n = range(Num)
Square = 1000
random.seed(Num)
Plant = [(random.randint(0, Square), random.randint(0, Square)) for j in n]
Job = [(random.randint(0, Square), random.randint(0, Square)) for i in n]


# Data
d = [[Distance(Plant[i], Job[j]) for j in n] for i in n]

# Variables
X = [[m.addVar(vtype=GRB.BINARY) for j in n] for i in n]

# Objective Function
m.setObjective(quicksum(d[i][j] * X[i][j] for j in n for i in n), GRB.MINIMIZE)

# Constraints
c1 = [m.addConstr(quicksum(X[i][j] for j in n) == 1) for i in n]
c1 = [m.addConstr(quicksum(X[i][j] for i in n) == 1) for j in n]

# Optimise
m.optimize()

# Prints
[pylab.plot(Plant[i][0], Plant[i][1], color = 'black', marker = '*') for i in n]
[pylab.plot(Plant[i][0], Job[j][0], Plant[i][1], Job[j][1], color = 'black') for i in n for j in n if X[i][j].x > 0.99]

pylab.show()