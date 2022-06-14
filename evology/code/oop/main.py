from simulation import Simulation

if __name__ == "__main__":
    s = Simulation(
        max_generations = 500, 
        population_size = 3,
        interest_rate=0.01,
        seed = 0)
    s.simulate()
