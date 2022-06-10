#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True

# See https://stackoverflow.com/questions/30564253/cython-boundscheck-true-faster-than-boundscheck-false
from libc.math cimport tanh, log2, isnan, exp
from cpython cimport list
import numpy as np

from deap import creator
import parameters
import balance_sheet_cython as bsc
from parameters import Short_Size_Percent, InitialPrice

cdef double LeverageTF = parameters.LeverageTF
cdef double LeverageVI = parameters.LeverageVI
cdef double LeverageNT = parameters.LeverageNT
cdef double SCALE_TF = parameters.SCALE_TF
cdef double SCALE_VI = parameters.SCALE_VI
cdef double SCALE_NT = parameters.SCALE_NT
cdef double T_th = parameters.T_threshold
cdef double tau = parameters.tau_threshold

cpdef sigmoid(double x):
    cdef double result 
    #result = 1. / (1. + exp(-x))
    result = 2. / (1. + exp(-x))
    # result = tanh(x)
    return result

cpdef signal(double x):
    return (x-1.) ** 3.

cdef double edf(Individual ind, double price):
    cdef int t = ind.type_as_int
    #cdef double corr = - 0.5
    #cdef double m = 0.0
    #cdef double VI_price = price_means[1]
    if t == 0: # NT 
        # return (LeverageNT * ind.wealth / price) * (sigmoid(SCALE_NT * ind.tsv)) - ind.asset
        return (LeverageNT * ind.wealth / price) * (tanh(SCALE_NT * ind.tsv)) - ind.asset
        #return (LeverageNT * ind.wealth / price) * (tanh(SCALE_NT * (log2((ind.tsv * ind.val) / price)))) #- ind.asset

    elif t == 1: # VI
        
        ''' order-based with cubic (less reactive than log) '''
        #return (LeverageVI * ind.wealth / price) * (tanh(SCALE_VI * signal(ind.val / price)))
       

        ''' order-based with p(t) recursion '''
        # return (LeverageVI * ind.wealth / price) * (tanh(SCALE_VI * (log2(ind.val / price)))) - ind.asset
       
        #return (LeverageVI * ind.wealth / price) * (tanh(SCALE_VI * (log2(ind.val / price)))) #- ind.asset
        return (LeverageVI * ind.wealth / price) * (tanh(SCALE_VI * (log2(ind.val / price)))) - ind.asset

       
        ''' order-based with scalar P(t-1), no recursion'''
        #return (LeverageVI * ind.wealth / price) * (tanh(SCALE_VI * (ind.tsv))) 

        # return (LeverageVI * ind.wealth / price) * (tanh(SCALE_VI * (ind.tsv))) - ind.asset

        ''' State-dependent threshold value investor
        m = log2(ind.val / price)
        if m > T_th:
            m = T_th
        if m < - T_th:
            m = - T_th
        else:
            m = 0
        return (LeverageVI * ind.wealth / price) * (tanh(SCALE_VI * m)) 
        '''

    elif t == 2: # TF 
        return (LeverageTF * ind.wealth / price) * (tanh(SCALE_TF * ind.tsv)) - ind.asset 

    elif t == 3: # AV
        raise RuntimeError('Old ED for AV')
        ''' Sigmoid on '''
        return (ind.wealth / price) * sigmoid(ind.tsv) - ind.asset


    # BH and IR agents do not interact in the market, they are fictious agents to measure their strategy performance.
    elif t == 4 or t == 5:
        pass
    else:
        raise Exception(f"Unexpected ind type: {ind.type}")

cpdef big_edf(
    Individual[:] pop,
    double price,
    double ToLiquidate,
    double asset_supply,
    double spoils,
    double current_shorts,
):
    cdef double result = ToLiquidate 
    cdef Individual ind
    cdef long t
    cdef double ind_result
    cdef int limit = 0

    # Determine if we are at the limit of the short position sizes
    if current_shorts == asset_supply * Short_Size_Percent / 100.:
        # We have reached the limit of shorts
        # ED values below 0 for funds with short sizes must count as 0
        limit = 1
        #print('Limit is attained during clearing')

    for ind in pop:
        ind_result = edf(ind, price)
        if isnan(ind_result) == False:
            result += ind_result 
            '''
            if limit == 0:
                result += ind_result
            elif limit == 1:
                if ind.asset + ind_result < 0.:
                    result += - np.inf
                else:
                    result += ind_result
            '''
            
    return result

def agg_ed_esl(pop, ToLiquidate, asset_supply, spoils, current_short):
    # array_pop = convert_to_array(pop)
    def aggregate_ed(asset_key, price):
        return big_edf(pop, price, ToLiquidate, asset_supply, spoils, current_short)
    return aggregate_ed

cdef convert_to_array(pop):
    array_pop = np.empty(len(pop), object)
    for idx, ind in enumerate(pop):
        array_pop[idx] = ind
    return array_pop

def agg_ed(pop, ToLiquidate, asset_supply, spoils, current_short):
    array_pop = convert_to_array(pop)
    def aggregate_ed(price):
        return big_edf(array_pop, price, ToLiquidate, asset_supply, spoils, current_short)
    return aggregate_ed

cpdef calculate_edv(
    list pop,
    double price,
):
    cdef double total_edv = 0.0
    cdef Individual ind
    for ind in pop:
        ind.edv = edf(ind, price)
        if isnan(ind.edv) == False:
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
        self.val = InitialPrice
        #self.investment_series = []

    def compute_wealth(self, double price):
        cdef int replace = 0
        self.wealth = self.cash + self.asset * price - self.loan
        self.prev_wealth = self.wealth
        
        ''' if self.wealth < 0:
            replace = 1
        return replace  '''

