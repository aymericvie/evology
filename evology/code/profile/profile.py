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
    tqdm_display,
    reset_wealth,
):
    # Initialisation
    generation, CurrentPrice, dividend, spoils = 0, InitialPrice, INITIAL_DIVIDEND, 0
    results = np.zeros((MAX_GENERATIONS - data.Barr, data.variables))
    price_history, dividend_history, replace, volume, avg_phi = [], [], 0, 0.0, 0.0

    # Population creation
    pop, asset_supply = cr.CreatePop(POPULATION_SIZE, space, wealth_coordinates, CurrentPrice)

    for generation in tqdm(
        range(MAX_GENERATIONS), disable=tqdm_display, miniters=100, mininterval=0.5
    ):
        if CurrentPrice >= 1_000_000:
            warnings.warn('Simulation break: price above 1M.')
            break

        # Population reset
        pop = cr.WealthReset(pop, space, wealth_coordinates, generation, reset_wealth)

        # Hypermutation
        
        pop, replacements, spoils = ga.hypermutate(
            pop, spoils, replace
        ) 
        if replacements < 0:
            break


        # Strategy evolution
        #pop = fit.ComputeFitness(pop, 252)

        #pop, CountSelected, CountMutated, CountCrossed, StratFlow = ga_evolution(
        #    pop,
        #    space,
        #    generation,
        #    wealth_coordinates,
        #    PROBA_SELECTION,
        #    MUTATION_RATE,
        #    252,
        #)

        # Market decisions 
        pop, replace = bsc.UpdateFullWealth(pop, CurrentPrice)
        pop = bsc.NoiseProcess(pop)
        pop = bsc.UpdateFval(pop, dividend)
        pop = bsc.CalculateTSV(pop, price_history, dividend_history, CurrentPrice)
        #pop = bsc.DetermineEDF(pop)
        

        # Market clearing
        #'''
        #pop, mismatch, CurrentPrice, price_history, ToLiquidate = marketClearing(
        #    pop, CurrentPrice, price_history, spoils, solver, volume
        #)
        #'''
        CurrentPrice, ToLiquidate = lc.linear_solver(pop, spoils, volume, CurrentPrice)
        price_history = lc.UpdatePriceHistory(price_history, CurrentPrice)
        pop, mismatch = bsc.CalculateEDV(pop, CurrentPrice)

        # Market activity
        '''
        (
            pop,
            volume,
            dividend,
            random_dividend,
            dividend_history,
            spoils,
            Liquidations,
        ) = mk.MarketActivity(
            pop,
            CurrentPrice,
            asset_supply,
            dividend,
            dividend_history,
            spoils,
            ToLiquidate,
            random_dividend_history
        )
        '''
        dividend, random_dividend = mk.draw_dividend(dividend, random_dividend_history)
        pop, volume, spoils, Liquidations = mk.execute_ed(pop, CurrentPrice, asset_supply, spoils, ToLiquidate)
        pop = mk.earnings(pop, dividend)
        dividend_history.append(dividend)
        pop = mk.update_margin(pop, CurrentPrice)
        pop = mk.clear_debt(pop, CurrentPrice)

        pop, replace = bsc.UpdateWealthProfitAge(pop, CurrentPrice)
        pop = bsc.UpdateQuarterlyWealth(pop, generation)
        pop = bsc.UpdateWealthSeries(pop)

        pop = iv.Emp_Investment(pop)
        #AvgT, PropSignif, HighestT, AvgAbsT = 0, 0, 0, 0

        # Record results 
        results, sim_break = data.record_results(
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
        )

        if sim_break == 1:
            warnings.warn('Simulation break: one of the 3 strategy types is extinct.')
            break

    if generation < MAX_GENERATIONS - data.Barr:
        results = results[0:generation+1]

    df = pd.DataFrame(results, columns=data.columns)

    return df, pop

np.random.seed(8)
wealth_coordinates = [1 / 3, 1 / 3, 1 / 3]
TIME, POPSIZE = 10000, 1000
df, pop = main(
    "extended",
    "linear",
    wealth_coordinates,
    POPSIZE,
    TIME,
    0,
    0,
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
