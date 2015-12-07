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
    folder = '../Results/D/Control'#-half_noise'
    if not os.path.exists(folder):
        os.makedirs(folder)


    folderTuf_first_day = folder + '/Testing_unfam'
    if not os.path.exists(folderTuf_first_day):
        os.makedirs(folderTuf_first_day)
    folderTuf_second_day = folder + '/Testing_unfam_2'
    if not os.path.exists(folderTuf_second_day):
        os.makedirs(folderTuf_second_day)

    for i in range(simulations):
        print 'Experiment: ', i + 1

        reset()



        print '\n-----------------Testing with GPi first 120----------------'

        task = Task_B(n=n_testing_trials)
        task = task[n_testing_trials:]
        ntt = 100
        task = task[:ntt]
        learning_trials(task, trials=ntt, debugging=False, debug_simulation=True)

        print "Mean performance	: %.1f %%\n" % (np.array(task.records["best"]).mean() * 100)
        print

        # Save results in files
        file = folderTuf_first_day + '/Cues' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.trials)
        file = folderTuf_first_day + '/Records' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.records)


        print '\n--------Testing with GPi last 120--------'

        task = Task_B(n=n_testing_trials)
        task = task[n_testing_trials:]
        task = task[:ntt]
        learning_trials(task, trials=ntt, debugging=False, debug_simulation=True)

        print "Mean performance	: %.1f %%\n" % (np.array(task.records["best"]).mean() * 100)
        print

        # Save results in files
        file = folderTuf_second_day + '/Cues' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.trials)
        file = folderTuf_second_day + '/Records' + "%03d" % (i + 1) + '.npy'
        np.save(file, task.records)

