"""
@Author: Alaaeddine Maggouri
@finished on : 4/5/2023

"""
import sys
sys.path.append('/paths_generator.py')
import paths_generator as pg
import matplotlib.pyplot as plt
import numpy as np
import time

#PS varialbes
problem = 'minimize'
n_particles = 200
n_iterations = 20 # 500 was suggested
inertia_coeff = 0.9  # inertia constant
c1 = 1  # cognitive constant
c2 = 2  # social constant
#constraints
def constraints(x):
    constraints_list = []
    x = np.array(x)
    x = np.reshape(x,(pg.zones_number,pg.zones_number))
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
    for i in range(pg.zones_number):
        e_i = pg.region[pg.Rcount(i)]
        for j in range(pg.zones_number):
            S += x[i][j] * max(0,(pg.slr - e_i))
    for constraint in constarray:
        S+= penalty_factor*max(0, constraint)**2
    return S
#returns the amount to be minimized


# Visualization
fig = plt.figure()
ax = fig.add_subplot()
fig.show()
plt.title('Evolutionary process of the objective function value')
plt.xlabel("Iteration")
plt.ylabel("Objective function")

if problem == 'minimize':
    initial_fitness = float("inf")
if problem == 'maximize':
    initial_fitness = -float("inf")
n_vars = pg.zones_number**2
#main code
class Particle:
    def __init__(self, bounds):
        self.particle_position = []
        self.particle_velocity = []
        self.local_best_particle_position = []
        self.fitness_local_best_particle_position = initial_fitness  # objective function value of the best particle position
        self.fitness_particle_position = initial_fitness  # objective function value of the particle position

        for i in range(n_vars):
            self.particle_position.append(
                np.random.randint(0, 2))  # generate random initial position (modified by alaa to generate binary particles)
            self.particle_velocity.append(np.random.uniform(-1, 1))  # generate random initial velocity

    def evaluate(self, objective_function):
        self.fitness_particle_position = objective_function(self.particle_position)
        if problem == 'minimize':
            if self.fitness_particle_position < self.fitness_local_best_particle_position:
                self.local_best_particle_position = self.particle_position  # update particle's local best poition
                self.fitness_local_best_particle_position = self.fitness_particle_position  # update fitness at particle's local best position
        if problem == 'maximize':
            if self.fitness_particle_position > self.fitness_local_best_particle_position:
                self.local_best_particle_position = self.particle_position  # update particle's local best position
                self.fitness_local_best_particle_position = self.fitness_particle_position  # update fitness at particle's local best position

    def update_velocity(self, global_best_particle_position):
        for i in range(n_vars):
            r1 = np.random.rand()
            r2 = np.random.rand()

            # local explorative position displacement component
            cognitive_velocity = c1 * r1 * (self.local_best_particle_position[i] - self.particle_position[i])

            # position displacement component towards global best
            social_velocity = c2 * r2 * (global_best_particle_position[i] - self.particle_position[i])

            self.particle_velocity[i] = inertia_coeff * self.particle_velocity[i] + cognitive_velocity + social_velocity

    def update_position(self, bounds):#(ifs modified by alaa for binary particles)
        for i in range(n_vars):
            self.particle_position[i] = self.particle_position[i] + self.particle_velocity[i]

            # check and repair to satisfy the upper bounds
            if self.particle_position[i] > 1:
                self.particle_position[i] = 1
            # check and repair to satisfy the lower bounds
            if self.particle_position[i] < 0:
                self.particle_position[i] = 0


class PSO:
    def __init__(self, objective_function, bounds, n_particles, n_iterations):
        fitness_global_best_particle_position = initial_fitness
        global_best_particle_position = []
        swarm_particle = []
        for i in range(n_particles):
            swarm_particle.append(Particle(bounds))
        A = []

        for i in range(n_iterations):
            for j in range(n_particles):
                swarm_particle[j].evaluate(objective_function)

                if problem == 'minimize':
                    if swarm_particle[j].fitness_particle_position < fitness_global_best_particle_position:
                        global_best_particle_position = list(swarm_particle[j].particle_position)
                        fitness_global_best_particle_position = float(swarm_particle[j].fitness_particle_position)
                if problem == 'maximize':
                    if swarm_particle[j].fitness_particle_position > fitness_global_best_particle_position:
                        global_best_particle_position = list(swarm_particle[j].particle_position)
                        fitness_global_best_particle_position = float(swarm_particle[j].fitness_particle_position)

            for j in range(n_particles):
                swarm_particle[j].update_velocity(global_best_particle_position)
                swarm_particle[j].update_position(bounds)

            A.append(fitness_global_best_particle_position)  # record the best fitness

            x = global_best_particle_position
            # ofunc_clean = sum(x[idx] * cost2d[idx // len(J), idx % len(J)] for idx in range(cost2d.size))

            # if i% 100 == 0:
            #     print(i, fitness_global_best_particle_position, ofunc_clean, global_best_particle_position)

            # Visualization
            ax.plot(A, color='r')
            fig.canvas.draw()
            ax.set_xlim(left=max(0, i - n_iterations), right=i + 3)
            time.sleep(0.001)
        S = 0
        for constraint in constraints(x):
            S += penalty_factor * max(0, constraint) ** 2
        print('RESULTS:')
        print('Objective function value(+ penalty):', fitness_global_best_particle_position)
        print('Oblective function net value :', fitness_global_best_particle_position - S )


        x = global_best_particle_position
        x = np.array(x)
        x = np.reshape(x,(pg.zones_number, pg.zones_number))
        for i in range(pg.zones_number):
            for j in range(pg.zones_number):
                if x[i,j]:
                    print('place barrier on zone '+ str(pg.Rcount(i)) + 'against zone' + str(pg.Rcount(j)))



PSO(objective, [], n_particles, n_iterations)
plt.show()