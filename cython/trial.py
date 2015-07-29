# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
#				Nicolas Rougier  (Nicolas.Rougier@inria.fr)
# -----------------------------------------------------------------------------
import numpy as np
from model import *
from display import *
from parameters import *

def trial(result, reverse = False, reverse_all = True, cues_pres = True, hist = False, f = None, learn = True, debugging = False, trial_n = 0, protocol = 'Piron', familiar = True, NoMove = [], wholeFig = False, Piron_learning = False):

	reset_activities()
	reset_history()
	ct = None
	cog_time = None
	time = None
	for i in xrange(  0, 500):
		iterate(dt)
		if CTX.cog.delta > 20 and not ct:
			ct = 1
		if CTX.cog.delta > threshold and not cog_time:
			cog_time=i-500
	if cues_pres:
		set_trial(n=2, trial = trial_n, protocol = protocol, familiar = familiar, Piron_learning = Piron_learning)
	for i in xrange(500,duration):
		iterate(dt)

		# Test if a decision has been made
		if CTX.cog.delta > threshold and not cog_time:
			cog_time = i - 500
			result["RT"]["cog"][trial_n]  = cog_time
		if CTX.mot.delta > decision_threshold and not time:
			time = (i-500)
			result["RT"]["mot"][trial_n]  = time
		if time and cog_time:
			if protocol == 'OneChoice':
				process(n = 1, reverse = reverse, reverse_all = reverse_all, learn = learn, result = result[trial_n])
			else:
				process(reverse = reverse, reverse_all = reverse_all, learn = learn, result = result[trial_n])
			result["W"]["STR"][trial_n] 	= connections["CTX.cog -> STR.cog"].weights
			result["W"]["CTXcog"][trial_n] 	= connections["CTX.cog -> CTX.ass"].weights
			result["W"]["CTXmot"][trial_n]	= connections["CTX.mot -> CTX.ass"].weights
			result["Values"][trial_n]		= CUE["value"]
			if 0:#ch[-1] is None:
				mot_choice = np.argmax(CTX.mot.U)
				cog_choice = np.argmax(CTX.cog.U)
				print 'Wrong choice... \nMotor choice: %d\nCognitive choice: %d' % (mot_choice,cog_choice)
				print Cue["mot"][:n], CUE["cog"][:n]
			if debugging:
				if protocol == 'OneChoice':
					debug1ch(RT = np.array(time), cgchoice = result["Choice"]["ch"][trial_n], c1 = CUE["cog"][0], m1 = CUE["mot"][0],P = result["P"][trial_n])
				else:
					debug(reverse = reverse, reverse_all = reverse_all, RT = np.array(time), cgchoice = result["Choice"]["ch"][trial_n], c1 = CUE["cog"][:n][0], c2 = CUE["cog"][:n][1], m1 = CUE["mot"][:n][0], m2 = CUE["mot"][:n][1],P = result["P"][trial_n])
				if learn:
					debug_learning(connections["CTX.cog -> CTX.ass"].weights, connections["CTX.mot -> CTX.ass"].weights, connections["CTX.cog -> STR.cog"].weights, CUE["value"])
				print
				debugging = False
			#if not wholeFig:
			if hist:
				histor = history()
				return histor, time
			else:
				return time
	time = 2500
	#if not wholeFig:
	if debugging:
		print 'Trial Failed!'
		print 'NoMove trial: ', NoMove

	if hist:
		histor = history()
		return histor, time
	else:
		return time
