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
    cdef public double investor_flow
    cdef public double investment_ratio
    cdef public double prev_wealth
    cdef public double DailyReturn
    cdef public object fitness
    cdef public object edf
    cdef public int age
    cdef public double profit_internal
    cdef public double val
    cdef public double val_net
    cdef public double quarterly_wealth
    cdef public list wealth_series
