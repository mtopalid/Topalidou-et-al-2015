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

	folder = '../Results/C-Piron'
	if not os.path.exists(folder):
		os.makedirs(folder)

	reverse = 1
	reverse_all = 1
	reverse_trial = input('\nAfter how many trials will be the reverse?\n')
	folder += '/' + str(reverse_trial)
	if not os.path.exists(folder):
		os.makedirs(folder)


	for i in range(simulations):
		print 'Simulation: ', i + 1
		reset(protocol = 'Piron', ntrials = n_reverse_trials)
		global learning_cues_cog, learning_cues_mot
		learning_cues_cog, t, t, learning_cues_mot, t, t = trials_cues(protocol = 'Piron', ltrials = n_reverse_trials_Piron)

		result = learning_trials(inversable = reverse, reverse_all = reverse_all, reverse_trial = reverse_trial, trials = n_reverse_trials_Piron, protocol = 'Piron', debugging = False, less_trained_trials = 5, Piron_learning = True, save = True, debug_simulation = True)

		debug(RT = result["RT"]["mot"][-1], P = result["P"][-1])
		debug_learning(result["W"]["CTXcog"][-1], result["W"]["CTXmot"][-1], result["W"]["STR"][-1], result["Values"][-1])

		file = folder + '/All-Results'  + "%03d" % (i+1) + '.npy'
		np.save(file,result)
		print




