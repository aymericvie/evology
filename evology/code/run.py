from main import *
from parameters import *

# wealth_coordinates = np.random.dirichlet(np.ones(3), size=1)[0].tolist()
np.random.seed(8)
wealth_coordinates = [1/3,1/3,1/3]
print(wealth_coordinates)

def func(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, d, v, g, r):
    return 0
df, pop, av_stats = main(
    strategy = None, #func, #None, #func,
    space = 'extended', # 'extended',
    wealth_coordinates=wealth_coordinates,
    POPULATION_SIZE = 200,
    MAX_GENERATIONS = 100 * 252, #20000, #1000 * 252,
    tqdm_display=False,
    reset_wealth=False,
)

print(df)
df.to_csv("rundata/run_data.csv")

print(av_stats)