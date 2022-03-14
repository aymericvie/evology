import numpy as np
import pandas as pd

""" Price """
# Data type for price: (0, [USD(102.55)])
P = []
with open(
    "data/replication/sample2/output/volatility_illustration/prices.txt", "r"
) as content_file:
    for l in content_file.readlines():
        P.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
prices = np.array(P)[offset_prices:-2]
print(prices)

""" Dividends """
# Data type for div: (0, 0.003983)
D = []
with open(
    "data/replication/sample2/output/volatility_illustration/0_dividend.txt", "r"
) as content_file:
    for l in content_file.readlines():
        D.append(float(l.split(",")[1].split(")")[0]))
dividends = np.array(D)[offset_prices:-2]
print(dividends)

""" Volume """  # Data type (0, [961837])
V = []
with open(
    "data/replication/sample2/output/volatility_illustration/volumes.txt", "r"
) as content_file:
    for l in content_file.readlines():
        V.append(int(l.split(", [")[1].split("])")[0]))
volumes = np.array(V)[offset_prices:-2]
print(volumes)

""" Noise trader """
# Cash (0, USD(10000785849.41))
NTC = []
with open(
    "data/replication/sample2/output/volatility_illustration/_2__cash.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTC.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
nt_cash = np.array(NTC)[offset_prices:-2]
print(nt_cash)

# Lending (0, USD(0.00))
NTS = []
with open(
    "data/replication/sample2/output/volatility_illustration/_2__lending.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTS.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
nt_lending = np.array(NTS)[offset_prices:-2]
print(nt_lending)

# Loans (0, USD(-9960782706.02))
NTL = []
with open(
    "data/replication/sample2/output/volatility_illustration/_2__loans.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTL.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
nt_loan = np.array(NTL)[offset_prices:-2]
print(nt_loan)

# Net asset value (0, USD(80003143.39))
NTA = []
with open(
    "data/replication/sample2/output/volatility_illustration/_2__net_asset_value.txt",
    "r",
) as content_file:
    for l in content_file.readlines():
        NTA.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
nt_nav = np.array(NTA)[offset_prices:-2]
print(nt_nav)

# Pnl (0, USD(3143.39))
NTP = []
with open(
    "data/replication/sample2/output/volatility_illustration/_2__pnl.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTP.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
nt_pnl = np.array(NTP)[offset_prices:-2]
print(nt_pnl)

# Signal (2, 101.885)
NTS = []
with open(
    "data/replication/sample2/output/volatility_illustration/_2__signal.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTS.append(float(l.split(",")[1].split(")")[0]))
nt_signal = np.array(NTS)[offset_prices:]
print(nt_signal)

# Stocks (0, USD(40000000.00))
NTS = []
with open(
    "data/replication/sample2/output/volatility_illustration/_2__stocks.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTS.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
nt_stock = np.array(NTS)[offset_prices:-2]
print(nt_stock)

print("-------------")

""" Value Investor """
# Cash (0, USD(10000785849.41))
NTC = []
with open(
    "data/replication/sample2/output/volatility_illustration/_3__cash.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTC.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
vi_cash = np.array(NTC)[offset_prices:-2]
print(vi_cash)

# Lending (0, USD(0.00))
NTS = []
with open(
    "data/replication/sample2/output/volatility_illustration/_3__lending.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTS.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
vi_lending = np.array(NTS)[offset_prices:-2]
print(vi_lending)

# Loans (0, USD(-9960782706.02))
NTL = []
with open(
    "data/replication/sample2/output/volatility_illustration/_3__loans.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTL.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
vi_loan = np.array(NTL)[offset_prices:-2]
print(vi_loan)

# Net asset value (0, USD(80003143.39))
NTA = []
with open(
    "data/replication/sample2/output/volatility_illustration/_3__net_asset_value.txt",
    "r",
) as content_file:
    for l in content_file.readlines():
        NTA.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
vi_nav = np.array(NTA)[offset_prices:-2]
print(vi_nav)

# Pnl (0, USD(3143.39))
NTP = []
with open(
    "data/replication/sample2/output/volatility_illustration/_3__pnl.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTP.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
vi_pnl = np.array(NTP)[offset_prices:-2]
print(vi_pnl)

# Signal (2, 101.885)
NTS = []
with open(
    "data/replication/sample2/output/volatility_illustration/_3__signal.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTS.append(float(l.split(",")[1].split(")")[0]))
vi_signal = np.array(NTS)[offset_prices:]
print(vi_signal)

# Stocks (0, USD(40000000.00))
NTS = []
with open(
    "data/replication/sample2/output/volatility_illustration/_3__stocks.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTS.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
vi_stock = np.array(NTS)[offset_prices:-2]
print(vi_stock)

print("-------------")

""" Noise trader """
# Cash (0, USD(10000785849.41))
NTC = []
with open(
    "data/replication/sample2/output/volatility_illustration/_4__cash.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTC.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
tf_cash = np.array(NTC)[offset_prices:-2]
print(tf_cash)

# Lending (0, USD(0.00))
NTS = []
with open(
    "data/replication/sample2/output/volatility_illustration/_4__lending.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTS.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
tf_lending = np.array(NTS)[offset_prices:-2]
print(tf_lending)

# Loans (0, USD(-9960782706.02))
NTL = []
with open(
    "data/replication/sample2/output/volatility_illustration/_4__loans.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTL.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
tf_loan = np.array(NTL)[offset_prices:-2]
print(tf_loan)

# Net asset value (0, USD(80003143.39))
NTA = []
with open(
    "data/replication/sample2/output/volatility_illustration/_4__net_asset_value.txt",
    "r",
) as content_file:
    for l in content_file.readlines():
        NTA.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
tf_nav = np.array(NTA)[offset_prices:-2]
print(tf_nav)

# Pnl (0, USD(3143.39))
NTP = []
with open(
    "data/replication/sample2/output/volatility_illustration/_4__pnl.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTP.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
tf_pnl = np.array(NTP)[offset_prices:-2]
print(tf_pnl)

# Signal (2, 101.885)
NTS = []
with open(
    "data/replication/sample2/output/volatility_illustration/_4__signal.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTS.append(float(l.split(",")[1].split(")")[0]))
tf_signal = np.array(NTS)[offset_prices:-2]
print(tf_signal)

# Stocks (0, USD(40000000.00))
NTS = []
with open(
    "data/replication/sample2/output/volatility_illustration/_4__stocks.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTS.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
tf_stock = np.array(NTS)[offset_prices:-2]
print(tf_stock)


def create_df():
    df = pd.DataFrame(
        columns=[
            "Price",
            "Dividends",
            "Volume",
            "NT_cash",
            "NT_lending",
            "NT_loan",
            "NT_nav",
            "NT_pnl",
            "NT_signal",
            "NT_stocks",
            "VI_cash",
            "VI_lending",
            "VI_loan",
            "VI_nav",
            "VI_pnl",
            "VI_signal",
            "VI_stocks",
            "TF_cash",
            "TF_lending",
            "TF_loan",
            "TF_nav",
            "TF_pnl",
            "TF_signal",
            "TF_stocks",
        ]
    )
    return df


df = create_df()


df["Price"] = prices
df["Dividends"] = dividends
df["Volume"] = volumes

df["NT_cash"] = nt_cash
df["NT_lending"] = nt_lending
df["NT_loan"] = nt_loan
df["NT_nav"] = nt_nav
df["NT_pnl"] = nt_pnl
df["NT_signal"] = nt_signal
df["NT_stocks"] = nt_stock

df["NT_cash"] = nt_cash
df["NT_lending"] = nt_lending
df["NT_loan"] = nt_loan
df["NT_nav"] = nt_nav
df["NT_pnl"] = nt_pnl
df["NT_signal"] = nt_signal
df["NT_stocks"] = nt_stock

df["VI_cash"] = vi_cash
df["VI_lending"] = vi_lending
df["VI_loan"] = vi_loan
df["VI_nav"] = vi_nav
df["VI_pnl"] = vi_pnl
df["VI_signal"] = vi_signal
df["VI_stocks"] = vi_stock

df["TF_cash"] = tf_cash
df["TF_lending"] = tf_lending
df["TF_loan"] = tf_loan
df["TF_nav"] = tf_nav
df["TF_pnl"] = tf_pnl
df["TF_signal"] = tf_signal
df["TF_stocks"] = tf_stock

print(df)
df.to_csv("data/replication_data_sample2.csv")


#############

""" Price """
# Data type for price: (0, [USD(102.55)])
P = []
with open(
    "data/replication/sample1/output/volatility_illustration/prices.txt", "r"
) as content_file:
    for l in content_file.readlines():
        P.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
prices = np.array(P)[offset_prices:-2]
print(prices)

""" Dividends """
# Data type for div: (0, 0.003983)
D = []
with open(
    "data/replication/sample1/output/volatility_illustration/0_dividend.txt", "r"
) as content_file:
    for l in content_file.readlines():
        D.append(float(l.split(",")[1].split(")")[0]))
dividends = np.array(D)[offset_prices:-2]
print(dividends)

""" Volume """  # Data type (0, [961837])
V = []
with open(
    "data/replication/sample1/output/volatility_illustration/volumes.txt", "r"
) as content_file:
    for l in content_file.readlines():
        V.append(int(l.split(", [")[1].split("])")[0]))
volumes = np.array(V)[offset_prices:-2]
print(volumes)

""" Noise trader """
# Cash (0, USD(10000785849.41))
NTC = []
with open(
    "data/replication/sample1/output/volatility_illustration/_2__cash.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTC.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
nt_cash = np.array(NTC)[offset_prices:-2]
print(nt_cash)

# Lending (0, USD(0.00))
NTS = []
with open(
    "data/replication/sample1/output/volatility_illustration/_2__lending.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTS.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
nt_lending = np.array(NTS)[offset_prices:-2]
print(nt_lending)

# Loans (0, USD(-9960782706.02))
NTL = []
with open(
    "data/replication/sample1/output/volatility_illustration/_2__loans.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTL.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
nt_loan = np.array(NTL)[offset_prices:-2]
print(nt_loan)

# Net asset value (0, USD(80003143.39))
NTA = []
with open(
    "data/replication/sample1/output/volatility_illustration/_2__net_asset_value.txt",
    "r",
) as content_file:
    for l in content_file.readlines():
        NTA.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
nt_nav = np.array(NTA)[offset_prices:-2]
print(nt_nav)

# Pnl (0, USD(3143.39))
NTP = []
with open(
    "data/replication/sample1/output/volatility_illustration/_2__pnl.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTP.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
nt_pnl = np.array(NTP)[offset_prices:-2]
print(nt_pnl)

# Signal (2, 101.885)
NTS = []
with open(
    "data/replication/sample1/output/volatility_illustration/_2__signal.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTS.append(float(l.split(",")[1].split(")")[0]))
nt_signal = np.array(NTS)[offset_prices:]
print(nt_signal)

# Stocks (0, USD(40000000.00))
NTS = []
with open(
    "data/replication/sample1/output/volatility_illustration/_2__stocks.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTS.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
nt_stock = np.array(NTS)[offset_prices:-2]
print(nt_stock)

print("-------------")

""" Value Investor """
# Cash (0, USD(10000785849.41))
NTC = []
with open(
    "data/replication/sample1/output/volatility_illustration/_3__cash.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTC.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
vi_cash = np.array(NTC)[offset_prices:-2]
print(vi_cash)

# Lending (0, USD(0.00))
NTS = []
with open(
    "data/replication/sample1/output/volatility_illustration/_3__lending.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTS.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
vi_lending = np.array(NTS)[offset_prices:-2]
print(vi_lending)

# Loans (0, USD(-9960782706.02))
NTL = []
with open(
    "data/replication/sample1/output/volatility_illustration/_3__loans.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTL.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
vi_loan = np.array(NTL)[offset_prices:-2]
print(vi_loan)

# Net asset value (0, USD(80003143.39))
NTA = []
with open(
    "data/replication/sample1/output/volatility_illustration/_3__net_asset_value.txt",
    "r",
) as content_file:
    for l in content_file.readlines():
        NTA.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
vi_nav = np.array(NTA)[offset_prices:-2]
print(vi_nav)

# Pnl (0, USD(3143.39))
NTP = []
with open(
    "data/replication/sample1/output/volatility_illustration/_3__pnl.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTP.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
vi_pnl = np.array(NTP)[offset_prices:-2]
print(vi_pnl)

# Signal (2, 101.885)
NTS = []
with open(
    "data/replication/sample1/output/volatility_illustration/_3__signal.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTS.append(float(l.split(",")[1].split(")")[0]))
vi_signal = np.array(NTS)[offset_prices:]
print(vi_signal)

# Stocks (0, USD(40000000.00))
NTS = []
with open(
    "data/replication/sample1/output/volatility_illustration/_3__stocks.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTS.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
vi_stock = np.array(NTS)[offset_prices:-2]
print(vi_stock)

print("-------------")

""" Noise trader """
# Cash (0, USD(10000785849.41))
NTC = []
with open(
    "data/replication/sample1/output/volatility_illustration/_4__cash.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTC.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
tf_cash = np.array(NTC)[offset_prices:-2]
print(tf_cash)

# Lending (0, USD(0.00))
NTS = []
with open(
    "data/replication/sample1/output/volatility_illustration/_4__lending.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTS.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
tf_lending = np.array(NTS)[offset_prices:-2]
print(tf_lending)

# Loans (0, USD(-9960782706.02))
NTL = []
with open(
    "data/replication/sample1/output/volatility_illustration/_4__loans.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTL.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
tf_loan = np.array(NTL)[offset_prices:-2]
print(tf_loan)

# Net asset value (0, USD(80003143.39))
NTA = []
with open(
    "data/replication/sample1/output/volatility_illustration/_4__net_asset_value.txt",
    "r",
) as content_file:
    for l in content_file.readlines():
        NTA.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
tf_nav = np.array(NTA)[offset_prices:-2]
print(tf_nav)

# Pnl (0, USD(3143.39))
NTP = []
with open(
    "data/replication/sample1/output/volatility_illustration/_4__pnl.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTP.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
tf_pnl = np.array(NTP)[offset_prices:-2]
print(tf_pnl)

# Signal (2, 101.885)
NTS = []
with open(
    "data/replication/sample1/output/volatility_illustration/_4__signal.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTS.append(float(l.split(",")[1].split(")")[0]))
tf_signal = np.array(NTS)[offset_prices:-2]
print(tf_signal)

# Stocks (0, USD(40000000.00))
NTS = []
with open(
    "data/replication/sample1/output/volatility_illustration/_4__stocks.txt", "r"
) as content_file:
    for l in content_file.readlines():
        NTS.append(float(l.split("USD(")[1].split(")")[0]))
offset_prices = 0
tf_stock = np.array(NTS)[offset_prices:-2]
print(tf_stock)


def create_df():
    df = pd.DataFrame(
        columns=[
            "Price",
            "Dividends",
            "Volume",
            "NT_cash",
            "NT_lending",
            "NT_loan",
            "NT_nav",
            "NT_pnl",
            "NT_signal",
            "NT_stocks",
            "VI_cash",
            "VI_lending",
            "VI_loan",
            "VI_nav",
            "VI_pnl",
            "VI_signal",
            "VI_stocks",
            "TF_cash",
            "TF_lending",
            "TF_loan",
            "TF_nav",
            "TF_pnl",
            "TF_signal",
            "TF_stocks",
        ]
    )
    return df


df = create_df()


df["Price"] = prices
df["Dividends"] = dividends
df["Volume"] = volumes

df["NT_cash"] = nt_cash
df["NT_lending"] = nt_lending
df["NT_loan"] = nt_loan
df["NT_nav"] = nt_nav
df["NT_pnl"] = nt_pnl
df["NT_signal"] = nt_signal
df["NT_stocks"] = nt_stock

df["NT_cash"] = nt_cash
df["NT_lending"] = nt_lending
df["NT_loan"] = nt_loan
df["NT_nav"] = nt_nav
df["NT_pnl"] = nt_pnl
df["NT_signal"] = nt_signal
df["NT_stocks"] = nt_stock

df["VI_cash"] = vi_cash
df["VI_lending"] = vi_lending
df["VI_loan"] = vi_loan
df["VI_nav"] = vi_nav
df["VI_pnl"] = vi_pnl
df["VI_signal"] = vi_signal
df["VI_stocks"] = vi_stock

df["TF_cash"] = tf_cash
df["TF_lending"] = tf_lending
df["TF_loan"] = tf_loan
df["TF_nav"] = tf_nav
df["TF_pnl"] = tf_pnl
df["TF_signal"] = tf_signal
df["TF_stocks"] = tf_stock

print(df)
df.to_csv("data/replication_data_sample1.csv")
