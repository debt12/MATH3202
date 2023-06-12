from gurobipy import *

"""
Notes and Assumptions:

Bananagrams is a word game played with 144 letter tiles, with the distribution of 
letters roughly matching English usage. The game is played by arranging tiles
into a grid of connected words.	

What is the smallest number of connected words that uses all 144 tiles?
"""

Tiles = 2 * ['j', 'k', 'q', 'x', 'z'] + 3 * ['b', 'c', 'f', 'h', 'm', 'p', 'v', 'w', 'y'] + \
        4 * ['g'] + 5 * ['l'] + 6 * ['d', 's', 'u'] + 8 * ['n'] + 9 * ['t', 'r'] + \
        11 * ['o'] + 12 * ['i'] + 13 * ['a'] + 18 * ['e']

Alphabet = 'abcdefghijklmnopqrstuvwxyz'


def LetterCount(word):
    counts = {l: 0 for l in Alphabet}
    for l in word:
        counts[l] += 1
    return counts


BaseCount = LetterCount(Tiles)

f = open("enable1.txt", "r")
WordList = [w[:-1] for w in f]

N = range(len(WordList))
print(len(WordList), 'words used')

A = [LetterCount(WordList[i]) for i in N]

m = Model('Bananagrams')

X = {i: m.addVar(vtype=GRB.BINARY) for i in N}

m.setObjective(quicksum(X[i] for i in N))

for l in Alphabet:
    m.addConstr(quicksum(A[i][l] * X[i] for i in N) >= BaseCount[l])

m.addConstr(quicksum(X[i] * len(WordList[i]) for i in N) ==
            len(Tiles) + quicksum(X[i] for i in N) - 1)

m.optimize()

LetterUsed = {l: 0 for l in Alphabet}

for i in N:
    if X[i].x > 0.9:
        print(WordList[i])
        for l in Alphabet:
            LetterUsed[l] += A[i][l]

for l in Alphabet:
    if LetterUsed[l] > BaseCount[l]:
        print(l, LetterUsed[l] - BaseCount[l])