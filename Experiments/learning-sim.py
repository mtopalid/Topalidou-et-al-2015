# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
# -----------------------------------------------------------------------------

# Testing learning for each model under Piron protocol
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    temp = '../cython/'
    import sys

    sys.path.append(temp)
    from model import *
    from display import *
    from learning import *
    from task import Task

    task = Task(n=n_trials)
    task = task[:n_trials]
    learning_trials(task, trials=n_trials, debugging=True, debug_simulation=False, debugging_learning=False)

    print("Mean performance	: %.1f %%\n" % (np.array(task.records["best"]).mean() * 100))
    print("First 25 trials 	: %.1f %%\n" % (np.array(task.records["best"][:25]).mean() * 100))
    print("Last 25 trials		: %.1f %%\n" % (np.array(task.records["best"][-25:]).mean() * 100))
    print()


    connections["GPI.cog -> THL.cog"].active = False
    connections["GPI.mot -> THL.mot"].active = False
    task = Task(n=n_trials)
    task = task[n_trials:]
    learning_trials(task, trials=n_trials, debugging=True, debug_simulation=False, debugging_learning=False)

    print("Mean performance	: %.1f %%\n" % (np.array(task.records["best"]).mean() * 100))
    print("First 25 trials 	: %.1f %%\n" % (np.array(task.records["best"][:25]).mean() * 100))
    print("Last 25 trials		: %.1f %%\n" % (np.array(task.records["best"][-25:]).mean() * 100))
    print()

    if 0: display_ctx(P, 3.0)
    if 0: display_ctx(hist, 3.0)
