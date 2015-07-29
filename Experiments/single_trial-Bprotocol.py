# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
# -----------------------------------------------------------------------------

# Evolution of single trial with Piron protocol
# -----------------------------------------------------------------------------

if __name__ == "__main__":
	temp = '../cython/'
	import sys
	sys.path.append(temp)
	from model import *
	from display import *
	from trial import *

	cues_pres = input('\nDo you want to present cues?\nChoose 1 for True or 0 for False\n')
	reset(protocol = 'Piron')
	# Make GPi lesion
	#connections["GPI.cog -> THL.cog"].active = False
	#connections["GPI.mot -> THL.mot"].active = Falsereset(protocol = 'Guthrie')
	global learning_cues_cog, testing_cues_cog_fam, testing_cues_cog_unfam, learning_cues_mot, testing_cues_mot_fam, testing_cues_mot_unfam
	learning_cues_cog, testing_cues_cog_fam, testing_cues_cog_unfam, learning_cues_mot, testing_cues_mot_fam, testing_cues_mot_unfam = trials_cues(protocol = 'Piron')
	result = results(n_trials = 1)
	histor, time = trial(result = result, hist = True, debugging = True, protocol = 'Piron', cues_pres = cues_pres, wholeFig = True)
	if 1: display_ctx(histor, 3.0)
	if 0: display_ctx(histor, 3.0, "single-trial-NoBG.pdf")
	if 0: display_all(histor, 3.0)#, "single-trial-all.pdf")
