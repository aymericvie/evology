from simulation import Simulation


def main(max_generations, population_size, wealth_coords, interest_rate, investment_bool, seed):
    s = Simulation(
        max_generations=max_generations,
        population_size=population_size,
        wealth_coords=wealth_coords,
        interest_rate=interest_rate,
        investment_bool=investment_bool,
        seed=seed,
    )
    s.simulate()
    df = s.return_data()
    return df


if __name__ == "__main__":
    df = main(
        max_generations=100,
        population_size=3,
        wealth_coords=[1/3, 1/3, 1/3],
        interest_rate=0.01,
        investment_bool=False,
        seed=98229,
    )
    df.to_csv("rundata/run_data.csv")
    print(df)
