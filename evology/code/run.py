""" #!/usr/bin/env python3 """
from main import *
from parameters import *



np.random.seed(9)
wealth_coordinates = [1 / 3, 1 / 3, 1 / 3]
# wealth_coordinates = [0.1233370025512552, 0.11705928057388676, 0.7596037168748581]
# np.random.seed(81)
# wealth_coordinates = np.random.dirichlet(np.ones(3), size=1)[0].tolist()
print(wealth_coordinates)

def run(
    POPULATION_SIZE, learning_mode, TIME, wealth_coordinates, tqdm_display, reset_wealth, ReinvestmentRate, InvestmentHorizon,
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
            tqdm_display,
            reset_wealth,
        )

# TODO; add extended ecology for run, or maybe alternative solvers

    return df, pop, ReturnsNT, ReturnsVI, ReturnsTF


df, pop, ReturnsNT, ReturnsVI, ReturnsTF = run(
    30, 0, 10000, wealth_coordinates, tqdm_display=False, reset_wealth=False, 
    ReinvestmentRate= 1.0, InvestmentHorizon = 252,
)

df.to_csv("evology/data/run_data.csv")
np.savetxt('evology/data/ReturnsNT.csv', ReturnsNT, delimiter=',')
np.savetxt('evology/data/ReturnsVI.csv', ReturnsVI, delimiter=',')
np.savetxt('evology/data/ReturnsTF.csv', ReturnsTF, delimiter=',')

print(df)
# print(stats.trim_mean(df['WealthAmp'], 0.1))


