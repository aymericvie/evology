# Evolutionary market ecology

##### Testing (master)

![Learning](https://github.com/aymericvie/evology/actions/workflows/learning_runs.yml/badge.svg?branch=master)
![No_Learning](https://github.com/aymericvie/evology/actions/workflows/no_learning_runs.yml/badge.svg?branch=master)
![Deterministic](https://github.com/aymericvie/evology/actions/workflows/deterministic.yml/badge.svg?branch=master)


## Description

We implement an artificial stock market with adaptive trading strategies: an evolutionary market ecology. On a simplified market with assets and cash, we apply various learning algorithms (imitation, Genetic Algorithm, Genetic Programming, ...) to model various means of financial learning. 

## Credits and funding

Code developed by Aymeric Vié with support from Doyne Farmer, Maarten Scholl and Louis Vié. This research has been supported by the EPSRC Centre for Doctoral Training in Mathematics of Random Systems: Analysis, Modelling and Simulation (EP/S023925/1)

## Documentation

### How to use

First, to install the libraries we need, run ```setup.py```.

### Code achitecture 

```main.py``` is the principal piece of the simulation. It initialises the simulation and describes the actions executed at each period.

A. Initialisation
* ```generation``` is the current time period of the model.
* ```CurrentPrice``` is the current price
* ```dividend``` is the current dividend
* ```spoils``` represents the asset shares under liquidation
* ```results``` is a numpy array that will contain our results
* ```price_history``` and ```dividend_history``` contain histories of price and dividends
* ```replace``` is a dummy variable specifying whether we need to apply hypermutation

B. Population creation
We create a population of size ```POPULATION_SIZE``` and initial wealth distribution ```wealth_coordinates```. The population of strategies is defined in the strategy ```space```. \\

At every period, the following actions are executed:

1. Population reset 
In some circumstances, we want to reset the population, i.e. setting the population back to its creation state. 

2. Hypermutation 
If a fund's wealth is negative, this fund is insolvent and must be removed. Its assets go to liquidation with ```spoils``` and the wealthiest fund splits to fill the vacant spot(s). If all the funds are simultaneously insolvent, the simulation stops.

3. Strategy evolution 
First, funds' fitness is computed as an exponential moving average of profits. Next, depending on this fitness, funds' strategies may evolve. The learning algorithm used depends on the strategy space selected.

4. Market decisions
The funds observe market variables (price, fundamental value, random process) to decide their trading signal values for the period. 
First, we recompute fund wealth to use its latest values. Second, we update the fundamental value observed by the value investors. Then, we compute the noise process values for noise traders. We can then compute the trading signal values (TSV) of all agents and update their individual excess demand functions (EDF).


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

