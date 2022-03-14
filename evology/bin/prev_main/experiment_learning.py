import matplotlib.pyplot as plt
import main
import parameters

MAX_GENERATIONS = parameters.MAX_GENERATIONS

# Optional because they are arguments to main
CROSSOVER_RATE = parameters.CROSSOVER_RATE
MUTATION_RATE = parameters.MUTATION_RATE


(
    initial_pop,
    pop,
    maxFitnessValues,
    meanFitnessValues,
    replacements,
    agent0_profit,
    agent0_ema,
    dividend_history,
    price_history,
    random_dividend_history,
    list_excess_demand_func,
    aggregate_ed,
) = main.main(0, CROSSOVER_RATE, MUTATION_RATE)

# Plot population histograms at the start and at the end
print("--------------------------")

# print("Initial population was " + str(initial_pop))
# sns.histplot(data=np.array(initial_pop), legend = False, stat = "density", shrink = 0.85, discrete=True, bins = 11)
# plt.show()
# print("Current population is " + str(pop))
# sns.histplot(data=np.array(pop), legend = False, stat = "density", shrink = 0.85, discrete=True, bins = 11)
# plt.show()

# Plot the fitness evolution over time
plt.plot(maxFitnessValues, color="red", label="Maximum fitness")
plt.plot(meanFitnessValues, color="green", label="Average fitness")
plt.xlabel("Generations")
plt.ylabel("Max / Average Fitness")
plt.title("Max and Average Fitness over Generations")
plt.xlim(0, MAX_GENERATIONS + 1)
plt.legend()
plt.show()

plt.plot(replacements, color="gray", label="Hypermutations")
plt.xlabel("Generations")
plt.ylabel("Hypermutations")
plt.title("Hypermutations over time")
plt.xlim(0, MAX_GENERATIONS + 1)
plt.legend()
plt.show()

plt.plot(agent0_ema, color="red", label="EMA")
plt.plot(agent0_profit, color="green", label="Profits")
plt.xlabel("Generations")
plt.ylabel("Profit")
plt.title("Profit and EMA profit of Albert")
plt.xlim(0, MAX_GENERATIONS + 1)
plt.legend()
plt.show()


plt.plot(agent0_ema, color="red", label="EMA")
plt.plot(agent0_profit, color="green", label="Profits")
plt.xlabel("Generations")
plt.ylabel("Profit")
plt.title("Profit and EMA profit of Albert")
plt.xlim(0, MAX_GENERATIONS + 1)
plt.legend()
plt.show()

plt.plot(dividend_history, color="red", label="dividend")
plt.xlabel("Generations")
plt.ylabel("Dividend")
plt.title("Dividends over time")
plt.legend()
plt.show()

plt.plot(price_history, color="black", label="price")
plt.xlabel("Generations")
plt.ylabel("Price")
plt.title("Prices over time")
plt.legend()
plt.show()

print("-----------------------")
