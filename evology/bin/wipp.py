''' estimated_daily_div_growth = (
    (1 + DIVIDEND_GROWTH_RATE_G) ** (1 / TRADING_DAYS)
) - 1
numerator = (1 + estimated_daily_div_growth) * dividend
for ind in pop:
    t = ind.type_as_int
    if t==1:
        denuminator = (
            1.0 + (AnnualInterestRate + ind.strategy) - DIVIDEND_GROWTH_RATE_G
        ) ** (1.0 / 252.0) - 1.0
        fval = numerator / denuminator
        ind[0] = fval # TODO This might be something to change later on
        if fval < 0:
            warnings.warn("Negative fval found in update_fval.")
        if fval == np.inf:
            raise ValueError('Infinite FVal.')
return pop
'''

g = 0.01
r = 0.01
rq = 0.01
dividend = 0.003983

gd = ((1+g) ** (1/252)) - 1
print(gd)
print(((1+gd) ** 252) - 1)

rd = (1 + r + rq - g) ** (1/252) - 1
print(rd)

# current way of computing
def fval1():

    return fval