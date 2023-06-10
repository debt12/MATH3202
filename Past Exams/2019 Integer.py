from gurobipy import *

# Sets
F = range(10)
C = range(20)

# Data
Build = [1204, 1757, 1357, 1519, 1785, 1959, 1597, 1683, 1219, 1373]
Assign = [
    [683, 811, 585, 769, 836, 942, 914, 548, 829, 719],
    [580, 869, 722, 972, 635, 957, 992, 787, 564, 528],
    [765, 966, 538, 852, 543, 912, 686, 710, 889, 951],
    [853, 716, 926, 705, 617, 882, 853, 992, 749, 533],
    [853, 815, 679, 803, 833, 618, 889, 560, 752, 806],
    [568, 567, 911, 532, 662, 663, 891, 917, 675, 768],
    [731, 511, 975, 874, 522, 781, 963, 502, 613, 695],
    [632, 967, 687, 570, 802, 652, 766, 982, 658, 548],
    [712, 670, 982, 880, 730, 974, 697, 648, 808, 995],
    [719, 806, 999, 720, 907, 800, 769, 804, 916, 853],
    [712, 597, 998, 527, 715, 647, 897, 833, 839, 689],
    [867, 552, 519, 522, 776, 776, 771, 585, 913, 850],
    [875, 567, 728, 880, 595, 518, 797, 788, 664, 560],
    [536, 760, 733, 503, 531, 904, 598, 891, 983, 908],
    [757, 548, 967, 585, 615, 508, 978, 793, 998, 970],
    [696, 754, 999, 565, 841, 717, 542, 719, 962, 574],
    [778, 715, 866, 713, 651, 809, 591, 513, 864, 953],
    [513, 832, 925, 887, 583, 590, 907, 981, 636, 983],
    [835, 942, 945, 868, 904, 905, 852, 751, 689, 748],
    [714, 985, 724, 721, 655, 964, 901, 726, 701, 977]]

maxCustomers = 6
d = 2   # Part B: increased capacity for upgraded factory.
r = 0.5   # Part B: Cost ratio for big factory.

# Model
m = Model("Factories")

# Variables
X = {(c, f): m.addVar(vtype=GRB.BINARY) for c in C for f in F}  # Assign customer to factory
Y = {f: m.addVar(vtype=GRB.BINARY) for f in F}  # Build Factory or not
Z = {f: m.addVar(vtype=GRB.BINARY) for f in F}  # Part B: If factory has been upgraded.

# Objective: Minimise the cost of building, and then the cost of the assignment.
m.setObjective(quicksum(Build[f] * Y[f] + r * Build[f] * Z[f] for f in F) +
               quicksum(Assign[c][f] * X[c, f] for c in C for f in F), GRB.MINIMIZE)

# Constraints
# Each customer can only be assigned to one factory and exactly one.
for c in C:
    m.addConstr(quicksum(X[c, f] for f in F) == 1)

# Maximum of 6 customers can be assigned to one factory.
for f in F:
    m.addConstr(quicksum(X[c, f] for c in C) <= maxCustomers * Y[f] + d * Z[f])

for f in F:
    m.addConstr(Z[f] <= Y[f]) # Part B: Can only upgrade if factory is built.




# Optimization
m.optimize()

# Prints
print("Total cost is $", m.objVal)
for f in F:
    if Y[f].x > .9:
        if Z[f].x > .9:
            print("Upgrade: ", end=' ')
        print("Factory: ", f, "Customers: ", [c for c in C if X[c, f].x > .9])
