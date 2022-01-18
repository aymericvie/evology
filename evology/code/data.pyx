#cython: boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True

#!/usr/bin/env python3
import pandas as pd
import numpy as np
import balance_sheet as bs
import timeit

from parameters import *
cimport cythonized
cdef float NAN
NAN = float("nan")

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
    # Value investors
    "VI_cash",
    "VI_lending",
    "VI_loans",
    "VI_nav",
    "VI_pnl",
    "VI_signal",
    "VI_stocks",
    "VI_returns",
    # Trend followers
    "TF_cash",
    "TF_lending",
    "TF_loans",
    "TF_nav",
    "TF_pnl",
    "TF_signal",
    "TF_stocks",
    "TF_returns",
    # Additional measures
    "MeanReturn",
    "Spoils",
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
    "WealthAmp"
    # TODO: add monthly returns back just as exponentiation of daily (because we would not track funds for this)
]
variables = len(columns)

""" We only record results after a year to avoid transient period biases. """
Barr = max(SHIELD_DURATION, ShieldResults)

def TrackWealth(wealth_tracker, pop, generation):
    cdef double wamp = NAN
    cdef int i = 0
    cdef cythonized.Individual ind

    for i, ind in enumerate(pop):
            wealth_tracker[generation,i] = ind.wealth 
    
    if generation - 252 >= 0: # We can start calculate the movements' annual amplitude.
        wamp_list = []
        for ind in pop:
            if wealth_tracker[generation-252,i] > 0 and ind.age >= 252:
                wamp_ind = (wealth_tracker[generation, i] - wealth_tracker[generation - 252, i]) / wealth_tracker[generation - 252, i]
                #wealth_window = wealth_tracker[generation-252:generation, i]
                #if len(wealth_window) != 252:
                #    raise ValueError('Incorrect length for Wealth window ' + str(len(wealth_window)))
                #avgw = sum(wealth_window) / 252
                #wamp_ind = (wealth_tracker[generation, i] - avgw) / avgw
            else: 
                wamp_ind = float("nan")
            wamp_list.append(100 * abs(wamp_ind))
        wamp = np.nanmean(wamp_list)
        
    return wealth_tracker, wamp

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
        float("nan"),
    )
    VIcash, VIlend, VIloan, VInav, VIpnl, VIsignal, VIstocks, VIreturn = (
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        float("nan"),
    )
    TFcash, TFlend, TFloan, TFnav, TFpnl, TFsignal, TFstocks, TFreturn = (
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        float("nan"),
    )

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

    if NTcount != 0:
        NTcash = NTcash / NTcount
        NTlend = NTlend / NTcount
        NTloan = NTloan / NTcount
        NTnav = NTnav / NTcount
        NTpnl = NTpnl / NTcount
        NTstocks = NTstocks / NTcount
        NTreturn = NTreturn / NTcount
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
        MeanVI = MeanVI / VIcount

    if TFcount != 0:
        TFcash = TFcash / TFcount
        TFlend = TFlend / TFcount
        TFloan = TFloan / TFcount
        TFnav = TFnav / TFcount
        TFpnl = TFpnl / TFcount
        TFstocks = TFstocks / TFcount
        TFreturn = TFreturn / TFcount
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
        VIcash,
        VIlend,
        VIloan,
        VInav,
        VIpnl,
        VIsignal,
        VIstocks,
        VIreturn,
        TFcash,
        TFlend,
        TFloan,
        TFnav,
        TFpnl,
        TFsignal,
        TFstocks,
        TFreturn,
    ]

    return ListOutput


def record_results(
    results,
    wealth_tracker,
    generation,
    current_price,
    mismatch,
    dividend,
    random_dividend,
    volume,
    replacements,
    pop,
    spoils,
    asset_supply,
    ReturnsNT,
    ReturnsVI,
    ReturnsTF,
    CountSelected,
    CountMutated,
    CountCrossed,
    StratFlow,
):

    if generation >= Barr:

        ListOutput = ResultsProcess(pop, spoils, current_price)

        starttime = timeit.default_timer()

        current = generation - Barr

        DailyNTReturns = FillList(GetDayReturn(pop, "nt"), len(pop))
        ReturnsNT[current, :] = DailyNTReturns

        DailyVIReturns = FillList(GetDayReturn(pop, "vi"), len(pop))
        ReturnsVI[current, :] = DailyVIReturns

        DailyTFReturns = FillList(GetDayReturn(pop, "tf"), len(pop))
        ReturnsTF[current, :] = DailyTFReturns

        wealth_tracker, wamp = TrackWealth(wealth_tracker, pop, generation)

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
        arr += ListOutput[11:19]

        """ Value investors """
        arr += ListOutput[19:27]

        """ Trend followers """
        arr += ListOutput[27:35]

        """ Additional measures """
        arr += [ComputeAvgReturn(results, current, pop), spoils]

        """ More measures """
        arr += [
            abs(100 * spoils / asset_supply),
            np.nanmean(DailyNTReturns),
            np.nanmean(DailyVIReturns),
            np.nanmean(DailyTFReturns),
            (results[current, 54] + results[current, 55] + results[current, 56]) / 3,
        ]

        """ Measures of adaptation """
        arr += [CountSelected, CountMutated, CountCrossed]
        arr += StratFlow

        """ Wealth measures """
        arr += [wamp]

        """ Record results """
        results[current, :] = arr

    return results, wealth_tracker, ReturnsNT, ReturnsVI, ReturnsTF


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
