
path = '/Users/aymericvie/Documents/GitHub/evology/evology/data/nport_p_info2022-06-10T17.csv.gz'

import pandas as pd
data = pd.read_csv(path, compression='gzip',
                   error_bad_lines=False)
print(data)
data.to_csv("nport_data.csv")
