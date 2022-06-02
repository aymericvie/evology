import numpy as np
from parameters import div_atc, G_day, div_vol, INITIAL_DIVIDEND, div_tau


def ExogeneousDividends(max_generations, rng):

    dividend_series = np.zeros((1, max_generations))
    rd_dividend_series = np.zeros((1, max_generations))
    z_process = rng.standard_normal(max_generations)

    dividend = INITIAL_DIVIDEND

    dividend_series[0, 0] = dividend
    rd_dividend_series[0, 0] = z_process[0]

    for i in range(max_generations):

        wiener_back = z_process[i]
        if i > div_tau:
            wiener_back = (1.0 - div_atc**2) * z_process[
                i
            ] + div_atc * rd_dividend_series[0, i - div_tau - 1]

        dividend = abs(dividend + G_day * dividend + div_vol * dividend * wiener_back)

        dividend_series[0, i] = dividend
        rd_dividend_series[0, i] = wiener_back

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
