# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
path = '/Users/aymericvie/Documents/GitHub/evology/evology/data/replication/empirical_funds/flow_data.csv'
df = pd.read_csv(path)

# %%
# Remove outliers and missing observations
df = df[df["net_assets"] > 0]
df = df.dropna(subset=['series_id'])
df = df[df["form"] == 'NPORT-P']

# Generate relevant variables 
df["Sum_redemptions"] = df['month_1_flow_redemption'] + df['month_2_flow_redemption'] + df['month_3_flow_redemption']
df["Red_flows_nav"] = 100 * df["Sum_redemptions"] / df["net_assets"]

# Sort data by fund ID and time to correctly estimate returns
df["report_date"] = pd.to_datetime(df["report_date"])
df = df.sort_values(by=['series_id', 'report_date'])

# Obtain quarterly returns
def returns(lag):
    arr = []
    arr = [np.nan]
    for i in range(len(df)):
        if i > 1:
            if df["series_id"].iloc[i] == df["series_id"].iloc[i-lag]:
                arr.append((df["net_assets"].iloc[i] - df["Sum_redemptions"].iloc[i]) / df["net_assets"].iloc[i-lag] - 1)
            else:
                arr.append(np.nan)
    arr.append(np.nan)
    return arr

df["nav_diff_1"] = returns(1)
df["nav_diff_2"] = returns(2)
df["nav_diff_3"] = returns(3)
df["nav_diff_4"] = returns(4)
df["nav_diff_5"] = returns(5)
df["nav_diff_6"] = returns(6)
df["nav_diff_7"] = returns(7)
df["nav_diff_8"] = returns(8)

# %%
# Remove unecessary columns
del df['Unnamed: 0']
# del df['Unnamed: 0.1']
del df['form']
del df['report_date']
del df['as_of_date']
del df['total_liabilities']
del df['month_1_flow_redemption']
del df['month_2_flow_redemption']
del df['month_3_flow_redemption']
del df["month_1_flow_sales"]
del df["month_2_flow_sales"]
del df["month_3_flow_sales"]
del df["month_1_flow_reinvestment"]
del df["month_2_flow_reinvestment"]
del df["month_3_flow_reinvestment"]

# %%
# Save adjusted data
df.to_csv("flow_data_processed.csv")
# %%
