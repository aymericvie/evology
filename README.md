# Evolutionary market ecology

##### Testing (master)

![Learning](https://github.com/aymericvie/evology/actions/workflows/learning_runs.yml/badge.svg?branch=master)
![No_Learning](https://github.com/aymericvie/evology/actions/workflows/no_learning_runs.yml/badge.svg?branch=master)
![Deterministic](https://github.com/aymericvie/evology/actions/workflows/deterministic.yml/badge.svg?branch=master)


## Description

We implement an artificial stock market with adaptive trading strategies: an evolutionary market ecology. On a simplified market with assets and cash, we apply various learning algorithms (imitation, Genetic Algorithm, Genetic Programming, ...) to model various means of financial learning. We estimate interactions between trading strategies and market convergence dynamics in these adaptive cases.

## How to use

First, to obtain the libraries we need, run ```setup.py```.

## Credits

Code developed by Aymeric Vié wth support from Maarten Scholl and Louis Vié. This research has been supported by the EPSRC Centre for Doctoral Training in Mathematics of Random Systems: Analysis, Modelling and Simulation (EP/S023925/1)

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
    1. Compute wealth as a function of last period price
    2. Determine excess demand functions
    3. Clear markets and compute mismatch
    4. Compute excess demand values
    5. Compute wealth
    6. Apply excess demand orders
    7. Apply earnings
    8. Update margin, clear debt, recompute wealth
    9. Replace insolvent traders
    10. Compute fitness
    11. Execute stratgy evolution
    12. Update the results data with the period's numbers


#### Code formatting
We use ```black``` to auto-format the code. After installing with ```pip install black```, go the the ```evology``` folder and run ```black evology``` to auto-format the full folder.

