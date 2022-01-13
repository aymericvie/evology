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

cpdef big_edf(
    Individual[:] pop,
    double price,
    double ToLiquidate,
):
    cdef double result = ToLiquidate
    cdef Individual ind
    cdef long t
    cdef double zero
    for ind in pop:
        t = ind.type_as_int
        if t == 0:
            result += (LeverageTF * ind.wealth / price) * tanh(SCALE_TF * ind.tsv) - ind.asset
        elif t == 1:
            zero = ind[0]
            result += (LeverageVI * ind.wealth / price) * tanh((5/zero) * (zero - price)) - ind.asset
        elif t == 2:
            zero = ind[0]
            result += (LeverageNT * ind.wealth / price) * tanh((5/(zero * ind.process)) * (zero * ind.process - price)) - ind.asset
        else:
            raise Exception(f"Unexpected ind type: {ind.type}")
    return result


def convert_ind_type_to_num(t):
    # We enumerate the individual type string into integer, for faster access
    # while inside Cython.
    if t == "tf":
        return 0
    elif t == "vi":
        return 1
    else:
        return 2


cdef class Individual(list):
    cdef object typecode
    cdef public double strategy
    cdef public double wealth
    cdef public object type
    cdef public long type_as_int
    cdef public double cash
    cdef public double asset
    cdef public double loan
    cdef public double margin
    cdef public double tsv
    cdef public double edv
    cdef public double process
    cdef public double ema
    cdef public double profit
    cdef public double prev_wealth
    cdef public double DailyReturn
    cdef public double leverage
    cdef public object fitness
    cdef public object edf

    def __init__(self, x):
        super().__init__(x)
        self.typecode = 'd'
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
        self.prev_wealth = 0.0
        self.DailyReturn = 0.0
        # This needs to be overriden as it is not always 0!
        self.leverage = 0.0
        self.fitness = creator.fitness_strategy()
        self.edf = None