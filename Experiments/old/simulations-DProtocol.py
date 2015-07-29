# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
# -----------------------------------------------------------------------------

# Simulate number of experiments that is given in parameters.py of the different
# models. Each simulation is a number of trials under Piron protocol.
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

	folder = '../Results/D-Results'
	if not os.path.exists(folder):
		os.makedirs(folder)

	f = None

	CVtotal = np.zeros((simulations, n))

	WtotalSTR = np.zeros((simulations, n_learning_trials, n))
	WtotalCog  = np.zeros((simulations, n_learning_trials, n))
	WtotalMot  = np.zeros((simulations, n_learning_trials, n))

	Ptest_fam = np.zeros((simulations, n_testing_trials))
	RTtest_fam = np.zeros((simulations, n_testing_trials))

	Ptest_unfam = np.zeros((simulations, n_testing_trials))
	RTtest_unfam = np.zeros((simulations, n_testing_trials))

	Ptest_fam_NoGPi = np.zeros((simulations, n_testing_trials))
	RTtest_fam_NoGPi = np.zeros((simulations, n_testing_trials))

	Ptest_unfam_NoGPi = np.zeros((simulations, n_testing_trials))
	RTtest_unfam_NoGPi = np.zeros((simulations, n_testing_trials))
	for i in range(simulations):
		print 'Experiment: ', i + 1
		reset(protocol = 'Piron', ntrials = n_learning_trials)
		print '-----------------Learning Phase----------------'
		#f.write('\n-----------------Learning Phase----------------')
		# Formation of Habits
		t1, t2, WtotalCog[i,:], WtotalMot[i,:], WtotalSTR[i,:] = learning_trials(trials = n_learning_trials, f = f, debugging = False, save = True, protocol = 'Piron', familiar = True, less_trained_trials = 5)
		CVtotal[i, :] = CUE["value"]
		wCog = connections["CTX.cog -> CTX.ass"].weights
		wMot = connections["CTX.mot -> CTX.ass"].weights
		wStr = connections["CTX.cog -> STR.cog"].weights
		debug_learning(wCog, wMot, wStr, cues_value = CUE["value"], f = f)

		print '\n\n-----------------Testing Phase----------------'
		#f.write('\n\n\n-----------------Testing Phase----------------')
		# Make GPI lesion
		connections["GPI.cog -> THL.cog"].active = False
		connections["GPI.mot -> THL.mot"].active = False

		W_COG = connections["CTX.cog -> CTX.ass"].weight
		W_MOT = connections["CTX.mot -> CTX.ass"].weights
		W_STR = connections["CTX.cog -> STR.cog"].weights
		reset(protocol = 'Piron', ntrials = n_testing_trials, W_COG = W_COG, W_MOT = W_MOT, W_STR = W_STR)

		for j in range(n_testing_trials/10):
			Ptest_fam_NoGPi[i,j*10:(j+1)*10], RTtest_fam_NoGPi[i,j*10:(j+1)*10], t1,t2,t3 = learning_trials(trials = 10, f = f, debugging = False, save = True, trained = True)

			Ptest_unfam_NoGPi[i,j*10:(j+1)*10], RTtest_unfam_NoGPi[i,j*10:(j+1)*10], t1,t2,t3 = learning_trials(trials = 10, f = f, debugging = False, save = True, familiar = False, trained = True)

		wCog = connections["CTX.cog -> CTX.ass"].weights
		wMot = connections["CTX.mot -> CTX.ass"].weights
		wStr = connections["CTX.cog -> STR.cog"].weights
		debug_learning(wCog, wMot, wStr, cues_value = CUE["value"], f = f)
		print '\n--------Testing Familiar without GPi--------'
		debug(RT = RTtest_fam_NoGPi[i,:], P = Ptest_fam_NoGPi[i,:])
		print
		print '--------Testing UnFamiliar without GPi--------'
		debug(RT = RTtest_unfam_NoGPi[i,:], P = Ptest_unfam_NoGPi[i,:])
		print

		connections["GPI.cog -> THL.cog"].active = True
		connections["GPI.mot -> THL.mot"].active = True


		W_COG = connections["CTX.cog -> CTX.ass"].weight
		W_MOT = connections["CTX.mot -> CTX.ass"].weights
		W_STR = connections["CTX.cog -> STR.cog"].weights
		reset(protocol = 'Piron', ntrials = n_testing_trials, W_COG = W_COG, W_MOT = W_MOT, W_STR = W_STR)

		for j in range(n_testing_trials/10):
			Ptest_fam[i,j*10:(j+1)*10], RTtest_fam[i,j*10:(j+1)*10],t1,t2,t3 = learning_trials(trials = 10, f = f, debugging = False, save = True, trained = True)

			Ptest_unfam[i,j*10:(j+1)*10], RTtest_unfam[i,j*10:(j+1)*10], t1,t2,t3 = learning_trials(trials = 10, f = f, debugging = False, save = True, familiar = False, trained = True)

		wCog = connections["CTX.cog -> CTX.ass"].weights
		wMot = connections["CTX.mot -> CTX.ass"].weights
		wStr = connections["CTX.cog -> STR.cog"].weights
		debug_learning(wCog, wMot, wStr, cues_value = CUE["value"], f = f)
		print '--------Testing Familiar with GPi--------'
		debug(RT = RTtest_fam[i,:], P = Ptest_fam[i,:])
		print

		print '\n--------Testing UnFamiliar with GPi--------'
		debug(RT = RTtest_unfam[i,:], P = Ptest_unfam[i,:])
		print
		print

	file = folder + '/MeanCuesValues.npy'
	np.save(file,CVtotal)
	file = folder + '/Weights_Str.npy'
	np.save(file,WtotalSTR)
	file = folder + '/Weights_Cog.npy'
	np.save(file,WtotalCog)
	file = folder + '/Weights_Mot.npy'
	np.save(file,WtotalMot)

	file = folder + '/RT-fam_NoGPi.npy'
	np.save(file,RTtest_fam_NoGPi)
	file = folder + '/Performance-fam_NoGPi.npy'
	np.save(file,Ptest_fam_NoGPi)

	file = folder + '/RT-unfam_NoGPi.npy'
	np.save(file,RTtest_unfam_NoGPi)
	file = folder + '/Performance-unfam_NoGPi.npy'
	np.save(file,Ptest_unfam_NoGPi)

	file = folder + '/RT-fam.npy'
	np.save(file,RTtest_fam)
	file = folder + '/Performance-fam.npy'
	np.save(file,Ptest_fam)
	file = folder + '/DifferentChoices-fam.npy'

	file = folder + '/RT-unfam.npy'
	np.save(file,RTtest_unfam)
	file = folder + '/Performance-unfam.npy'
	np.save(file,Ptest_unfam)
