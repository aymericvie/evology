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
# wealth_coordinates = [0.5, 0.15, 0.35]
# wealth_coordinates = [0.09102807903879707, 0.5774996771459384, 0.33147224381526447]
print(wealth_coordinates)
df, pop = run(
    250,
    0,
    800 * 252, # 200_000,
    "esl.true", # "linear",
    "extended", 
    # "scholl",
    wealth_coordinates,
    tqdm_display=False,
    reset_wealth=False,
    ReinvestmentRate=1.0, #limited impact?
    InvestmentHorizon=21, #ineffective right now?
)

df.to_csv("rundata/run_data.csv")
