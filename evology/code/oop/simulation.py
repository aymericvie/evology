from tqdm import tqdm
from population import Population
from asset import Asset

class Simulation:
    def __init__(self, max_generations, population_size):
        self.max_generations = max_generations
        self.population_size = population_size


    def simulate(self):
        pop = Population(self.population_size)
        asset = Asset()
        pop.create_pop()
        pop.count_wealth(self.price)
        
        for generation in tqdm(range(self.max_generations)):
            print("Generation", generation)
        print([[ind.type, ind.wealth] for ind in pop.agents])




