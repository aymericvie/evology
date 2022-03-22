#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True

# See https://stackoverflow.com/questions/30564253/cython-boundscheck-true-faster-than-boundscheck-false
from libc.math cimport tanh
from cpython cimport list

from deap import creator
import parameters

cdef double LeverageTF = parameters.LeverageTF
cdef double LeverageVI = parameters.LeverageVI
cdef double LeverageNT = parameters.LeverageNT
cdef double SCALE_TF = parameters.SCALE_TF
cdef double SCALE_VI = parameters.SCALE_VI
cdef double SCALE_NT = parameters.SCALE_NT

cdef double edf(Individual ind, double price):
    t = ind.type_as_int
    if t == 0:
        return (LeverageNT * ind.wealth / price) * tanh(SCALE_NT * ind.tsv + 0.5) - ind.asset 
    elif t == 1:
        return (LeverageVI * ind.wealth / price) * tanh(SCALE_VI * ind.tsv + 0.5) - ind.asset
    elif t == 2:
        #
        return (LeverageTF * ind.wealth / price) * tanh(SCALE_TF * ind.tsv + 0.5) - ind.asset
    else:
        raise Exception(f"Unexpected ind type: {ind.type}")

cpdef big_edf(
    Individual[:] pop,
    double price,
    double ToLiquidate,
):
    cdef double result = ToLiquidate
    cdef Individual ind
    cdef long t
    #cdef double zero
    for ind in pop:
        result += edf(ind, price)
    return result


cpdef calculate_edv(
    list pop,
    double price,
):
    cdef double total_edv = 0.0
    cdef Individual ind
    for ind in pop:
        ind.edv = edf(ind, price)
        total_edv += ind.edv
    return pop, total_edv


def convert_ind_type_to_num(t):
    # We enumerate the individual type string into integer, for faster access
    # while inside Cython.
    if t == "nt":
        return 0
    elif t == "vi":
        return 1
    else:
        return 2


cdef class Individual(list):
    def __init__(self, x):
        super().__init__(x)
        self.typecode = 'd'
        self.age = 0
        self.strategy = 0.0
        self.wealth = 0.0
        # This needs to be overriden as it is not always 'tf'!
        self.type = 'tf'
        # self.type_as_int is basically enumeration of self.type, because it is
        # much simpler for Cython to compare an int, than a Python string / C
        # char array.
        # This needs to be overriden as it is not always 0!
        self.type_as_int = 0
        self.cash = 0.0
        self.asset = 0.0
        self.loan = parameters.RefLoan
        self.margin = 0.0
        self.tsv = 0.0
        self.edv = 0.0
        self.process = 1.0
        self.ema = 0.0
        self.profit = 0.0
        self.investor_flow = 0.0
        self.investment_ratio = 0.0
        self.prev_wealth = 0.0
        self.DailyReturn = 0.0
        # This needs to be overriden as it is not always 0!
        self.fitness = creator.fitness_strategy()
        self.edf = None
