#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True

# See https://stackoverflow.com/questions/30564253/cython-boundscheck-true-faster-than-boundscheck-false
from libc.math cimport tanh, log2, isnan
from cpython cimport list
import numpy as np

from deap import creator
import parameters

cdef double LeverageTF = parameters.LeverageTF
cdef double LeverageVI = parameters.LeverageVI
cdef double LeverageNT = parameters.LeverageNT
cdef double SCALE_TF = parameters.SCALE_TF
cdef double SCALE_VI = parameters.SCALE_VI
cdef double SCALE_NT = parameters.SCALE_NT

cdef double edf(Individual ind, double price, list price_means):
    cdef int t = ind.type_as_int
    cdef double corr = 0.1
    #cdef double VI_price = price_means[1]
    if t == 0:
        return (LeverageNT * ind.wealth / price) * tanh(SCALE_NT * ind.tsv + corr) - ind.asset 
    elif t == 1:
        ''' for previous-price VI '''
        #return (LeverageVI * ind.wealth / price) * tanh(SCALE_VI * ind.tsv + corr) - ind.asset
        ''' for contemporaneous-price VI '''
        return (LeverageVI * ind.wealth / price) * tanh(SCALE_VI * (log2(ind.val / price)) + corr) - ind.asset
    elif t == 2: # TF
        return (LeverageTF * ind.wealth / price) * tanh(SCALE_TF * ind.tsv + corr) - ind.asset 
    elif t == 3: # AV
        return (ind.wealth / price) * tanh(ind.tsv) - ind.asset 
    # BH and IR agents do not interact in the market, they are fictious agents to measure their strategy performance.
    elif t == 4 or t == 5:
        pass
    else:
        raise Exception(f"Unexpected ind type: {ind.type}")

cpdef big_edf(
    Individual[:] pop,
    double price,
    double ToLiquidate,
    list price_means
):
    cdef double result = ToLiquidate
    cdef Individual ind
    cdef long t
    cdef double ind_result
    #cdef double zero
    for ind in pop:
        ind_result = edf(ind, price, price_means)
        if isnan(ind_result) == False:
            result += ind_result
    return result

def agg_ed_esl(pop, ToLiquidate, price_means):
    # array_pop = convert_to_array(pop)
    def aggregate_ed(asset_key, price):
        return big_edf(pop, price, ToLiquidate, price_means)
    return aggregate_ed

cdef convert_to_array(pop):
    array_pop = np.empty(len(pop), object)
    for idx, ind in enumerate(pop):
        array_pop[idx] = ind
    return array_pop

def agg_ed(pop, ToLiquidate, price_means):
    array_pop = convert_to_array(pop)
    def aggregate_ed(price):
        return big_edf(array_pop, price, ToLiquidate, price_means)
    return aggregate_ed

cpdef calculate_edv(
    list pop,
    double price,
    list price_means
):
    cdef double total_edv = 0.0
    cdef Individual ind
    for ind in pop:
        ind.edv = edf(ind, price, price_means)
        total_edv += ind.edv
    return pop, total_edv


def convert_ind_type_to_num(t):
    # We enumerate the individual type string into integer, for faster access
    # while inside Cython.
    if t == "nt":
        return 0
    elif t == "vi":
        return 1
    elif t == 'tf':
        return 2
    elif t == 'av':
        return 3
    elif t == 'bh':
        return 4
    elif t == 'ir':
        return 5
    else:
        return TypeError('Unrecognised type' +str(t))


cdef class Individual(object):
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
        #self.process = 1.0
        self.ema = 0.0
        self.profit = 0.0
        #self.investor_flow = 0.0
        #self.investment_ratio = 0.0
        self.prev_wealth = 0.0
        self.DailyReturn = 0.0
        # This needs to be overriden as it is not always 0!
        self.fitness = creator.fitness_strategy()
        #self.edf = None
        self.wealth_series = []
        self.last_wealth = 0.0
        self.last_price = 100.0
        self.adaptive_strategy = None
        self.strategy_index = 0
        #self.investment_series = []

    def compute_wealth(self, double price):
        cdef int replace = 0
        self.wealth = self.cash + self.asset * price - self.loan
        self.prev_wealth = self.wealth
        
        ''' if self.wealth < 0:
            replace = 1
        return replace  '''

