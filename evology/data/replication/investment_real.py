# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
path = '/Users/aymericvie/Documents/GitHub/evology/evology/data/replication/empirical_funds/flow_data.csv'
df = pd.read_csv(path)

# %%
# remove extinct funds
df = df[df["net_assets"] > 0]

# Investment flows
df["Sum_redemptions"] = df['month_1_flow_redemption'] + df['month_2_flow_redemption'] + df['month_3_flow_redemption']

# Ratio of redemptions to net asset values
df["Red_flows_nav"] = 100 * df["Sum_redemptions"] / df["net_assets"]


df.hist(column='Red_flows_nav', bins = range(-40,40))
# plt.vlines(x=np.nanmean(df["Red_flows_nav"]), ymin=0, ymax=15000, colors='red', linestyles='dashed')
plt.show()

# %%
# remove funds with no series_id
df = df.dropna(subset=['series_id'])
df = df[df["form"] == 'NPORT-P']
print(df)

# %%
df["report_date"] = pd.to_datetime(df["report_date"])
print(df["report_date"])


# %%
df = df.sort_values(by=['series_id', 'report_date'])
print(df)

# %%

# number of distinct funds and dates
print(len(df["series_id"].unique()))
# 13005

# print(df["report_date"].unique())
# from Sept 2019 to November 2021


# %%
# Get data on returns 

# one quarter
arr = [np.nan]
for i in range(len(df)):
    if i > 1:
        if df["series_id"].iloc[i] == df["series_id"].iloc[i-1]:
            arr.append((df["net_assets"].iloc[i] - df["Sum_redemptions"].iloc[i]) / df["net_assets"].iloc[i-1] - 1)
        else:
            arr.append(np.nan)
# print(arr)
arr.append(np.nan)
df["nav_diff_1"] = arr

# two quarters
arr = [np.nan]
for i in range(len(df)):
    if i > 1:
        if df["series_id"].iloc[i] == df["series_id"].iloc[i-2]:
            arr.append((df["net_assets"].iloc[i] - df["Sum_redemptions"].iloc[i]) / df["net_assets"].iloc[i-2] - 1)
        else:
            arr.append(np.nan)
# print(arr)
arr.append(np.nan)
df["nav_diff_2"] = arr

# 3 quarters
arr = [np.nan]
for i in range(len(df)):
    if i > 1:
        if df["series_id"].iloc[i] == df["series_id"].iloc[i-3]:
            arr.append((df["net_assets"].iloc[i] - df["Sum_redemptions"].iloc[i]) / df["net_assets"].iloc[i-3] - 1)
        else:
            arr.append(np.nan)
# print(arr)
arr.append(np.nan)
df["nav_diff_3"] = arr

# 4 quarters
arr = [np.nan]
for i in range(len(df)):
    if i > 1:
        if df["series_id"].iloc[i] == df["series_id"].iloc[i-4]:
            arr.append((df["net_assets"].iloc[i] - df["Sum_redemptions"].iloc[i]) / df["net_assets"].iloc[i-4] - 1)
        else:
            arr.append(np.nan)
# print(arr)
arr.append(np.nan)
df["nav_diff_4"] = arr

# 5 quarters
arr = [np.nan]
for i in range(len(df)):
    if i > 1:
        if df["series_id"].iloc[i] == df["series_id"].iloc[i-5]:
            arr.append((df["net_assets"].iloc[i] - df["Sum_redemptions"].iloc[i]) / df["net_assets"].iloc[i-5] - 1)
        else:
            arr.append(np.nan)
# print(arr)
arr.append(np.nan)
df["nav_diff_5"] = arr

# 6 quarters
arr = [np.nan]
for i in range(len(df)):
    if i > 1:
        if df["series_id"].iloc[i] == df["series_id"].iloc[i-6]:
            arr.append((df["net_assets"].iloc[i] - df["Sum_redemptions"].iloc[i]) / df["net_assets"].iloc[i-6] - 1)
        else:
            arr.append(np.nan)
# print(arr)
arr.append(np.nan)
df["nav_diff_6"] = arr

# 7 quarters
arr = [np.nan]
for i in range(len(df)):
    if i > 1:
        if df["series_id"].iloc[i] == df["series_id"].iloc[i-7]:
            arr.append((df["net_assets"].iloc[i] - df["Sum_redemptions"].iloc[i]) / df["net_assets"].iloc[i-7] - 1)
        else:
            arr.append(np.nan)
# print(arr)
arr.append(np.nan)
df["nav_diff_7"] = arr

# 8 quarters
arr = [np.nan]
for i in range(len(df)):
    if i > 1:
        if df["series_id"].iloc[i] == df["series_id"].iloc[i-8]:
            arr.append((df["net_assets"].iloc[i] - df["Sum_redemptions"].iloc[i]) / df["net_assets"].iloc[i-8] - 1)
        else:
            arr.append(np.nan)
# print(arr)
arr.append(np.nan)
df["nav_diff_8"] = arr

# %%
'''
# 9 quarters
arr = [np.nan]
for i in range(len(df)):
    if i > 1:
        if df["series_id"].iloc[i] == df["series_id"].iloc[i-9]:
            arr.append((df["net_assets"].iloc[i] - df["Sum_redemptions"].iloc[i]) / df["net_assets"].iloc[i-9] - 1)
        else:
            arr.append(np.nan)
# print(arr)
arr.append(np.nan)
df["nav_diff_9"] = arr

# 10 quarters
arr = [np.nan]
for i in range(len(df)):
    if i > 1:
        if df["series_id"].iloc[i] == df["series_id"].iloc[i-10]:
            arr.append((df["net_assets"].iloc[i] - df["Sum_redemptions"].iloc[i]) / df["net_assets"].iloc[i-10] - 1)
        else:
            arr.append(np.nan)
# print(arr)
arr.append(np.nan)
df["nav_diff_10"] = arr
'''


# %%
print(df.count())
'''
nav_diff_1                   86145
nav_diff_2                   73586
nav_diff_3                   61430
nav_diff_4                   49732
nav_diff_5                   38444
nav_diff_6                   27498
nav_diff_7                   17086
nav_diff_8                    7578
'''

# %%
# clean data of outlier movements
df2 = df[(df["nav_diff_1"] <= 1.0) &  (df["nav_diff_1"] >= -1.0)]
df2 = df2[(df2["Red_flows_nav"] <= 50) & (df2["Red_flows_nav"] >= -50)]
# plots for various returns levels

# sns.regplot(x="nav_diff_1", y="Red_flows_nav", data=df2, line_kws={"color": "red"})
plt.hlines(y=0, colors='black', linestyles='dashed',xmin = -1, xmax = 1)
plt.vlines(x=0, colors='black', linestyles='dashed',ymin = -50, ymax = 50)
sns.regplot(x="nav_diff_1", y="Red_flows_nav", data=df2, line_kws={"color": "red"}, lowess=True, scatter_kws={'s':2})
plt.xlabel('Return')
plt.ylabel('% of redemption flows to NAV')
plt.title('Redemption flows vs quarterly(1) returns, with lowess fit')
# plt.savefig('redemption_flows_linear.png', dpi=300)
plt.show()

# %%
params = {"ytick.color" : "w",
          "xtick.color" : "w",
          "axes.labelcolor" : "w",
          "axes.edgecolor" : "w"}
plt.rcParams.update(params)

df2 = df[(df["nav_diff_1"] <= 0.5) &  (df["nav_diff_1"] >= -0.5)]
df2 = df2[(df2["Red_flows_nav"] <= 50) & (df2["Red_flows_nav"] >= -50)]
plt.hlines(y=0, colors='black', linestyles='dashed',xmin = -0.5, xmax = 0.5)
plt.vlines(x=0, colors='black', linestyles='dashed',ymin = -50, ymax = 50)
sns.regplot(x="nav_diff_1", y="Red_flows_nav", data=df2, line_kws={"color": "red"}, lowess=True, scatter_kws={'s':2})
plt.xlabel('Return')
plt.ylabel('% of redemption flows to NAV')
# plt.title('Redemption flows vs quarterly(1) returns, with lowess fit')
plt.savefig('redemption_flows_lowess.png', dpi=300)
plt.show()

# %%

df2 = df[(df["nav_diff_2"] <= 1.0) &  (df["nav_diff_2"] >= -1.0)]
df2 = df2[(df2["Red_flows_nav"] <= 50) & (df2["Red_flows_nav"] >= -50)]

sns.regplot(x="nav_diff_2", y="Red_flows_nav", data=df2, line_kws={"color": "red"}, lowess=True, scatter_kws={'s':2})
# sns.regplot(x="nav_diff_2", y="Red_flows_nav", data=df2, line_kws={"color": "red"})
plt.hlines(y=0, colors='black', linestyles='dashed',xmin = -1, xmax = 1)
plt.vlines(x=0, colors='black', linestyles='dashed',ymin = -50, ymax = 50)
plt.xlabel('Return')
plt.ylabel('% of redemption flows to NAV')
plt.title('Redemption flows vs quarterly(2) returns, with lowess fit')
# plt.savefig('redemption_flows_lowess.png', dpi=300)
plt.show()

# %%
df2 = df[(df["nav_diff_3"] <= 1.0) &  (df["nav_diff_3"] >= -1.0)]
df2 = df2[(df2["Red_flows_nav"] <= 50) & (df2["Red_flows_nav"] >= -50)]

sns.regplot(x="nav_diff_3", y="Red_flows_nav", data=df2, line_kws={"color": "red"})
plt.hlines(y=0, colors='black', linestyles='dashed',xmin = -1, xmax = 1)
plt.vlines(x=0, colors='black', linestyles='dashed',ymin = -50, ymax = 50)
plt.xlabel('Return')
plt.ylabel('% of redemption flows to NAV')
plt.title('Redemption flows vs quarterly(3) returns, with lowess fit')
# plt.savefig('redemption_flows_linear.png', dpi=300)
plt.show()


# %%
df2 = df[(df["nav_diff_4"] <= 1.0) &  (df["nav_diff_4"] >= -1.0)]
df2 = df2[(df2["Red_flows_nav"] <= 50) & (df2["Red_flows_nav"] >= -50)]

# sns.regplot(x="nav_diff_4", y="Red_flows_nav", data=df2, line_kws={"color": "red"}, scatter_kws={'s':2, "color": "black"})
plt.hlines(y=0, colors='black', linestyles='dashed',xmin = -1, xmax = 1)
plt.vlines(x=0, colors='black', linestyles='dashed',ymin = -50, ymax = 50)
sns.regplot(x="nav_diff_4", y="Red_flows_nav", data=df2, line_kws={"color": "red"}, lowess=True, scatter_kws={'s':2})
plt.xlabel('Return')
plt.ylabel('% of redemption flows to NAV')
plt.title('Redemption flows vs yearly returns, with lowess fit')
# plt.savefig('redemption_flows_linear.png', dpi=300)
plt.show()

# %%
df2 = df[(df["nav_diff_8"] <= 1.0) &  (df["nav_diff_8"] >= -1.0)]
df2 = df2[(df2["Red_flows_nav"] <= 50) & (df2["Red_flows_nav"] >= -50)]

# sns.regplot(x="nav_diff_4", y="Red_flows_nav", data=df2, line_kws={"color": "red"}, scatter_kws={'s':2, "color": "black"})
plt.hlines(y=0, colors='black', linestyles='dashed',xmin = -1, xmax = 1)
plt.vlines(x=0, colors='black', linestyles='dashed',ymin = -50, ymax = 50)
sns.regplot(x="nav_diff_8", y="Red_flows_nav", data=df2, line_kws={"color": "red"}, lowess=True, scatter_kws={'s':2})
plt.xlabel('Return')
plt.ylabel('% of redemption flows to NAV')
plt.title('Redemption flows vs 2Y returns, with lowess fit')
# plt.savefig('redemption_flows_linear.png', dpi=300)
plt.show()
# %%

df2 = df.copy()
del df2['cik']
# del df2['Unnamed: 0']
del df2['month_1_flow_redemption']
del df2['month_2_flow_redemption']
del df2['month_3_flow_redemption']
del df2['month_1_flow_sales']
del df2['month_2_flow_sales']
del df2['month_3_flow_sales']

df.corr()
ax = sns.heatmap(df2.corr(), annot=False)
plt.show()

# %%
# Linear regressions

# compute with statsmodels, another way, using formula
import statsmodels.formula.api as sm
result = sm.ols(
    formula="Red_flows_nav ~ nav_diff_1 + nav_diff_2 + nav_diff_3 + nav_diff_4 + nav_diff_5 + nav_diff_6 + nav_diff_7 + nav_diff_8 ", 
    data=df).fit()
print (result.summary())
print (result.rsquared, result.rsquared_adj)

# %%
print(result.summary().as_latex())
# %%
result = sm.ols(
    formula="Red_flows_nav ~ nav_diff_1 + nav_diff_2 + nav_diff_3 + nav_diff_4 + nav_diff_5 + nav_diff_6 + nav_diff_7", 
    data=df).fit()
print (result.summary())
print (result.rsquared, result.rsquared_adj)

# %%
result = sm.ols(formula="Red_flows_nav ~ nav_diff_1 + nav_diff_2 + nav_diff_3 + nav_diff_4 + nav_diff_5 + nav_diff_6", 
    data=df).fit()
print (result.summary())
print (result.rsquared, result.rsquared_adj)

# %%
result = sm.ols(formula="Red_flows_nav ~ nav_diff_1 + nav_diff_2 + nav_diff_3 + nav_diff_4 + nav_diff_5", 
    data=df).fit()
print (result.summary())
print (result.rsquared, result.rsquared_adj)
# %%
result = sm.ols(formula="Red_flows_nav ~ nav_diff_1 + nav_diff_2 + nav_diff_3 + nav_diff_4", 
    data=df).fit()
print (result.summary())
print (result.rsquared, result.rsquared_adj)
# %%
result = sm.ols(formula="Red_flows_nav ~ nav_diff_1 + nav_diff_2 + nav_diff_3", 
    data=df).fit()
print (result.summary())
print (result.rsquared, result.rsquared_adj)
# %%
result = sm.ols(formula="Red_flows_nav ~ nav_diff_1 + nav_diff_2", 
    data=df).fit()
print (result.summary())
print (result.rsquared, result.rsquared_adj)
# %%
result = sm.ols(formula="Red_flows_nav ~ nav_diff_1 ", 
    data=df).fit()
print (result.summary())
print (result.rsquared, result.rsquared_adj)