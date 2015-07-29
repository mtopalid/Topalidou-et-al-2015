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
	folder = '../Results/C-Results'
	reverse = 1
	reverse_trial = input('\nAfter how many trials will be the reverse?\n')
	reverse_all = input('\nDo you want to reverse all probabilities or just the middle ones?\nChoose:\n0 for middle ones\n1 for all\n')
	folder += '-reverse-after' + str(reverse_trial)
	folder += 'all' if reverse_all else 'middle cues'#-NoCortLearn-HalfParam

	#path += '-9000'
	if not os.path.exists(folder):
		os.makedirs(folder)


	CVtotal = np.zeros((simulations, n))
	WtotalSTR = np.zeros((simulations, n_reverse_trials, n))
	WtotalCog = np.zeros((simulations, n_reverse_trials, n))
	WtotalMot = np.zeros((simulations, n_reverse_trials, n))

	P = np.zeros((simulations, n_reverse_trials))
	RT = np.zeros((simulations, n_reverse_trials))


	for i in range(simulations):
		print 'Experiment: ', i + 1
		reset(protocol = 'Guthrie', ntrials = n_reverse_trials)

		P[i,:], RT[i,:], WtotalCog[i], WtotalMot[i], WtotalSTR[i] = learning_trials(inversable = reverse, reverse_all = reverse_all, reverse_trial = reverse_trial, protocol = 'Guthrie', trials = n_reverse_trials, debugging = False, save = True)

		CVtotal[i, :] = CUE["value"]
		wCog = connections["CTX.cog -> CTX.ass"].weights
		wMot = connections["CTX.mot -> CTX.ass"].weights
		wStr = connections["CTX.cog -> STR.cog"].weights
		debug_learning(wCog, wMot, wStr, cues_value = CUE["value"])
		debug(RT = RT[i,:], P = P[i,:])
		print
		print

	debug_total(P, RT, CVtotal, WtotalCog, WtotalMot, WtotalSTR)
	file = folder + '/Weights_Str.npy'
	np.save(file,WtotalSTR)
	file = folder + '/Weights_Cog.npy'
	np.save(file,WtotalCog)
	file = folder + '/Weights_Mot.npy'
	np.save(file,WtotalMot)

	file = folder + '/MeanCuesValues.npy'
	np.save(file,CVtotal)
	file = folder + '/RT.npy'
	np.save(file,RT)
	file = folder + '/Performance.npy'
	np.save(file,P)
