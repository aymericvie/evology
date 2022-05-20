import numpy as np
from parameters import div_atc, G_day, div_vol, INITIAL_DIVIDEND

def ExogeneousDividends(max_generations, rng):

    dividend_series = np.zeros((1, max_generations))
    rd_dividend_series = np.zeros((1, max_generations))
    z_process = rng.random(max_generations)

    dividend = INITIAL_DIVIDEND
    rdiv = z_process[0]

    dividend_series[0,0] = dividend
    rd_dividend_series[0,0] = rdiv 

    for i in range(max_generations - 1):

        rdiv = div_atc * rdiv + (1 - div_atc ** 2) * z_process[i]
        dividend = (1. + G_day + div_vol * rdiv) * dividend 

        dividend_series[0,i] = dividend
        rd_dividend_series[0,i] = rdiv 

    return dividend_series, rd_dividend_series



# cpdef draw_dividend(double dividend, list random_dividend_history):

#     cdef double Z = np.random.normal(0,1)
#     cdef double random_dividend

#     if len(random_dividend_history) > 2:
#         random_dividend =  (
#             div_atc * random_dividend_history[-2] 
#             + (1.0 - div_atc ** 2.0) * Z)
#     else:
#         random_dividend = Z
#     #) * random_dividend + parameters.div_atc * random_dividend_history[
#     #    - 1.0 - 1.0
#         #]
#     dividend = abs(
#         dividend * (1 + G_day)
#         + div_vol * dividend * random_dividend
#     )
#     return dividend, random_dividend