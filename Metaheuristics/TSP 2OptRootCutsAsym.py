import math
import random
from gurobipy import *
import pylab


def Distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


N = 300
random.seed(N)
Square = 1000
Pos = [(random.randint(0, Square), random.randint(0, Square)) for i in range(N)]
# PtDict = {}
# Pos = []
# for i in range(N):
#  while True:
#    p = (int(random.randint(0,1000)), int(random.randint(0,1000)))
#    if p not in PtDict:
#      break
#  Pos.append(p)
#  PtDict[p] = i

NLevel = 10

EPS = 0.000001

D = [[Distance(Pos[i], Pos[j]) for j in range(N)] for i in range(N)]

m = Model('TSP')
X = [[m.addVar(obj=D[i][j]) for j in range(i)] for i in range(N)]
m.update()

for i in range(N):
    m.addConstr(quicksum(X[i][j] for j in range(i)) + quicksum(X[j][i] for j in range(i + 1, N)) == 2)

numCuts = 0


def cmplen(a, b):
    return len(a) - len(b)


def GenerateCuts(vlistpass):
    ## Takes a list of (x_ij, i, j) and returns a list of clique cuts
    ## The cuts are sorted by length

    # Sort the list by x_value (decreasing) for subsequent processing
    vlist = sorted(vlistpass, reverse=True)
    cutlist = []
    while len(cutlist) == 0 and sum(v[0] for v in vlist) > N / 2:
        groupused = [True for i in range(N)]
        group = [i for i in range(N)]
        for v in vlist:
            # For each variable, combine the groups
            if group[v[1]] != group[v[2]]:
                groupused[group[v[2]]] = False
                gv2 = group[v[2]]
                for i in range(N):
                    if group[i] == gv2:
                        group[i] = group[v[1]]
        ngroups = 0
        for i in range(N):
            if groupused[i]:
                ngroups += 1
                tlist = [j for j in range(N) if group[j] == i]
                nGroup = len(tlist)
                vGroup = sum(v[0] for v in vlistpass if group[v[1]] == i and group[v[2]] == i)
                if nGroup < N and vGroup > nGroup - 1 + 0.2:
                    cutlist.append(list(tlist))
        if ngroups == 1 or len(vlistpass) == N:
            break
        del (vlist[-1])
    return sorted(cutlist, key=len)


m.setParam('OutputFlag', 0)
while True:
    m.optimize()
    vlist = [(X[i][j].x, i, j) for i in range(N) for j in range(i) if X[i][j].x > EPS]
    cuts = GenerateCuts(vlist)
    print(m.objVal, len(cuts))
    if len(cuts) == 0:
        break
    for cut in cuts:
        m.addConstr(quicksum(X[i][j] for i in cut for j in cut if j < i) <= len(cut) - 1)
        if len(cut) > NLevel:
            break
m.setParam('OutputFlag', 1)

for i in range(N):
    for j in range(i):
        X[i][j].vtype = GRB.BINARY


def AddCut(model, tlist):
    global numCuts
    model.cbLazy(quicksum(X[i][j] for i in tlist for j in tlist if j < i) <= len(tlist) - 1)
    numCuts += 1


def KnitCost(l1, l2):
    ## Find the cheapest way to break and recombine the two lists
    bestCost = 999999999
    p1 = -1
    p2 = -1
    doRev = False
    for i in range(len(l1)):
        for j in range(len(l2)):
            f1 = l1[i]
            t1 = l1[(i + 1) % len(l1)]
            f2 = l2[j]
            t2 = l2[(j + 1) % len(l2)]
            cost = D[f1][t2] + D[f2][t1] - D[f1][t1] - D[f2][t2]
            if cost < bestCost:
                bestCost = cost
                p1 = i
                p2 = j
                doRev = False
            cost = D[f1][f2] + D[t2][t1] - D[f1][t1] - D[f2][t2]
            if cost < bestCost:
                bestCost = cost
                p1 = i
                p2 = j
                doRev = True
    return (bestCost, p1, p2, doRev)


def Cost(alist):
    return sum(D[alist[i]][alist[(i + 1) % len(alist)]] for i in range(len(alist)))


def Knit(l1, l2):
    [tCost, p1, p2, doRev] = KnitCost(l1, l2)
    costStart = Cost(l1) + Cost(l2)
    tlist = l1[0:p1 + 1]
    if doRev:
        tlist += [l2[i] for i in range(p2, -1, -1)]
        tlist += [l2[i] for i in range(len(l2) - 1, p2, -1)]
    else:
        tlist += l2[p2 + 1:len(l2)]
        tlist += l2[0:p2 + 1]
    tlist += l1[p1 + 1:len(l1)]
    dcost = costStart + tCost - Cost(tlist)
    if dcost > EPS or dcost < -EPS:
        print("##### Cost error", dcost)
    return tlist


postSolution = False
postList = []
postCost = 999999999


def TwoOpt(alist):
    tcost = Cost(alist)
    newcost = tcost
    while True:
        for i in range(N - 3):
            for j in range(i + 2, N - 1):
                # Look at removing the piece from i+1 to j and reversing it
                if D[alist[i]][alist[i + 1]] + D[alist[j]][alist[j + 1]] > \
                        D[alist[i]][alist[j]] + D[alist[i + 1]][alist[j + 1]]:
                    for k in range(0, int((j - i) / 2)):
                        alist[i + 1 + k], alist[j - k] = alist[j - k], alist[i + 1 + k]
                    oldcost = newcost
                    newcost = Cost(alist)
                    if newcost >= oldcost:
                        print("###### Cost error in TwoOpt")
        if newcost >= tcost:
            break
        tcost = newcost


def Patch(allList):
    ## Patch all the lists together
    ## print allList
    global postSolution
    global postCost
    global postList
    while len(allList) > 1:
        bestKnit = 999999999
        besti = bestj = -1
        for i in range(1, len(allList)):
            for j in range(0, i):
                tCost = KnitCost(allList[j], allList[i])[0]
                if tCost < bestKnit:
                    bestKnit = tCost
                    besti = i
                    bestj = j
        ## print "Patch called", len(allList), besti, bestj, bestKnit
        allList[bestj] = Knit(allList[bestj], allList.pop(besti))
    if len(allList[0]) == N:
        TwoOpt(allList[0])
        tCost = Cost(allList[0])
        if tCost < postCost:
            postSolution = True
            postCost = tCost - EPS
            print("Posting", postCost)
            postList = list(allList[0])
    else:
        print("########## Patch failed ##########")


def messageCB(model, where):
    if where == GRB.Callback.MIPNODE:
        global postSolution
        global postCost
        global postList
        if postSolution:
            if postCost < model.cbGet(GRB.Callback.MIPNODE_OBJBST) - EPS:
                for i in range(N):
                    if postList.count(i) != 1:
                        print("##### Item error #####", i, postList.count(i))
                    if postList[i] > postList[(i + 1) % N]:
                        model.cbSetSolution(X[postList[i]][postList[(i + 1) % N]], 1.0)
                    else:
                        model.cbSetSolution(X[postList[(i + 1) % N]][postList[i]], 1.0)
            else:
                postSolution = False
                postCost = model.cbGet(GRB.Callback.MIPNODE_OBJBST)
        if model.cbGet(GRB.Callback.MIPNODE_STATUS) != GRB.OPTIMAL:
            return
        ## See if we can quickly find some disconnected graphs
        Xval = [model.cbGetNodeRel(X[i]) for i in range(N)]
        ##    if sum(Xval[i][j]*D[i][j] for i in range(N) for j in range(i)) > \
        ##       model.cbGet(GRB.Callback.MIPNODE_OBJBND) + EPS:
        ##      return
        vlist = [(Xval[i][j], i, j) for i in range(N) for j in range(i) if Xval[i][j] > EPS]
        cuts = GenerateCuts(vlist)
        if len(cuts) == 0:
            return
        for cut in cuts:
            AddCut(model, cut)
            if len(cut) > NLevel:
                break
    elif where == GRB.Callback.MIPSOL:
        ##print "MIPSOL"
        ## See if we have to add a lazy cut to get rid of a loop
        Xval = [model.cbGetSolution(X[i]) for i in range(N)]
        vlist = [(Xval[i][j], i, j) for i in range(N) for j in range(i) if Xval[i][j] > EPS]
        cuts = GenerateCuts(vlist)
        if len(cuts) == 0:
            # print len(vlist)
            return
        for cut in cuts:
            AddCut(model, cut)
            if len(cut) > NLevel:
                break
        nextNode = [[] for i in range(N)]
        for i in range(N):
            for j in range(i):
                if Xval[i][j] > 0.5:
                    nextNode[i].append(j)
                    nextNode[j].append(i)
        ##print nextNode
        done = [False for i in range(N)]
        allList = []
        ## Try to post a heuristic if < threshold loops - knit together
        for i in range(N):
            if done[i]:
                continue
            nLen = 0
            j = i
            nList = []
            while nLen <= 0 or j != i:
                nLen += 1
                done[j] = True;
                nList.append(j)
                nextj = nextNode[j][0]
                nextNode[j].remove(nextj)
                nextNode[nextj].remove(j)
                j = nextj
            allList.append(list(nList))
        Patch(allList)
        ##print "MIPSOL Exit"


m.setParam("LazyConstraints", 1)
m.setParam("MIPGap", 0.0000001)
##m.setParam("MIPFocus", 3)
## Force variables to branch up - seems to generate more solutions
m.setParam("BranchDir", 1)
## This seems to work best, but needs more experiments
# m.setParam("VarBranch", 2)
## m.setParam("Cuts", 3)
## Turn heuristics off - probably not a good idea for problems with
## lots of good solutions
m.setParam("Heuristics", 0.01)
##m.setParam("CutPasses", 0)

m.optimize(messageCB)

nextNode = [[] for i in range(N)]
for i in range(N):
    for j in range(i):
        if X[i][j].x > 0.5:
            nextNode[i].append(j)
            nextNode[j].append(i)
##print nextNode
done = [False for i in range(N)]
allList = []
for i in range(N):
    if done[i]:
        continue
    nLen = 0
    j = i
    nList = []
    while nLen <= 0 or j != i:
        nLen += 1
        done[j] = True;
        nList.append(j)
        nextj = nextNode[j][0]
        nextNode[j].remove(nextj)
        nextNode[nextj].remove(j)
        j = nextj
    allList.append(list(nList))

ansList = [Pos[j] for j in allList[0]]

ansList.append(Pos[0])
pylab.plot([a[0] for a in ansList], [a[1] for a in ansList])
pylab.show()
