""" #!/usr/bin/env python3 """
from main import *
from parameters import *

np.random.seed(8)
wealth_coordinates = [1 / 3, 1 / 3, 1 / 3]
# wealth_coordinates = [0.026841462875044363, 0.4807191977989481, 0.4924393393260076]
# np.random.seed()
# wealth_coordinates = np.random.dirichlet(np.ones(3), size=1)[0].tolist()
print(wealth_coordinates)

def run(
    POPULATION_SIZE, learning_mode, TIME, wealth_coordinates, tqdm_display, reset_wealth, ReinvestmentRate
):
    if learning_mode == 0:
        df, pop = main(
            "scholl",
            "esl.true",
            wealth_coordinates,
            POPULATION_SIZE,
            TIME,
            0,
            0,
            ReinvestmentRate,
            tqdm_display,
            reset_wealth
        )

    if learning_mode == 1:
        df, pop = main(
            "scholl",
            "esl.true",
            wealth_coordinates,
            POPULATION_SIZE,
            TIME,
            PROBA_SELECTION,
            MUTATION_RATE,
            ReinvestmentRate,
            tqdm_display,
            reset_wealth,
        )

# TODO; add extended ecology for run, or maybe alternative solvers

    return df, pop


df, pop = run(
    100, 0, 100000, wealth_coordinates, tqdm_display=False, reset_wealth=False, ReinvestmentRate= 0
)

df.to_csv("evology/data/run_data.csv")
print(df)
print(stats.trim_mean(df['WealthAmp'], 0.1))

