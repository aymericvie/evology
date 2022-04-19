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
np.random.seed(9)
wealth_coordinates = [1/3,1/3,1/3]
wealth_coordinates = [0.09197907715627632, 0.7401382118614593, 0.16788271098226437]
print(wealth_coordinates)
df, pop = run(
    10,
    0,
    25000,
    #"esl.true",
    #"newton.true",
    #"esl.true",
    "esl.true", # "linear",
    "scholl", #exgtended
    wealth_coordinates,
    tqdm_display=False,
    reset_wealth=False,
    ReinvestmentRate=1,
    InvestmentHorizon=252,
)

df.to_csv("rundata/run_data.csv")
# print(df)
