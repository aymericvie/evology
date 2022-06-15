import sys
sys.path.append('./evology/code/oop')
import numpy as np
from main import main as model

def runs(repetitions, time, agents, inv_bool):
    went_smoothly = True
    i = 0
    while i < repetitions:
        try: 
            seed = np.random.randint(0,100)
            np.random.seed(seed)
            df = model(time, agents, 0.01, inv_bool, seed)
        except Exception as e: 
            went_smoothly = False
            print('Investment Bool ' + str(inv_bool))
            print('Seed ' + str(seed))
            print(str(e))
            break
        i += 1
    return went_smoothly

def test_runs(repetitions, time, agents, inv_bool):
    went_smoothly = runs(repetitions, time, agents, inv_bool)
    assert went_smoothly == True

def random_bool():
    n = np.random()
    if n <= 0.5:
        return True
    else:
        return False 

print('Testing many short runs')
test_runs(30, 1000, 3, random_bool())

print('Testing less long runs')
test_runs(5, 100000, 3, random_bool())

# TODO: add a determinism test as well?
# TODO: multiprocessing?