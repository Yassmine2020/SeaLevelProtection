import pulp
import sys
sys.path.append('/paths_generator.py')
import paths_generator as pg
from pulp import *
import numpy as np

T_Ci, assets,slr,region = pg.generator()
prob = LpProblem('assets_protection', LpMinimize)

# decision variables+ objective function
x = np.zeros(region.shape()[0], range(8))
obj = []
for i in region.shape()[0]:
    for j in range(8):
        x[i,j] = LpVariable(name=f"x{i,j}", cat='Binary') #
        obj.append(x[i,j]*(slr-region[i]))
# objective function
prob += lpSum(obj)
x = np.array(x, ())
for asset_label in T_Ci.keys():
    for road_labels in T_Ci[asset_label]:
        road_labels = [road_labels[0]]+road_labels # convention: x_ii =1 for i in entry means that we should place an barrier on the sea-entry i border
        temp = []
        for i in range(len(road_labels)-1):
            temp.append(x[road_labels[i+1],road_labels[i]])
        prob += lpSum(temp)

status = prob.solve()

# Print the values of the decision variables
for i in region.shape()[0]:
    for j in range(8):
        if x[i,j].value() ==1 : print(f"x{i,j} = {x[i,j].value()}")
        obj_value = value(prob.objective)
print(f"Objective function value: {obj_value}")

