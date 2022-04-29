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
            tqdm_display,
            reset_wealth,
        )
    return df, pop


wealth_coordinates = np.random.dirichlet(np.ones(3), size=1)[0].tolist()
np.random.seed()
wealth_coordinates = [1/3,1/3,1/3]
print(wealth_coordinates)
df, pop = run(
    100,
    0,
    100 * 252, # 200_000,
    "linear", 
    #"esl.true",
    "extended", 
    #"scholl",
    wealth_coordinates,
    tqdm_display=False,
    reset_wealth=False,
)

df.to_csv("rundata/run_data.csv")


