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

	folder = '../Results/D'
	if not os.path.exists(folder):
		os.makedirs(folder)

	folderL = folder + '/Learning'
	if not os.path.exists(folderL):
		os.makedirs(folderL)
	folderTf = folder + '/Testing_fam'
	if not os.path.exists(folderTf):
		os.makedirs(folderTf)
	folderTuf = folder + '/Testing_unfam'
	if not os.path.exists(folderTuf):
		os.makedirs(folderTuf)
	folderTfnG = folder + '/Testing_fam_NoGPi'
	if not os.path.exists(folderTfnG):
		os.makedirs(folderTfnG)
	folderTufnG = folder + '/Testing_unfam_NoGPi'
	if not os.path.exists(folderTufnG):
		os.makedirs(folderTufnG)


	for i in range(simulations):
		print 'Experiment: ', i + 1
		reset(protocol = 'Piron', ntrials = n_learning_trials)
		global learning_cues_cog, testing_cues_cog_fam, testing_cues_cog_unfam, learning_cues_mot, testing_cues_mot_fam, testing_cues_mot_unfam
		learning_cues_cog, testing_cues_cog_fam, testing_cues_cog_unfam, learning_cues_mot, testing_cues_mot_fam, testing_cues_mot_unfam = trials_cues(protocol = 'Piron', ltrials = n_learning_trials, ttrials = n_testing_trials)


		print '-----------------Learning Phase----------------'
		#f.write('\n-----------------Learning Phase----------------')
		# Formation of Habits

		result = learning_trials(protocol = 'Piron', trials = n_learning_trials, debugging = False, trained = False, save = True, less_trained_trials = 5, Piron_learning = True, debug_simulation = True)

		file = folderL + '/All-Results' + "%03d" % (i+1) + '.npy'
		np.save(file,result)
		#debug(RT = result["RT"]["mot"], P = result["P"])
		#debug_learning(result["W"]["CTXcog"][-1], result["W"]["CTXmot"][-1], result["W"]["STR"][-1], result["Values"][-1])


		print '\n\n-----------------Testing Phase----------------'
		#f.write('\n\n\n-----------------Testing Phase----------------')
		# Make GPI lesion and Testing changing between familiar and unfamiliar cues every 10 trials
		connections["GPI.cog -> THL.cog"].active = False
		connections["GPI.mot -> THL.mot"].active = False

		reset_activities()

		result_fam = results(n_trials = n_testing_trials)
		result_unfam = results(n_trials = n_testing_trials)
		steps = n_testing_trials/10
		print 'Starting   ',
		for j in range(n_testing_trials/10):

			result_fam[j*10:(j+1)*10]  	= learning_trials(protocol = 'Piron', trials = 10, debugging = False, trained = True, save = True)
			print '\b.',
			sys.stdout.flush()
			result_unfam[j*10:(j+1)*10] = learning_trials(protocol = 'Piron', trials = 10, debugging = False, trained = True, save = True, familiar = False)
			print '\b.',
			sys.stdout.flush()
		print '   Done!'
		print '\n--------Testing Familiar without GPi--------'
		debug(RT = result_fam["RT"]["mot"], P = result_fam["P"])
		print
		print '--------Testing UnFamiliar without GPi--------'
		debug(RT = result_unfam["RT"]["mot"], P = result_unfam["P"])
		print

		file = folderTfnG + '/All-Results'  + "%03d" % (i+1) + '.npy'
		np.save(file,result_fam)
		file = folderTufnG + '/All-Results' + "%03d" % (i+1) + '.npy'
		np.save(file,result_unfam)

		#Reactivation of GPi and Testing  changing between familiar and unfamiliar cues every 10 trials
		connections["GPI.cog -> THL.cog"].active = True
		connections["GPI.mot -> THL.mot"].active = True

		learning_cues_cog, testing_cues_cog_fam, testing_cues_cog_unfam, learning_cues_mot, testing_cues_mot_fam, testing_cues_mot_unfam = trials_cues(protocol = 'Piron', ltrials = n_learning_trials, ttrials = n_testing_trials)


		result_fam = results(n_trials = n_testing_trials)
		result_unfam = results(n_trials = n_testing_trials)

		print 'Starting   ',
		for j in range(n_testing_trials/10):

			result_fam[j*10:(j+1)*10]  	= learning_trials(protocol = 'Piron', trials = 10, debugging = False, trained = True, save = True)
			print '\b.',
			sys.stdout.flush()
			result_unfam[j*10:(j+1)*10] = learning_trials(protocol = 'Piron', trials = 10, debugging = False, trained = True, save = True, familiar = False)
			print '\b.',
			sys.stdout.flush()

		print '   Done!'

		print '\n--------Testing Familiar with GPi--------'
		debug(RT = result_fam["RT"]["mot"], P = result_fam["P"])
		print
		print '--------Testing UnFamiliar with GPi--------'
		debug(RT = result_unfam["RT"]["mot"], P = result_unfam["P"])
		print

		file = folderTf  + '/All-Results' + "%03d" % (i+1) + '.npy'
		np.save(file,result_fam)
		file = folderTuf + '/All-Results' + "%03d" % (i+1) + '.npy'
		np.save(file,result_unfam)

		debug_learning(result["W"]["CTXcog"][-1], result["W"]["CTXmot"][-1], result["W"]["STR"][-1], result["Values"][-1])

		print
