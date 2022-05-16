#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True

#!/usr/bin/env python3
import pandas as pd
import numpy as np
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
   # Investment statistics
    "NTflows",
    "VIflows",
    "TFflows",
    # Age
    "AvgAge",
    # DiffReturns
    "DiffReturns",
    # NT noise process and VI val and nan avg flow
    "NT_process",
    "VI_val",
    "nav_pct",
    # Adaptive fund statistics
    "AV_wealth",
    "AV_return",
    "AV_WShare",
    "BH_wealth",
    "BH_return",
    "BH_WShare",
    "IR_wealth",
    "IR_return",
    "IR_WShare",
]
variables = len(columns) 

""" We only record results after a year to avoid transient period biases. """
Barr = max(SHIELD_DURATION, ShieldResults)

'''
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
'''
def ResultsProcess(list pop, double spoils, double price, double generation):

    cdef cythonized.Individual ind
    cdef double ind_zero
    cdef double AvgAge = 0.0
    cdef double LongAssets = 0.0
    cdef double ShortAssets = 0.0
    cdef double NTcount = 0.0
    cdef double VIcount = 0.0
    cdef double TFcount = 0.0
    cdef double MeanNT = 0.0
    cdef double MeanVI = 0.0
    cdef double MeanTF = 0.0
    cdef double WSNT = 0.0
    cdef double WSVI = 0.0
    cdef double WSTF = 0.0
    cdef double flow 
    cdef double nav_pct = 0.0
    cdef list ListOutput 

    cdef double NTcash = 0.0
    cdef double NTlend = 0.0
    cdef double NTloan = 0.0
    cdef double NTnav = 0.0
    cdef double NTpnl = 0.0
    cdef double NTsignal = 0.0
    cdef double NTstocks = 0.0
    cdef double NTreturn = 0.0

    cdef double VIcash = 0.0
    cdef double VIlend = 0.0
    cdef double VIloan = 0.0
    cdef double VInav = 0.0
    cdef double VIpnl = 0.0
    cdef double VIsignal = 0.0
    cdef double VIstocks = 0.0
    cdef double VIreturn = 0.0

    cdef double TFcash = 0.0
    cdef double TFlend = 0.0
    cdef double TFloan = 0.0
    cdef double TFnav = 0.0
    cdef double TFpnl = 0.0
    cdef double TFsignal = 0.0
    cdef double TFstocks = 0.0
    cdef double TFreturn = 0.0

    cdef double NT_process = 0.0
    cdef double VI_val = 0.0

    cdef double NTflows = 0.0
    cdef double VIflows = 0.0
    cdef double TFflows = 0.0
    cdef double WSNT_ 
    cdef double WSVI_ 
    cdef double WSTF_ 
    cdef int sim_break

    cdef double av_wealth = NAN
    cdef double av_return = NAN
    cdef double av_wshare = NAN
    cdef double bh_wealth = NAN
    cdef double bh_return = NAN
    cdef double bh_wshare = NAN
    cdef double ir_wealth = NAN
    cdef double ir_return = NAN
    cdef double ir_wshare = NAN


    for ind in pop:
        AvgAge += ind.age

        if ind.asset > 0.0:
            LongAssets += ind.asset
        elif ind.asset < 0.0:
            ShortAssets += abs(ind.asset)

        if (generation + 1) % 63 == 0:
            flow = (ind.wealth / ind.quarterly_wealth) - 1
            if isnan(flow) == False:
                nav_pct += abs(flow)
        else:
            nav_pct = NAN

        if ind.type == "av":
            av_wealth = ind.wealth
            if ind.prev_wealth != 0:
                av_return = ind.DailyReturn
            else:
                av_return = NAN

        if ind.type == "bh":
            bh_wealth = ind.wealth
            if ind.prev_wealth != 0:
                bh_return = ind.DailyReturn
            else:
                bh_return = NAN

        
        if ind.type == "ir":
            ir_wealth = ind.wealth
            if ind.prev_wealth != 0:
                ir_return = ind.DailyReturn
            else:
                ir_return = NAN

        if ind.type == "nt":
            NTcount += 1
            MeanNT += ind.strategy * ind.wealth
            NTcash += ind.cash
            NTlend += ind.margin
            NTloan += ind.loan
            NTnav += ind.wealth
            if ind.wealth > 0:
                WSNT += ind.wealth
            NTpnl += ind.profit
            NTsignal += ind.tsv
            NTstocks += price * ind.asset
            if ind.prev_wealth != 0:
                NTreturn += ind.DailyReturn
            NTflows += 0 #ind.investor_flow
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
            VIflows += 0 #ind.investor_flow
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
            TFflows += 0 #ind.investor_flow

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

    if isnan(av_wealth) == False:
        WSNT_ = (100 * WSNT) / (WSNT + WSVI + WSTF + av_wealth)
        WSVI_ = (100 * WSVI) / (WSNT + WSVI + WSTF + av_wealth)
        WSTF_ = (100 * WSTF) / (WSNT + WSVI + WSTF + av_wealth)
        av_wshare = (100 * av_wealth) / (WSNT + WSVI + WSTF + av_wealth)
    else:
        WSNT_ = (100 * WSNT) / (WSNT + WSVI + WSTF)
        WSVI_ = (100 * WSVI) / (WSNT + WSVI + WSTF)
        WSTF_ = (100 * WSTF) / (WSNT + WSVI + WSTF)
        av_wshare = NAN
    bh_wshare = bh_wealth / (WSNT + WSVI + WSTF)
    ir_wshare = ir_wealth / (WSNT + WSVI + WSTF)
    WSNT = WSNT_
    WSVI = WSVI_
    WSTF = WSTF_
    if abs(100 - (WSNT + WSVI + WSTF + av_wealth)) > 1:
        raise ValueError(
            "Sum of wealth shares superior to 100. " + str([WSNT + WSVI + WSTF + av_wealth])
        )
    if WSNT < 0 or WSNT < 0 or WSNT < 0 or av_wshare < 0:
        raise ValueError("Negative wealth share. " + str([WSNT, WSVI, WSTF, av_wshare]))

    AvgAge = AvgAge / len(pop)

    if WSNT == 0.0 or WSVI == 0.0 or WSTF == 0.0:
        sim_break = 1
    else:
        sim_break = 0

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
        nav_pct,
        av_wealth,
        av_return,
        av_wshare,
        bh_wealth,
        bh_return,
        bh_wshare,
        ir_wealth,
        ir_return,
        ir_wshare,
    ]

    return ListOutput, sim_break


def record_results(
    results,
    #wealth_tracker,
    #wealth_tracker_noinv,
    double generation,
    double current_price,
    double mismatch,
    double dividend,
    double random_dividend,
    double volume,
    int replacements,
    list pop,
    double spoils,
    double Liquidations,
    double asset_supply,
):

    cdef int current = generation - Barr
    cdef list arr 
    cdef int sim_break = 0

    if generation >= Barr :

        ListOutput, sim_break = ResultsProcess(pop, spoils, current_price, generation)

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
        arr += [abs(100 * spoils / asset_supply)]

        """ Investment Statistics """
        arr += ListOutput[38:41] # flows

        ''' average age '''
        arr += [ListOutput[41]]

        ''' diff return '''
        arr += [(ListOutput[18] - ListOutput[27]) ** 2 + (ListOutput[18] - ListOutput[36]) ** 2 + (ListOutput[27] - ListOutput[36]) ** 2]

        ''' NT noise process and VI val and nan avg flow'''
        arr += [ListOutput[42], ListOutput[43], ListOutput[44]]

        ''' AV, BH, IR fund statistics '''
        arr += [ListOutput[45], ListOutput[46], ListOutput[47]]
        arr += [ListOutput[48], ListOutput[49], ListOutput[50]]
        arr += [ListOutput[51], ListOutput[52], ListOutput[53]]


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
    

