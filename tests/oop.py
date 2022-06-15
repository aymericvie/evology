import sys
sys.path.append('./evology/code/oop')
import numpy as np
from main import main as model

def runs(repetitions, time, agents):
    went_smoothly = True
    i = 0
    while i < repetitions:
        try: 
            seed = np.random.randint(0,100)
            np.random.seed(seed)
            df = model(time, agents, 0.01, False, seed)
        except Exception as e: 
            went_smoothly = False
            print('Seed ' + str(seed))
            print('Process ' + str(i) + ' encoutered an exception.')
            print(str(e))
            break
        i += 1
    return went_smoothly

def test_runs(repetitions, time, agents):
    went_smoothly = runs(repetitions, time, agents)
    assert went_smoothly == True

print('Testing many short runs')
test_runs(30, 1000, 3)

print('Testing less long runs')
test_runs(5, 100000, 3)

# TODO: add a determinism test as well?
# TODO: multiprocessing?