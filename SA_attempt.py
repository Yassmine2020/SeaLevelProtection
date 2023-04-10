"""
@Author: Alaaeddine Maggouri
@finished on : 4/5/2023

"""

import sys
sys.path.append('/paths_generator.py')
import paths_generator as pg
from scipy.optimize import dual_annealing
import numpy as np

def SA():

    n_iterations = int(input('enter number of iteration (1000 by default)'))
    zones_number = pg.region.shape[0]*pg.region.shape[1]

    def constraints(x):
        constraints_list = []
        x = np.array(x)
        x = np.reshape(x,(pg.zones_number, pg.zones_number))
        for asset_label in pg.T_Ci.keys():
            for road_labels in pg.T_Ci[asset_label]:
                temp = []
                for i in range(len(road_labels)-1):
                    temp.append(x[road_labels[i+1]][road_labels[i]])
                temp.append(x[road_labels[-1]][road_labels[-1], road_labels[-1]])
                constraints_list.append(1-sum(temp))
        return np.array(constraints_list)
    #returns an array where each element should be <= 0

    penalty_factor = 100

    def objective(x):  # m, n depends on the path: temperary
        constarray = constraints(x)
        x = np.array(x)
        x = np.reshape(x,(pg.zones_number, pg.zones_number))
        S = 0
        for i in range(zones_number):
            e_i = pg.region[pg.Rcount(i)]
            for j in range(zones_number):
                S += x[i][j] * max(0,(pg.slr - e_i))
        for constraint in constarray:
            S+= penalty_factor*max(0, constraint)**2
        return S
    #returns the amount to be minimized


    bounds = [(0, 1) for _ in range(zones_number**2)]
    result = dual_annealing(objective, bounds, maxiter= n_iterations)

    x_optimal = result.x.reshape((zones_number,zones_number))
    print("Optimal solution found:\n", x_optimal)
