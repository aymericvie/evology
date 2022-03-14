# Imports
import matplotlib
import matplotlib.pyplot as plt
import sys

print(sys.path)
sys.path.insert(
    0, r"C:\Users\aymer\OneDrive\Research\2021_MarketEcology\EvoMarketEcology"
)
from code import market

# Results section

# Market validation

history1 = market.dividend_series(1 * 252)
history10 = market.dividend_series(10 * 252)
history100 = market.dividend_series(100 * 252)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 5), sharey=True)
fig.suptitle("Time series of dividends (single run)")
ax1.plot(history1)
ax1.set_title("1 year")
ax1.set_xlabel("Time (days)")
ax1.set_ylabel("Daily dividend amount")
ax2.plot(history10)
ax2.set_title("10 years")
ax2.set_xlabel("Time (days)")
ax3.plot(history100)
ax3.set_title("100 years")
ax3.set_xlabel("Time (days)")
plt.savefig("figures/dividend_series.png", dpi=300)
plt.show()
