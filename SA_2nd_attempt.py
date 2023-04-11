'''
@author : Sir Alaaeddine Maggouri
@finishid on : 10/4/2023
'''

import random
import math
import numpy as np
import paths_generator as pg
from collections import defaultdict


util_later1 = {}# move cpl to index
util_later2 = {}#index to move cpl
util = -1
for r in [-1, 0, 1]:
    for c in [-1, 0, 1]:
        util+=1
        util_later1[(r,c)] = util
        util_later2[util] = (r,c)
listI = [pg.Rcount(header) for header in range(0,pg.count(pg.rows -1, pg.cols -1))]
penalty_factor = 100
entries_risk_foreign = defaultdict(int)

def constraints(x):
    # takes a list of xij- i refers to a zone label-j refers to one of its 8 surrounding zones
    # returns an array where each element should be <= 0

    constraints_list = []
    x = np.array(x)
    x = np.reshape(x, (pg.zones_number, 9))
    for asset_label in pg.T_Ci.keys():
        for road_labels in pg.T_Ci[asset_label]:
            temp = []
            for i in range(len(road_labels)-1):
                visited_entry = 0
                m,k = pg.Rcount(road_labels[i+1])
                for r in [-1, 0, 1]:
                    for c in [-1,0,1]:
                        if i in pg.entries and (not pg.count(m+r, k+c) in listI) :
                            if  not visited_entry:
                                temp.append(x[road_labels[i+1]][4])
                                visited_entry = 1
                        elif pg.count(m+r, k+c) == road_labels[i]:
                            temp.append(x[road_labels[i+1]][util_later1[(r,c)]])
            constraints_list.append(1-sum(temp))
    return np.array(constraints_list)

def objective(x):
    #takes a list of xij- i refers to a zone label-j refers to one of its 9 near zones
    # returns the amount to be minimized
    constarray = constraints(x)
    x = np.array(x)
    x = np.reshape(x, (pg.zones_number, 9))
    S = 0
    for i in range(pg.zones_number):#go over all zones labels
        e_i = pg.region[pg.Rcount(i)]
        if i in pg.entries:
            S += x[i][4] * max(0, (pg.slr - e_i)) * entries_risk_foreign[i]
        for j in range(9):
            if x[i][j] ==1 and j != 4 :
                S+=max(0, (pg.slr - e_i))
    for constraint in constarray:
        S += penalty_factor * max(0, constraint) ** 2
    return S

# returns the amount to be minimized
class SimulatedAnneling():
    def __init__(self, function, T0, Tmin, alpha):#objective function, initial temp, minimal temp, temp update factor
        self.function = function
        self.T0 = T0
        self.Tmin = Tmin
        self.alpha = alpha
        self.X = np.array([])
        self.Xfitness = 0  # Fitness of current X solution
        self.best = np.array([])
        self.F_min = 0  # Fitness of best solution
        self.D = pg.zones_number *9

    def generate_initial_solution(self):
        return [random.randint(0, 1) for _ in range(self.D)]

    def update_temp(self, current_temp):
        new_temp = self.alpha * current_temp
        return new_temp

    def next_step(self, current_solution):
        """
        This function can be adapted to the problem
        """
        # Copy the solution
        new_solution = current_solution.copy()

        # Take 2 random indexes
        indexes_to_swap = random.sample(list(range(self.D)), 7)
        idx1, idx2 = indexes_to_swap[0], indexes_to_swap[1]

        # Swap the values from the indexes and handle entries problem and eleminate useless barriers
        new_solution[idx1], new_solution[idx2] = new_solution[idx2], new_solution[idx1]

        x_temp = np.array(new_solution)
        x_temp = np.reshape(x_temp, (pg.zones_number, 9))
        for i in range(pg.zones_number):
            list_foreign_indices = []
            for j in range(9):
                if not (pg.Rcount(i)[0]+util_later2[ j ][0] , pg.Rcount(i)[1]+util_later2[j ][1]) in listI:
                    list_foreign_indices.append(j)
                elif pg.region[(pg.Rcount(i)[0] + util_later2[j][0], pg.Rcount(i)[1] + util_later2[j][1])] > pg.slr:
                    x_temp[i][j] = 0
            for inx in list_foreign_indices:
                if x_temp[i][inx] == 1:
                    entries_risk_foreign[i] += 1
                    x_temp[i][inx]= 0
            if entries_risk_foreign[i]: x_temp[i][4] =1
            else : x_temp[i][4] = 0

        return list(x_temp.reshape(pg.zones_number*9))

    def get_probability(self, delta_fitness, current_temp):
        probability = math.exp(-delta_fitness / current_temp)
        return probability

    def execute(self):
        self.X = self.generate_initial_solution()
        self.Xfitness = self.function(self.X)
        self.best = self.X.copy()
        self.F_min = self.Xfitness

        t = self.T0
        while t > self.Tmin:
            # Generate a new solution from the current X solution
            newX = self.next_step(self.X)
            newX_fitness = self.function(newX)

            delta_fitness = newX_fitness - self.Xfitness

            if delta_fitness < 0:
                self.X = newX.copy()
                self.Xfitness = newX_fitness
            else:
                p = self.get_probability(delta_fitness, t)

                if random.random() < p:
                    self.X = newX.copy()
                    self.Xfitness = newX_fitness

            if self.Xfitness < self.F_min:
                self.best = self.X.copy()
                self.F_min = self.Xfitness

            t = self.update_temp(t)
            #print(t)
        x = np.array(self.best)
        x = np.reshape(x, (pg.zones_number, 9))
        S = 0
        for constraint in constraints(x):
            S += penalty_factor * max(0, constraint) ** 2
        print('RESULTS:')
        print('Objective function value(+ penalty):', self.F_min)
        print('Oblective function net value :', self.F_min - S)
        for i in range(pg.zones_number):
            for j in range(9):
                if x[i][j] == 1:
                    print('place barrier on zone '+ str(pg.Rcount(i))+' against zone '+ str((pg.Rcount(i)[0]+util_later2[ j ][0] , pg.Rcount(i)[1]+util_later2[j ][1])))

        return self.F_min


t0 = 1e100
tmin = 0.1
alpha = 0.9 # focus on this 0.9999999 or larger values so close to 1 and   THINK OF BIGGER NUMBER OF SWITCHES IN NEW STEP FUNCTION
sa = SimulatedAnneling(objective, t0, tmin, alpha)
print(sa.execute())
#it once gave 36
#fix seeds to test relations
