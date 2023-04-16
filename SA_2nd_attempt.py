'''
@author : Sir Alaaeddine Maggouri
@finishid on : 10/4/2023
'''
import matplotlib.pyplot as plt
import random
import math
import numpy as np
import paths_generator as pg
from collections import defaultdict
pg.generator()

interisting_zones = defaultdict(int)
for i in range(pg.zones_number):
    for asset in pg.T_Ci.keys():
        for road in pg.T_Ci[asset]:
            if i in road:
                interisting_zones[i] = 1
                break

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
            m, k = pg.Rcount(road_labels[0])
            for r in [-1, 0, 1]:
                for c in [-1, 0, 1]:
                    if road_labels[0] in pg.entries and not (m + r, k + c) in listI:
                        temp.append(x[road_labels[0]][4])
                    if len(road_labels)>1 and pg.count(m + r, k + c) == road_labels[1]:
                        temp.append(x[road_labels[0]][util_later1[(r, c)]])
            for i in range(len(road_labels)-1):
                visited_entry = 0
                m,k = pg.Rcount(road_labels[i+1])
                mm,kk = pg.Rcount(road_labels[i])
                for r in [-1, 0, 1]:
                    for c in [-1,0,1]:
                        if road_labels[i+1] in pg.entries and not (m+r, k+c) in listI :
                            if not visited_entry:
                                temp.append(x[road_labels[i+1]][4])
                                visited_entry = 1
                        on_current = 0
                        on_other_side = 0
                        if pg.count(m+r, k+c) == road_labels[i]:
                            #temp.append(x[road_labels[i+1]][util_later1[(r,c)]])
                            on_current = x[road_labels[i+1]][util_later1[(r,c)]]
                        if pg.count(mm+r, kk+c) == road_labels[i+1]:
                            on_other_side = x[road_labels[i]][util_later1[(r,c)]]
                        temp.append(on_other_side or on_current)
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
        init = [0 for _ in range(self.D)]
        init = np.array(init)
        init = np.reshape(init, (pg.zones_number, 9))
        for i in pg.assets:
            for j in range(9):
                init[i][j] = 1
            init[i][4] = 0
        for i in range(pg.zones_number):
            list_foreign_indices = []
            for j in range(9):
                if not interisting_zones[i]:
                    init[i][j] = 0
                    continue
                if interisting_zones and not (pg.Rcount(i)[0]+util_later2[ j ][0] , pg.Rcount(i)[1]+util_later2[j ][1]) in listI:
                    list_foreign_indices.append(j)
                elif interisting_zones and pg.region[(pg.Rcount(i)[0] + util_later2[j][0], pg.Rcount(i)[1] + util_later2[j][1])] >= pg.slr:
                    init[i][j] = 0
            if interisting_zones[i]:
                for inx in list_foreign_indices:
                    if init[i][inx] == 1:
                        entries_risk_foreign[i] += 1
                        init[i][inx]= 0
                if entries_risk_foreign[i]: init[i][4] =1
                else : init[i][4] = 0
        # return [random.randint(0, 1) for _ in range(self.D)]
        return list(init.reshape(self.D,))

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
        new_solution[idx1], new_solution[idx2]= new_solution[idx2],new_solution[idx1]

        # Take 5 random indexes

        # indexes_to_swap = random.sample(list(range(self.D)), 7)
        # idx1, idx2,idx3, idx4, idx5,idx6,idx7 = indexes_to_swap[0], indexes_to_swap[1],indexes_to_swap[2],indexes_to_swap[3],indexes_to_swap[4],indexes_to_swap[5],indexes_to_swap[6]
        # new_solution[idx1], new_solution[idx2],new_solution[idx3],new_solution[idx4],new_solution[idx5],new_solution[idx6] ,new_solution[idx7]  = \
        #     new_solution[idx2], new_solution[idx3],new_solution[idx4],new_solution[idx5],new_solution[idx6],new_solution[idx7],new_solution[idx1]
        # # Swap the values from the indexes and handle entries problem and eleminate useless barriers
        # #no barriers on zones having part in no road
        x_temp = np.array(new_solution)
        x_temp = np.reshape(x_temp, (pg.zones_number, 9))
        for i in range(pg.zones_number):
            list_foreign_indices = []
            for j in range(9):
                if not interisting_zones[i]:
                    x_temp[i][j] = 0
                    continue
                if interisting_zones and not (pg.Rcount(i)[0]+util_later2[ j ][0] , pg.Rcount(i)[1]+util_later2[j ][1]) in listI:
                    list_foreign_indices.append(j)
                elif interisting_zones and pg.region[(pg.Rcount(i)[0] + util_later2[j][0], pg.Rcount(i)[1] + util_later2[j][1])] >= pg.slr:
                    x_temp[i][j] = 0
            if interisting_zones[i]:
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
        self.values = [self.Xfitness]
        self.iterations = [0]

        t = self.T0
        while t > self.Tmin:
            self.iterations.append(self.iterations[-1]+1)
            # Generate a new solution from the current X solution
            newX = self.next_step(self.X)
            newX_fitness = self.function(newX)
            self.values.append(newX_fitness)

            delta_fitness = newX_fitness - self.Xfitness

            if delta_fitness < 0:
                self.X = newX.copy()
                self.Xfitness = newX_fitness
            else:
                p = self.get_probability(delta_fitness, t)

                if 0.2 <= p:#small or random
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
        print('Objective function net value :', self.F_min - S)
        for i in range(pg.zones_number):
            for j in range(9):
                if x[i][j] == 1:
                    print('place barrier on zone '+ str(pg.Rcount(i))+' against zone '+ str((pg.Rcount(i)[0]+util_later2[ j ][0] , pg.Rcount(i)[1]+util_later2[j ][1])))
        plt.plot(self.iterations, self.values)
        plt.show()


t0 = 1e100
tmin = 0.1
alpha = 0.9999 # focus on this 0.9999999 or larger values so close to 1 and   THINK OF BIGGER NUMBER OF SWITCHES IN NEW STEP FUNCTION
sa = SimulatedAnneling(objective, t0, tmin, alpha)
print(sa.execute())
#it once gave 36
#fix seeds to test relations
