'''
@author : Sir Alaaeddine Maggouri
@finishid on : 10/4/2023
'''

import random
import math
import numpy as np
import paths_generator as pg

util_later1 = {}
util_later2 = {}
util = -1
for r in [-1, 0, 1]:
    l = [-1, 0, 1] if r != 0 else [-1, 1]
    for c in l:
        util+=1
        util_later1[(r,c)] = util
        util_later2[util] = (r,c)

def constraints(x):
    # takes a list of xij- i refers to a zone label-j refers to one of its 8 surrounding zones
    # returns an array where each element should be <= 0

    constraints_list = []
    x = np.array(x)
    x = np.reshape(x, (pg.zones_number, 8))
    for asset_label in pg.T_Ci.keys():
        for road_labels in pg.T_Ci[asset_label]:
            temp = []
            for i in range(len(road_labels)-1):
                m,k = pg.Rcount(road_labels[i+1])
                for r in [-1, 0, 1]:
                    l = [-1,0,1] if r!=0 else [-1,1]
                    for c in l:
                        if pg.count(m+r, k+c) == road_labels[i]:
                            temp.append(x[road_labels[i+1]][util_later1[(r,c)]])
            constraints_list.append(1-sum(temp))
    return np.array(constraints_list)

penalty_factor = 100

def objective(x):
    #takes a list of xij- i refers to a zone label-j refers to one of its 8 surrounding zones
    # returns the amount to be minimized
    constarray = constraints(x)
    x = np.array(x)
    x = np.reshape(x, (pg.zones_number, 8))
    S = 0
    for i in range(pg.zones_number):#go over all zones labels
        e_i = pg.region[pg.Rcount(i)]
        for j in range(8):
            S += x[i][j] * max(0, (pg.slr - e_i))
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
        self.D = pg.zones_number *8

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
        indexes_to_swap = random.sample(list(range(self.D)), 2)
        idx1, idx2 = indexes_to_swap[0], indexes_to_swap[1]

        # Swap the values from the indexes
        new_solution[idx1], new_solution[idx2] = new_solution[idx2], new_solution[idx1]
        return new_solution

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
            print(t)
        x = np.array(self.best)
        x = np.reshape(x, (pg.zones_number, 8))
        for i in range(pg.zones_number):
            for j in range(8):
                if x[i][j] == 1:
                    print('place barrier on zone '+ str(pg.Rcount(i))+' against zone '+ str((pg.Rcount(i)[0]+util_later2[ x[i][j] ][0] , pg.Rcount(i)[1]+util_later2[ x[i][j] ][1])))

        return self.F_min


t0 = 1e100
tmin = 0.1
alpha = 0.9 # focus on this 0.9999999 or larger values so close to 1 and   THINK OF BIGGER NUMBER OF SWITCHES IN NEW STEP FUNCTION
sa = SimulatedAnneling(objective, t0, tmin, alpha)
print(sa.execute())
#it once gave 36