from simulation import Simulation

def main(
    max_generations, 
    population_size,
    interest_rate,
    seed
    ):
    s = Simulation(
        max_generations = max_generations, 
        population_size = population_size,
        interest_rate=interest_rate,
        seed = seed)
    s.simulate()

if __name__ == "__main__":
    main(
        max_generations = 10000, 
        population_size = 3,
        interest_rate = 0.01,
        seed = 0
    )    
    
