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
    tqdm_display,
    reset_wealth,
):
    # Initialise important variables and dataframe to store results
    generation, CurrentPrice, dividend, spoils = 0, InitialPrice, INITIAL_DIVIDEND, 0
    results = np.zeros((MAX_GENERATIONS - data.Barr, data.variables))
    # wealth_tracker= np.zeros((MAX_GENERATIONS, POPULATION_SIZE))
    # wealth_tracker_noinv = np.zeros((MAX_GENERATIONS, POPULATION_SIZE))
    # returns_tracker= np.zeros((MAX_GENERATIONS, POPULATION_SIZE))
    price_history, dividend_history = [], []
    TestThreshold = stdtrit(InvestmentHorizon, 0.95)
    replace = 0

    pop, asset_supply = cr.CreatePop(POPULATION_SIZE, space, wealth_coordinates)
    bs.calculate_wealth(pop, CurrentPrice)
    bs.UpdatePrevWealth(pop)

    for generation in tqdm(
        range(MAX_GENERATIONS), disable=tqdm_display, miniters=100, mininterval=0.5
    ):
        if CurrentPrice >= 1_000_000:
            break

        # Population reset
        pop = cr.WealthReset(pop, space, wealth_coordinates, generation, reset_wealth)

        # Hypermutation
        pop, replacements, spoils = ga.hypermutate(
            pop, spoils, replace
        )  # Replace insolvent agents
        if replacements < 0:
            break

        # Strategy evolution
        pop = fit.ComputeFitness(pop, InvestmentHorizon)
        pop, CountSelected, CountMutated, CountCrossed, StratFlow = ga_evolution(
            pop,
            space,
            generation,
            wealth_coordinates,
            PROBA_SELECTION,
            MUTATION_RATE,
            InvestmentHorizon,
        )

        # Calculate wealth and previous wealth
        bs.calculate_wealth(pop, CurrentPrice)
        bs.UpdatePrevWealth(pop)

        # Market decisions (tsv, proc, edf)
        pop = decision_updates(pop, price_history, dividend_history, CurrentPrice)

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
        pop, replace = update_wealth(
            pop,
            CurrentPrice,
        )

        # (
        #     wealth_tracker,
        #     wealth_tracker_noinv,
        #     returns_tracker
        # ) = data.UpdateWealthReturnTracking(
        #     wealth_tracker,
        #     wealth_tracker_noinv,
        #     returns_tracker,
        #     pop,
        #     generation
        # )

        (pop, AvgT, PropSignif, HighestT, AvgAbsT) = ProfitDrivenInvestment(
            pop,
            generation,
            # returns_tracker,
            InvestmentHorizon,
            TestThreshold,
            ReinvestmentRate,
        )

        results = data.record_results(
            results,
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
            CountSelected,
            CountMutated,
            CountCrossed,
            StratFlow,
            AvgT,
            TestThreshold,
            PropSignif,
            HighestT,
            AvgAbsT,
        )

    if generation < MAX_GENERATIONS - data.Barr:
        # It means the simulation has breaked.
        results[generation + 1 : MAX_GENERATIONS - data.Barr, :] = (
            np.empty((MAX_GENERATIONS - data.Barr - generation - 1, data.variables))
            * np.nan
        )

    df = pd.DataFrame(results, columns=data.columns)

    return df, pop


np.random.seed(8)
wealth_coordinates = [1 / 3, 1 / 3, 1 / 3]
TIME, POPSIZE = 10000, 1000
df, pop = main(
    "scholl",
    "esl.true",
    wealth_coordinates,
    POPSIZE,
    TIME,
    0,
    0,
    1.05,
    252,
    False,
    False,
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
