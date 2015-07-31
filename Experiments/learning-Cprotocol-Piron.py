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
	from task_cp import Task_C

	reverse_trial = input('\nAfter how many trials will be the reverse?\n')

	reset()

	task = Task_C(n=n_reverse_trials, r = reverse_trial)
	learning_trials(task, trials = n_reverse_trials)


	print 'Mean performance of the 25 last trials: ', np.array(task.records["best"]).mean()
	if 0: display_all(hist, 3.0)#, "single-trial-all.pdf")
	if 0: display_ctx(hist, 3.0)
	if 0: display_all(hist, 3.0)#, "single-trial-all.pdf")
