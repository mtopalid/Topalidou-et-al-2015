# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
# -----------------------------------------------------------------------------

# Simulate number of experiments that is given in parameters.py of the different
# models. Each simulation is a number of trials under Guthrie protocol.
# -----------------------------------------------------------------------------

if __name__ == "__main__":

	temp = '../cython/'
	import sys
	sys.path.append(temp)
	import numpy as np
	import os
	from model import *
	from learning import *
	from parameters import *
	from task_cp import Task_C

	fld = '../Results/C-1-100-Piron'
	start = input('First reverse after how many trials?\n')
	print start
	finish = input('Last reverse after how many trials?\n')
	print finish
	print


	for j in range (start,finish+1):
		print 'Reverse after: ', j
		print
		folder = fld + '/Reverse' + "%03d" % j
		if not os.path.exists(folder):
			os.makedirs(folder)
		for i in range(simulations):
			print 'Experiment: ', i + 1

			reset()
			task = Task_C(n=n_reverse_trials_Piron, r = j)
			learning_trials(task, trials = n_reverse_trials_Piron, debugging = False, debug_simulation = True)
			print "Mean performance of 30 last trials	: %.1f %%\n" %(np.array(task.records["best"][-30:]).mean()*100)
			debug_learning(task.records["Wcog"][-1], task.records["Wmot"][-1], task.records["Wstr"][-1], task.records["CueValues"][-1])

			file = folder + '/Cues'  + "%03d" % (i+1) + '.npy'
			np.save(file,task.trials)
			file = folder + '/Records'  + "%03d" % (i+1) + '.npy'
			np.save(file,task.records)
			print
		print




