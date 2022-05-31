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

path = '/Users/aymericvie/Documents/GitHub/evology/evology/data/replication/flow_data_processed.csv'
df = pd.read_csv(path)

# %%

