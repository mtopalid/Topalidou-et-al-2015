# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
# -----------------------------------------------------------------------------

# Simulate number of experiments that is given in parameters.py of the different
# models. Each simulation is a number of trials under Guthrie protocol.
# -----------------------------------------------------------------------------

if __name__ == "__main__":

	temp = '../cython/'
	import sys
	sys.path.append(temp)
	import numpy as np
	import os
	from model import *
	from learning import *
	from testing import *
	from parameters import *
	folder = '../Results/C-Results-1-100'


	reverse = 1
	reverse_all = 1

	start = input('First reverse after how many trials?\n')
	print start
	finish = input('Last reverse after how many trials?\n')
	print finish


	for j in range (start,finish+1):
		print 'Reverse after: ', j
		print
		folder += '/Reverse' + str(j)
		if not os.path.exists(folder):
			os.makedirs(folder)
		for i in range(simulations):
			print 'Simulation: ', i + 1
			reset(protocol = 'Guthrie', ntrials = n_reverse_trials)
			global cues_cog, cues_mot
			cues_cog, cues_mot = trials_cues(protocol = 'Guthrie', ntrials = n_reverse_trials)

			history, P, Cvalues, wCog, wMot, wStr, RT_cg, RT_mot, R, ch, ch_cog, ch_mot = learning_trials(inversable = reverse, reverse_all = reverse_all, reverse_trial = j, protocol = 'Guthrie', trials = n_reverse_trials, debugging = False, trained = True, hist = True, save = True)


			file = folder + '/HistoryOfStructures' + str(i) + '.npy'
			np.save(file,np.array(history))
			file = folder + '/Trials_cues_cog' + str(i) + '.npy'
			np.save(file,cues_cog)
			file = folder + '/Trials_cues_mot' + str(i) + '.npy'
			np.save(file,cues_mot)
			file = folder + '/Cvalues' + str(i) + '.npy'
			np.save(file,np.array(Cvalues))
			file = folder + '/wCog' + str(i) + '.npy'
			np.save(file,np.array(wCog))
			file = folder + '/wMot' + str(i) + '.npy'
			np.save(file,np.array(wMot))
			file = folder + '/wStr' + str(i) + '.npy'
			np.save(file,np.array(wStr))
			file = folder + '/RT_cg' + str(i) + '.npy'
			np.save(file,np.array(RT_cg))
			file = folder + '/RT_mot' + str(i) + '.npy'
			np.save(file,np.array(RT_mot))
			file = folder + '/R' + str(i) + '.npy'
			np.save(file,np.array(R))
			file = folder + '/ch' + str(i) + '.npy'
			np.save(file,np.array(ch))
			file = folder + '/ch_cog' + str(i) + '.npy'
			np.save(file,np.array(ch_cog))
			file = folder + '/ch_mot' + str(i) + '.npy'
			np.save(file,np.array(ch_mot))


		print




