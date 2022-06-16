import numpy as np
import pandas as pd

class Result:

    variables = [
        "Generation",
        "Price",
        "Dividend",
        "Volume",
        "NT_process",
        "VI_val",
        "WShare_NT",
        "WShare_VI",
        "WShare_TF",
        "NT_flows",
        "VI_flows",
        "TF_flows",
    ]

    def __init__(self, max_generations):
        self.max_generations = max_generations
        self.data = np.zeros((max_generations, len(Result.variables)))

    def update_results(
        self, 
        generation, 
        price, 
        dividend, 
        volume, 
        NT_process,
        VI_val,
        wshareNT,
        wshareVI,
        wshareTF,
        NTflows,
        VIflows,
        TFflows,
    ):
        arr = [
            generation,
            price,
            dividend,
            volume,
            NT_process,
            VI_val,
            wshareNT,
            wshareVI,
            wshareTF,
            NTflows,
            VIflows,
            TFflows,
        ]
        self.data[generation, :] = arr 

    def convert_df(self):
        df = pd.DataFrame(self.data, columns=Result.variables)
        return df