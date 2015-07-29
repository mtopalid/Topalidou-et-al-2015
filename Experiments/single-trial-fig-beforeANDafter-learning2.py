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
	import os
	folder = '../Results/Single-Trial-History'
	if not os.path.exists(folder):
		os.makedirs(folder)


	reset(protocol = 'Guthrie')
	connections["GPI.cog -> THL.cog"].active = False
	connections["GPI.mot -> THL.mot"].active = False
	histor, time = trial(hist = True, protocol = 'Guthrie', cues_pres = 1, wholeFig = True)
	file = folder + '/Histor-BefLearn-NoGPi.npy'
	np.save(file,histor)
	file = folder + '/single-trial-BefLearn-NoGPi.pdf'
	if 1: display_ctx(histor, 3.0, file)
	hist, P = learning_trials(hist = True, protocol = 'Guthrie', wholeFig = True, less_trained_trials = 1)
	file = folder + '/Histor-AftLearn-NoGPi.npy'
	np.save(file,hist)
	file = folder + '/single-trial-AftLearn-NoGPi.pdf'
	if 1: display_ctx(hist, 3.0, file)

	# No cortical connectivity
	if 0:
		reset(protocol = 'Guthrie')
		connections["CTX.mot -> CTX.mot"].active = False
		connections["CTX.cog -> CTX.cog"].active = False
		connections["CTX.ass -> CTX.ass"].active = False
		connections["CTX.cog -> CTX.ass"].active = False
		connections["CTX.mot -> CTX.ass"].active = False
		connections["CTX.ass -> CTX.cog"].active = False
		connections["CTX.ass -> CTX.mot"].active = False
		histor, time = trial(hist = True, debugging = True, protocol = 'Guthrie', cues_pres = 1, wholeFig = True)
		file = folder + '/Histor-BefLearn-NoCtx.npy'
		np.save(file,histor)
		if 1: display_ctx(histor, 3.0, "single-trial-BefLearn-NoCtx.pdf")
		hist, P = learning_trials(hist = True, protocol = 'Guthrie')
		file = folder + '/Histor-AftLearn-NoCtx.npy'
		np.save(file,hist)
		if 1: display_ctx(hist, 3.0, "single-trial-AftLearn-NoCtx.pdf")



