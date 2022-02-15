#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True

#!/usr/bin/env python3
import pandas as pd
import numpy as np
import balance_sheet as bs
from libc.math cimport log, sqrt, isnan

from parameters import *
cimport cythonized
cdef float NAN
NAN = float("nan")

cdef double nanmean(double[:] x) nogil:
    cdef int N = len(x)
    cdef double out = 0.0
    cdef int i = 0
    cdef int N2 = 0
    for i in range(N):
        if isnan(x[i]) == False:
            out += x[i]
            N2 += 1
    return out / N2

cdef double nanstd(double[:] x) nogil:
    cdef int N = len(x)
    cdef double _mean = nanmean(x)
    cdef double out = 0.0
    cdef int i = 0
    cdef int N2 = 0
    for i in range(N):
        if isnan(x[i]) == False:
            out += (x[i] - _mean) ** 2
            N2 += 1
    return sqrt(out / N2)

columns = [
    # Global variables
    "Gen",
    "Price",
    "Mismatch",
    "Dividends",
    "RDividend",
    "Volume",
    "Rep",
    "Pos+",
    "Pos-",
    # General ecology variables
    "Num_NT",
    "Num_VI",
    "Num_TF",
    "Mean_NT",
    "Mean_VI",
    "Mean_TF",
    "WShare_NT",
    "WShare_VI",
    "WShare_TF",
    # Noise traders
    "NT_cash",
    "NT_lending",
    "NT_loans",
    "NT_nav",
    "NT_pnl",
    "NT_signal",
    "NT_stocks",
    "NT_returns",
    "NT_returns_noinv",
    # Value investors
    "VI_cash",
    "VI_lending",
    "VI_loans",
    "VI_nav",
    "VI_pnl",
    "VI_signal",
    "VI_stocks",
    "VI_returns",
    "VI_returns_noinv",
    # Trend followers
    "TF_cash",
    "TF_lending",
    "TF_loans",
    "TF_nav",
    "TF_pnl",
    "TF_signal",
    "TF_stocks",
    "TF_returns",
    "TF_returns_noinv",
    # Additional measures
    "MeanReturn",
    "Spoils",
    "Liquidations",
    # More measures
    "PerSpoils",
    "NT_DayReturns",
    "VI_DayReturns",
    "TF_DayReturns",
    "AvgDayReturn",
    # Measures of adaptation
    "CountSelected",
    "CountMutated",
    "CountCrossed",
    "TowardsNT",
    "TowardsVI",
    "TowardsTF",
    "FromNT",
    "FromVI",
    "FromTF",
    "WealthAmp",
    # Annual Sharpes and Delta
    "SharpeNT",
    "SharpeVI",
    "SharpeTF",
    "Delta",
    # Annual return computed over wealth
    "NT_AnnualReturns",
    "VI_AnnualReturns",
    "TF_AnnualReturns",
    # Annual return computed over wealth, without investment
    "NT_AnnualReturns_Noinv",
    "VI_AnnualReturns_Noinv",
    "TF_AnnualReturns_Noinv",
    # Significance
    "AvgSignificance",
    "AvgNumberDev",
    "PerSignif",
    "NTflows",
    "VIflows",
    "TFflows",
]
variables = len(columns) 

""" We only record results after a year to avoid transient period biases. """
Barr = max(SHIELD_DURATION, ShieldResults)

def TrackWealth(wealth_tracker, pop, generation):
    cdef double wamp = NAN
    cdef int i = 0
    cdef cythonized.Individual ind
    wamp_list = []

    if generation - 21 >= 0:
        for i, ind in enumerate(pop):
         # We can start calculate the movements' monthly amplitude.
            old_wealth = wealth_tracker[generation-21,i]
            #for ind in pop:
            if old_wealth > 0 and ind.age >= 21:
                wamp_ind = (wealth_tracker[generation, i] - old_wealth) / old_wealth
            else: 
                wamp_ind = float("nan")
            wamp_list.append(100 * abs(wamp_ind))
    wamp = np.nanmean(wamp_list)
        
    return wealth_tracker, wamp




def AnnualReturns(wealth_tracker, pop, generation):
    cdef double wamp_nt = NAN
    cdef double wamp_vi = NAN
    cdef double wamp_tf = NAN
    cdef int i = 0
    cdef cythonized.Individual ind

    wamp_list_nt, wamp_list_vi, wamp_list_tf,  = [],[],[]
    
    
    if generation - 252 >= 0: # We can start calculate the movements' annual amplitude.
        for i, ind in enumerate(pop):
            old_wealth = wealth_tracker[generation-252,i]
            #for ind in pop:
            if old_wealth > 0 and ind.age >= 252 + 10:
                wamp_ind = (wealth_tracker[generation, i] - old_wealth) / old_wealth
            else: 
                wamp_ind = float("nan")

            if ind.type == 'nt':
                wamp_list_nt.append(wamp_ind)
            elif ind.type == 'vi':
                wamp_list_vi.append(wamp_ind)
            elif ind.type == 'tf':
                wamp_list_tf.append(wamp_ind)

    wamp_nt = np.nanmean(wamp_list_nt)
    wamp_vi = np.nanmean(wamp_list_vi)
    wamp_tf = np.nanmean(wamp_list_tf)
        
    return wamp_nt, wamp_vi, wamp_tf


def AnnualReturnsNoInv(wealth_tracker_noinv, pop, generation):
    cdef double NT_AR_noinv = NAN
    cdef double VI_AR_noinv = NAN
    cdef double TF_AR_noinv = NAN
    cdef int i = 0
    cdef cythonized.Individual ind

    list_nt, list_vi, list_tf,  = [],[],[]
    
    if generation - 252 >= 0: # We can start calculate the movements' annual amplitude.
        for i, ind in enumerate(pop):
            old_wealth = wealth_tracker_noinv[generation-252,i]
            #for ind in pop:
            if old_wealth > 0 and ind.age >= 252 + 10:
                w_ind = (wealth_tracker_noinv[generation, i] - old_wealth) / old_wealth
            else: 
                w_ind = float("nan")

            if ind.type == 'nt':
                list_nt.append(w_ind)
            elif ind.type == 'vi':
                list_vi.append(w_ind)
            elif ind.type == 'tf':
                list_tf.append(w_ind)

    NT_AR_noinv = np.nanmean(list_nt)
    VI_AR_noinv = np.nanmean(list_vi)
    TF_AR_noinv = np.nanmean(list_tf)
        
    return NT_AR_noinv, VI_AR_noinv, TF_AR_noinv 

def ResultsProcess(list pop, double spoils, double price):

    LongAssets, ShortAssets = 0.0, 0.0
    NTcount, VIcount, TFcount = 0.0, 0.0, 0.0
    MeanNT, MeanVI, MeanTF = 0.0, 0.0, 0.0
    WSNT, WSVI, WSTF = 0.0, 0.0, 0.0
    NTcash, NTlend, NTloan, NTnav, NTpnl, NTsignal, NTstocks, NTreturn, NTreturn_noinv = (
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0, #float("nan"),
        0.0, #float("nan"),
    )
    VIcash, VIlend, VIloan, VInav, VIpnl, VIsignal, VIstocks, VIreturn, VIreturn_noinv = (
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0, #float("nan"),
        0.0, #float("nan"),
    )
    TFcash, TFlend, TFloan, TFnav, TFpnl, TFsignal, TFstocks, TFreturn, TFreturn_noinv = (
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0, #float("nan"),
        0.0, # float("nan"),
    )

    NTflows, VIflows, TFflows = 0.0, 0.0, 0.0

    cdef cythonized.Individual ind
    cdef double ind_zero
    for ind in pop:

        if ind.asset > 0.0:
            LongAssets += ind.asset
        elif ind.asset < 0.0:
            ShortAssets += abs(ind.asset)

        ind_zero = ind[0]
        if ind.type == "nt":
            NTcount += 1
            MeanNT += ind_zero
            NTcash += ind.cash
            NTlend += ind.margin
            NTloan += ind.loan
            NTnav += ind.wealth  # before, we imposed w>0
            if ind.wealth > 0:
                WSNT += ind.wealth
            NTpnl += ind.profit
            NTsignal += ind_zero * ind.process  # already included?
            NTstocks += price * ind.asset
            if ind.prev_wealth != 0:
                NTreturn += ind.DailyReturn
            if ind.prev_wealth_noinv != 0:
                NTreturn_noinv += ind.DailyReturn_noinv
            NTflows += ind.investment_ratio

        elif ind.type == "vi":
            VIcount += 1
            MeanVI += ind_zero
            VIcash += ind.cash
            VIlend += ind.margin
            VIloan += ind.loan
            VInav += ind.wealth  # before, we imposed w>0
            if ind.wealth > 0:
                WSVI += ind.wealth
            VIpnl += ind.profit
            # VIsignal += ind[0] #double with MeanVI
            VIstocks += price * ind.asset
            if ind.prev_wealth != 0:
                VIreturn += ind.DailyReturn
            if ind.prev_wealth_noinv != 0:
                VIreturn_noinv += ind.DailyReturn_noinv
            VIflows += ind.investment_ratio

        elif ind.type == "tf":
            TFcount += 1
            MeanTF += ind_zero
            TFcash += ind.cash
            TFlend += ind.margin
            TFloan += ind.loan
            TFnav += ind.wealth  # before, we imposed w>0
            if ind.wealth > 0:
                WSTF += ind.wealth
            TFpnl += ind.profit
            TFsignal += ind.tsv
            TFstocks += price * ind.asset
            if ind.prev_wealth != 0:
                TFreturn += ind.DailyReturn
            if ind.prev_wealth_noinv != 0:
                TFreturn_noinv += ind.DailyReturn_noinv
            TFflows += ind.investment_ratio

    if NTcount != 0:
        NTcash = NTcash / NTcount
        NTlend = NTlend / NTcount
        NTloan = NTloan / NTcount
        NTnav = NTnav / NTcount
        NTpnl = NTpnl / NTcount
        NTstocks = NTstocks / NTcount
        NTreturn = NTreturn / NTcount
        NTreturn_noinv = NTreturn_noinv / NTcount
        NTsignal = NTsignal / NTcount
        MeanNT = MeanNT / NTcount

    if VIcount != 0:
        VIcash = VIcash / VIcount
        VIlend = VIlend / VIcount
        VIloan = VIloan / VIcount
        VInav = VInav / VIcount
        VIpnl = VIpnl / VIcount
        VIstocks = VIstocks / VIcount
        VIreturn = VIreturn / VIcount
        VIreturnno_inv = VIreturn_noinv / VIcount
        MeanVI = MeanVI / VIcount

    if TFcount != 0:
        TFcash = TFcash / TFcount
        TFlend = TFlend / TFcount
        TFloan = TFloan / TFcount
        TFnav = TFnav / TFcount
        TFpnl = TFpnl / TFcount
        TFstocks = TFstocks / TFcount
        TFreturn = TFreturn / TFcount
        TFreturn_noinv = TFreturn_noinv / TFcount
        TFsignal = TFsignal / TFcount
        MeanTF = MeanTF / TFcount

    if spoils > 0:
        LongAssets += spoils
    elif spoils < 0:
        ShortAssets += abs(spoils)

    VIsignal = MeanVI

    WSNT_ = (100 * WSNT) / (WSNT + WSVI + WSTF)
    WSVI_ = (100 * WSVI) / (WSNT + WSVI + WSTF)
    WSTF_ = (100 * WSTF) / (WSNT + WSVI + WSTF)
    WSNT = WSNT_
    WSVI = WSVI_
    WSTF = WSTF_
    if abs(100 - (WSNT + WSVI + WSTF)) > 1:
        raise ValueError(
            "Sum of wealth shares superior to 100. " + str([WSNT + WSVI + WSTF])
        )
    if WSNT < 0 or WSNT < 0 or WSNT < 0:
        raise ValueError("Negative wealth share. " + str([WSNT, WSVI, WSTF]))


    ListOutput = [
        LongAssets,
        ShortAssets,
        NTcount,
        VIcount,
        TFcount,
        MeanNT,
        MeanVI,
        MeanTF,
        WSNT,
        WSVI,
        WSTF,
        NTcash,
        NTlend,
        NTloan,
        NTnav,
        NTpnl,
        NTsignal,
        NTstocks,
        NTreturn,
        NTreturn_noinv,
        VIcash,
        VIlend,
        VIloan,
        VInav,
        VIpnl,
        VIsignal,
        VIstocks,
        VIreturn,
        VIreturn_noinv,
        TFcash,
        TFlend,
        TFloan,
        TFnav,
        TFpnl,
        TFsignal,
        TFstocks,
        TFreturn,
        TFreturn_noinv,
        NTflows,
        VIflows,
        TFflows
    ]

    return ListOutput


def record_results(
    results,
    wealth_tracker,
    wealth_tracker_noinv,
    generation,
    current_price,
    mismatch,
    dividend,
    random_dividend,
    volume,
    replacements,
    pop,
    spoils,
    Liquidations,
    asset_supply,
    ReturnsNT,
    ReturnsVI,
    ReturnsTF,
    CountSelected,
    CountMutated,
    CountCrossed,
    StratFlow,
    AvgValSignif,
    TestThreshold,
    PerSignif,
    NumDev,
):

    if generation >= Barr:

        ListOutput = ResultsProcess(pop, spoils, current_price)
        current = generation - Barr

        if generation >= Barr + 21 * 3:
            resultsNT = results[0:current, -12]
            resultsVI = results[0:current, -11]
            resultsTF = results[0:current, -10]
            SharpeNT, SharpeVI, SharpeTF, Delta = computeSharpe(resultsNT, resultsVI, resultsTF)
        else:
            SharpeNT, SharpeVI, SharpeTF, Delta = NAN, NAN, NAN, NAN

        DailyNTReturns = FillList(GetDayReturn(pop, "nt"), len(pop))
        ReturnsNT[current, :] = DailyNTReturns

        DailyVIReturns = FillList(GetDayReturn(pop, "vi"), len(pop))
        ReturnsVI[current, :] = DailyVIReturns

        DailyTFReturns = FillList(GetDayReturn(pop, "tf"), len(pop))
        ReturnsTF[current, :] = DailyTFReturns

        try:
            MeanNTReturn = np.nanmean(DailyNTReturns)
        except RuntimeWarning:
            MeanNTReturn = np.nan
        try:
            MeanVIReturn = np.nanmean(DailyVIReturns)
        except RuntimeWarning:
            MeanVIReturn = np.nan
        try:
            MeanTFReturn = np.nanmean(DailyTFReturns)
        except RuntimeWarning:
            MeanTFReturn = np.nan

        wealth_tracker, wamp = TrackWealth(wealth_tracker, pop, generation)
        wamp_nt, wamp_vi, wamp_tf = AnnualReturns(wealth_tracker, pop, generation)
        NT_AR_noinv, VI_AR_noinv, TF_AR_noinv = AnnualReturnsNoInv(wealth_tracker_noinv, pop, generation)

        """ Global variables """
        arr = [
            generation - Barr,
            current_price,
            mismatch,
            dividend,
            random_dividend,
            volume,
            replacements,
            ListOutput[0],  # bs.count_long_assets(pop, spoils)
            ListOutput[1],  # bs.count_short_assets(pop, spoils)
        ]

        """ General ecology variables """
        arr += ListOutput[2:11]

        """ Noise traders """
        arr += ListOutput[11:20]

        """ Value investors """
        arr += ListOutput[20:29]

        """ Trend followers """
        arr += ListOutput[29:38]

        """ Additional measures """
        arr += [ComputeAvgReturn(results, current, pop), spoils, Liquidations]

        """ More measures """

        arr += [
            abs(100 * spoils / asset_supply),
            MeanNTReturn,
            MeanVIReturn,
            MeanTFReturn,
            (results[current, 54] + results[current, 55] + results[current, 56]) / 3,
        ]

        """ Measures of adaptation """
        arr += [CountSelected, CountMutated, CountCrossed]
        arr += StratFlow

        """ Wealth measures """
        arr += [wamp]

        """ Sharpe and Delta """
        arr += [SharpeNT, SharpeVI, SharpeTF, Delta]

        """ Annual returns """
        arr += [wamp_nt, wamp_vi, wamp_tf]
        # -12, -11, -10

        """ Annual returns without investment """
        arr += [NT_AR_noinv, VI_AR_noinv, TF_AR_noinv]

        """ Investment Statistics """
        arr += [AvgValSignif, NumDev, PerSignif]

        arr += ListOutput[38:41]

        if len(arr) != len(results[current,:]):
            print(len(arr))
            print(len(results[current,:]))
            raise ValueError('Mismatch in lengths of arrays in results recording.')

        # Warning: This must be at the end.
        """ Record results """
        results[current, :] = arr

    return results, wealth_tracker, wealth_tracker_noinv, ReturnsNT, ReturnsVI, ReturnsTF


def GetDayReturn(pop, strat):
    lis = []
    for ind in pop:
        if ind.type == strat:
            lis.append(ind.DailyReturn)
    return lis


def FillList(lis, n):
    while len(lis) < n:
        lis.append(np.nan)
    return lis


def ComputeAvgReturn(results, generation, pop):
    AvgReturn = (
        results[generation, 10] * results[generation, 26]
        + results[generation, 11] * results[generation, 34]
        + results[generation, 12] * results[generation, 42]
    ) / len(pop)
    return AvgReturn


def ComputeAvgMonReturn(results, generation, pop):
    AvgReturn = (
        results[generation, 10] * results[generation, 54]
        + results[generation, 11] * results[generation, 55]
        + results[generation, 12] * results[generation, 56]
    ) / len(pop)
    return AvgReturn

def UpdateWealthReturnTracking(wealth_tracker, wealth_tracker_noinv, returns_tracker, pop, generation):
    wealth_tracker = WealthTracking(wealth_tracker, pop, generation)
    wealth_tracker_noinv = WealthNoInvTracking(wealth_tracker_noinv, pop, generation)
    returns_tracker = ReturnTracking(returns_tracker, pop, generation)
    return wealth_tracker, wealth_tracker_noinv, returns_tracker

cdef WealthTracking(wealth_tracker, list pop, int generation):
    cdef cythonized.Individual ind
    if generation >= Barr:
        for i, ind in enumerate(pop):
            if ind.age > 0:
                wealth_tracker[generation,i] = ind.wealth 
            else: 
                wealth_tracker[generation, i] = np.nan # to mark the replacement in the data  
    return wealth_tracker

cdef WealthNoInvTracking(wealth_tracker_noinv, list pop, int generation):
    cdef cythonized.Individual ind
    if generation >= Barr:
        for i, ind in enumerate(pop):
            if ind.age > 0:
                wealth_tracker_noinv[generation,i] = ind.wealth - ind.investor_flow
            else: 
                wealth_tracker_noinv[generation, i] = np.nan # to mark the replacement in the data  
    return wealth_tracker_noinv

cdef ReturnTracking(returns_tracker, list pop, int generation):
    if generation >= Barr + 1: # Otherwise there won't be a previous_wealth.
        for i, ind in enumerate(pop):
            if ind.age > 2:
                previous_wealth = ind.prev_wealth + ind.investor_flow
                if previous_wealth != 0 and previous_wealth != np.nan and ind.wealth != np.nan and ind.wealth:
                    returns_tracker[generation, i] = (ind.wealth - previous_wealth) / previous_wealth
                else:
                    returns_tracker[generation, i] = np.nan
                # Mark investor flows as being applied, so that we don't deduct them at the next period.
                ind.investor_flow = 0.0
    return returns_tracker

cdef computeSharpe(resultsNT, resultsVI, resultsTF):
    cdef double SharpeNT = 0.0
    cdef double SharpeVI = 0.0
    cdef double SharpeTF = 0.0
    cdef double Delta = 0.0

    N = len(resultsNT)
    SharpeNT = nanmean(resultsNT) / nanstd(resultsNT)
    SharpeVI = nanmean(resultsVI) / nanstd(resultsVI)
    SharpeTF = nanmean(resultsTF) / nanstd(resultsTF)

    SENT = sqrt((1 + 0.5 * SharpeNT ** 2)/N)
    SEVI = sqrt((1 + 0.5 * SharpeVI ** 2)/N)
    SETF = sqrt((1 + 0.5 * SharpeTF ** 2)/N)
    

    return SharpeNT, SharpeVI, SharpeTF, Delta