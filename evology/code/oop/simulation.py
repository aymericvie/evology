from tqdm import tqdm
from population import Population

class Simulation:
    def __init__(self, max_generations, population_size):
        self.max_generations = max_generations
        self.population_size = population_size
    
    # def create_pop(self):
    #     self.pop = Population(self.population_size)

    # def pop_count_wealth(self, pop, price):
    #     for ind in pop:
    #         ind.wealth = ind.count_wealth(ind, price)
    #     return pop

    def simulate(self):
        pop = Population(self.population_size)
        pop.create_pop()
        # pop = Simulation.pop_count_wealth(pop, 100)
        
        for generation in tqdm(range(self.max_generations)):
            print("Generation", generation)
        print([[ind.type, ind.wealth] for ind in pop.agents])




