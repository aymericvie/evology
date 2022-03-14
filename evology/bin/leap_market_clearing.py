from parameters import *
import numpy as np

"""
Here is a simple optimisation solver for the market clearing algorithm. 
We minimise the squared of aggregate excess demand, under the constraint of
a Limit-Up-Limit-Down (LU-LD) circuit breaker, which limits prices to 
[LD*p(t-1), LU*p(t-1)], with LD=1/2 and LU = 2
"""
from leap_ec import Individual, Representation
from leap_ec import ops, probe
from leap_ec.algorithm import generational_ea
from leap_ec.problem import FunctionProblem
from leap_ec.real_rep import create_real_vector
from leap_ec.real_rep.ops import mutate_gaussian


def ea_solve_noverbose(
    function,
    bounds,
    generations,
    pop_size,
    mutation_std,
    maximize=False,
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
        stop=lambda pop: (max(pop).fitness < 1),
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


def leap_solver(pop, price):

    # Define aggregate demand function
    def squared_agg_ed(p):
        result = 0
        for ind in pop:
            result += ind.edf(p)
        return result

    """ Define the circuit breaker bounds """
    limit_down = price * 0.1
    limit_up = price * 10.0

    mutation_rate = 10

    """ Run the solver on the squared agg ED function"""
    best_genome = ea_solve_noverbose(
        squared_agg_ed,
        bounds=[(limit_down, limit_up)],
        generations=50,
        pop_size=50,
        mutation_std=mutation_rate,
        hard_bounds=True,
    )

    """ Return the clearing price """
    return best_genome[0]


# def f(x):
#     return sum(x)**2
# best_genome = ea_solve_noverbose(f,
#           bounds=[(1.1111, 10)], generations = 50, pop_size = 50,
#           mutation_std=0.1, hard_bounds = True) #max = False
# print(best_genome)
