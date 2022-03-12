#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
cimport cythonized

def ComputeFitness(pop, Horizon):
    pop = Cython_ComputeFitness(pop, Horizon)
    return pop

cdef Cython_ComputeFitness(list pop, int Horizon):
    cdef cythonized.Individual ind
    cdef double ema 

    for ind in pop:
        #ema = (2 / (Horizon + 1)) * (ind.profit + ind.investor_flow - ind.ema) + ind.ema
        ema = (2 / (Horizon + 1)) * (ind.profit_internal + ind.investor_flow - ind.ema) + ind.ema
        ind.ema = ema
        #ind.fitness.values = (ema,)
    return pop