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
    from task_b import Task_B

    # Creation of folders to save the results
    folder = '../Results/D-D1_D2_D3-100/Control'  # -half_noise'
    if not os.path.exists(folder):
        os.makedirs(folder)

    folderTuf = folder + '/Testing_unfam'
    if not os.path.exists(folderTuf):
        os.makedirs(folderTuf)
    folderTufnG = folder + '/Testing_unfam_NoGPi'
    if not os.path.exists(folderTufnG):
        os.makedirs(folderTufnG)
    folderTufnG2 = folder + '/Testing_unfam_NoGPi_2'
    if not os.path.exists(folderTufnG2):
        os.makedirs(folderTufnG2)

    for i in range(simulations):
        print('Experiment: ', i + 1)

        reset()

        print('\n\n-----------------Testing with GPi trials 120----------------')
        # Make GPI lesion
        # connections["GPI.cog -> THL.cog"].active = False
        # connections["GPI.mot -> THL.mot"].active = False

        task = Task_B(n=n_testing_trials)
        # task = task[:n_testing_trials]
        ntt = 100
        task = task[:ntt]
        learning_trials(task, trials=n_testing_trials, debugging=False, debug_simulation=True)

        print("Mean performance	: %.1f %%\n" % (np.array(task.records["best"]).mean() * 100))
        print()

        # Save results in files
        file = folderTufnG + '/Cues' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.trials)
        file = folderTufnG + '/Records' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.records)

        print('\n--------Testing with GPi trials 1200--------')
        # Reactivation of GPi
        connections["GPI.cog -> THL.cog"].active = True
        connections["GPI.mot -> THL.mot"].active = True

        nt = 1200
        task = Task_B(n=nt)#n_testing_trials)
        task = task[:nt]#n_testing_trials:]
        # task = task[:ntt]
        learning_trials(task, trials=nt, debugging=False, debug_simulation=True)

        print("Mean performance	: %.1f %%\n" % (np.array(task.records["best"]).mean() * 100))
        print()

        # Save results in files
        file = folderTuf + '/Cues' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.trials)
        file = folderTuf + '/Records' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.records)

        print('\n\n-----------------Testing with GPi 120 trials----------------')
        # Make GPI lesion
        # connections["GPI.cog -> THL.cog"].active = False
        # connections["GPI.mot -> THL.mot"].active = False

        task = Task_B(n=n_testing_trials)
        # task = task[:n_testing_trials]
        task = task[:ntt]
        learning_trials(task, trials=n_testing_trials, debugging=False, debug_simulation=True)

        print("Mean performance	: %.1f %%\n" % (np.array(task.records["best"]).mean() * 100))
        print()

        # Save results in files
        file = folderTufnG2 + '/Cues' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.trials)
        file = folderTufnG2 + '/Records' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.records)
