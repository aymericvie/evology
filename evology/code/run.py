""" #!/usr/bin/env python3 """
from main import *
from parameters import *

np.random.seed(3)
wealth_coordinates = [1 / 3, 1 / 3, 1 / 3]
wealth_coordinates = [0.026841462875044363, 0.4807191977989481, 0.4924393393260076]
# np.random.seed()
# wealth_coordinates = np.random.dirichlet(np.ones(3), size=1)[0].tolist()
print(wealth_coordinates)

def run(
    POPULATION_SIZE, learning_mode, TIME, wealth_coordinates, tqdm_display, reset_wealth, ReinvestmentRate
):

    if learning_mode == 0:
        df, pop = main(
            "static",
            "scholl",
            "esl.true",
            TIME,
            0,
            POPULATION_SIZE,
            0,
            wealth_coordinates,
            tqdm_display,
            reset_wealth,
            ReinvestmentRate
        )
    if learning_mode == 10:
        df, pop = main(
            "static",
            "scholl",
            "esl",
            TIME,
            0,
            POPULATION_SIZE,
            0,
            wealth_coordinates,
            tqdm_display,
            reset_wealth,
            ReinvestmentRate
        )
    if learning_mode == 1:
        df, pop = main(
            "between",
            "scholl",
            "esl.true",
            TIME,
            PROBA_SELECTION,
            POPULATION_SIZE,
            MUTATION_RATE,
            wealth_coordinates,
            tqdm_display,
            reset_wealth,
            ReinvestmentRate
        )
    if learning_mode == 2:
        df, pop = main(
            "between",
            "scholl",
            "esl.true",
            TIME,
            PROBA_SELECTION,
            POPULATION_SIZE,
            0,
            wealth_coordinates,
            tqdm_display,
            reset_wealth,
            ReinvestmentRate
        )
    if learning_mode == 3:
        df, pop = main(
            "static",
            "extended",
            "esl",
            TIME,
            0,
            POPULATION_SIZE,
            0,
            wealth_coordinates,
            tqdm_display,
            reset_wealth,
            ReinvestmentRate
        )
    if learning_mode == 4:
        df, pop = main(
            "between",
            "extended",
            "esl",
            TIME,
            PROBA_SELECTION,
            POPULATION_SIZE,
            MUTATION_RATE,
            wealth_coordinates,
            tqdm_display,
            reset_wealth,
            ReinvestmentRate
        )
    return df, pop


df, pop = run(
    100, 0, 10000, wealth_coordinates, tqdm_display=False, reset_wealth=False, ReinvestmentRate= 0
)

df.to_csv("evology/data/run_data.csv")
print(df)
print(stats.trim_mean(df['WealthAmp'], 0.1))

