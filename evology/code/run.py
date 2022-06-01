from main import *
from parameters import *


wealth_coordinates = [1/3,1/3,1/3]
# wealth_coordinates = [0.15, 0.6, 0.25]
# wealth_coordinates = [0.3, 0.3, 0.4]
# wealth_coordinates=[0.37469673478000054, 0.21665619652962376, 0.40864706869037576]
# wealth_coordinates = np.random.dirichlet(np.ones(3), size=1)[0].tolist()
# wealth_coordinates=[0.3877491723252324, 0.439903019419811, 0.17234780825495657]
seed = 9
np.random.seed(seed)
print(wealth_coordinates)

def func(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, d, v, g, r):
    return 0
df, pop = main(
    strategy = None, #func, #None, #func,
    space = 'extended', # 'extended',
    wealth_coordinates = wealth_coordinates,
    POPULATION_SIZE = 1000,
    MAX_GENERATIONS = 300, #50 * 252, #20000, #1000 * 252,
    seed = seed,
    tqdm_display = False,
    reset_wealth = False,
)

print(df)
df.to_csv("rundata/run_data.csv")
print(df["WShare_NT"].iloc[-1], df["WShare_VI"].iloc[-1], df["WShare_TF"].iloc[-1])

# for ind in pop:
#     if ind.type == 'vi':
#         print([ind.strategy, ind.val, ind.val_net])