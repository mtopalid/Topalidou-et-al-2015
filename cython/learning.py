# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
# -----------------------------------------------------------------------------

import numpy as np
import random
from trial import *
from parameters import *
import sys


def learning(result, reverse = False, reverse_all = True, trial_n = 0, debugging = True, protocol = 'Piron', familiar = True, learn = True, hist = False, Piron_learning = False):
	if hist:
		histor, time = trial(result, reverse = reverse, reverse_all = reverse_all, trial_n = trial_n, learn = learn, protocol = protocol, hist = hist, familiar = familiar, debugging = False, Piron_learning = Piron_learning)
	else:
		time = trial(result, reverse = reverse, reverse_all = reverse_all, trial_n = trial_n, learn = learn, protocol = protocol, hist = hist, familiar = familiar, debugging = False, Piron_learning = Piron_learning)

	if debugging:
			if protocol == 'OneChoice':
				debug1ch(RT = result["RT"]["mot"][:trial_n+1], cgchoice = result["Choice"]["ch"][trial_n], c1 = CUE["cog"][0], m1 = CUE["mot"][0],P = result["P"][:trial_n+1])

			else:
				debug(reverse = reverse, reverse_all = reverse_all, RT = result["RT"]["mot"][:trial_n+1], cgchoice = result["Choice"]["ch"][trial_n], c1 = CUE["cog"][:n][0], c2 = CUE["cog"][:n][1], m1 = CUE["mot"][:n][0], m2 = CUE["mot"][:n][1], P = result["P"][:trial_n+1])

			if learn:
				debug_learning(connections["CTX.cog -> CTX.ass"].weights, connections["CTX.mot -> CTX.ass"].weights, connections["CTX.cog -> STR.cog"].weights, CUE["value"])

			print


	if hist:
		return histor
		if 0:
			print "Mean Cognitive Striatal activity: [",
			for i in range(n):
				print np.amax(histor["STR"]["cog"][:,i]),

				#print histor["STR"]["cog"][np.nonzero(histor["STR"]["cog"][:,i]),i].mean(),
				#print histor["STR"]["cog"][:,i].mean(),
			print "]"
			print "Mean Motor Striatal activity: [",
			for i in range(n):
				print histor["STR"]["mot"][np.nonzero(histor["STR"]["mot"][:,i]),i].mean(),
				#print histor["STR"]["mot"][:,i].mean(),
			print "]"
			return histor
	else:
		return

def learning_trials(inversable = 0, reverse_all = True, reverse_trial = 50, less_trained_trials = 20, f = None, hist = False, trials = n_trials, debugging = True, save = False, protocol = 'Piron', familiar = True, type = 'learning', W_COG = None, W_MOT = None, W_STR = None, trained = False, j = -1, Piron_learning = False, debug_simulation = False, learn = True):
# type = 'learning' isn't needed because if you don't want reset of protocol or training you just put trained = True
	result = results(n_trials = trials)
	if debug_simulation:
		steps = trials/10
		print 'Starting   ',
	while not trained:
		result = results(n_trials = trials)
		reset(protocol = protocol, ntrials = trials, W_COG = W_COG, W_MOT = W_MOT, W_STR = W_STR)
		reverse = False
		for j in range(less_trained_trials):

			if debugging:
				print 'Trial: ', j + 1
			if hist:
				histor = learning(result, trial_n = j, debugging = debugging, protocol = protocol, familiar = familiar, hist = hist, Piron_learning = Piron_learning, learn = learn)
			else:
				learning(result, trial_n = j, debugging = debugging, protocol = protocol, familiar = familiar, hist = hist, Piron_learning = Piron_learning, learn = learn)
			result["W"]["STR"][j] 		= connections["CTX.cog -> STR.cog"].weights
			result["W"]["CTXcog"][j] 	= connections["CTX.cog -> CTX.ass"].weights
			result["W"]["CTXmot"][j]	= connections["CTX.mot -> CTX.ass"].weights
			result["Values"][j]			= CUE["value"]

			if debug_simulation:
				if j%steps == 0:
					print '\b.',
					sys.stdout.flush()


		if np.mean(result["P"][:j]) > 0.70:
				trained = True

	else:
		reverse = False

		for i in range(j+1, trials):
			if inversable == 1:
				if i == reverse_trial:
					if reverse_all:
						if protocol == 'Piron':
							CUE["reward"] = rewards_Piron_reverse
						elif protocol == 'Guthrie':
							CUE["reward"] = rewards_Guthrie_reverse_all
					else:
						CUE["reward"] = rewards_Guthrie_reverse_middle
					reverse = True
			elif inversable == 2:
				if i == reverse_trial:
					CUE["reward"] = 0., 0., 0., 0.
				reverse = False
			else:
				reverse = False
			if debugging:
				print 'Trial: ', i + 1
			if hist:
				histor = learning(result, reverse = reverse, reverse_all = reverse_all, trial_n = i, debugging = debugging, protocol = protocol, familiar = familiar, hist = hist, Piron_learning = Piron_learning, learn = learn)
			else:
				learning(result, reverse = reverse, reverse_all = reverse_all, trial_n = i, debugging = debugging, protocol = protocol, familiar = familiar, hist = hist, Piron_learning = Piron_learning, learn = learn)

			result["W"]["STR"][i] 		= connections["CTX.cog -> STR.cog"].weights
			result["W"]["CTXcog"][i] 	= connections["CTX.cog -> CTX.ass"].weights
			result["W"]["CTXmot"][i]	= connections["CTX.mot -> CTX.ass"].weights
			result["Values"][i]			= CUE["value"]

			if debug_simulation:
				if i%steps == 0:
					print '\b.',
					sys.stdout.flush()
		if debug_simulation:
			print '   Done!'
		if debugging:
			debug(RT = result["RT"]["mot"], P = result["P"])
			debug_learning(result["W"]["CTXcog"][-1], result["W"]["CTXmot"][-1], result["W"]["STR"][-1], result["Values"][-1])
	if save:
		if hist:
			return histor, result
		else:
			return result
	if hist:
		return histor, result["P"]
	else:
		return result["P"]
