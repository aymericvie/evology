"""
 ## Market block 
 
The market folder contains the market functions.
1) Initialise market
2) Apply interest, dividends and reinvestment
3) Update wealth and profit
-) Compute excess demand functions
-) Market clearing algorithm
-) Apply excess demand 
-) Market parameters?

 ## Strategy block
A) Compute trading signal Phi


## Testing block
A testing folder that has a script for every script in the code, to test it 
does work well and normally.



 ## Learning block 
Organised in different cases depending on the learning algorithm we use.
- No learning - Maarten's model
- Genetic Programming (DEAP)
- Genetic algorithm (3 types, parametric evolution)
 

## Experiment block
The experiment folder contains folder experiments, one for each.
An experiment uses a market parameter, a learning parameter, a script.
Data and figures should be saved in separate folders for each experiment.




#### Next tasks

DEAP is constraining our job for the EAs. Why? Because of GP.
Should we start coding for the most constraining thing first? So that we can 
then have a structure as generalised as possible.

"""


"""

Objects
- orders [TSF, EDF, TSV, EDV]
- types [1*n]
- strategy [?]
- balance_sheet [W C S L M]
- performance [Profit Ema(profit)]
- price (1*T)

Strategy object
for GP: 1*n of functions (TSF will be complete copy)
for GA: one-parametric? Two-parametric? lets say one and keep it simple.

0) Initialisation of market, initialisation of population. 
    ## Requires a first wealth comput.

A) Determine phenotype
    1) Compute TS
    2) Compute ED

    orders = compute_ts(types, strategy, balance_sheet)

B) Market process
    3) Market clearing
    4) Apply ED
    5) Apply dividends, interest rate, reinvestment
    6) compute wealth, profits

    price, orders, balance_sheet = market(orders, balance_sheet)

C) Evolution of genotype
    7) hypermutate (initialise fitness as 0 to not impact evolution) LOC TBC ##
    8) Evolution block
        a. Fitness
        b. Adaptation
    
    strategy, balance_sheet, types, performance = evolution(strategy, balance_sheet, types, performance)



MODELS
- A simple GA with 3 strategy types: TF (time horizon), VI (value), NT (value), close to Maarten's. 
- A GP model (much more open and interesting and deep), varying terminals/primitives
- Maybe also: novelty search, MAP elites, elitist GA/GP

AXES OF ANALYSIS
- ALife & ecology dynamics, predator-prey, interactions...
- Open-Ended Evolution: is it OE? Learning model? Search space size? 
    Measures of complexity/phenotype diversity?
- Market efficiency over time
- Market stylized facts
- Market dynamics and impact of evolution (off/on/amount/modalities (ex: high mutation low cross))
- EC analysis: characterising the fitness landscape
- Systemic risk and FED activity (just a variation of hypermutation)




For GA: we start with initial distributions
One important point is how the distribution changes.
Two main modes of evolution: crossover.
1- Srategies able to mix with other types (Free GA)
    Obvious coding issue as we cannot crossover those that easily.
    If ind A meets B and B is of different type, children C and D will be copies?
    Or C and D become at random A or B? (potentially CD both A or B)
    
    It would be really nice to have a ind.types object, like ind.fitness
    
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, 
                   types=None)
    for ind in pop:
        ind.types = random.random()
    for ind in pop:
        print(ind.types)
        
    And it works!! So we would have something like if ind1.types == ind2.types: [] else []
    This is a very cool way to store agent characteristics. Should we store all?
    Such as ind.wealth, ind.cash, ind.loan, ind.asset, ind.profit, naturally into ind.fitness
    Can we store a function?
    Wow we can! 
    def func(x):
        return x**2
    for ind in pop:
        ind.tsf = func
        for ind in pop:
            print(ind.tsf)
            print(ind.tsf(2)) and it works!
    Do we even need the type/balance_sheet/strategy/performance objects? Maybe not!
    We could do everything with pop inside deap.
    
2- Strategies cannot mix with any type (Fidelity cst GA)
    Strat change only through hypermutation.
Check if this choice matters for the model dynamics. 

For hypermutation and reinitialisation:
1- As a function of current distribution (maybe a bit too stochastic, artificially convergent
        unless we have a types mutation mechanism.)
2- As a function of initial probabilities
    We consider that traders in our market are sampled from a larger population with this distr.








A) Determine phenotype
    1) Compute TS
    2) Compute ED
    
    ind.tsf = toolbox.compile(expr=ind) #for gp
    ind.(tsf,tsv,edf) = compute_ts(pop)

B) Market process
    3) Market clearing
    4) Apply ED
    5) Apply dividends, interest rate, reinvestment
    6) compute wealth, profits

    price, ind(edv, wealth, cash, asset, profit) = market(pop)

C) Evolution of genotype
    7) hypermutate (initialise fitness as 0 to not impact evolution) LOC TBC ##
    pop = hypermutate(pop)
    8) Evolution block
        a. Fitness
        b. Adaptation
    ind, ind.(types, fitness) = evolution(pop)
    







"""
