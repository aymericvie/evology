""" #!/usr/bin/env python3 """
from main import *
from parameters import *


np.random.seed(8)
wealth_coordinates = [1 / 3, 1 / 3, 1 / 3]
# wealth_coordinates = [0.20899108903451205, 0.1210376286378561, 0.6699712823276319]
# wealth_coordinates = np.random.dirichlet(np.ones(3), size=1)[0].tolist()

print(wealth_coordinates)


# main(mode, space, solver, circuit, MAX_GENERATIONS, PROBA_SELECTION, POPULATION_SIZE, MUTATION_RATE, wealth_coordinates, tqdm_display, reset_wealth):


def run(
    POPULATION_SIZE, learning_mode, TIME, wealth_coordinates, tqdm_display, reset_wealth
):

    if learning_mode == 0:
        df, pop = main(
            "static",
            "scholl",
            "esl.true",
            False,
            TIME,
            0,
            POPULATION_SIZE,
            0,
            wealth_coordinates,
            tqdm_display,
            reset_wealth,
        )
    if learning_mode == 1:
        df, pop = main(
            "between",
            "scholl",
            "esl.true",
            False,
            TIME,
            PROBA_SELECTION,
            POPULATION_SIZE,
            MUTATION_RATE,
            wealth_coordinates,
            tqdm_display,
            reset_wealth,
        )
    if learning_mode == 2:
        df, pop = main(
            "between",
            "scholl",
            "esl.true",
            False,
            TIME,
            PROBA_SELECTION,
            POPULATION_SIZE,
            0,
            wealth_coordinates,
            tqdm_display,
            reset_wealth,
        )
    if learning_mode == 3:
        df, pop = main(
            "static",
            "extended",
            "esl",
            False,
            TIME,
            0,
            POPULATION_SIZE,
            0,
            wealth_coordinates,
            tqdm_display,
            reset_wealth,
        )
    if learning_mode == 4:
        df, pop = main(
            "between",
            "extended",
            "esl",
            False,
            TIME,
            PROBA_SELECTION,
            POPULATION_SIZE,
            MUTATION_RATE,
            wealth_coordinates,
            tqdm_display,
            reset_wealth,
        )
    return df, pop


df, pop = run(
    100, 1, 10000, wealth_coordinates, tqdm_display=False, reset_wealth=False
)
# df.to_csv("evology/data/run_data.csv")
df.to_csv("evology/data/run_data.csv", compression = 'gzip')
print(df)
print(df['WealthAmp'])
