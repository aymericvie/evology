from parameters import RHO_NT, MU_NT, GAMMA_NT

def ExogeneousProcess(MAX_GENERATIONS, rng):
    process_series = []
    value = 1. # Initial value of the process
    randoms = rng.normal(0, 1, MAX_GENERATIONS)

    for i in range(MAX_GENERATIONS):
        value = value + RHO_NT * (MU_NT - 1. - value) + GAMMA_NT * randoms[i]
        process_series.append(value)

    return process_series
