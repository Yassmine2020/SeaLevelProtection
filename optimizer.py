import pulp
import sys
sys.path.append('/paths_generator.py')
import paths_generator as pg
from pulp import *
import numpy as np

T_Ci, assets,slr,region = pg.generator()
prob = LpProblem('assets_protection', LpMinimize)

# decision variables+ objective function
x = []
obj = []
for i in region.shape()[0]:
    for j in range(8):
        x.append(LpVariable(name="x{i,j}", cat='Binary')) #
        obj.append(x[-1]*(slr-region[i]))
# objective function
prob += lpSum(obj)

for asset_label in T_Ci.keys():
    for road_labels in T_Ci[asset_label]:
        road_labels = [road_labels[0]]+road_labels # convention: x_ii =1 for i in entry means that we should place an barrier on the sea-entry i border
        temp = []
        for zone_label in road_labels:
            temp.append(x[])




