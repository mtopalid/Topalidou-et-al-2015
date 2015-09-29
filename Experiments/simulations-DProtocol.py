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
    folder = '../Results/D'
    if not os.path.exists(folder):
        os.makedirs(folder)

    folderTuf = folder + '/Testing_unfam'
    if not os.path.exists(folderTuf):
        os.makedirs(folderTuf)
    folderTufnG = folder + '/Testing_unfam_NoGPi'
    if not os.path.exists(folderTufnG):
        os.makedirs(folderTufnG)

    existing_learning = True
    for i in range(137,simulations):
        print 'Experiment: ', i + 1

        reset()

        print '\n\n-----------------Testing without GPi----------------'
        # Make GPI lesion
        connections["GPI.cog -> THL.cog"].active = False
        connections["GPI.mot -> THL.mot"].active = False

        task = Task_B(n=n_testing_trials)
        learning_trials(task[n_testing_trials:], trials=n_testing_trials, debugging=False, debug_simulation=True)

        # Debugging information
        print "Mean performance	: %.1f %%\n" % (np.array(task.records["best"][n_testing_trials:]).mean() * 100)
        print "Mean RT			: %.1f ms\n" % (np.array(task.records["RTmot"][n_testing_trials:]).mean())
        print

        # Save results in files
        file = folderTufnG + '/Cues' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.trials[n_testing_trials:])
        file = folderTufnG + '/Records' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.records[n_testing_trials:])


        print '\n--------Testing with GPi--------'
        # Reactivation of GPi
        connections["GPI.cog -> THL.cog"].active = True
        connections["GPI.mot -> THL.mot"].active = True

        task = Task_B(n=n_testing_trials)
        learning_trials(task[n_testing_trials:], trials=n_testing_trials, debugging=False, debug_simulation=True)

        print " Mean performance	: %.1f %%\n" % (np.array(task.records["best"][n_testing_trials:]).mean() * 100)
        print " Mean RT			: %.1f ms\n" % (np.array(task.records["RTmot"][n_testing_trials:]).mean())
        print

        # Save results in files
        file = folderTuf + '/Cues' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.trials[n_testing_trials:])
        file = folderTuf + '/Records' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.records[n_testing_trials:])
