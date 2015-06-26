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

	reset(protocol = 'Piron')
	connections["GPI.cog -> THL.cog"].active = False
	connections["GPI.mot -> THL.mot"].active = False
	hist, P = learning_trials(hist = True, protocol = 'Piron', trials = n_learning_trials, less_trained_trials = 5)
	connections["GPI.cog -> THL.cog"].active = True
	connections["GPI.mot -> THL.mot"].active = True
	hist, P = learning_trials(hist = True, protocol = 'Piron', trials = n_learning_trials, trained = True)
	if 0: display_ctx(P, 3.0)
	if 0: display_ctx(hist, 3.0)
