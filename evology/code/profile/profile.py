import sys

sys.path.append("./evology/code/")
sys.path.append("/Users/aymericvie/Documents/GitHub/evology/evology/code")
from steps import *
from parameters import *
import numpy as np

@profile

def main(
    strategy,
    space,
    wealth_coordinates,
    POPULATION_SIZE,
    MAX_GENERATIONS,
    seed,
    tqdm_display,
    reset_wealth,
):
    # Initialisation
    generation, CurrentPrice, dividend, spoils = 0, InitialPrice, INITIAL_DIVIDEND, 0.0
    results = np.zeros((MAX_GENERATIONS - data.Barr, data.variables))
    replace, volume = 0, 0.0

    # Random generator 
    rng = np.random.default_rng(seed=seed)
    np.random.seed(seed)

    # Population creation
    pop, asset_supply = cr.CreatePop(POPULATION_SIZE, space, wealth_coordinates, CurrentPrice, strategy, rng)

    # Dividend and NT process generation
    #price_history = prc.FictiousPriceSeries(rng)
    price_history = []

    dividend_series, rd_dividend_series = div.ExogeneousDividends(MAX_GENERATIONS, rng)
    rng = np.random.default_rng(seed=seed+1)
    process_series = prc.ExogeneousProcess(MAX_GENERATIONS, rng)
    rng = np.random.default_rng(seed=seed)

    for generation in tqdm(
        range(MAX_GENERATIONS), disable=tqdm_display, miniters=100, mininterval=0.5
        ):
    #for generation in range(MAX_GENERATIONS):

        # Population reset
        pop = cr.WealthReset(pop, POPULATION_SIZE, space, wealth_coordinates, generation, reset_wealth, CurrentPrice, strategy, rng)

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
        pop = bsc.UpdateFval(pop, dividend)
        price_means = bsc.subset_means(price_history, max_strat_lag)
        pop, price_means = bsc.CalculateTSV_staticf(pop, price_history, CurrentPrice, process_series[generation], rng, price_means)
        pop = bsc.CalculateTSV_avf(pop, generation, strategy, price_history, dividend)        
        ToLiquidate = bsc.DetermineLiquidation(spoils, volume)

        # ''' for VI on contemporaneous price ''' 
        # ed_functions = bsc.agg_ed_esl(pop, ToLiquidate)
        # CurrentPrice = mc.esl_solver(ed_functions, CurrentPrice)
        ed_functions = cz.agg_ed(pop, ToLiquidate, price_means)
        NewPrice = mc.scipy_solver(ed_functions, CurrentPrice)
        pop, mismatch = cz.calculate_edv(pop, NewPrice, price_means)

        # Market activity
        dividend, random_dividend = dividend_series[0, generation], rd_dividend_series[0, generation]
        pop, volume, spoils, Liquidations = mk.execute_ed(pop, NewPrice, asset_supply, spoils, ToLiquidate)

        # if volume != 0:
        #     CurrentPrice = NewPrice
        CurrentPrice = NewPrice


        if CurrentPrice >= 1_000_000:
            warnings.warn('Simulation break: price above 1M.')
            #raise RuntimeError('Price above 1M')
            break
        price_history = bsc.UpdatePriceHistory(price_history, CurrentPrice)

        pop = mk.earnings(pop, dividend)
        pop = mk.update_margin(pop, CurrentPrice)
        pop = mk.clear_debt(pop, CurrentPrice)

        pop, replace = bsc.UpdateWealthProfitAge(pop, CurrentPrice)
        pop = bsc.UpdateQuarterlyWealth(pop, generation)
        pop = bsc.UpdateWealthSeries(pop)
        
        '''
        if generation >= ShieldInvestment:
            pop = iv.Emp_Investment(pop, rng)
        '''

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
            process_series[generation]
        )
        
        if sim_break == 1 and reset_wealth != True:
           warnings.warn('Only one base strategy left.')
           break

    if generation < MAX_GENERATIONS - data.Barr:
        results = results[0:generation]

    df = pd.DataFrame(results, columns=data.columns)

    # av_stats = [df["AV_wealth"].iloc[-1] / df["AV_wealth"].iloc[0] - 1, round(df["AV_return"].mean(),4), round(df["AV_return"].std(),3), 
    # df["AV_wealth"].iloc[0], df["AV_wealth"].iloc[-1]]


    return df, pop #, av_stats


np.random.seed(8)
wealth_coordinates = [1 / 3, 1 / 3, 1 / 3]
wealth_coordinates = [0.3, 0.5, 0.2]
TIME, POPSIZE = 10_000, 1_000
df, pop = main(
    None,
    "scholl",
    wealth_coordinates,
    POPSIZE,
    TIME,
    8,
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
