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
    from task_b import Task_B

    task = Task_B(n=n_testing_trials)
    task = task[n_testing_trials:]
    connections["GPI.cog -> THL.cog"].active = False
    connections["GPI.mot -> THL.mot"].active = False
    learning_trials(task, trials=n_testing_trials, debugging=True)
    P = task.records[:]["best"]
    print "  Mean performance		: %.1f %%" % np.array(P * 100).mean()


    task = Task_B(n=n_testing_trials)
    task = task[n_testing_trials:]
    connections["GPI.cog -> THL.cog"].active = True
    connections["GPI.mot -> THL.mot"].active = True
    learning_trials(task, trials=n_testing_trials, debugging=True)

    print "Mean performance	: %.1f %%\n" % (np.array(task.records["best"]).mean() * 100)
    if 0: display_ctx(P, 3.0)
    if 0: display_ctx(hist, 3.0)
