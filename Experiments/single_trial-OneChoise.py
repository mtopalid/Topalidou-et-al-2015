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

	reset(protocol = 'OneChoice')
	# Make GPi lesion
	#connections["GPI.cog -> THL.cog"].active = False
	#connections["GPI.mot -> THL.mot"].active = False
	global cues_cog, cues_mot
	cues_cog, cues_mot = trials_cues(protocol = 'OneChoice')
	#print cues_cog
	result = results(n_trials = 1)
	histor, time = trial(result, hist = True, debugging = True, protocol = 'OneChoice', wholeFig = True)
	if 1: display_ctx(histor, 3.0)
	if 0: display_ctx(histor, 3.0, "single-trial-NoBG.pdf")
	if 0: display_all(histor, 3.0)#, "single-trial-all.pdf")
