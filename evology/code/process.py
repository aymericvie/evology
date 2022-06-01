from parameters import RHO_NT, MU_NT, GAMMA_NT

def ExogeneousProcess(MAX_GENERATIONS, rng):
    process_series = []
    value = MU_NT # Initial value of the process
    randoms = rng.normal(0, 1, MAX_GENERATIONS)

    for i in range(MAX_GENERATIONS):
        value = abs(value + RHO_NT * (MU_NT - value) + GAMMA_NT * randoms[i])
        process_series.append(value)

    return process_series

def FictiousPriceSeries(rng):
    previous_price_series = []
    price_history = []
    length = 1000
    value = 100
    randoms = rng.normal(0, 1, length)

    for i in range(length):
        value = value + (RHO_NT/10) * (100 - value) + GAMMA_NT * randoms[i]
        previous_price_series.append(value)

    previous_price_series_reversed = reversed(previous_price_series)

    for item in previous_price_series_reversed:
        price_history.append(item)
    
    return price_history


# import numpy as np
# import matplotlib.pyplot as plt
# rng = np.random.default_rng(seed=9)
# price_history = FictiousPriceSeries(rng)
# plt.plot(price_history)
# plt.show()

