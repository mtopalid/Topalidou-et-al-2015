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
	from model2 import *
	from display import *
	from learning2 import *

	reset(protocol = 'Piron')
	global learning_cues_cog, testing_cues_cog_fam, testing_cues_cog_unfam, learning_cues_mot, testing_cues_mot_fam, testing_cues_mot_unfam
	learning_cues_cog, testing_cues_cog_fam, testing_cues_cog_unfam, learning_cues_mot, testing_cues_mot_fam, testing_cues_mot_unfam = trials_cues(protocol = 'Piron', ltrials = n_learning_trials, ttrials = n_testing_trials)

	P = learning_trials(trials = n_learning_trials, protocol = 'Piron', less_trained_trials = 5, Piron_learning = True)
	print
	print
	print 'Mean performance of the 25 first trials: ', np.array(P[:25]).mean()
	print 'Mean performance of the 25 last trials: ', np.array(P[-25:]).mean()
	print
	print

 	if 0:
		print "Familiar cues"
		P = learning_trials(trials = n_testing_trials, protocol = 'Piron', trained = True)
		print
		print
		print 'Mean performance of the 25 first trials: ', np.array(P[:25]).mean()
		print 'Mean performance of the 25 last trials: ', np.array(P[-25:]).mean()
		print
		print
		print "UnFamiliar cues"
		P = learning_trials(trials = n_testing_trials, protocol = 'Piron', trained = True, familiar = False)
		print
		print
		print 'Mean performance of the 25 first trials: ', np.array(P[:25]).mean()
		print 'Mean performance of the 25 last trials: ', np.array(P[-25:]).mean()
		print
		print


		connections["CTX.cog -> CTX.ass"].weights[2:] = weights(2, 0.00005)#0.5*np.ones(4)
		connections["CTX.cog -> STR.cog"].weights[2:] = weights(2)
		CUE["value"][2:]  = 0.5

 	if 1:
		connections["GPI.cog -> THL.cog"].active = False
		connections["GPI.mot -> THL.mot"].active = False
		print "Familiar cues"
		P = learning_trials(trials = n_testing_trials, protocol = 'Piron', trained = True)
		print
		print
		print 'Mean performance of the 25 first trials: ', np.array(P[:25]).mean()
		print 'Mean performance of the 25 last trials: ', np.array(P[-25:]).mean()
		print
		print
		print "UnFamiliar cues"
		P = learning_trials(trials = n_testing_trials, protocol = 'Piron', trained = True, familiar = False)
		print
		print
		print 'Mean performance of the 25 first trials: ', np.array(P[:25]).mean()
		print 'Mean performance of the 25 last trials: ', np.array(P[-25:]).mean()
		print
		print
	if 0: display_all(hist, 3.0)#, "single-trial-all.pdf")
	if 0: display_ctx(hist, 3.0)
	if 0: display_all(hist, 3.0)#, "single-trial-all.pdf")
