import matplotlib
import matplotlib.pyplot as plt
import main
import numpy as np

np.set_printoptions(precision=4)
import parameters


MAX_GENERATIONS = parameters.MAX_GENERATIONS
RANDOM_SEED = parameters.RANDOM_SEED

# Optional because they are arguments to main
CROSSOVER_RATE = parameters.CROSSOVER_RATE
MUTATION_RATE = parameters.MUTATION_RATE
PROBA_SELECTION = parameters.PROBA_SELECTION

# price, initial_pop, pop, maxFitnessValues, meanFitnessValues, replacements, agent0_profit, agent0_ema, dividend_history, price_history, random_dividend_history, list_excess_demand_func, aggregate_ed, df = main.main(PROBA_SELECTION, CROSSOVER_RATE, MUTATION_RATE)
df, extended_price_history, pop_ex, balance_sheet = main.main(
    "extended", PROBA_SELECTION, CROSSOVER_RATE, MUTATION_RATE
)

print(df)
print("--------------------------")

df.plot(x="Gen", y=["Price"], kind="line", figsize=(15, 6))
plt.show()

df.plot(x="Gen", y=["LogP"], kind="line", figsize=(15, 6))
plt.show()

df.plot(x="Gen", y=["MeanT"], kind="line", figsize=(15, 6))
plt.show()

plt.plot(extended_price_history)
plt.show()


print("-----------------------")
