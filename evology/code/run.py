from main import *
from parameters import *

seed = 9
np.random.seed()
wealth_coordinates = [1/3,1/3,1/3]
# wealth_coordinates = [0.3, 0.3, 0.4]
# wealth_coordinates=[0., 0., 1.]
# wealth_coordinates = np.random.dirichlet(np.ones(3), size=1)[0].tolist()
np.random.seed(seed)
print(wealth_coordinates)

def func(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, d, v, g, r):
    return 0
df, pop = main(
    strategy = None, #func, #None, #func,
    space = 'scholl', # 'extended',
    wealth_coordinates = wealth_coordinates,
    POPULATION_SIZE = 3,
    MAX_GENERATIONS = 100000, #50 * 252, #20000, #1000 * 252,
    seed = seed,
    tqdm_display = False,
    reset_wealth = True,
)

print(df)
df.to_csv("rundata/run_data.csv")
print(df["WShare_NT"].iloc[-1], df["WShare_VI"].iloc[-1], df["WShare_TF"].iloc[-1])
