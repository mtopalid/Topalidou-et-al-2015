# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
# -----------------------------------------------------------------------------

# Testing learning for each model under Piron protocol
# -----------------------------------------------------------------------------
if __name__ == "__main__":
	temp = '../cython/'
	import sys
	sys.path.append(temp)
	from model import *
	from display import *
	from learning import *

	reverse = 1
	reverse_trial = input('\nAfter how many trials will be the reverse?\n')
	reverse_all = 1

	Guthrie = False
	Piron 	= True

	if Guthrie:
		reset(protocol = 'Guthrie', ntrials = n_reverse_trials)
		global cues_cog, cues_mot
		cues_cog, cues_mot = trials_cues(protocol = 'Guthrie', ntrials = n_reverse_trials)
		hist, P = learning_trials(inversable = reverse, reverse_all = reverse_all, reverse_trial = reverse_trial, hist = True, protocol = 'Guthrie', trials = n_reverse_trials)

	if Piron:
		reset(protocol = 'Piron')
		global learning_cues_cog, learning_cues_mot
		learning_cues_cog, t, t, learning_cues_mot, t, t = trials_cues(protocol = 'Piron', ltrials = n_reverse_trials_Piron)

		P = learning_trials(inversable = reverse, reverse_all = reverse_all, reverse_trial = reverse_trial, trials = n_reverse_trials_Piron, hist = False, protocol = 'Piron', less_trained_trials = 5, Piron_learning = True)

	print 'Mean performance of the 25 last trials: ', np.array(P[-25:]).mean()
	if 0: display_all(hist, 3.0)#, "single-trial-all.pdf")
	if 0: display_ctx(hist, 3.0)
	if 0: display_all(hist, 3.0)#, "single-trial-all.pdf")
