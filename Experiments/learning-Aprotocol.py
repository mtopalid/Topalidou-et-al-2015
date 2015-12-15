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
	from task_a import Task_A

	reset()
	task = Task_A(n=n_trials)
	'''
	file = 'task.npy'
	np.save(file,task.trials)

	learning_trials(task)
	file = 'records.npy'
	np.save(file,task.records)
	'''
	learning_trials(task)
	print('Mean performance of the 25 first trials: ', np.array(task.records["best"][:25]).mean())
	print('Mean performance of the 25 last trials: ', np.array(task.records["best"][-25:]).mean())

	if 0:
		t = np.load('records.npy')
		print(t["RTmot"][-1])
		print(t["Wstr"][-1])
		print(t["Wmot"][-1])
		print(t["Wcog"][-1])
		print(t["CueValues"][-1])

	if 0: display_all(hist, 3.0)#, "single-trial-all.pdf")
	if 0: display_ctx(hist, 3.0)
	if 0: display_all(hist, 3.0)#, "single-trial-all.pdf")
