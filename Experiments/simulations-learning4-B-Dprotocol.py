# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
#               Nicolas Rougier (Nicolas.Rougier@inria.fr)

# -----------------------------------------------------------------------------


# Simulations of protocol B.
# 	Habitual Condition (HC): The pair of pre-learned shapes is presented.
# 							  P1 = 75% and P2 = 25%
# 	Novel	 Condition (NC): An unknown pair of shapes is shown
# 							  P1 = 75% and P2 = 25%
# Learning phase: Two unknown shapes, with reward probabilities P1 = 75% and
# P2 = 25%, are shown to the system. This pair is used to HC.
# Testing Phase: Blocks of 10 trials HC and NC are mixed in each simulation.
# 				 Inactivation of connection between GPi and Thalamus and
#				 presentation of mixed blocks of HC and NC trials
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    # Include to the path files from cython folder
    temp = '../cython/'
    import sys

    sys.path.append(temp)

    import numpy as np
    import os

    # model file build the structures and initialize the model
    from model import *
    from learning import *
    from parameters import *
    from task_b import Task_B

    # Creation of folders to save the results
    folder = '../Results'
    if not os.path.exists(folder):
        os.makedirs(folder)

    folderBL = folder + '/B/Learning'
    if not os.path.exists(folderBL):
        os.makedirs(folderBL)

    folderDL = folder + '/D/Learning'
    if not os.path.exists(folderDL):
        os.makedirs(folderDL)

    for i in range(simulations):
        print 'Experiment: ', i + 1
        reset()

        # Formation of Habits

        # Define the shapes and the positions that we'll be used to each trial
        # n should be multiple of 6 because there are 6 valuable combinations of positions
        # The number of tasks are 2*n:
        # First n are formed only by the pair [0,1] that we want to learn
        # Last n are formed only by [2,3]
        task = Task_B(n=n_learning_trials)
        # In this phase, we want only the pair [0,1]
        task = task[:n_learning_trials]

        # Repeated trials with learning after each trial
        learning_trials(task, trials=n_learning_trials, debugging=False, debug_simulation=True)

        # Save results in files
        file = folderBL + '/Cues' + '%03d' % (i + 1) + '.npy'
        np.save(file, task.trials)
        file = folderBL + '/Records' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.records)
        file = folderDL + '/Cues' + '%03d' % (i + 1) + '.npy'
        np.save(file, task.trials)
        file = folderDL + '/Records' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.records)

        # Debugging information
        print " Mean performance of 30 last trials	: %.1f %%" % (np.array(task.records["best"][-30:]).mean() * 100)
        print " Mean RT								: %.1f ms" % (np.array(task.records["RTmot"][-30:]).mean())
        debug_learning(task.records["Wcog"][-1], task.records["Wmot"][-1], task.records["Wstr"][-1],
                       task.records["CueValues"][-1])
        print
