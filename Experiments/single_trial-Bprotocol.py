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
	from task_b import Task_B

	cues_pres = 1#input('\nDo you want to present cues?\nChoose 1 for True or 0 for False\n')
	reset()
	task = Task_B(n=6)
	result = results(n_trials = 2)
	task1= task[:6]
	time = trial(result, task1, hist = True, debugging = True, cues_pres = cues_pres, wholeFig = True)
	histor = history()
	#print task1.records
	task2 = task[6:]
	time = trial(result, task2, hist = True, debugging = True, cues_pres = cues_pres, wholeFig = True)
	histor = history()
	#print task2.records
	#print task.records
	# Make GPi lesion
	#connections["GPI.cog -> THL.cog"].active = False
	#connections["GPI.mot -> THL.mot"].active = Falsereset(protocol = 'Guthrie')

	if 1: display_ctx(histor, 3.0)
	if 0: display_ctx(histor, 3.0, "single-trial-NoBG.pdf")
	if 0: display_all(histor, 3.0)#, "single-trial-all.pdf")
