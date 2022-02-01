#!/usr/bin/env python3
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
    reset_wealth
):
    # Initialise important variables and dataframe to store results
    ReturnsNT, ReturnsVI, ReturnsTF = (
        np.zeros((MAX_GENERATIONS - data.Barr, POPULATION_SIZE)),
        np.zeros((MAX_GENERATIONS - data.Barr, POPULATION_SIZE)),
        np.zeros((MAX_GENERATIONS - data.Barr, POPULATION_SIZE)),
    )
    generation, CurrentPrice, dividend, spoils, InvestmentSupply = 0, InitialPrice, INITIAL_DIVIDEND, 0, RefInvestmentSupply * POPULATION_SIZE
    results = np.zeros((MAX_GENERATIONS - data.Barr, data.variables))
    wealth_tracker= np.zeros((MAX_GENERATIONS, POPULATION_SIZE))
    returns_tracker= np.zeros((MAX_GENERATIONS, POPULATION_SIZE))
    price_history, dividend_history = [], []

    pop, asset_supply = cr.CreatePop(POPULATION_SIZE, space, wealth_coordinates)
    bs.calculate_wealth(pop, CurrentPrice)
    bs.UpdatePrevWealth(pop)

    for generation in tqdm(
        range(MAX_GENERATIONS), disable=tqdm_display, miniters=100, mininterval=0.5
    ):

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
            ReinvestmentRate,
        )

        # Investment
        (
            wealth_tracker, 
            returns_tracker, 
            pop, 
            propSignif
        ) = ApplyInvestment(
            pop, 
            generation, 
            wealth_tracker, 
            returns_tracker, 
            InvestmentHorizon, 
            InvestmentSupply, 
        )

        # Record results
        # wealth_tracker = iv.WealthTracking(wealth_tracker, pop, generation)
        results, wealth_tracker, ReturnsNT, ReturnsVI, ReturnsTF = data.record_results(
            results,
            wealth_tracker,
            generation,
            CurrentPrice,
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
        )

    df = pd.DataFrame(results, columns=data.columns)

    return df, pop, ReturnsNT, ReturnsVI, ReturnsTF
