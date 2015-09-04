# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
#               Nicolas Rougier (Nicolas.Rougier@inria.fr)
# -----------------------------------------------------------------------------


# Simulations of protocol C with reverse after 250 or 500 trials.
# Two unknown shapes, with reward probabilities P1 = 75% and P2 = 25%, are shown
# to the system. After x number of trials the same shapes are presented but with
# reverse of their probabilities, P1 = 25% and P2 = 75%.
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
	from task_cp import Task_C

	# Creation of folder to save the results
	folder = '../Results/C-Piron'
	if not os.path.exists(folder):
		os.makedirs(folder)

	# Trial number that the reward probabilities are reversed
	reverse_trial = 250 #500

	folder += '/' + str(reverse_trial)
	if not os.path.exists(folder):
		os.makedirs(folder)


	for i in range(simulations):
		print 'Experiment: ', i + 1
		reset()
        # Define the shapes and the positions that we'll be used to each trial
        # n number of trials for each simulation, should be multiple of 6 because there are 6 valuable combinations of shapes and positions
        # r the number of trial that the reward probabilities are reversed
		task = Task_C(n=n_reverse_trials_Piron, r = reverse_trial)
		learning_trials(task, trials = n_reverse_trials_Piron, debugging = False, debug_simulation = True)

        # Debugging information
		print "Mean performance of 30 last trials	: %.1f %%\n" %(np.array(task.records["best"][-30:]).mean()*100)
		debug_learning(task.records["Wcog"][-1], task.records["Wmot"][-1], task.records["Wstr"][-1], task.records["CueValues"][-1])

        # Save the results in files
		file = folder + '/Cues'  + "%03d" % (i+1) + '.npy'
		np.save(file,task.trials)
		file = folder + '/Records'  + "%03d" % (i+1) + '.npy'
		np.save(file,task.records)

		print
