import math
import random
from gurobipy import *
import pylab


def Distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


EPS = 0.0001
nLoc = 150
N = range(nLoc)
Square = 1000
random.seed(nLoc)
Pos = [(random.randint(0, Square), random.randint(0, Square)) for i in N]
D = [[Distance(Pos[i], Pos[j]) for j in N] for i in N]


def Cost(Path):
    return sum(D[Path[i - 1]][Path[i]] for i in N)


Path = list(N)
random.shuffle(Path)


def Improve(Path):
    found = False
    for ii in N:
        for jj in range(nLoc // 2):
            j = (ii + jj + 1) % nLoc
            if ii < j:
                i = ii
            else:
                i, j = j, ii
            if j - i >= nLoc - 1:
                continue
            a1 = Path[i - 1]
            a2 = Path[i]
            b1 = Path[j]
            b2 = Path[(j + 1) % nLoc]
            if D[a1][b1] + D[a2][b2] < D[a1][a2] + D[b1][b2]:
                # Reverse everything from i to j
                for k in range((j - i + 1) // 2):
                    Path[i + k], Path[j - k] = Path[j - k], Path[i + k]
                found = True
    return found


pylab.plot([Pos[Path[i]][0] for i in range(-1, nLoc)], [Pos[Path[i]][1] for i in range(-1, nLoc)])
pylab.show()
while Improve(Path):
    print(Cost(Path))

    pylab.plot([Pos[Path[i]][0] for i in range(-1, nLoc)], [Pos[Path[i]][1] for i in range(-1, nLoc)])
    pylab.show()

