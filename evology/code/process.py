from parameters import RHO_NT, MU_NT, GAMMA_NT

def ExogeneousProcess(MAX_GENERATIONS, rng):
    process_series = []
    value = 1. # Initial value of the process
    randoms = rng.normal(0, 1, MAX_GENERATIONS)

    for i in range(MAX_GENERATIONS):
        value = value + RHO_NT * (MU_NT - value) + GAMMA_NT * randoms[i]
        process_series.append(value)

    return process_series

def FictiousPriceSeries(rng):
    previous_price_series = []
    price_history = []
    value = 100
    randoms = rng.normal(0, 1, 252)

    for i in range(252):
        value = value + RHO_NT * (MU_NT - value) + GAMMA_NT * randoms[i]
        previous_price_series.append(value)

    previous_price_series_reversed = reversed(previous_price_series)

    for item in previous_price_series_reversed:
        price_history.append(item)
    
    return price_history

