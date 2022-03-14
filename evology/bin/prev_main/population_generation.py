import parameters
import numpy as np
import genetic_algorithm_functions as ga
import random

INITIAL_CASH = parameters.INITIAL_CASH
INITIAL_ASSETS = parameters.INITIAL_ASSETS
PROBA_TF = parameters.PROBA_TF
PROBA_VI = parameters.PROBA_VI
PROBA_GP = parameters.PROBA_GP
POPULATION_SIZE = parameters.POPULATION_SIZE


def generate_population(mode):

    if mode == "extended":
        PROBA_TF = parameters.PROBA_TF
        PROBA_VI = parameters.PROBA_VI
        PROBA_GP = 0
    if mode == "open":
        PROBA_GP = 1
        PROBA_TF = 0
        PROBA_VI = 0
    if mode == "combined":
        PROBA_GP = parameters.PROBA_GP
        PROBA_TF = parameters.PROBA_TF
        PROBA_VI = parameters.PROBA_VI

    ### create the populations ###

    types = np.array(["NA"])

    if PROBA_GP == 1:
        pop_ex = []
        # pop_op = gp.create-population(.POPULATIOn_SIZE...)
        pop_op = []  # temp
        for i in range(POPULATION_SIZE):
            types = np.vstack((types, "GP"))

    elif PROBA_TF == 1:
        pop_ex = ga.toolbox.tf_population_creation2(n=POPULATION_SIZE)
        pop_op = []
        for i in range(POPULATION_SIZE):
            types = np.vstack((types, "TF"))
    elif PROBA_VI == 1:
        pop_ex = ga.toolbox.vi_population_creation2(n=POPULATION_SIZE)
        pop_op = []
        for i in range(POPULATION_SIZE):
            types = np.vstack((types, "VI"))
    else:
        if PROBA_GP == 0:
            pop_ex, types = ga.create_mixed_population(
                POPULATION_SIZE, PROBA_TF, PROBA_VI
            )
            pop_op = []
        else:
            # Determine respective population sizes
            POP_OP_SIZE = 0
            POP_EX_SIZE = 0
            for i in range(POPULATION_SIZE):
                rd = random.random()
                if rd <= PROBA_GP:
                    POP_OP_SIZE += 1
                elif rd > PROBA_GP:
                    POP_EX_SIZE += 1
            # Create the two populations
            pop_ex, types = ga.create_mixed_population(POP_EX_SIZE, PROBA_TF, PROBA_VI)
            # pop_op = gp.create-population(POP_OP_SIZE)
            pop_op = []  # temp
            # for i in range{POP_OP_SIZE}:
            # types = np.vstack((types, "GP"))

    """ TODO (GP) """

    """ Warning: when adding new strategy, we will need to modify here """

    # If we need to give different starting conditions to different strategies, we can do it here.
    balance_sheet = np.array([0, INITIAL_CASH, INITIAL_ASSETS, 0, 0, 0, 0, 0, 0])
    for i in range(POPULATION_SIZE - 1):
        ind_bs = np.array([0, INITIAL_CASH, INITIAL_ASSETS, 0, 0, 0, 0, 0, 0])
        balance_sheet = np.vstack((balance_sheet, ind_bs))

    types = np.delete(types, (0), axis=0)

    balance_sheet = balance_sheet.astype("float64")

    return pop_ex, pop_op, balance_sheet, types


pop_ex, pop_op, balance_sheet, types = generate_population("extended")
# print(('{}\n'*len(pop_ex)).format(*pop_ex))
# print(('{}\n'*len(pop_op)).format(*pop_op))
# print(types)
