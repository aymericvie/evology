import sys
sys.path.append('./evology/code/oop')
import numpy as np
from main import main as model

np.random.seed()

def runs(repetitions, time, agents):
    went_smoothly = True
    i = 0
    while i < repetitions:
        try: 
            seed = np.random.randint(0,100000)
            wealth_coords = np.random.dirichlet(np.ones(3), size=1)[0].tolist()
            np.random.seed(seed)
            inv_bool = random_bool()
            df = model(time, agents, wealth_coords, 0.01, inv_bool, seed)
        except Exception as e: 
            went_smoothly = False
            print('Investment Bool ' + str(inv_bool))
            print('Seed ' + str(seed))
            print('Coords ' + str(wealth_coords))
            print(str(e))
            break
        i += 1
    return went_smoothly

def test_runs(repetitions, time, agents,):
    went_smoothly = runs(repetitions, time, agents)
    assert went_smoothly == True

def random_bool():
    n = np.random.random()
    if n <= 0.5:
        return True
    else:
        return False 

# print('For multiprocessing')
# import multiprocessing as mp
# print(mp.cpu_count())

print('Testing many short runs...')
test_runs(30, 1000, 3)
print('Succesful!')

print('Testing long runs with higher populations ...')
test_runs(10, 100000, 10)
print('Succesful!')



# TODO: add a determinism test as well?
# TODO: multiprocessing?