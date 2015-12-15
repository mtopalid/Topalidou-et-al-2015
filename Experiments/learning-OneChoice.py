# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
# -----------------------------------------------------------------------------

# Testing learning for each model under Guthrie protocol
# -----------------------------------------------------------------------------
if __name__ == "__main__":
	temp = '../cython/'
	import sys
	sys.path.append(temp)
	from model import *
	from display import *
	from learning import *

	reset(protocol = 'OneChoice')
	global cues_cog, cues_mot
	cues_cog, cues_mot = trials_cues(protocol = 'OneChoice', perc1 = 0.05, perc2 = 0.95)
	hist, P = learning_trials(trials = n_trials, hist = True, protocol = 'OneChoice', debugging = False, debug_simulation = True)
	debug_learning(connections["CTX.cog -> CTX.ass"].weights, connections["CTX.mot -> CTX.ass"].weights, connections["CTX.cog -> STR.cog"].weights, CUE["value"])
	print()
	print()
	print()
	global learning_cues_cog, testing_cues_cog_fam, testing_cues_cog_unfam, learning_cues_mot, testing_cues_mot_fam, testing_cues_mot_unfam
	learning_cues_cog, testing_cues_cog_fam, testing_cues_cog_unfam, learning_cues_mot, testing_cues_mot_fam, testing_cues_mot_unfam = trials_cues(protocol = 'Piron', ltrials = 10, ttrials = 10)
	result = results(n_trials = 1)

	for i in range(10):
		hist, time = trial(result, hist = True, debugging = True, protocol = 'Piron', wholeFig = True, learn = True)

	if 0: display_all(hist, 3.0)#, "single-trial-all.pdf")
	if 0: display_ctx(hist, 3.0)
	if 0: display_all(hist, 3.0)#, "single-trial-all.pdf")
