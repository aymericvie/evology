from steps import *


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

        # Market decisions 
        pop, replace = bsc.UpdateFullWealth(pop, CurrentPrice)
        pop = bsc.NoiseProcess(pop)
        pop = bsc.UpdateFval(pop, dividend)
        pop = bsc.CalculateTSV(pop, price_history, dividend_history, CurrentPrice)
        pop = bsc.DetermineEDF(pop)

        # Market clearing
        pop, mismatch, CurrentPrice, price_history, ToLiquidate = marketClearing(
            pop, CurrentPrice, price_history, spoils, solver, volume
        )

        # Market activity
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
            np.random.normal(0.0, 1.0)
        )
        pop, replace = bsc.UpdateWealthProfitAge(pop, CurrentPrice)

        # Investment
        (pop, AvgT, PropSignif, HighestT, AvgAbsT) = iv.Profit_Investment(
        pop, ReinvestmentRate, InvestmentHorizon, generation
        )

        # Record results 
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
