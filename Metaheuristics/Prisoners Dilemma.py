import pylab
import random


def decimal(v):
    s = 0
    for x in v:
        s = 2 * s + x
    return s


def randbits(m):
    return [random.randint(0, 1) for k in range(m)]


def initial(n, m):
    return [randbits(m) for i in range(n)]


def fitness(f, p):
    return [f(v) for v in p]


def parents(fs):
    ps = []
    s = sum(fs)
    r = [x / s for x in fs]
    for j in fs:
        k = 0
        y = random.random() - r[k]
        while y > 0:
            k += 1
            y -= r[k]
        ps.append(k)
    return ps


def crossover(v1, v2):
    m = len(v1)
    cp = random.randint(1, m - 1)
    return (v1[0:cp] + v2[cp:m], v2[0:cp] + v1[cp:m])


def mutate(v, mp):
    return [1 - x if (random.random() < mp) else x for x in v]


def population_sorted(p, fs):
    ts = [(f, k) for k, f in enumerate(fs)]
    ts.sort()
    return [p[k] for (f, k) in ts]


def children(p, fs, mp):
    pnew = population_sorted(p, fs)
    n = len(p)
    ps = parents(fs)
    for j in range(0, n - 4, 2):
        (c1, c2) = crossover(p[ps[j]], p[ps[j + 1]])
        pnew[j] = mutate(c1, mp)
        pnew[j + 1] = mutate(c2, mp)
    return pnew


# Iterated Prisoners Dilemma

def play_ipd(u, v):
    payoff = [[3, 0], [5, 1]]
    su = u[0:6]
    sv = v[0:6]
    t = 0
    for j in range(20):
        pu = u[6 + decimal(su)]
        pv = v[6 + decimal(sv)]
        t += payoff[pu][pv]
        su = su[2:6] + [pu, pv]
        sv = sv[2:6] + [pv, pu]
    return t / 20


def fitness_ipd(p):
    n = len(p)
    fs = []
    for u in p:
        t = 0
        for v in p:
            t += play_ipd(u, v)
        fs.append(t / n)
    return fs


def ga_ipd(m, n, mp, generations):
    evolution = []
    p = initial(n, m)
    for g in range(generations):
        fs = fitness_ipd(p)
        evolution.append((max(fs), sum(fs) / n))
        p = children(p, fs, mp)

    pylab.plot(range(generations), evolution)
    pylab.show()
    return p
