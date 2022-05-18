from steps import *

def main(
    strategy,
    space,
    wealth_coordinates,
    POPULATION_SIZE,
    MAX_GENERATIONS,
    tqdm_display,
    reset_wealth,
):
    # Initialisation
    generation, CurrentPrice, dividend, spoils = 0, InitialPrice, INITIAL_DIVIDEND, 0
    results = np.zeros((MAX_GENERATIONS - data.Barr, data.variables))
    price_history, dividend_history, replace, volume = [], [], 0, 0.0

    # Population creation
    pop, asset_supply = cr.CreatePop(POPULATION_SIZE, space, wealth_coordinates, CurrentPrice, strategy)

    for generation in tqdm(
        range(MAX_GENERATIONS), disable=tqdm_display, miniters=100, mininterval=0.5
        ):
    #for generation in range(MAX_GENERATIONS):



        # Population reset
        pop = cr.WealthReset(pop, space, wealth_coordinates, generation, reset_wealth, CurrentPrice, strategy)

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
        pop = bsc.CalculateTSV_staticf(pop, price_history, dividend_history, CurrentPrice)
        pop = bsc.CalculateTSV_avf(pop, generation, strategy, price_history, dividend)
        #pop = bsc.DetermineEDF(pop)
        

        # Market clearing
        #'''
        #pop, mismatch, CurrentPrice, price_history, ToLiquidate = marketClearing(
        #    pop, CurrentPrice, price_history, spoils, solver, volume
        #)
        #'''
        

        ''' For VI on previous price (scalar tsf)'''
        # CurrentPrice = lc.linear_solver(pop, ToLiquidate, CurrentPrice)
        
        ToLiquidate = lc.DetermineLiquidation(spoils, volume)

        # ''' for VI on contemporaneous price ''' 
        # ed_functions = bsc.agg_ed_esl(pop, ToLiquidate)
        # CurrentPrice = mc.esl_solver(ed_functions, CurrentPrice)

        ''' Test scipy '''
        ''' for VI on contemporaneous price ''' 
        ed_functions = bsc.agg_ed(pop, ToLiquidate)[0]
        CurrentPrice = mc.scipy_solver(ed_functions, CurrentPrice)

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

        if generation >= ShieldInvestment:
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

        if sim_break == 1 and reset_wealth != True:
           warnings.warn('Only one base strategy left.')
           break

        if CurrentPrice >= 1_000_000:
            warnings.warn('Simulation break: price above 1M.' + str(generation))
            # X = np.linspace(0.01, 500, 1000)
            # Y = [ed_functions(x) for x in X]
            # plt.plot(X, Y)
            # plt.ylim(0, 10000)
            # plt.show()

            # plt.plot(X, Y)
            # plt.show()

            # X = np.linspace(0, 100_000_000, 10000)
            # Y = [ed_functions(x) for x in X]
            # plt.plot(X, Y)
            # plt.show()
            break

    

    if generation < MAX_GENERATIONS - data.Barr:
        results = results[0:generation+1]

    df = pd.DataFrame(results, columns=data.columns)

    #print(df["AV_wealth"])
    # av_stats = [df["AV_wealth"].iloc[-1] / df["AV_wealth"].iloc[0] - 1, round(df["AV_return"].mean(),4), round(df["AV_return"].std(),3), 
    # df["AV_wealth"].iloc[0], df["AV_wealth"].iloc[-1]]

    return df, pop #, av_stats
