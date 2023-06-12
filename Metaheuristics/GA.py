import random
import pylab
import math

def decimal(v):
    s = 0
    for x in v:
        s = 2 * s + x
    return s


def randbits(m):
    return [random.randint(0, 1) for k in range(m)]


def parents(fs):
    ps = []
    s = sum(fs)
    p = [f / s for f in fs]
    for j in range(len(fs)):
        k = 0
        y = random.random() - p[k]
        while y > 0:
            k += 1
            y -= p[k]
        ps.append(k)
    return ps


def crossover(v1, v2):
    m = len(v1)
    cp = random.randint(1, m - 1)
    return (v1[0:cp] + v2[cp:m], v2[0:cp] + v1[cp:m])


def mutate(v, mp):
    if random.random() < mp:
        m = len(v)
        j = random.randint(0, m - 1)
        v[j] = 1 - v[j]
    return v


def population_sorted(p, fs):
    ts = [(f, k) for k, f in enumerate(fs)]
    ts.sort()
    return [p[k] for (f, k) in ts]


def children(p, fs, mp):
    # pnew = [v for v in p]
    pnew = population_sorted(p, fs)
    n = len(p)
    ps = parents(fs)
    for j in range(0, n - 4, 2):
        (c1, c2) = crossover(p[ps[j]], p[ps[j + 1]])
        pnew[j] = mutate(c1, mp)
        pnew[j + 1] = mutate(c2, mp)
    return pnew


def GA(f, m, n, mp, generations):
    data = []
    p = [randbits(m) for j in range(n)]
    for g in range(generations):
        fitness = [f(v) for v in p]
        data.append((max(fitness), sum(fitness) / n))
        p = children(p, fitness, mp)

    pylab.plot(range(generations), data)
    pylab.show()
    return p


def square(v):
    x = decimal(v)
    return x * x


def cosfun(v):
    x = 80 * decimal(v) / 1023 - 40
    return 1 + math.cos(x) / (1 + .01 * x ** 2)


