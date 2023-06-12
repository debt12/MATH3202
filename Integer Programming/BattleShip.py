from gurobipy import *

Ship = [
    [],
    [[1]],
    [[2, 3], [4, 5]],
    [[2, 6, 3], [4, 6, 5]],
    [[2, 6, 6, 3], [4, 6, 6, 5]],
    [[2, 6, 6, 6, 3], [4, 6, 6, 6, 5]]
]

ShipChar = '0123456'

big = True

if big:
    f = open('FILE HERE', 'r')
    # Read the dimensions
    nRow, nCol = [int(s) for s in f.readline().split(',')[:2]]
    Row = range(nRow)
    Col = range(nCol)
    # Read the number of ships of each length
    L = [int(s) for s in f.readline().split(',')[:len(Ship)]]
    Len = range(1, len(L))
    # Read the general data
    D = [[int(s) for s in f.readline().split(',')[:nCol + 1]] for i in Row]
    # Read the row of column sums
    ColSum = [int(s) for s in f.readline().split(',')[:nCol]]
    # Take the row sums from the end of the general data
    RowSum = [D[i][-1] for i in Row]
    for i in Row:
        D[i] = D[i][0:-1]
else:
    nRow = nCol = 8
    Row = range(nRow)
    Col = range(nCol)
    # The number of ships of each length
    L = [0, 3, 3, 2, 1, 0]
    Len = range(1, len(L))
    # The general data
    ColSum = [5, 1, 3, 0, 5, 1, 3, 1]
    RowSum = [2, 2, 1, 3, 2, 4, 2, 3]
    D = [
        [100, 100, 100, 100, 100, 100, 100, 100],
        [2, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100, 100, 100, 100],
        [100, 100, 6, 100, 100, 100, 5, 100],
        [100, 100, 100, 100, 100, 100, 100, 100],
    ]


def PieceOK(d, i, j, l):
    # Is it OK to place a ship of length l at location i,j in orientation d
    if l == 1:
        # Only have horizontal submarines
        if d == 1:
            return False
    # Check for running off the end, all compatible squares and surrounded by water
    if d == 0:
        if j + l > nCol:
            return False
        for ll in range(l):
            if D[i][j + ll] < 100 and D[i][j + ll] != Ship[l][d][ll]:
                return False
        for ii in range(max(0, i - 1), min(i + 2, nRow)):
            for jj in range(max(0, j - 1), min(j + l + 1, nCol)):
                ## Fail if it is not in the ship itself and it is anything except water
                if ii < i or ii > i or jj < j or jj >= j + l:
                    if D[ii][jj] < 100 and D[ii][jj] > 0:
                        return False
    else:
        if i + l > nRow:
            return False
        for ll in range(l):
            if D[i + ll][j] < 100 and D[i + ll][j] != Ship[l][d][ll]:
                return False
        for ii in range(max(0, i - 1), min(i + l + 1, nRow)):
            for jj in range(max(0, j - 1), min(j + 2, nCol)):
                ## Fail if it is not in the ship itself and it is anything except water
                if ii < i or ii >= i + l or jj < j or jj > j:
                    if D[ii][jj] < 100 and D[ii][jj] > 0:
                        return False
    return True


m = Model('BattleShip')
# Set of all the possible ways to place a ship
P = {(d, i, j, l)
     for d in [0, 1] for i in Row for j in Col for l in Len
     if PieceOK(d, i, j, l)}

# The squares the ship actually uses
Use = {(d, i, j, l):
           {(i, j + k) for k in range(l)} if d == 0 else
           {(i + k, j) for k in range(l)}
       for (d, i, j, l) in P}
# The squares the ship covers (buffer), including surrounding water
# This can run off the end
Cover = {(d, i, j, l):
             {(i, j + k) for k in range(l + 1)} | {(i + 1, j + k) for k in range(l + 1)}
             if d == 0 else
             {(i + k, j) for k in range(l + 1)} | {(i + k, j + 1) for k in range(l + 1)}
         for (d, i, j, l) in P}

# Our placement variables are indexed by H/V(0/1), i, j, len
X = {p: m.addVar(vtype=GRB.BINARY) for p in P}

RightShipsForLength = {l:
                           m.addConstr(quicksum(X[p] for p in P if p[3] == l) == L[l])
                       for l in Len}
# Row and col sums add up
RowSums = {i:
               m.addConstr(quicksum(len({(i, j) for j in Col} & Use[p]) * X[p] for p in P) == RowSum[i])
           for i in Row}
ColSums = {j:
               m.addConstr(quicksum(len({(i, j) for i in Row} & Use[p]) * X[p] for p in P) == ColSum[j])
           for j in Col}

# Each square covered at most once (or exactly once if non-zero)
CoverData = {(i, j):
                 m.addConstr(quicksum(X[p] for p in P if (i, j) in Cover[p]) == 1)
             for i in Row for j in Col if D[i][j] != 0 and D[i][j] != 100}

CoverOther = {(i, j):
                  m.addConstr(quicksum(X[p] for p in P if (i, j) in Cover[p]) <= 1)
              for i in Row for j in Col if D[i][j] == 0 or D[i][j] == 100}

while True:
    m.optimize()
    if m.Status != GRB.OPTIMAL:
        break
    ## Write out the answer
    STR = [['-' for j in Col] for i in Row]
    for d, i, j, l in P:
        if X[d, i, j, l].x > 0.1:
            for k in range(l):
                STR[i + d * k][j + (1 - d) * k] = ShipChar[Ship[l][d][k]]

    for i in Row:
        print(''.join(STR[i]))

    TL = [X[p] for p in P if X[p].x > 0.1]
    print(len(TL), sum(L))
    # Remove this next break if you want to check for multiple solutions
    # break
    m.addConstr(quicksum(TL) <= len(TL) - 1)
