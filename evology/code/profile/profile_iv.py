import sys
import random
sys.path.append("./evology/code/")
sys.path.append("/Users/aymericvie/Documents/GitHub/evology/evology/code")
from steps import *
from parameters import *
import numpy as np
from investment import sigmoid


@profile
def profile_iv(popsize, iterations):
    pop, asset_supply = cr.CreatePop(popsize, 'extended', [1/3, 1/3, 1/3], 100)
    for ind in pop:
        ind.wealth_series = [random.randint(1000, 10000) + 1] * 63
        if ind.wealth_series[0] == 0:
            print(ind.wealth_series)
            raise ValueError('Wealth series = 0')
        ind.age = 65

    for t in tqdm(range(iterations)):
        
        # Apply investment
        randoms = np.random.random(size=len(pop))
        gumbel_draws_positive = np.random.gumbel(3.89050923, 2.08605884, size=len(pop)) 
        gumbel_draws_negative = np.random.gumbel(3.55311431, 2.13949923, size=len(pop)) 

        for i, ind in enumerate(pop):
            if ind.age >= 63:    
                if randoms[i] <= sigmoid((ind.wealth / ind.wealth_series[0]) - 1.):
                    ind.cash += (- gumbel_draws_negative[i] / (6300)) * ind.wealth
                else: #positive side
                    ind.cash += (gumbel_draws_positive[i] / (6300)) * ind.wealth
    return pop


np.random.seed(8)
pop = profile_iv(1000, 1000)

# kernprof -v -l profile/profile_iv.py > profile/profile_iv.txt