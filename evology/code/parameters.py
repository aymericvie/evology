#!/usr/bin/env python3
import numpy as np


""" Imitation parmeters """
MUTATION_RATE = 1 / (252 * 4)
PROBA_SELECTION = 1 / (252 * 4)

""" GA-only parameters """

CROSSOVER_RATE = 1 / 21

""" GP PARAMETERS """

""" STRATEGY PARAMETERS """
# General parameters

LeverageNT, LeverageVI, LeverageTF = 1, 1, 1
SCALE_NT, SCALE_VI, SCALE_TF = 1, 1, 1  # np.pi, np.pi, np.pi
ATC_TF = 1

GAMMA_NT = 0.2 * np.sqrt(1 / 252)
MU_NT = 1.0
RHO_NT = 0.00045832561


""" MARKET PARAMETERS """
TRADING_DAYS = 252
InitialPrice = 100

RefLoan = 0
RefCash = 3 * 50_000_000
RefAssets = 3 * 500_000
RefInvestmentSupply = 10_000_000 / (21)

AnnualInterestRate = 0.01
INTEREST_RATE = AnnualInterestRate / TRADING_DAYS
EMA_HORIZON = 2 * TRADING_DAYS

interest_year = 0.01
interest_day = interest_year / 252.0

G = 0.01 # Dividend growth rate
DIVIDEND_GROWTH_RATE_G = 0.01
INITIAL_DIVIDEND = 0.003983

div_vol = 0.1 / np.sqrt(TRADING_DAYS) # Dividend volatility
# DIVIDEND_GROWTH_VOLATILITY = 0.1 / np.sqrt(TRADING_DAYS)
# DIVIDEND_AUTOCORRELATION = 0.1
div_atc = 0.1 # Dividend autocorrelation
# INITIAL_RANDOM_DIVIDEND = 0
DIVIDEND_ATC_TAU = 1
LIQUIDATION_ORDER_SIZE = 20_000

""" RESET WEALTH """

SHIELD_DURATION = 0  # 21
ShieldResults = 0  # 1 #21
SHIELD_TOLERANCE = 0.01
MAX_ATTEMPTS = 100
ShieldInvestment = 252


""" RESULTS STORAGE """
dividend_history = []
random_dividend_history = []


# For extended strategy space
MIN_THETA = 2
MAX_THETA = 4

MIN_RR_VI = 0
MAX_RR_VI = 20

MIN_RR_NT = 0
MAX_RR_NT = 20

MIN_RR_TF = 0
MAX_RR_TF = 20
