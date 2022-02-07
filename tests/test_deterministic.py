from test_functions import *
print('Testing seed reproducibility for 30 agents, 1,000 periods with 10 repetitions, no learning...')
test_det_pop_nolearning(10, 1000, 30)
print('...Succesful!')

print('Testing seed reproducibility for 30 agents, 1,000 periods with 10 repetitions, learning...')
test_det_pop_learning(10, 1000, 30)
print('...Succesful!')
