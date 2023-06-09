from gurobipy import *

# Model
m = Model("Farmer Jones")

# Sets
Cakes = ["Chocolate", "Plain"]
Ingredients = ["Time", "Milk", "Eggs"]
C = range(len(Cakes))
I = range(len(Ingredients))

# Data
price = [4, 2]
storage = [480, 5, 30]
quantities = [[20, 0.250, 4],[50, 0.200, 1]]

# Variables

