"""
@Author: Alaaeddine Maggouri
@finished on : 4/5/2023

"""


import pandas as pd
from collections import defaultdict
import numpy as np

size = input('run on which instance ? Choose 1,2 or 3 ')
df_assets_coo = pd.read_excel('instance_'+size+'.xlsx', sheet_name='Assets')
df_levels = pd.read_excel('instance_'+size+'.xlsx', sheet_name='RegionLevel',header=None)
df_param = pd.read_excel('instance_'+size+'.xlsx', sheet_name='Param')
n = df_param.loc[df_param['Param'] == 'dimension_1', 'Value'].iloc[0]
slr = df_param.loc[df_param['Param'] == 'slr', 'Value'].iloc[0]
assets =(df_assets_coo['Coordinate_1'] * n + df_assets_coo['Coordinate_2']).tolist()#contains headers of assets
region = df_levels.to_numpy()
entries = []#contains headers of zone with low elevation
rows, cols = df_levels.shape
zones_number = region.shape[0]*region.shape[1]
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
    if k == currentAsset:
        T_Ci[currentAsset].append(currentPath[::-1])
        return

    for r in (-1,0,1):
        for c in (-1,0,1):
            if 0<=i+r<n and 0<=j+c<n:
                q = count(i+r,j+c)
                if q not in currentPath:
                    if q == currentAsset or q not in assets:#remove q not in assets to literaly generate all possible paths
                        if region[Rcount(q)] <=2:
                            NearBadZones(q, currentPath+[q], currentAsset)

# #for yassmine's code
# T_Cy = {}
# for asset in T_Ci.keys():
#     maxlength = 0
#     temp = []
#     for road in T_Ci[asset]:
#         maxlength = max(maxlength, len(road))
#     for road in T_Ci[asset]:
#         temp.append(road[::-1] + [np.nan]*(maxlength - len(road)))
#     T_Cy[asset] = np.array(temp)

# def generator(): #generates road from entries to assets inverted
#     for asset in assets:
#         for entry in entries:
#             NearBadZones(entry,[entry],asset)
#     return T_Ci, assets, slr, region, entries, rows, cols,T_Cy



'''
*T_Ci : a dictionnary of asset : list of roads from that asset to an entry
exmaple : 
        [[8], [8, 17]] = T_Ci[8]
        [[42, 51, 61, 71], [42, 50, 51, 61, 71], [42, 50, 60, 51, 61, 71]] : first three elements of T_Ci[42]
        note that T_Ci[asset] is a list of lists. each sub-list defines a road from the asset to an entry 
        + an entry is a zone directly open to the sea and whom elevation is less than slr
        + in all those lists, I used labels given by the function Count instead of indicies 
        
*assets : list of labels of assets = [8, 24, 42] for instance_1

*region : an np.array of elevations of each zone. it is like the table we see in excel: 
                                    [[8 8 7 7 6 6 7 6 2]    labeled as    [[0,1,2,3,4,5,6,7,8]
                                     [2 4 7 6 8 5 1 5 2]                   [9,10,11,12 .....]]
                                     [4 8 7 3 4 5 2 5 6]
                                     [6 8 2 6 5 2 8 8 7]
                                     [1 8 8 3 4 9 2 3 6]
                                     [9 5 7 7 3 1 1 3 2]
                                     [5 3 2 5 3 4 2 1 1]
                                     [7 3 9 6 9 6 2 4 2]
                                     [7 4 3 1 1 1 5 1 8]]
we can easily obtain the elevation of zone
example  : elevation of zone 0 (first zone) = region[Rcount(0)] = region[(0,0)] = 8 
            elevation of zone 8 =  region[Rcount(8)] = region[(0,9)] = 2
entries  : list of labels of entries : [36, 71, 8, 9, 75, 76, 77, 79, 17, 53, 62] for instance_1
                    + an entry is a zone directly open to the sea and whom elevation is less than slr


                
*T_Cy is made to replace T_Ci for Yassmine's code
how it looks : 
print(T_Cy[42][0:3]) : first three road leading to asset 42
[[71. 61. 51. 42. nan nan nan nan nan nan nan nan nan]
 [71. 61. 51. 50. 42. nan nan nan nan nan nan nan nan]
 [71. 61. 51. 60. 50. 42. nan nan nan nan nan nan nan]]
 
 
 print(T_Cy[8]) : all road leading to asset 8:
[[ 8. nan]
 [17.  8.]]
(Pdb) 
'''