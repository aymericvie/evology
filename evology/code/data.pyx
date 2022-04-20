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
    #"NT_DayReturns",
    #"VI_DayReturns",
    #"TF_DayReturns",
    #"AvgDayReturn",
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
    #"WealthAmp",
    # Annual Sharpes and Delta
    "SharpeNT",
    "SharpeVI",
    "SharpeTF",
    "DeltaNTVI",
    "DeltaNTTF",
    "DeltaVITF",
    # Annual return computed over wealth
    "NT_AnnualReturns",
    "VI_AnnualReturns",
    "TF_AnnualReturns",
    # Annual return computed over wealth, without investment
    #"NT_AnnualReturns_Noinv",
    #"VI_AnnualReturns_Noinv",
    #"TF_AnnualReturns_Noinv",
    # Significance
    "AvgT",
    "AvgAbsT",
    "HighestT",
    "PropSignif",
    "NTflows",
    "VIflows",
    "TFflows",
    # Age
    "AvgAge",
    # DiffReturns
    "DiffReturns",
    "NT_process",
    "VI_val",
    "nav_pct"
]
variables = len(columns) 

""" We only record results after a year to avoid transient period biases. """
Barr = max(SHIELD_DURATION, ShieldResults)


def AnnualReturns(wealth_tracker, pop, generation):
    cdef double wamp_nt = NAN
    cdef double wamp_vi = NAN
    cdef double wamp_tf = NAN
    cdef int i = 0
    cdef cythonized.Individual ind

    wamp_list_nt, wamp_list_vi, wamp_list_tf,  = [],[],[]
    
    
    if generation - 252 >= 0: # We can start calculate the movements' annual amplitude.
        for i, ind in enumerate(pop):
            DataSlice = wealth_tracker[generation-252:generation,i]
            old_wealth = wealth_tracker[generation-252,i]
            wamp_ind = float("nan")
            #for ind in pop:
            if old_wealth > 0:
                if isnan(sum(DataSlice)) == False:
                    wamp_ind = (wealth_tracker[generation, i] - old_wealth) / old_wealth

            if ind.type == 'nt':
                wamp_list_nt.append(wamp_ind)
            elif ind.type == 'vi':
                wamp_list_vi.append(wamp_ind)
            elif ind.type == 'tf':
                wamp_list_tf.append(wamp_ind)

    if len(wamp_list_nt) > 1:
        wamp_nt = np.nanmean(wamp_list_nt)
    else:
        wamp_nt = np.mean(wamp_list_nt)

    if len(wamp_list_vi) > 1:
        wamp_vi = np.nanmean(wamp_list_vi)
    else:
        wamp_vi = np.mean(wamp_list_vi)

    if len(wamp_list_tf) > 1:
        wamp_tf = np.nanmean(wamp_list_tf)
    else:
        wamp_tf = np.mean(wamp_list_tf)
        
    return wamp_nt, wamp_vi, wamp_tf

def ResultsProcess(list pop, double spoils, double price):

    LongAssets, ShortAssets = 0.0, 0.0
    NTcount, VIcount, TFcount = 0.0, 0.0, 0.0
    MeanNT, MeanVI, MeanTF = 0.0, 0.0, 0.0
    WSNT, WSVI, WSTF = 0.0, 0.0, 0.0
    NTcash, NTlend, NTloan, NTnav, NTpnl, NTsignal, NTstocks, NTreturn = (
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0, #float("nan"),
    )
    VIcash, VIlend, VIloan, VInav, VIpnl, VIsignal, VIstocks, VIreturn = (
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0, #float("nan"),
    )
    TFcash, TFlend, TFloan, TFnav, TFpnl, TFsignal, TFstocks, TFreturn = (
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0, #float("nan"),
    )
    NT_process = 0.0
    VI_val = 0.0

    NTflows, VIflows, TFflows = 0.0, 0.0, 0.0
    nav_pct = 0.0

    cdef cythonized.Individual ind
    cdef double ind_zero
    cdef double AvgAge = 0.0

    for ind in pop:
        AvgAge += ind.age

        if ind.asset > 0.0:
            LongAssets += ind.asset
        elif ind.asset < 0.0:
            ShortAssets += abs(ind.asset)

        flow = abs((ind.wealth / ind.prev_wealth) - 1)
        if isnan(flow) == False:
            nav_pct += flow

        if ind.type == "nt":
            NTcount += 1
            MeanNT += ind.strategy * ind.wealth
            NTcash += ind.cash
            NTlend += ind.margin
            NTloan += ind.loan
            NTnav += ind.wealth  # before, we imposed w>0
            if ind.wealth > 0:
                WSNT += ind.wealth
            NTpnl += ind.profit
            NTsignal += ind.tsv
            NTstocks += price * ind.asset
            if ind.prev_wealth != 0:
                NTreturn += ind.DailyReturn
            #if ind.prev_wealth_noinv != 0:
            #    NTreturn_noinv += ind.DailyReturn_noinv
            NTflows += ind.investor_flow
            NT_process += ind.process

        elif ind.type == "vi":
            VIcount += 1
            MeanVI += ind.strategy * ind.wealth
            VIcash += ind.cash
            VIlend += ind.margin
            VIloan += ind.loan
            VInav += ind.wealth  # before, we imposed w>0
            if ind.wealth > 0:
                WSVI += ind.wealth
            VIpnl += ind.profit
            VIsignal = ind.tsv
            VIstocks += price * ind.asset
            if ind.prev_wealth != 0:
                VIreturn += ind.DailyReturn
            VIflows += ind.investor_flow
            VI_val += ind.val * ind.wealth

        elif ind.type == "tf":
            TFcount += 1
            MeanTF += ind.strategy * ind.wealth
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
            TFflows += ind.investor_flow

    if NTcount != 0:
        NTcash = NTcash / NTcount
        NTlend = NTlend / NTcount
        NTloan = NTloan / NTcount
        NTnav = NTnav / NTcount
        NTpnl = NTpnl / NTcount
        NTstocks = NTstocks / NTcount
        NTreturn = NTreturn / NTcount
        #NTreturn_noinv = NTreturn_noinv / NTcount
        NTsignal = NTsignal / NTcount
        MeanNT = MeanNT / (NTnav * NTcount)
        NT_process = NT_process / NTcount

    if VIcount != 0:
        VIcash = VIcash / VIcount
        VIlend = VIlend / VIcount
        VIloan = VIloan / VIcount
        VInav = VInav / VIcount
        VIpnl = VIpnl / VIcount
        VIstocks = VIstocks / VIcount
        VIreturn = VIreturn / VIcount
        #VIreturnno_inv = VIreturn_noinv / VIcount
        MeanVI = MeanVI / (VIcount * VInav)
        VI_val = VI_val / (VIcount * VInav)

    if TFcount != 0:
        TFcash = TFcash / TFcount
        TFlend = TFlend / TFcount
        TFloan = TFloan / TFcount
        TFnav = TFnav / TFcount
        TFpnl = TFpnl / TFcount
        TFstocks = TFstocks / TFcount
        TFreturn = TFreturn / TFcount
        #TFreturn_noinv = TFreturn_noinv / TFcount
        TFsignal = TFsignal / TFcount
        MeanTF = MeanTF / (TFcount * TFnav)

    if spoils > 0:
        LongAssets += spoils
    elif spoils < 0:
        ShortAssets += abs(spoils)


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

    AvgAge = AvgAge / len(pop)

    if WSNT == 0.0 or WSVI == 0.0 or WSTF == 0.0:
        sim_break = True
    else:
        sim_break = False

    nav_pct = nav_pct / len(pop)

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
        0.0, #NTreturn_noinv,
        VIcash,
        VIlend,
        VIloan,
        VInav,
        VIpnl,
        VIsignal,
        VIstocks,
        VIreturn,
        0.0,
        TFcash,
        TFlend,
        TFloan,
        TFnav,
        TFpnl,
        TFsignal,
        TFstocks,
        TFreturn,
        0.0,
        NTflows,
        VIflows,
        TFflows,
        AvgAge,
        NT_process,
        VI_val,
        nav_pct
    ]

    return ListOutput, sim_break


def record_results(
    results,
    #wealth_tracker,
    #wealth_tracker_noinv,
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
    #ReturnsNT,
    #ReturnsVI,
    #ReturnsTF,
    CountSelected,
    CountMutated,
    CountCrossed,
    StratFlow,
    AvgT,
    PropSignif,
    HighestT,
    AvgAbsT,
):

    if generation >= Barr :

        ListOutput, sim_break = ResultsProcess(pop, spoils, current_price)
        current = generation - Barr
        SharpeNT, SharpeVI, SharpeTF, DeltaNTVI, DeltaNTTF, DeltaVITF  = NAN, NAN, NAN, NAN, NAN, NAN
        wamp_nt, wamp_vi, wamp_tf = 0,0,0 #AnnualReturns(wealth_tracker, pop, generation)

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
        arr += [abs(100 * spoils / asset_supply),]

        """ Measures of adaptation """
        arr += [CountSelected, CountMutated, CountCrossed]
        arr += StratFlow

        """ Sharpe and Delta """
        arr += [SharpeNT, SharpeVI, SharpeTF,  DeltaNTVI, DeltaNTTF, DeltaVITF]

        """ Annual returns """
        arr += [wamp_nt, wamp_vi, wamp_tf]
        # -12, -11, -10

        """ Annual returns without investment """
        #arr += [NT_AR_noinv, VI_AR_noinv, TF_AR_noinv]

        """ Investment Statistics """
        arr += [AvgT, AvgAbsT, HighestT, PropSignif]

        arr += ListOutput[38:41]

        ''' average age '''
        arr += [ListOutput[41]]

        ''' diff return '''
        arr += [(ListOutput[18] - ListOutput[27]) ** 2 + (ListOutput[18] - ListOutput[36]) ** 2 + (ListOutput[27] - ListOutput[36]) ** 2]

        ''' NT noise process and VI val and nan avg flow'''
        arr += [ListOutput[42], ListOutput[43], ListOutput[44]]


        if len(arr) != len(results[current,:]):
            print(len(arr))
            print(len(results[current,:]))
            raise ValueError('Mismatch in lengths of arrays in results recording.')


        # Warning: This must be at the end.
        """ Record results """
        results[current, :] = arr

    return results, sim_break 


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
    cdef double DeltaNT = 0.0
    cdef double DeltaVI = 0.0
    cdef double DeltaTF = 0.0
    cdef list BoundsNT
    cdef list BoundsVI
    cdef list BoundsTF

    N = len(resultsNT)
    SharpeNT = nanmean(resultsNT) / nanstd(resultsNT)
    SharpeVI = nanmean(resultsVI) / nanstd(resultsVI)
    SharpeTF = nanmean(resultsTF) / nanstd(resultsTF)

    SENT = sqrt((1 + 0.5 * SharpeNT ** 2)/N)
    SEVI = sqrt((1 + 0.5 * SharpeVI ** 2)/N)
    SETF = sqrt((1 + 0.5 * SharpeTF ** 2)/N)

    BoundsNT = [SharpeNT - 1.96 * SENT, SharpeNT + 1.96 * SENT]
    BoundsVI = [SharpeVI - 1.96 * SEVI, SharpeVI + 1.96 * SEVI]
    BoundsTF = [SharpeTF - 1.96 * SETF, SharpeTF + 1.96 * SETF]

    DeltaNTVI = ComputeDelta(SharpeNT, SharpeVI, SENT, SEVI, BoundsNT, BoundsVI, N)
    DeltaNTTF = ComputeDelta(SharpeNT, SharpeTF, SENT, SETF, BoundsNT, BoundsTF, N)
    DeltaVITF = ComputeDelta(SharpeVI, SharpeTF, SEVI, SETF, BoundsVI, BoundsTF, N)

    return SharpeNT, SharpeVI, SharpeTF, DeltaNTVI, DeltaNTTF, DeltaVITF

cdef ComputeDelta(double Sharpe1, double Sharpe2, double SE1, double SE2, list B1, list B2, double N):
    cdef double DS = 0.0
    cdef double Pooled = 0.0
    cdef double BP = 0.0
    cdef double BM = 0.0

    Pooled = (SE1 + SE2) / sqrt(2) 

    if Sharpe1 > Sharpe2:
        DS = Sharpe1 - Sharpe2
        BP = B1[0]
        BM = B2[1]

    if Sharpe1 < Sharpe2:
        DS = Sharpe2 - Sharpe1
        BM = B1[1]
        BP = B2[0]

    S = (BP - BM) / Pooled
    D = log(N) / log(S/DS)

    return D
    