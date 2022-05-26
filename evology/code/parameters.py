#!/usr/bin/env python3
import numpy as np


""" Imitation parmeters """
MUTATION_RATE = 1 / (252 * 4)
PROBA_SELECTION = 1 / (252 * 4)

""" GA-only parameters """

CROSSOVER_RATE = 1 / 21

""" GP PARAMETERS """

""" STRATEGY PARAMETERS """
FlowCorr = 1.0
LeverageNT, LeverageVI, LeverageTF = 1.0 * FlowCorr, 1.0 * FlowCorr, 1.0 * FlowCorr

ScaleCorr = 1.0
ATC_TF = 1.0
SCALE_NT, SCALE_VI, SCALE_TF = 1.0 * ScaleCorr, 1.0 * ScaleCorr, 1.0 * ScaleCorr * ATC_TF

GAMMA_NT = 0.2 * np.sqrt(1 / 252)
MU_NT = 0.
RHO_NT = 0.00045832561


""" MARKET PARAMETERS """
TRADING_DAYS = 252
InitialPrice = 100
Short_Size_Percent = 100 #1.17

RefLoan = 0
RefCash = 50_000_000
RefAssets = 500_000

EMA_HORIZON = 2 * TRADING_DAYS

interest_year = 0.01
interest_day = interest_year / 252.0


''' Dividend process '''

G = 0.01 # Dividend growth rate
G_day = (((1.0 + G) ** (1.0 / 252.0)) - 1.0)
INITIAL_DIVIDEND = 0.003983
div_vol = 0.1 / np.sqrt(TRADING_DAYS) # Dividend volatility
div_atc = 0.1 # Dividend autocorrelation
div_tau = 252 // 12 # https://github.com/INET-Complexity/market-ecology/blob/b002d0bc715e264b70d1b1c8d573359fd71d24ca/traded_company.hpp



liquidation_perc = 10 / 100

""" RESET WEALTH """

SHIELD_DURATION = 0  # 21
ShieldResults = 0 #252 * 2 #0  # 1 #21
ShieldInvestment = 252
SHIELD_TOLERANCE = 0.01
MAX_ATTEMPTS = 100


""" RESULTS STORAGE """
dividend_history = []
random_dividend_history = []

# NT strat is divided by 1000 
# And also substracted 10
min_nt_strat = 0 
max_nt_strat = 0

# VI strat is divided by 1000
min_vi_strat = 8
max_vi_strat = 12

min_tf_strat = 2
max_tf_strat = 21 #252