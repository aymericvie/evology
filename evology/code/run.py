from main import *
from parameters import *

seed = 8
np.random.seed()
wealth_coordinates = [1/3,1/3,1/3]
# wealth_coordinates=[0.3, 0.3, 0.4]
# wealth_coordinates = np.random.dirichlet(np.ones(3), size=1)[0].tolist()
wealth_coordinates = [0.31418887808615753, 0.029839754449283655, 0.6559713674645588]
np.random.seed(seed)
print(wealth_coordinates)

def func(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, d, v, g, r):
    return 0
df, pop = main(
    strategy = None, #func, #None, #func,
    space = 'extended', # 'extended',
    wealth_coordinates=wealth_coordinates,
    POPULATION_SIZE = 100,
    MAX_GENERATIONS = 5000, #50 * 252, #20000, #1000 * 252,
    seed = seed,
    tqdm_display=False,
    reset_wealth=False,
)

print(df)
df.to_csv("rundata/run_data.csv")
print(df["WShare_NT"].iloc[-1], df["WShare_VI"].iloc[-1], df["WShare_TF"].iloc[-1])

# print(av_stats)
'''
df["Mispricing"] = (df["Mean_VI"] / df["Price"]) - 1
df["LogPriceReturns"] = np.log(df["Price"]/df["Price"].shift(1))
df["Volatility"] = df["LogPriceReturns"].rolling(window=252).std()*np.sqrt(252)
volatility = df["Volatility"].mean()
if df["NT_nav"].iloc[0] != 0 and math.isnan(df["NT_nav"].iloc[0]) == False and math.isnan(df["NT_nav"].iloc[-1]) == False:
    multi_NT = df["NT_nav"].iloc[-1] / df["NT_nav"].iloc[0]
if df["NT_nav"].iloc[-1] == 0 and df["NT_nav"].iloc[0] > 0 :
    multi_NT = -1.
else:
    multi_NT = 0.0
if df["VI_nav"].iloc[0] != 0 and math.isnan(df["VI_nav"].iloc[0]) == False and math.isnan(df["VI_nav"].iloc[-1]) == False:
    multi_VI = df["VI_nav"].iloc[-1] / df["VI_nav"].iloc[0]
if df["VI_nav"].iloc[-1] == 0 and df["VI_nav"].iloc[0] > 0 :
    multi_VI = -1.
else:
    multi_VI = 0.0
if df["TF_nav"].iloc[0] != 0 and math.isnan(df["TF_nav"].iloc[0]) == False and math.isnan(df["TF_nav"].iloc[-1]) == False:
    multi_TF = df["TF_nav"].iloc[-1] / df["TF_nav"].iloc[0]
if df["TF_nav"].iloc[-1] == 0 and df["TF_nav"].iloc[0] > 0 :
    multi_TF = -1.
else:
    multi_TF = 0.0
if math.isnan(df["BH_wealth"].iloc[-1]) == False:
    multi_BH = df["BH_wealth"].iloc[-1] / df["BH_wealth"].iloc[0]
if df["BH_wealth"].iloc[-1] == 0 and df["BH_wealth"].iloc[0] > 0 :
    multi_BH = -1.
else:
    multi_BH = 0.0
if math.isnan(df["IR_wealth"].iloc[-1]) == False:
    multi_IR = df["IR_wealth"].iloc[-1] / df["IR_wealth"].iloc[0] 
if df["IR_wealth"].iloc[-1] == 0 and df["IR_wealth"].iloc[0] > 0 :
    multi_IR = -1.
else:
    multi_IR = 0.0

print([volatility, multi_NT, multi_VI, multi_TF, multi_BH, multi_IR])
'''