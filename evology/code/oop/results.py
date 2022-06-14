import numpy as np
import pandas as pd

class Result:

    variables = [
        "Generation",
        "Price",
        "Dividend",
        "Volume"
    ]

    def __init__(self, max_generations):
        self.max_generations = max_generations
        self.data = np.zeros((max_generations, len(Result.variables)))

    def update_results(self, generation, price, dividend, volume):
        arr = [
            generation,
            price,
            dividend,
            volume
        ]
        self.data[generation, :] = arr 

    def convert_df(self):
        df = pd.DataFrame(self.data, columns=Result.variables)
        print(df)
        df.to_csv("rundata/run_data.csv")
        return df