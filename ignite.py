"""
@Author: Alaaeddine Maggouri
@finished on : 4/5/2023

"""

if __name__ == '__main__':

    method = input('choose between LP, PS, SA ')

    if method == 'LP':
        import optimizer
        optimizer.optimize()


    elif method == "PS":
        import Particle_Swarm
        Particle_Swarm.PA()

    elif method == "SA":
        import SA_attempt
        SA_attempt.SA()

