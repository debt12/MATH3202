import math
import random
from gurobipy import *
import pylab

def Distance(p1, p2):
  return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

nLoc = 150
N = range(nLoc)
Square = 1000
random.seed(nLoc)
Pos = [(random.randint(0,Square), random.randint(0,Square)) for i in N]

m = Model('TSP')
X = [[m.addVar(vtype=GRB.BINARY, obj=Distance(Pos[i],Pos[j]) if i != j else Square*nLoc)
      for j in N] for i in N]

[m.addConstr(quicksum(X[i][j] for j in N) == 1) for i in N]
[m.addConstr(quicksum(X[j][i] for j in N) == 1) for i in N]
m._lCuts = 0

def GetNext(Xval):
  nextNode = [0 for i in N]
  for i in N:
    for j in N:
      if Xval[i][j] > 0.99:
        nextNode[i] = j
        break
  return nextNode

def messageCB(model, where):
    if where == GRB.Callback.MIPSOL:
      nextNode = GetNext([model.cbGetSolution(X[i]) for i in N])
      done = [False for i in N]
      for i in N:
        if done[i]:
          continue
        tlist = []
        j = i
        while len(tlist) == 0 or j != i:
          tlist.append(j)
          done[j] = True
          j = nextNode[j]
        if len(tlist) <= nLoc/2:
          model.cbLazy(quicksum(X[ii][jj] for ii in tlist for jj in tlist) <= len(tlist) - 1)
          m._lCuts += 1

m.setParam("LazyConstraints", 1)
m.setParam("MIPGap", 0.00)
# m.optimize()
m.optimize(messageCB)

[pylab.plot([Pos[i][0], Pos[j][0]], [Pos[i][1], Pos[j][1]], 'black')
  for i in N for j in N if X[i][j].x > 0.99]
pylab.show()
