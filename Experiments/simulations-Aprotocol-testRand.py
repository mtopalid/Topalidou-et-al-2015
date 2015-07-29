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

	folder = '../Results/AtestRand'
	if not os.path.exists(folder):
		os.makedirs(folder)

	for i in range(simulations):
		print 'Simulation: ', i + 1
		reset(protocol = 'Guthrie')
		global cues_cog, cues_mot
		cues_cog, cues_mot = trials_cues(protocol = 'Guthrie', ntrials = n_trials)

		result = learning_trials(protocol = 'Guthrie', trials = n_trials, debugging = False, trained = True, save = True, debug_simulation = True, learn = False)

		file = folder + '/All-Results'  + "%03d" % (i+1) + '.npy'
		np.save(file,result)
		print




