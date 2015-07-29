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

	reset(protocol = 'Guthrie')
	global cues_cog, cues_mot
	cues_cog, cues_mot = trials_cues(protocol = 'Guthrie')
	hist, P = learning_trials(hist = True, protocol = 'Guthrie', less_trained_trials = 20)
	print 'Mean performance of the 25 first trials: ', np.array(P[:25]).mean()
	print 'Mean performance of the 25 last trials: ', np.array(P[-25:]).mean()
	if 0:
		result = learning_trials(protocol = 'Guthrie', save = True)
		print 'Mean performance of the 25 first trials: ', np.array(result["P"][:25]).mean()
		print 'Mean performance of the 25 last trials: ', np.array(result["P"][-25:]).mean()
		P = result["P"]
	#print P
	if 0: display_all(hist, 3.0)#, "single-trial-all.pdf")
	if 0: display_ctx(hist, 3.0)
	if 0: display_all(hist, 3.0)#, "single-trial-all.pdf")
