import sys
sys.path.append('./evology/code/oop')
import numpy as np
from main import main as model
import multiprocessing as mp

np.random.seed()

# def runs(repetitions, time, agents):
#     went_smoothly = True
#     i = 0
#     while i < repetitions:
#         try: 
#             seed = np.random.randint(0,100000)
#             wealth_coords = np.random.dirichlet(np.ones(3), size=1)[0].tolist()
#             np.random.seed(seed)
#             inv_bool = random_bool()
#             df = model(time, agents, wealth_coords, 0.01, inv_bool, seed)
#         except Exception as e: 
#             went_smoothly = False
#             print('Investment Bool ' + str(inv_bool))
#             print('Seed ' + str(seed))
#             print('Coords ' + str(wealth_coords))
#             print(str(e))
#             break
#         i += 1
#     return went_smoothly

# def test_runs(repetitions, time, agents,):
#     went_smoothly = runs(repetitions, time, agents)
#     assert went_smoothly == True

# def random_bool():
#     n = np.random.random()
#     if n <= 0.5:
#         return True
#     else:
#         return False 

# # print('For multiprocessing')
# # import multiprocessing as mp
# # print(mp.cpu_count())

# print('Testing many short runs...')
# test_runs(30, 1000, 3)
# print('Succesful!')

# print('Testing long runs with higher populations ...')
# test_runs(10, 100000, 10)
# print('Succesful!')

# """
# new mp design for tests
# """

# # TODO: add a determinism test as well?
# # TODO: multiprocessing?

def random_bool():
    n = np.random.random()
    if n <= 0.5:
        return True
    else:
        return False 

def job1():
    went_smoothly = True
    time, agents = 1000, 3
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
        went_smoothly = False
    assert went_smoothly == True
        
def job2():
    went_smoothly = True
    time, agents = 100000, 10
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
        went_smoothly = False
    assert went_smoothly == True
    


# Run experiment
def main():
    repetitions1, repetitions2 = 30, 10
    p = mp.Pool()
    p.map(job1, range(repetitions1))
    p.map(job2, range(repetitions2))
    p.close()


if __name__ == "__main__":
    data = main()