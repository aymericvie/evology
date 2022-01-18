""" here we define the numerical experiments that we base our research on. 
Hence, to experiment, we only have to import the corresponding function from this module and run it. """

from main import *
import parameters


def MC_LongRunsWS(
    Reps: int,
    InitialCondition: list,
    Time: int,
    PopSize: int,
    ProbaSelection,
    ProbaMutation,
):
    """Monte Carlo long runs
    For a specific initial condition, record the transitory and final wealth coordinates.
    Output: csv data on the trajectories of the system (in terms of wealth shares) for further analysis.
    One line per path realisation.

    Default parameters for the main() function:"""
    tqdm_display = True
    reset_wealth = False
    solver = "esl"
    space = "scholl"
    circuit = False
    if ProbaSelection > 0 or ProbaMutation > 0:
        mode = "between"
    if ProbaSelection == 0 and ProbaMutation == 0:
        mode = "static"
    # TODO: possible additions: reinvestment rate, EMA length ...

    """ Results object"""
    PathsNT = np.zeros((Reps, Time - parameters.ShieldResults))
    PathsVI = np.zeros((Reps, Time - parameters.ShieldResults))
    PathsTF = np.zeros((Reps, Time - parameters.ShieldResults))

    for i in tqdm(range(Reps)):
        # TODO: parallelise the experiments

        df, pop = main(
            mode,
            space,
            solver,
            circuit,
            Time,
            ProbaSelection,
            PopSize,
            ProbaMutation,
            InitialCondition,
            tqdm_display,
            reset_wealth,
        )

        PathsNT[i, :] = df["WShare_NT"]
        PathsVI[i, :] = df["WShare_VI"]
        PathsTF[i, :] = df["WShare_TF"]

    return PathsNT, PathsVI, PathsTF
