# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

# %%
x_points = [
    -0.18,
    -0.12,
    -0.09,
    -0.07,
    -0.06,
    -0.05,
    -0.04,
    -0.03,
    -0.02,
    -0.01,
    0.005,
    0.015,
    0.025,
    0.035,
    0.045,
    0.065,
    0.08,
    0.1,
    0.13,
    0.22
]

y_points = [ 
    -0.021,
    -0.013,
    -0.011,
    -0.009,
    -0.008,
    -0.0065,
    -0.005,
    -0.0045,
    -0.003,
    -0.002,
    -0.0015,
    -0.0005,
    0.00,
    0.002,
    0.0035,
    0.006,
    0.008,
    0.009,
    0.0135,
    0.0235,
]

print([len(x_points), len(y_points)])
df = pd.DataFrame()
df['Return'] = x_points 
df['Flow'] = y_points 

# %%
sns.regplot(x="Return", y="Flow", data=df)
plt.show()

# %%
X = df[['Return']] 
Y = df['Flow']

X = sm.add_constant(X) # adding a constant

model = sm.OLS(Y, X).fit()
predictions = model.predict(X) 

print_model = model.summary()
print(print_model)

# %%

'''
Constant is -0.0012
Return coeff is 0.1089
All signficantm p=0.00.


'''
