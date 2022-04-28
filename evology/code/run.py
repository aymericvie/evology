""" #!/usr/bin/env python3 """
from main import *
from parameters import *

def run(
    POPULATION_SIZE,
    learning_mode,
    TIME,
    solver,
    space,
    wealth_coordinates,
    tqdm_display,
    reset_wealth,
    ReinvestmentRate,
    InvestmentHorizon,
):
    if learning_mode == 0:
        df, pop = main(
            space,
            solver,
            wealth_coordinates,
            POPULATION_SIZE,
            TIME,
            0,
            0,
            ReinvestmentRate,
            InvestmentHorizon,
            tqdm_display,
            reset_wealth,
        )

    if learning_mode == 1:
        df, pop = main(
            space,
            solver,
            wealth_coordinates,
            POPULATION_SIZE,
            TIME,
            PROBA_SELECTION,
            MUTATION_RATE,
            ReinvestmentRate,
            InvestmentHorizon,
            tqdm_display,
            reset_wealth,
        )
    return df, pop


wealth_coordinates = np.random.dirichlet(np.ones(3), size=1)[0].tolist()
np.random.seed(8)
wealth_coordinates = [1/3,1/3,1/3]
print(wealth_coordinates)
df, pop = run(
    500,
    0,
    20 * 252, # 200_000,
    "linear", #"esl.true", # "linear",
    #"extended", 
    "scholl",
    wealth_coordinates,
    tqdm_display=False,
    reset_wealth=False,
    ReinvestmentRate=1.5, #limited impact?
    InvestmentHorizon=21, #ineffective right now?
)

df.to_csv("rundata/run_data.csv")

arr = []
for ind in pop:
    arr.append(ind.investor_flow * 63.0)

plt.hist(arr)
plt.show()

arr = []
for ind in pop:
    arr.append((ind.wealth / ind.wealth_series[0]) - 1)

plt.hist(arr)
plt.show()

