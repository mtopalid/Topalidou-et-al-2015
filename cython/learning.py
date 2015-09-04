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

def learning(task, trial_n = 0, learn = True, debugging = True):

	time = trial(task, trial_n = trial_n, learn = learn, debugging = debugging)

	if debugging and learn:
		debug_learning(connections["CTX.cog -> CTX.ass"].weights, connections["CTX.mot -> CTX.ass"].weights, connections["CTX.cog -> STR.cog"].weights, CUE["value"])

	return

def learning_trials(task, trials = n_trials, learn = True, debugging = True, debug_simulation = False):
	if debug_simulation:
		steps = trials/10
		print '  Starting   ',

	for i in range(trials):

		learning(task, trial_n = i, learn = learn, debugging = debugging)

		if debug_simulation:
			if i%steps == 0:
				print '\b.',
				sys.stdout.flush()
	if debug_simulation:
		print '   Done!'
	if debugging:
		debug_learning(task.records["Wcog"][-1], task.records["Wmot"][-1], task.records["Wstr"][-1], task.records["CueValues"][-1])

	return
