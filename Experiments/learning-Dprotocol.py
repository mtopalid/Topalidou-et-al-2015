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

    n_testing_trials=960
    print '\n\n-----------------Testing without GPi----------------'
    # Make GPI lesion
    connections["GPI.cog -> THL.cog"].active = False
    connections["GPI.mot -> THL.mot"].active = False

    task = Task_B(n=n_testing_trials)  # Debugging information
    learning_trials(task[n_testing_trials:], trials=n_testing_trials, debugging=False, debug_simulation= True)

    print
    print "Mean performance	: %.1f %%\n" % (np.array(task.records["best"][n_testing_trials:]).mean() * 100)
    print "Mean RT			: %.1f ms\n" % (np.array(task.records["RTmot"][n_testing_trials:]).mean())
    print

    print '\n--------Testing with GPi--------'
    # Reactivation of GPi
    connections["GPI.cog -> THL.cog"].active = True
    connections["GPI.mot -> THL.mot"].active = True

    task = Task_B(n=n_testing_trials)
    learning_trials(task[n_testing_trials:], trials=n_testing_trials, debugging=False, debug_simulation= True)

    print
    print '--------UnFamiliar--------'
    print " Mean performance	: %.1f %%\n" % (np.array(task.records["best"][n_testing_trials:]).mean() * 100)
    print " Mean RT			: %.1f ms\n" % (np.array(task.records["RTmot"][n_testing_trials:]).mean())
    print
