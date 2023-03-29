import pandas as pd
from collections import defaultdict
import pdb
import numpy as np
df_assets_coo = pd.read_excel('instance_1.xlsx', sheet_name='Assets')
df_levels = pd.read_excel('instance_1.xlsx', sheet_name='RegionLevel',header=None)
df_param = pd.read_excel('instance_1.xlsx', sheet_name='Param')
n = df_param.loc[df_param['Param'] == 'dimension_1', 'Value'].iloc[0]
slr = df_param.loc[df_param['Param'] == 'slr', 'Value'].iloc[0]
assets =(df_assets_coo['Coordinate_1'] * n + df_assets_coo['Coordinate_2']).tolist()#contains headers of assets
region = df_levels.to_numpy()
entries = []#contains headers of zone with low elevation
def count(i,j): return i*n+j
def Rcount(k): return (k//n,k%n)
for i in (0,n-1):
    for j in range(n):
        if region[i,j] <slr: entries.append(count(i,j))
        if region[j,i] <slr and i!=j : entries.append(count(j,i))
entries = list(set(entries))
T_Ci = defaultdict(list)#maps key = asset to value = matrix of roads
def NearBadZones(k,currentPath,currentAsset):#takes the header of a zone and returns a list of headers of near zones that have low elevation
    i,j = Rcount(k)
    if k == currentAsset and len(currentPath)>1:
        T_Ci[currentAsset].append(currentPath[::-1])
        #print(currentPath[::-1])
        return
    if k == currentAsset and len(currentPath) == 1:
        T_Ci[currentAsset].append(currentPath[::-1])
    for r in (-1,0,1):
        for c in (-1,0,1):
            if 0<=i+r<n and 0<=j+c<n:
                q = count(i+r,j+c)
                if q not in currentPath:
                    if q == currentAsset or q not in assets:#remove q not in assets to literaly generate all possible paths
                        if region[Rcount(q)] <=2:
                            NearBadZones(q, currentPath+[q], currentAsset)


for asset in assets:
    for entry in entries:
        NearBadZones(entry,[entry],asset)

print(T_Ci[count(4,6)])
