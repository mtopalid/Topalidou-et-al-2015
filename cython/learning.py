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

def learning(reverse = False, reverse_all = True, f = None, trial_n = 0, debugging = True, protocol = 'Piron', familiar = True, learn = True, hist = False, P = [], RT = []):
	if hist:
		histor, time = trial(reverse = reverse, reverse_all = reverse_all, f = f, trial_n = trial_n, learn = learn, protocol = protocol, hist = hist, familiar = familiar, debugging = debugging, P = P)
	else:
		time = trial(reverse = reverse, reverse_all = reverse_all, f = f, trial_n = trial_n, learn = learn, protocol = protocol, hist = hist, familiar = familiar, debugging = debugging, P = P)
	RT.append(time)
	if not len(P) == trial_n+1:
		P.append(0)
	if hist:
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
		return histor, RT, P
	else:
		return RT, P

def learning_trials(inversable = 0, reverse_all = True, reverse_trial = 50, less_trained_trials = 20, f = None, hist = False, trials = n_trials, debugging = True, save = False, protocol = 'Piron', familiar = True, type = 'learning', W_COG = None, W_MOT = None, W_STR = None, trained = False, j = -1):
# type = 'learning' isn't needed because if you don't want reset of protocol or training you just put trained = True
	P, RT = [], []
	wCog = np.zeros((trials,n))
	wMot = np.zeros((trials,n))
	wStr = np.zeros((trials,n))
	while not trained:
		P, RT = [], []
		wCog = np.zeros((trials,n))
		wMot = np.zeros((trials,n))
		wStr = np.zeros((trials,n))
		reset(protocol = protocol, W_COG = W_COG, W_MOT = W_MOT, W_STR = W_STR)
		reverse = False
		for j in range(less_trained_trials):

			if debugging:
				print 'Trial: ', j + 1
			if hist:
				histor, RT, P = learning(f = f, trial_n = j, debugging = debugging, protocol = protocol, familiar = familiar, hist = hist, P = P, RT = RT)
			else:
				RT, P = learning(f = f, trial_n = j, debugging = debugging, protocol = protocol, familiar = familiar, hist = hist, P = P, RT = RT)

			wCog[j,:] = connections["CTX.cog -> CTX.ass"].weights
			wMot[j,:] = connections["CTX.mot -> CTX.ass"].weights
			wStr[j,:] = connections["CTX.cog -> STR.cog"].weights

		if np.mean(P) > 0.70:
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
				histor, RT, P = learning(reverse = reverse, reverse_all = reverse_all, f = f, trial_n = i, debugging = debugging, protocol = protocol, familiar = familiar, hist = hist, P = P, RT = RT)
			else:
				RT, P = learning(reverse = reverse, reverse_all = reverse_all, f = f, trial_n = i, debugging = debugging, protocol = protocol, familiar = familiar, hist = hist, P = P, RT = RT)
		if debugging:
			wCog[i,:] = connections["CTX.cog -> CTX.ass"].weights
			wMot[i,:] = connections["CTX.mot -> CTX.ass"].weights
			wStr[i,:] = connections["CTX.cog -> STR.cog"].weights
			debug(RT = RT, P = P)
			debug_learning(wCog[-1,:], wMot[-1,:], wStr[-1,:], cues_value = CUE["value"], f = f)
	if save:
		if hist:
			return histor, P, RT, wCog, wMot, wStr
		else:
			return P, RT, wCog, wMot, wStr
	if hist:
		return histor, P
	else:
		return P
