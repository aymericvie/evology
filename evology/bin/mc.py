print(
    "Looking at different choices to represent the trading functions and how they impact the price, when we initialise at p=100"
)

initial_price = 100
wealth = 50_000_000 + 500_000 * initial_price
assets = 500_000

print("For ValNT = 100, reference")


def func1(asset_key, price):  # VI
    return (wealth / price) * np.tanh(np.log2(100) - np.log2(price)) - assets


def func2(asset_key, price):  # NT
    return (wealth / price) * np.tanh(np.log2(100) - np.log2(price)) - assets


def func3(asset_key, price):  # TF
    return (wealth / price) * np.tanh(0.5) - assets


functions = [func1, func2, func3]
new_price = solve(functions, initial_price)
print(new_price)

initial_price = 100
wealth = 50_000_000 + 500_000 * initial_price
assets = 500_000

print("For ValNT = 100, reference WITH LEVERAGE ")


def func1(asset_key, price):  # VI
    return (8 * wealth / price) * np.tanh(np.log2(100) - np.log2(price)) - assets


def func2(asset_key, price):  # NT
    return (wealth / price) * np.tanh(np.log2(100) - np.log2(price)) - assets


def func3(asset_key, price):  # TF
    return (wealth / price) * np.tanh(0.5) - assets


functions = [func1, func2, func3]
new_price = solve(functions, initial_price)
print(new_price)

print("For ValNT = 110, higher price as expected")


def func1(asset_key, price):  # VI
    return (wealth / price) * np.tanh(np.log2(100) - np.log2(price)) - assets


def func2(asset_key, price):  # NT
    return (wealth / price) * np.tanh(np.log2(110) - np.log2(price)) - assets


def func3(asset_key, price):  # TF
    return (wealth / price) * np.tanh(0.5) - assets


functions = [func1, func2, func3]
new_price = solve(functions, initial_price)
print(new_price)

print("For ValNT = 90, lower price as expected")


def func1(asset_key, price):  # VI
    return (wealth / price) * np.tanh(np.log2(100) - np.log2(price)) - assets


def func2(asset_key, price):  # NT
    return (wealth / price) * np.tanh(np.log2(90) - np.log2(price)) - assets


def func3(asset_key, price):  # TF
    return (wealth / price) * np.tanh(0.5) - assets


functions = [func1, func2, func3]
new_price = solve(functions, initial_price)
print(new_price)

print("With 0,5 inside tanh, price is higher")


def func1(asset_key, price):  # VI
    return (wealth / price) * np.tanh(np.log2(100) - np.log2(price) + 0.5) - assets


def func2(asset_key, price):  # NT
    return (wealth / price) * np.tanh(np.log2(90) - np.log2(price) + 0.5) - assets


def func3(asset_key, price):  # TF
    return (wealth / price) * np.tanh(0.5 + 0.5) - assets


functions = [func1, func2, func3]
new_price = solve(functions, initial_price)
print(new_price)

print("With 0,5 outside tanh, price is even higher")


def func1(asset_key, price):  # VI
    return (wealth / price) * (np.tanh(np.log2(100) - np.log2(price)) + 0.5) - assets


def func2(asset_key, price):  # NT
    return (wealth / price) * (np.tanh(np.log2(90) - np.log2(price)) + 0.5) - assets


def func3(asset_key, price):  # TF
    return (wealth / price) * (np.tanh(0.5) + 0.5) - assets


functions = [func1, func2, func3]
new_price = solve(functions, initial_price)
print(new_price)

print(
    "Question: MC is deterministic, which is good. Because now, does the 0,.5 choice gives unintended power to some strategies?"
)


""" 
print('----')
print('Lets study the resulting 10 day series')

print('VI 90, no 0.5')

new_price = 100
cash = 50_000_000
asset = 500_000

for i in range(10):
  wealth = cash + asset * new_price 

  def func1(asset_key, price): #VI
    return (wealth / price) * np.tanh(np.log2(100) - np.log2(price)) - assets
  def func2(asset_key, price): #NT
    return (wealth / price) * np.tanh(np.log2(90) - np.log2(price)) - assets 
  def func3(asset_key, price): #TF
    return (wealth / price) * np.tanh(0.5) - assets  

  functions = [func1, func2, func3]
  new_price = float(solve(functions, initial_price)[0])
  print(new_price)

print('With 0,5 inside tanh')

new_price = 100
cash = 50_000_000
asset = 500_000

for i in range(10):
  wealth = cash + asset * new_price 

  def func1(asset_key, price): #VI
    return (wealth / price) * np.tanh(np.log2(100) - np.log2(price) + 0.5) - assets
  def func2(asset_key, price): #NT
    return (wealth / price) * np.tanh(np.log2(90) - np.log2(price) + 0.5) - assets 
  def func3(asset_key, price): #TF
    return (wealth / price) * np.tanh(0.5 + 0.5) - assets  

  functions = [func1, func2, func3]
  new_price = float(solve(functions, initial_price)[0])
  print(new_price)

print('With 0,5 outside tanh')

new_price = 100
cash = 50_000_000
asset = 500_000

for i in range(10):
  wealth = cash + asset * new_price 

  def func1(asset_key, price): #VI
    return (wealth / price) * (np.tanh(np.log2(100) - np.log2(price)) + 0.5) - assets
  def func2(asset_key, price): #NT
    return (wealth / price) * (np.tanh(np.log2(90) - np.log2(price)) + 0.5) - assets 
  def func3(asset_key, price): #TF
    return (wealth / price) * (np.tanh(0.5) + 0.5) - assets  

  functions = [func1, func2, func3]
  new_price = float(solve(functions, initial_price)[0])
  print(new_price)
"""
"""
print('With 0,5 outside tanh, and VI/NT depending on previous price')
print('Then we get oscillations around two attractors')
print('Unless we adapt TF and then nothing happens')

new_price = 100
previous_price = 90
cash = 50_000_000
asset = 500_000

for i in range(10):
  wealth = cash + asset * new_price 

  LogPrev = np.log2(new_price)

  def func1(asset_key, price): #VI
    return (wealth / price) * (np.tanh(np.log2(100) - LogPrev) + 0.5) - assets
  def func2(asset_key, price): #NT
    return (wealth / price) * (np.tanh(np.log2(90) - LogPrev) + 0.5) - assets 
  def func3(asset_key, price): #TF
    return (wealth / price) * (np.tanh(np.log2(price) - LogPrev) + 0.5) - assets  

  functions = [func1, func2, func3]
  new_price = float(solve(functions, initial_price)[0])
  print(new_price)

print('Without and VI/NT depending on previous price')
print('Then we stabilise')

new_price = 100
previous_price = 90
cash = 50_000_000
asset = 500_000

for i in range(10):
  wealth = cash + asset * new_price 

  LogPrev = np.log2(new_price)

  def func1(asset_key, price): #VI
    return (wealth / price) * (np.tanh(np.log2(100) - LogPrev) + 0) - assets
  def func2(asset_key, price): #NT
    return (wealth / price) * (np.tanh(np.log2(90) - LogPrev) + 0) - assets 
  def func3(asset_key, price): #TF
    return (wealth / price) * (np.tanh(np.log2(price) - LogPrev) + 0) - assets  

  functions = [func1, func2, func3]
  new_price = float(solve(functions, initial_price)[0])
  print(new_price)

"""
"""
print('Y Y N with noise')

def func1(asset_key, price): #value investor
  return ((50_000_000 + 500_000 * float(initial_price)) / price ) * (np.tanh(np.log2(100) - np.log2(price) + 0.5)) - 500_000

ValNT = 100 + 10
print(ValNT)
def func2(asset_key, price): #noise trader
  return ((50_000_000 + 500_000 * float(initial_price)) / price) * (np.tanh(np.log2(ValNT)) - np.log2(price) + 0.5) - 500_000

def func3(asset_key, price): #trend follower
  return ((50_000_000 + 500_000 * float(initial_price)) / price ) * (np.tanh(0) + 0.5) - 500_000 


functions = [func1, func2, func3]
new_price = solve(functions, initial_price)
print(new_price)

print('Y Y N without noise')
initial_price = 100
def func1(asset_key, price): #value investor
  return ((50_000_000 + 500_000 * float(initial_price)) / price ) * (np.tanh(np.log2(100) - np.log2(price) + 0.5)) - 500_000

ValNT = 100
print(ValNT)
def func2(asset_key, price): #noise trader
  return ((50_000_000 + 500_000 * float(initial_price)) / price) * (np.tanh(np.log2(ValNT)) - np.log2(price) + 0.5) - 500_000

def func3(asset_key, price): #trend follower
  return ((50_000_000 + 500_000 * float(initial_price)) / price ) * (np.tanh(0) + 0.5) - 500_000 

  print('Y Y N with noise without 05')
initial_price = 100
def func1(asset_key, price): #value investor
  return ((50_000_000 + 500_000 * float(initial_price)) / price ) * (np.tanh(np.log2(100) - np.log2(price))) - 500_000

ValNT = 100 + 10
print(ValNT)
def func2(asset_key, price): #noise trader
  return ((50_000_000 + 500_000 * float(initial_price)) / price) * (np.tanh(np.log2(ValNT)) - np.log2(price)) - 500_000

def func3(asset_key, price): #trend follower
  return ((50_000_000 + 500_000 * float(initial_price)) / price ) * (np.tanh(0)) - 500_000 


functions = [func1, func2, func3]
new_price = solve(functions, initial_price)
print(new_price)

print('Y Y N without noise without 0.5')
initial_price = 100
def func1(asset_key, price): #value investor
  return ((50_000_000 + 500_000 * float(initial_price)) / price ) * (np.tanh(np.log2(100) - np.log2(price))) - 500_000

ValNT = 100
print(ValNT)
def func2(asset_key, price): #noise trader
  return ((50_000_000 + 500_000 * float(initial_price)) / price) * (np.tanh(np.log2(ValNT)) - np.log2(price)) - 500_000

def func3(asset_key, price): #trend follower
  return ((50_000_000 + 500_000 * float(initial_price)) / price ) * (np.tanh(0)) - 500_000 



functions = [func1, func2, func3]
new_price = solve(functions, initial_price)
print(new_price)

print('N N N ')
initial_price = 100
def func1(asset_key, price): #value investor
  return ((50_000_000 + 500_000 * float(initial_price)) / price ) * (np.tanh(np.log2(100 + random.normalvariate(0,1)) - np.log2(price)) + 0.5) - 500_000

def func2(asset_key, price): #noise trader
  return ((50_000_000 + 500_000 * float(initial_price)) / price) * (np.tanh(np.log2(100 + random.normalvariate(0,1)) - np.log2(price)) + 0.5) - 500_000

def func3(asset_key, price): #trend follower
  return ((50_000_000 + 500_000 * float(initial_price)) / price ) * (np.tanh(0) + 0.5) - 500_000 


functions = [func1, func2, func3]
new_price = solve(functions, initial_price)
print(new_price)

print('Y Y Y ')
initial_price = 100
import random 
def func1(asset_key, price): #value investor
  return ((50_000_000 + 500_000 * float(initial_price)) / price ) * (np.tanh(np.log2(100) - np.log2(price) + 0.5)) - 500_000

def func2(asset_key, price): #noise trader
  return ((50_000_000 + 500_000 * float(initial_price)) / price) * (np.tanh(np.log2(100 + random.normalvariate(0,1)) - np.log2(price) + 0.5)) - 500_000

def func3(asset_key, price): #trend follower
  return ((50_000_000 + 500_000 * float(initial_price)) / price ) * (np.tanh(0 + 0.5)) - 500_000 


functions = [func1, func2, func3]
new_price = solve(functions, initial_price)
print(new_price)
# print(func1(0, float(new_price[0])))
# print(func2(0, float(new_price[0])))
# print(func3(0, float(new_price[0])))
# for i in range(10):
#   new_price = solve(functions, float(new_price[0]))
#   print(new_price)


print('------')
print('VI and NT depending on last price')
initial_price = 100
def func1(asset_key, price): #value investor
  return ((50_000_000 + 500_000 * float(initial_price)) / price ) * (np.tanh(np.log2(100) - np.log2(initial_price) + 0.5)) - 500_000

def func2(asset_key, price): #noise trader
  return ((50_000_000 + 500_000 * float(initial_price)) / price) * (np.tanh(np.log2(100  + random.normalvariate(0,1)) - np.log2(initial_price) + 0.5)) - 500_000

def func3(asset_key, price): #trend follower
  return ((50_000_000 + 500_000 * float(initial_price)) / price ) * (np.tanh(0 + 0.5)) - 500_000 


functions = [func1, func2, func3]
new_price = solve(functions, initial_price)
print(new_price)
# print(func1(0, float(new_price[0])))
# print(func2(0, float(new_price[0])))
# print(func3(0, float(new_price[0])))
# for i in range(10):
#   new_price = solve(functions, float(new_price[0]))
#   print(new_price)

print('------')
print('Removing 0.5')
initial_price = 100
def func4(asset_key, price): #value investor
  return ((50_000_000 + 500_000 * float(initial_price)) / price ) * (np.tanh(np.log2(100) - np.log2(initial_price))) - 500_000

def func5(asset_key, price): #noise trader
  return ((50_000_000 + 500_000 * float(initial_price)) / price) * (np.tanh(np.log2(100  + random.normalvariate(0,1)) - np.log2(initial_price))) - 500_000

def func6(asset_key, price): #trend follower
  return ((50_000_000 + 500_000 * float(initial_price)) / price ) * (np.tanh(0)) - 500_000 


functions = [func4, func5, func6]
new_price = solve(functions, initial_price)
print(new_price)
"""


initial_price = 100
wealth = 50_000_000 + 500_000 * initial_price
assets = 500_000
assets = 400_000


print("For ValNT = 100, reference")


def func1(asset_key, price):  # VI
    return ((60_000_000 + assets * initial_price) / price) * np.tanh(
        np.log2(100) - np.log2(price)
    ) - assets


def func2(asset_key, price):  # NT
    return ((60_000_000 + assets * initial_price) / price) * np.tanh(
        np.log2(100) - np.log2(price)
    ) - assets


def func3(asset_key, price):  # TF
    return ((60_000_000 + assets * initial_price) / price) * np.tanh(0.5) - assets


functions = [func1, func2, func3]
new_price = solve(functions, initial_price)
print(new_price)

assets = 500_000
print("For ValNT = 100, reference")


def func1(asset_key, price):  # VI
    return ((50_000_000 + assets * initial_price) / price) * np.tanh(
        np.log2(100) - np.log2(price)
    ) - assets


def func2(asset_key, price):  # NT
    return ((50_000_000 + assets * initial_price) / price) * np.tanh(
        np.log2(100) - np.log2(price)
    ) - assets


def func3(asset_key, price):  # TF
    return ((50_000_000 + assets * initial_price) / price) * np.tanh(0.5) - assets


functions = [func1, func2, func3]
new_price = solve(functions, initial_price)
print(new_price)
