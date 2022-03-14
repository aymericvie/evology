def aggregate_ed(values):
    # return (3 * x - 10) for x in values

    return sum([3 * x - 10 for x in values])


price = 1

# '''
# Here is a simple optimisation solver for the market clering algorithm.
# We minimise the squared of aggregate excess demand, under the constraint of
# a Limit-Up-Limit-Down (LU-LD) circuit breaker, which limits prices to
# [LD*p(t-1), LU*p(t-1)], with LD=1/2 and LU = 2
# '''

# ''' First define squared aggregate demand '''
# def squared_agg_ed(x):
#     result = aggregate_ed(x) ** 2
#     return result

# limit_down = price * 0.5
# limit_up = price * 2.0

# import leap_simple_modif as leapm

# best_genome = leapm.ea_solve_verbose_false(squared_agg_ed,
#          bounds=[(limit_down, limit_up)], generations = 1000, pop_size = 50,
#          mutation_std=0.1, hard_bounds = True)

# # best_genome = ea_solve(squared_agg_ed,
# #          bounds=[(limit_down, limit_up)], generations = 1000, pop_size = 50,
# #          mutation_std=0.1)
# print(best_genome)
# print(best_genome[0])


# # best_genome = leapm.ea_solve_verbose_false(squared_agg_ed,
# #          bounds=[(0.5, 2)], generations = 1000, pop_size = 50,
# #          mutation_std=0.1)


# from leap_ec.simple import ea_solve
# def f(x):
#     return sum(x)**2
# ea_solve(f, bounds=[(4, 5.12) for _ in range(1)], maximize=False, hard_bounds = True)
