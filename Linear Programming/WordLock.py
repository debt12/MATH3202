from gurobipy import *


def wordletters(w):
    return [ord(w[j]) - 97 for j in range(4)]


wordsfile = open('dictionary.txt', 'r')

words = [w.strip() for w in wordsfile if len(w.strip()) == 4]

Letters = range(26)

letterdata = [wordletters(w) for w in words]

Words = range(len(letterdata))

print(len(Words), "total words")

Dials = range(4)

m = Model('Word Lock')

# X[d,l] is letter l on dial d?
X = {(d, l): m.addVar(vtype=GRB.BINARY) for l in Letters for d in Dials}

# Y[w] is word w possible?
Y = {w: m.addVar(vtype=GRB.BINARY) for w in Words}

m.setObjective(quicksum(Y[w] for w in Words), GRB.MAXIMIZE)

for d in Dials:
    m.addConstr(quicksum(X[d, l] for l in Letters) == 10)

# Link X and Y
# for w in Words:
#    m.addConstr(4*Y[w] <= quicksum(X[d,letterdata[w][d]] for d in Dials))

# Disagregating the constraints gives an improvement in performance
for w in Words:
    for d in Dials:
        m.addConstr(Y[w] <= X[d, letterdata[w][d]])

m.optimize()

# Display results
for d in Dials:
    print(d, ": ", end=" ")
    for l in Letters:
        if X[d, l].x > 0.99:
            print(chr(65 + l), end=" ")
    print()

print(int(sum(Y[w].x for w in Words)), "words")