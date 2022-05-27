#!/usr/bin/env python3
from test_functions import *

print('[Scholl] Testing for 10 agents, 100,000 periods with 10 repetitions...')
test_nolearning(10, 100_000, 10)
print('...Succesful!')

print('[Extended] Testing for 100 agents, 100,000 periods with 10 repetitions...')
test_nolearning_ext(10, 100_000, 100)
print('...Succesful!')


