import pulp
import sys
sys.path.append('/paths_generator.py')
import paths_generator as pg
from pulp import *
from collections import defaultdict
import numpy as np
import pdb

T_Ci, assets, slr, region, entries= pg.generator()
prob = LpProblem('assets_protection', LpMinimize)

assetNentry = 0
assetsNentries = []
# decision variables
x =defaultdict(dict)
obj = []
for zone in range(pg.count(0,0), pg.count(region.shape[0]-1, region.shape[1]-1)): # loop over labels of all zones
    temp = []
    m,k = pg.Rcount(zone)
    for r in [-1, 0, 1]:
        for c in [-1, 0, 1]:
            q = pg.count(m+r,k+c) # q one of the surrounding 8 zones
            temp.append(LpVariable(name=f"x{ pg.Rcount(zone),pg.Rcount(q)}", cat='Binary'))
            x[zone][zone,q] = temp[-1]
            if slr > region[pg.Rcount(zone)] : obj.append((x[zone][zone,q]) *(slr-region[pg.Rcount(zone)]))
    if zone in assets and zone in entries:
        assetsNentries.append(pg.Rcount(zone))
        assetNentry += slr-region[pg.Rcount(zone)]

# objective function
prob += lpSum(obj)
#constraints
for asset_label in assets:
    for road_labels in T_Ci[asset_label]:
        temp = []
        for i in range(len(road_labels)-1):
            temp.append(x[road_labels[i+1]][road_labels[i+1], road_labels[i]])
        prob += lpSum(temp) >=1

status = prob.solve()

# Print the values of the decision variables
for zone in range(pg.count(0,0), pg.count(region.shape[0]-1, region.shape[1]-1)): # loop over labels of all zones
    for var in x[zone].values():
        if var.value()==1: print(f"{var.name}: {var.value()}")
print(f"Objective function value: {value(prob.objective)}")
print('total cost = objective function value + barriers for assets on the edges of the island = ', value(prob.objective) + assetNentry )
print('assets on the edge of the island', assetsNentries)