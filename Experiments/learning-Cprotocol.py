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


	reset(protocol = 'Guthrie')
	hist, P = learning_trials(inversable = reverse, reverse_all = reverse_all, reverse_trial = reverse_trial, hist = True, protocol = 'Guthrie', trials = n_trials, less_trained_trials = 5)
	if 0: display_ctx(hist, 3.0)
