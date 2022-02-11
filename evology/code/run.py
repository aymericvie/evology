""" #!/usr/bin/env python3 """
from main import *
from parameters import *

np.random.seed(9)
wealth_coordinates = [1 / 3, 1 / 3, 1 / 3]
# wealth_coordinates = [0.42, 0.33, 0.25]
np.random.seed(8)
# wealth_coordinates = np.random.dirichlet(np.ones(3), size=1)[0].tolist()
print(wealth_coordinates)

def run(
    POPULATION_SIZE, learning_mode, TIME, wealth_coordinates, tqdm_display, reset_wealth, ReinvestmentRate, InvestmentHorizon, InvestmentIntensity, InvestorBehavior,
):
    if learning_mode == 0:
        df, pop, ReturnsNT, ReturnsVI, ReturnsTF = main(
            "scholl",
            "esl.true",
            wealth_coordinates,
            POPULATION_SIZE,
            TIME,
            0,
            0,
            ReinvestmentRate,
            InvestmentHorizon,
            InvestmentIntensity,
            InvestorBehavior,
            tqdm_display,
            reset_wealth
        )

    if learning_mode == 1:
        df, pop, ReturnsNT, ReturnsVI, ReturnsTF = main(
            "scholl",
            "esl.true",
            wealth_coordinates,
            POPULATION_SIZE,
            TIME,
            PROBA_SELECTION,
            MUTATION_RATE,
            ReinvestmentRate,
            InvestmentHorizon,
            InvestmentIntensity,
            InvestorBehavior,
            tqdm_display,
            reset_wealth,
        )
# TODO; add extended ecology for run, or maybe alternative solvers

    return df, pop

df, pop, ReturnsNT, ReturnsVI, ReturnsTF = run(
    3, 0, 10000, wealth_coordinates, tqdm_display=False, reset_wealth=False, 
    ReinvestmentRate= 1.95, InvestmentHorizon = 1, InvestmentIntensity = 1.0, InvestorBehavior = 'JKM'
)
df.to_csv("rundata/run_data.csv")
print(df)
print([df['WShare_NT'].mean(), df['WShare_VI'].mean(), df['WShare_TF'].mean()])


