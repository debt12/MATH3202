from gurobipy import *

"""
Notes and Assumptions:

Context: Storm approaching bay with 18 boats on the water
Ports: M, C, D
Time: t, in minutes of travel time for each boat to port
Capacity: M: 8, C: 8, D: 6
Objective: Minimise the total travel time for each boat.
"""

Ports = ['Manly','Cleveland','Dunwich']
P = range(len(Ports))
B = range(18)

Travel = [
	[29, 27, 21], [39, 18, 30], [40, 20, 31], [33, 19, 27], [35, 29, 36], [21, 23, 20],
	[30, 41, 32], [37, 27, 36], [20, 25, 34], [36, 28, 20], [24, 23, 25], [38, 22, 40],
	[39, 19, 27], [30, 18, 28], [40, 20, 32], [21, 32, 40], [23, 18, 20], [31, 18, 20]
]

# Model
m = Model("Boats")

# Variables
X = {(b, p): m.addVar(vtype=GRB.BINARY) for b in B for p in P} # Assign boat b to port p

# Objective Function
m.setObjective(quicksum(Travel[b][p]*X[b, p] for b in B for p in P), GRB.MINIMIZE)

# Constraints
# Port capacities constraints
for p in P:
	if p == 0:
		m.addConstr(quicksum(X[b, p] for b in B) <= 8) # Manly port capacity
	elif p == 1:
		m.addConstr(quicksum(X[b, p] for b in B) <= 8) # Cleveland port capacity
	else:
		m.addConstr(quicksum(X[b, p] for b in B) <= 6) # Dunwich port capacity

# One boat per port
for b in B:
	m.addConstr(quicksum(X[b, p] for p in P) == 1)

# Optimization
m.optimize()