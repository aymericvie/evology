# %%
# Packages and data loading

import pandas as pd 
from scipy.special import boxcox1p
from sklearn.preprocessing import PowerTransformer
from scipy import stats
import statsmodels.formula.api as sm
from statsmodels.stats.stattools import jarque_bera
from statsmodels.graphics.gofplots import qqplot
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

path = '/Users/aymericvie/Documents/GitHub/evology/evology/data/replication/flow_data_processed.csv'
df = pd.read_csv(path)
del df['Unnamed: 0']

print(df.columns)

#%%
# Additional clearing

# Remove the funds for which we don't even have lag1 returns
df = df.dropna(subset=['nav_diff_1'])

# Remove funds with excessive flows
df = df[(df["Red_flows_nav"] >= -100) & (df["Red_flows_nav"] <= 100)]

# Remove excessive returns (300% in abs in a quarter)
df = df[(df["nav_diff_1"] >= -3) & (df["nav_diff_1"] <= 3)]
df = df[(df["nav_diff_2"] >= -3) & (df["nav_diff_2"] <= 3)]
df = df[(df["nav_diff_3"] >= -3) & (df["nav_diff_3"] <= 3)]
df = df[(df["nav_diff_4"] >= -3) & (df["nav_diff_4"] <= 3)]
df = df[(df["nav_diff_5"] >= -3) & (df["nav_diff_5"] <= 3)]
df = df[(df["nav_diff_6"] >= -3) & (df["nav_diff_6"] <= 3)]
df = df[(df["nav_diff_7"] >= -3) & (df["nav_diff_7"] <= 3)]
df = df[(df["nav_diff_8"] >= -3) & (df["nav_diff_8"] <= 3)]


# %%
def analysis(results):
    # Print summary
    print(ols_results.summary())

    # Test for normality of residuals
    name = ['Jarque-Bera', 'Chi^2 two-tail prob.', 'Skew', 'Kurtosis']
    test = jarque_bera(results.resid)
    print(name)
    print(test)

    # Show QQ plot of residuals
    fig = qqplot(results.resid)
    plt.show()
# %%
# Basic linear regression

ols_model = sm.ols(
    formula="Red_flows_nav ~ nav_diff_1 + nav_diff_2 + nav_diff_3 + nav_diff_4 + nav_diff_5 + nav_diff_6 + nav_diff_7 + nav_diff_8", 
    data=df)
ols_results = ols_model.fit()
analysis(ols_results)

'''
R2 is quite high, but coefficients are fairly extreme. 
Issue: nowhere near normally distributed residuals.
There are various ways we can work on this:

0. Investigate residuals (Done and applied)
1. Checking for outliers in the data (Done and applied)
2. Normalising (boxcox) '''


# %%
# testing for heteroskedasticity
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.diagnostic import het_white

white_test = het_white(ols_results.resid,  ols_results.model.exog)

labels = ['LM Statistic', 'LM-Test p-value', 'F-Statistic', 'F-Test p-value']

print(dict(zip(labels, white_test)))
# We have heteroskedasticity. 

# %%
ols_model = sm.ols(
    formula="Red_flows_nav ~ nav_diff_1 + nav_diff_2 + nav_diff_3 + nav_diff_4 + nav_diff_5 + nav_diff_6 + nav_diff_7 + nav_diff_8", 
    data=df)
ols_results = ols_model.fit(cov_type='HC1')
analysis(ols_results)
# %%
# Trying with quantiles

highq = 0.99
lowq = 0.01

df2 = df.copy()
df2 = df2[(df2["Red_flows_nav"] <= df["Red_flows_nav"].quantile(highq)) & (df2["Red_flows_nav"] >= df["Red_flows_nav"].quantile(lowq))]
df2 = df2[(df2["nav_diff_1"] <= df["nav_diff_1"].quantile(highq)) & (df2["nav_diff_1"] >= df["nav_diff_1"].quantile(lowq))]
df2 = df2[(df2["nav_diff_2"] <= df["nav_diff_2"].quantile(highq)) & (df2["nav_diff_2"] >= df["nav_diff_2"].quantile(lowq))]
df2 = df2[(df2["nav_diff_3"] <= df["nav_diff_3"].quantile(highq)) & (df2["nav_diff_3"] >= df["nav_diff_3"].quantile(lowq))]
df2 = df2[(df2["nav_diff_4"] <= df["nav_diff_4"].quantile(highq)) & (df2["nav_diff_4"] >= df["nav_diff_4"].quantile(lowq))]
df2 = df2[(df2["nav_diff_5"] <= df["nav_diff_5"].quantile(highq)) & (df2["nav_diff_5"] >= df["nav_diff_5"].quantile(lowq))]
df2 = df2[(df2["nav_diff_6"] <= df["nav_diff_6"].quantile(highq)) & (df2["nav_diff_6"] >= df["nav_diff_6"].quantile(lowq))]
df2 = df2[(df2["nav_diff_7"] <= df["nav_diff_7"].quantile(highq)) & (df2["nav_diff_7"] >= df["nav_diff_7"].quantile(lowq))]
df2 = df2[(df2["nav_diff_8"] <= df["nav_diff_8"].quantile(highq)) & (df2["nav_diff_8"] >= df["nav_diff_8"].quantile(lowq))]

ols_model = sm.ols(
    formula="Red_flows_nav ~ nav_diff_1 + nav_diff_2 + nav_diff_3 + nav_diff_4 + nav_diff_5 + nav_diff_6 + nav_diff_7 + nav_diff_8", 
    data=df2)
ols_results = ols_model.fit(cov_type='HC1')
analysis(ols_results)

# %%
ols_model = sm.ols(
    formula="Red_flows_nav ~ nav_diff_1", 
    data=df2)
ols_results = ols_model.fit(cov_type='HC1')
analysis(ols_results)
# %%
