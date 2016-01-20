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
    from task import Task

    # Creation of folders to save the results
    folder = '../Results/D-D1_D2_D3-120/Control'  # -half_noise'
    if not os.path.exists(folder):
        os.makedirs(folder)

    folderTuf = folder + '/D2'
    if not os.path.exists(folderTuf):
        os.makedirs(folderTuf)
    folderTufnG = folder + '/D1'
    if not os.path.exists(folderTufnG):
        os.makedirs(folderTufnG)
    folderTufnG2 = folder + '/D3'
    if not os.path.exists(folderTufnG2):
        os.makedirs(folderTufnG2)

    for i in range(simulations):
        print('Experiment: ', i + 1)

        reset()

        print('\n\n-----------------Testing with GPi D1----------------')

        task = Task(n=n_trials)
        task = task[:n_trials]
        learning_trials(task, trials=n_trials, debugging=False, debug_simulation=True)

        print("Mean performance	: %.1f %%\n" % (np.array(task.records["best"]).mean() * 100))
        print()

        # Save results in files
        file = folderTufnG + '/Cues' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.trials)
        file = folderTufnG + '/Records' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.records)

        print('\n--------Testing with GPi D2--------')

        task = Task(n=n_trials)
        task = task[:n_trials]
        learning_trials(task, trials=n_trials, debugging=False, debug_simulation=True)

        print("Mean performance	: %.1f %%\n" % (np.array(task.records["best"]).mean() * 100))
        print()

        # Save results in files
        file = folderTuf + '/Cues' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.trials)
        file = folderTuf + '/Records' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.records)

        print('\n\n-----------------Testing with D3----------------')

        task = Task(n=n_trials)
        task = task[:n_trials]
        learning_trials(task, trials=n_trials, debugging=False, debug_simulation=True)

        print("Mean performance	: %.1f %%\n" % (np.array(task.records["best"]).mean() * 100))
        print()

        # Save results in files
        file = folderTufnG2 + '/Cues' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.trials)
        file = folderTufnG2 + '/Records' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.records)
