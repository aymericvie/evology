from simulation import Simulation

def main(
    max_generations, 
    population_size,
    interest_rate,
    investment_bool,
    seed
    ):
    s = Simulation(
        max_generations = max_generations, 
        population_size = population_size,
        interest_rate=interest_rate,
        investment_bool = investment_bool,
        seed = seed)
    s.simulate()
    df = s.return_data()
    return df

if __name__ == "__main__":
    df = main(
        max_generations = 5000, #88128, 
        population_size = 3,
        interest_rate = 0.01,
        investment_bool = False,
        seed = 4242
    )  
    df.to_csv("rundata/run_data.csv")  
    print(df)
    
