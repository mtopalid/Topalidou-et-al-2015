# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
# -----------------------------------------------------------------------------

# Evolution of single trial with Guthrie protocol
# -----------------------------------------------------------------------------

if __name__ == "__main__":

	temp = '../cython/'
	import sys
	sys.path.append(temp)
	from model import *
	from display import *
	from trial import *
	from task_a import Task_A

	cues_pres = 1#input('\nDo you want to present cues?\nChoose 1 for True or 0 for False\n')
	reset()
	task = Task_A(n=6)
	result = results(n_trials = 1)
	time = trial(result, task, hist = True, debugging = True, cues_pres = cues_pres, wholeFig = True)
	histor = history()
	if 1: display_ctx(histor, 3.0)
	if 0: display_ctx(histor, 3.0, "single-trial-NoBG.pdf")
	#if 1: display_all(histor, 3.0)#, "single-trial-all.pdf")
