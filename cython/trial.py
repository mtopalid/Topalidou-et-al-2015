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

def trial(reverse = False, reverse_all = True, cues_pres = True, hist = False, f = None, learn = False, debugging = False, trial_n = 0, protocol = 'Piron', familiar = True, NoMove = [], ct = [], cog_time = [], P = [], wholeFig = False):

	reset_activities()
	reset_history()
	ct = None
	cog_time = None
	for i in xrange(  0, 500):
		iterate(dt)
		if CTX.cog.delta > 20 and not ct:
			ct = 1
		if CTX.cog.delta > threshold and not cog_time:
			cog_time=i-500
	if cues_pres:
		set_trial(n=2, trial = trial_n, protocol = protocol, familiar = familiar)
	for i in xrange(500,duration):
		iterate(dt)

		# Test if a decision has been made
		if CTX.cog.delta > threshold and not cog_time:
			cog_time=i-500
		if CTX.mot.delta > decision_threshold:
			time = (i-500)
			choice = process(reverse = reverse, reverse_all = reverse_all, learning = learn, P = P)
			if choice is None:
				mot_choice = np.argmax(CTX.mot.U)
				cog_choice = np.argmax(CTX.cog.U)
				print 'Wrong choice... \nMotor choice: %d\nCognitive choice: %d' % (mot_choice,cog_choice)
				print Cue["mot"][:n], CUE["cog"][:n]
			if not wholeFig:
				if debugging:
					debug(reverse = reverse, reverse_all = reverse_all, RT = time, cgchoice = choice, c1 = CUE["cog"][:n][0], c2 = CUE["cog"][:n][1], m1 = CUE["mot"][:n][0], m2 = CUE["mot"][:n][1],P = P)
					if learn:
						debug_learning(connections["CTX.cog -> CTX.ass"].weights, connections["CTX.mot -> CTX.ass"].weights, connections["CTX.cog -> STR.cog"].weights, CUE["value"],f = f)
					print
				if hist:
					histor = history()
					return histor, time
				return time
	time = 2500
	if not wholeFig:
		if debugging:
			print 'Trial Failed!'
			print 'NoMove trial: ', NoMove
	if hist:
		histor = history()
		return histor, time
	else:
		return time
