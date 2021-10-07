# Evolutionary market ecology

## Description

We implement an artificial stock market with adaptive trading strategies: an evolutionary market ecology. On a simplified market with assets and cash, we apply various learning algorithms (imitation, Genetic Algorithm, Genetic Programming, ...) to model various means of financial learning. We estimate interactions between trading strategies and market convergence dynamics in these adaptive cases.

## How to use

First, to obtain the packages we need, run ```system.py```.

## Credits

Code developed by Aymeric Vié wth support from Maarten Scholl. This research has been supported by the EPSRC Centre for Doctoral Training in Mathematics of Random Systems: Analysis, Modelling and Simulation (EP/S023925/1)

## Documentation

### Code

#### main.py

* Compute trading signal values
* Determine excess demand functions
* Execute market clearing
* Execute excess demand orders
* Apply earnings (dividends, interest, reinvestment)
* Compute fitness and apply strategy evolution

In more detail:
1. Initialise important variables (generation, price, dividend)
2. Create the population
3. Iteration loop
    1. Determine excess demand functions
    2. Clear markets and compute mismatch
    3. Compute excess demand values
    4. Compute wealth
    5. Apply excess demand orders
    6. Apply earnings
    7. Update margin, clear debt, recompute wealth
    8. Replace insolvent traders
    9. Compute fitness
    10. Execute stratgy evolution
    11. Update the results data with the period's numbers

