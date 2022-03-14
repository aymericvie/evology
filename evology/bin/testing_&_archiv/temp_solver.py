import numpy as np

"""
Here is a simple optimisation solver for the market clearing algorithm. 
We minimise the squared of aggregate excess demand, under the constraint of
a Limit-Up-Limit-Down (LU-LD) circuit breaker, which limits prices to 
[LD*p(t-1), LU*p(t-1)], with LD=1/2 and LU = 2


The solver uses the LEAP package: https://github.com/AureumChaos/LEAP
It is a package focusing on evolutionary algorithms, that has an amazing 
ea_solve function that ... solves a real valued function.
"""

from leap_ec import Individual, Representation
from leap_ec import ops, probe
from leap_ec.algorithm import generational_ea
from leap_ec.problem import FunctionProblem
from leap_ec.real_rep import create_real_vector
from leap_ec.real_rep.ops import mutate_gaussian

"""Provides a simple, top-level interfact that optimizes a real-valued
function using a simple generational EA.
:param function: the function to optimize; should take lists of real
    numbers as input and return a float fitness value
:param [(float, float)] bounds: a list of (min, max) bounds to define the
    search space
:param int generations: the number of generations to run for
:param int pop_size: the population size
:param float mutation_std: the width of the mutation distribution
:param bool maximize: whether to maximize the function (else minimize)
:param bool viz: whether to display a live best-of-generation plot
:param bool hard_bounds: if True, bounds are enforced at all times during
evolution; otherwise they are only used to initialize the population. """


def ea_solve_noverbose(
    function,
    bounds,
    generations=100,
    pop_size=2,
    mutation_std=1.0,
    maximize=False,
    viz=False,
    viz_ylim=(0, 1),
    hard_bounds=True,
):

    if hard_bounds:
        mutation_op = mutate_gaussian(
            std=mutation_std, hard_bounds=bounds, expected_num_mutations="isotropic"
        )
    else:
        mutation_op = mutate_gaussian(
            std=mutation_std, expected_num_mutations="isotropic"
        )
    pipeline = [
        ops.tournament_selection,
        ops.clone,
        mutation_op,
        ops.uniform_crossover(p_swap=0.4),
        ops.evaluate,
        ops.pool(size=pop_size),
    ]
    ea = generational_ea(
        max_generations=generations,
        pop_size=pop_size,
        problem=FunctionProblem(function, maximize),
        representation=Representation(
            individual_cls=Individual, initialize=create_real_vector(bounds=bounds)
        ),
        pipeline=pipeline,
    )
    best_genome = None
    # print('generation, bsf')
    for g, ind in ea:
        # print(f"{g}, {ind.fitness}")
        best_genome = ind.genome
    return best_genome


""" Example """


def f(x):
    return sum(x) ** 2


best_genome = ea_solve_noverbose(
    f,
    bounds=[(1, 10)],
    generations=50,
    pop_size=500,
    mutation_std=0.1,
    hard_bounds=True,
    maximize=False,
)
print(best_genome)
