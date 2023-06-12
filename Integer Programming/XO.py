import math
import random
from gurobipy import *

N = range(9)
Lines = [
  [0,1,2],
  [3,4,5],
  [6,7,8],
  [0,3,6],
  [1,4,7],
  [2,5,8],
  [0,4,8],
  [2,4,6]
  ]
L = range(len(Lines))

m = Model('XO')
X = {i: m.addVar(vtype=GRB.BINARY) for i in N}
Y = {l: m.addVar(vtype=GRB.BINARY) for l in L}

m.setObjective(quicksum(Y[l] for l in L))
for l in L:
    m.addConstr(quicksum(X[i] for i in Lines[l]) + Y[l] >= 1)
    m.addConstr(quicksum(X[i] for i in Lines[l]) - Y[l] <= 2)
## Change the RHS of the next constraint to to limit the number of X's
m.addConstr(quicksum(X[i] for i in N) == 0)

m.optimize()

for i in range(3):
  lstr = ''
  for j in range(3):
    lstr += 'X' if X[i*3+j].x > 0.99 else 'O'
  print (lstr)

