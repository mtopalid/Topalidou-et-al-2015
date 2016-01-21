# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
# -----------------------------------------------------------------------------


# Simulations of protocol D.
# 	Habitual Condition (HC): The pair of pre-learned shapes is presented.
# 							  P1 = 75% and P2 = 25%
# 	Novel	 Condition (NC): An unknown pair of shapes is shown
# 							  P1 = 75% and P2 = 25%
# Learning phase: Two unknown shapes, with reward probabilities P1 = 75% and
# P2 = 25%, are shown to the system. This pair is used to HC.
# Testing Phase: Inactivation of connection between GPi and Thalamus and
#				 presentation of mixed blocks of HC and NC trials
# 				 Re-activation of GPi-Thalamus connection and presentation of
# 				 mixed blocks of 10 trials HC and NC. At NC trials the same
# 				 pair is presented with the one presented with inactive
# 				 connections.
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    # Include to the path files from cython subfolder
    temp = '../cython/'
    import sys

    sys.path.append(temp)

    import numpy as np
    import os
    # model file build the structures and initialize the model
    from model import *
    from learning import *
    from parameters import *
    from task import Task
    from performances import *

    # Creation of folders to save the results
    folder = '../Results/D-D1_D2_D3-120a' + str(a)
    subfolder = folder + '/Control'  # -half_noise'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)

    folderD1 = subfolder + '/D1'
    if not os.path.exists(folderD1):
        os.makedirs(folderD1)
    folderD2 = subfolder + '/D2'
    if not os.path.exists(folderD2):
        os.makedirs(folderD2)
    folderD3 = subfolder + '/D3'
    if not os.path.exists(folderD3):
        os.makedirs(folderD3)

    for i in range(simulations):
        print('Experiment: ', i + 1)

        reset()

        print('\n\n-----------------Testing with GPi D1----------------')

        task = Task(n=n_trials)
        task = task[:n_trials]
        learning_trials(task, trials=n_trials, debugging=False, debug_simulation=True, debugging_learning=False)

        print("Mean performance	: %.1f %%\n" % (np.array(task.records["best"]).mean() * 100))
        print("First 25 trials 	: %.1f %%\n" % (np.array(task.records["best"][:25]).mean() * 100))
        print("Last 25 trials		: %.1f %%\n" % (np.array(task.records["best"][-25:]).mean() * 100))
        print()

        # Save results in files
        file = folderD1 + '/Cues' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.trials)
        file = folderD1 + '/Records' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.records)

        print('\n--------Testing with GPi D2--------')

        task = Task(n=n_trials)
        task = task[:n_trials]
        learning_trials(task, trials=n_trials, debugging=False, debug_simulation=True, debugging_learning=False)

        print("Mean performance	: %.1f %%\n" % (np.array(task.records["best"]).mean() * 100))
        print("First 25 trials 	: %.1f %%\n" % (np.array(task.records["best"][:25]).mean() * 100))
        print("Last 25 trials		: %.1f %%\n" % (np.array(task.records["best"][-25:]).mean() * 100))
        print()

        # Save results in files
        file = folderD2 + '/Cues' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.trials)
        file = folderD2 + '/Records' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.records)

        print('\n\n-----------------Testing with D3----------------')

        task = Task(n=n_trials)
        task = task[:n_trials]
        learning_trials(task, trials=n_trials, debugging=False, debug_simulation=True, debugging_learning=False)

        print("Mean performance	: %.1f %%\n" % (np.array(task.records["best"]).mean() * 100))
        print("First 25 trials 	: %.1f %%\n" % (np.array(task.records["best"][:25]).mean() * 100))
        print("Last 25 trials		: %.1f %%\n" % (np.array(task.records["best"][-25:]).mean() * 100))
        print()
        print()
        print()

        # Save results in files
        file = folderD3 + '/Cues' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.trials)
        file = folderD3 + '/Records' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.records)

    compute_Performances(folder, control=True)