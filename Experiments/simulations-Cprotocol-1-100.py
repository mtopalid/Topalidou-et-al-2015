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
	from testing import *
	from parameters import *
	fld = '../Results/C-1-100'


	reverse = 1
	reverse_all = 1

	start = input('First reverse after how many trials?\n')
	print start
	finish = input('Last reverse after how many trials?\n')
	print finish


	for j in range (start,finish+1):
		print 'Reverse after: ', j
		print
		folder = fld + '/Reverse' + "%03d" % j
		if not os.path.exists(folder):
			os.makedirs(folder)
		for i in range(simulations):
			print 'Simulation: ', i + 1
			reset(protocol = 'Guthrie', ntrials = n_reverse_trials)
			global cues_cog, cues_mot
			cues_cog, cues_mot = trials_cues(protocol = 'Guthrie', ntrials = n_reverse_trials)

			result = learning_trials(inversable = reverse, reverse_all = reverse_all, reverse_trial = j, protocol = 'Guthrie', trials = n_reverse_trials, debugging = False, trained = True, save = True, debug_simulation = True)


			file = folder + '/All-Results'  + "%03d" % (i+1) + '.npy'
			np.save(file,result)

			print
		print




