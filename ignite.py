if __name__ == '__main__':

    method = input('choose between LP, PS, SA ')

    if method == 'LP':
        import Optimizer.optimizer as optimizer
        optimizer.optimize()


    elif method == "PS":
        import Meta_heuristics.Particle_Swarm
        Particle_Swarm.PA()

    elif method == "SA":
        import Meta_heuristics.SA_attempt
        SA_attempt.SA()

