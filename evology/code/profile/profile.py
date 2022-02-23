import sys

sys.path.append("./evology/code/")
sys.path.append("/Users/aymericvie/Documents/GitHub/evology/evology/code")
from steps import *
from parameters import *
import numpy as np


@profile

def main(
    space,
    solver,
    wealth_coordinates,
    POPULATION_SIZE,
    MAX_GENERATIONS,
    PROBA_SELECTION,
    MUTATION_RATE,
    ReinvestmentRate,
    InvestmentHorizon,
    InvestorBehavior,
    tqdm_display,
    reset_wealth
):
    # Initialise important variables and dataframe to store results
    ReturnsNT, ReturnsVI, ReturnsTF = (
        np.zeros((MAX_GENERATIONS - data.Barr, POPULATION_SIZE)),
        np.zeros((MAX_GENERATIONS - data.Barr, POPULATION_SIZE)),
        np.zeros((MAX_GENERATIONS - data.Barr, POPULATION_SIZE)),
    )
    generation, CurrentPrice, dividend, spoils = 0, InitialPrice, INITIAL_DIVIDEND, 0
    results = np.zeros((MAX_GENERATIONS - data.Barr, data.variables))
    wealth_tracker= np.zeros((MAX_GENERATIONS, POPULATION_SIZE))
    wealth_tracker_noinv = np.zeros((MAX_GENERATIONS, POPULATION_SIZE))
    returns_tracker= np.zeros((MAX_GENERATIONS, POPULATION_SIZE))
    price_history, dividend_history = [], []
    TestThreshold = stdtrit(InvestmentHorizon, 0.95)
    InvestmentIntensity = 1.0
    InvestmentSupply = RefInvestmentSupply * POPULATION_SIZE * max(0, ReinvestmentRate - 1)

    pop, asset_supply = cr.CreatePop(POPULATION_SIZE, space, wealth_coordinates)
    bs.calculate_wealth(pop, CurrentPrice)
    bs.UpdatePrevWealth(pop)

    for generation in tqdm(
        range(MAX_GENERATIONS), disable=tqdm_display, miniters=100, mininterval=0.5
    ):
        InvestmentSupply = InvestmentSupply * (1+INTEREST_RATE)

        # Population reset
        pop = cr.WealthReset(pop, space, wealth_coordinates, generation, reset_wealth)

        # Hypermutation
        pop, replacements, spoils = ga.hypermutate(
            pop,
            spoils,
        )  # Replace insolvent agents

        # Strategy evolution
        pop, CountSelected, CountMutated, CountCrossed, StratFlow = ga_evolution(
            pop,
            space,
            generation,
            wealth_coordinates,
            PROBA_SELECTION,
            MUTATION_RATE,
            InvestmentHorizon
        )

        # Calculate wealth and previous wealth
        bs.calculate_wealth(pop, CurrentPrice)
        bs.UpdatePrevWealth(pop)

        # Market decisions (tsv, proc, edf)
        pop = decision_updates(pop, price_history, dividend_history)

        # Market clearing
        pop, mismatch, CurrentPrice, price_history, ToLiquidate = marketClearing(
            pop, CurrentPrice, price_history, spoils, solver
        )

        # Market execution
        (
            pop,
            volume,
            dividend,
            random_dividend,
            dividend_history,
            spoils,
            Liquidations,
        ) = marketActivity(
            pop,
            CurrentPrice,
            asset_supply,
            dividend,
            dividend_history,
            spoils,
            ToLiquidate,
        )

        # Earnings, compute profits, age
        pop = update_wealth(
            pop,
            CurrentPrice,
        )

        # Investment
        (
            wealth_tracker, 
            wealth_tracker_noinv,
            returns_tracker
        ) = data.UpdateWealthReturnTracking(
            wealth_tracker, 
            wealth_tracker_noinv,
            returns_tracker, 
            pop, 
            generation
        )

        (
            pop, 
            AvgT, 
            PropSignif, 
            HighestT, 
            AvgAbsT 
        ) = ApplyInvestment(
            pop, 
            generation, 
            returns_tracker, 
            InvestmentHorizon, 
            InvestmentSupply, 
            TestThreshold,
            InvestmentIntensity,
            InvestorBehavior,
            ReinvestmentRate
        )
        #pop = ApplyReinvestment(pop, ReinvestmentRate)

        # Record results
        # wealth_tracker = iv.WealthTracking(wealth_tracker, pop, generation)
        results, wealth_tracker, wealth_tracker_noinv, ReturnsNT, ReturnsVI, ReturnsTF = data.record_results(
            results,
            wealth_tracker,
            wealth_tracker_noinv,
            generation,
            CurrentPrice,
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
            AvgT,
            TestThreshold,
            PropSignif,
            HighestT,
            AvgAbsT 
        )

    df = pd.DataFrame(results, columns=data.columns)

    return df, pop



# Known issues
# - Age after replacement does not behave normally. It just goes back to normal instead of increeasing 1 by 1. 

np.random.seed(8)
wealth_coordinates = [1 / 3, 1 / 3, 1 / 3]
TIME, POPSIZE = 10000, 100
df, pop = main(
    "scholl",
    "esl.true",
    wealth_coordinates,
    POPSIZE,
    TIME,
    1/252,
    1/252,
    1.05,
    252,
    'profit',
    False,
    False
)
print(df)


""" In command: 
kernprof -v -l evology/code/profile/profile.py > evology/code/profile/profile.txt

# For cythonized
cd evology/code
cythonize -i cythonized.pyx
chmod +x ./profile/profile.py
kernprof -v -l profile/profile.py > profile/profile.txt
 ; no need to be in python env first"""
