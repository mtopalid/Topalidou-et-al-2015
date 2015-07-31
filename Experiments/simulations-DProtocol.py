# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
# -----------------------------------------------------------------------------

# Simulate number of experiments that is given in parameters.py of the different
# models. Each simulation is a number of trials under Piron protocol.
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
	from task_b import Task_B

	folder = '../Results/D'
	if not os.path.exists(folder):
		os.makedirs(folder)

	folderL = folder + '/Learning'
	if not os.path.exists(folderL):
		os.makedirs(folderL)
	folderTf = folder + '/Testing_fam'
	if not os.path.exists(folderTf):
		os.makedirs(folderTf)
	folderTuf = folder + '/Testing_unfam'
	if not os.path.exists(folderTuf):
		os.makedirs(folderTuf)
	folderTfnG = folder + '/Testing_fam_NoGPi'
	if not os.path.exists(folderTfnG):
		os.makedirs(folderTfnG)
	folderTufnG = folder + '/Testing_unfam_NoGPi'
	if not os.path.exists(folderTufnG):
		os.makedirs(folderTufnG)


	for i in range(simulations):
		print 'Experiment: ', i + 1

		reset()

		print '-----------------Learning Phase----------------'
		# Formation of Habits
		task = Task_B(n=n_learning_trials)
		task = task[:n_learning_trials]
		learning_trials(task, trials = n_learning_trials, debugging = False, debug_simulation = True)

		file = folderL + '/Cues' + "%03d" % (i+1) + '.npy'
		np.save(file,task.trials)
		file = folderL + '/Records' + "%03d" % (i+1) + '.npy'
		np.save(file,task.records)
		print "Mean performance of 30 last trials	: %.1f %%\n" %(np.array(task.records["best"][-30:]).mean()*100)
		print "Mean RT								: %.1f ms\n" %(np.array(task.records["RTmot"][-30:]).mean())
		debug_learning(task.records["Wcog"][-1], task.records["Wmot"][-1], task.records["Wstr"][-1], task.records["CueValues"][-1])


		print '\n\n-----------------Testing Phase----------------'
		#f.write('\n\n\n-----------------Testing Phase----------------')
		# Make GPI lesion and Testing changing between familiar and unfamiliar cues every 10 trials
		connections["GPI.cog -> THL.cog"].active = False
		connections["GPI.mot -> THL.mot"].active = False


		task = Task_B(n=n_testing_trials)
		steps = n_testing_trials/10
		print 'Starting   ',
		for j in range(n_testing_trials/10):

			taskf = task[j*10:(j+1)*10]
			learning_trials(taskf, trials = 10, debugging = False)
			print '\b.',
			sys.stdout.flush()
			taskf = task[n_testing_trials+j*10:n_testing_trials+(j+1)*10]
			learning_trials(taskf, trials = 10, debugging = False)
			print '\b.',
			sys.stdout.flush()
		print '   Done!'
		print '\n--------Testing Familiar without GPi--------'
		print "Mean performance	: %.1f %%\n" %(np.array(task.records["best"][:n_testing_trials]).mean()*100)
		print "Mean RT			: %.1f ms\n" %(np.array(task.records["RTmot"][:n_testing_trials]).mean())
		print
		print '--------Testing UnFamiliar without GPi--------'
		print "Mean performance	: %.1f %%\n" %(np.array(task.records["best"][n_testing_trials:]).mean()*100)
		print "Mean RT			: %.1f ms\n" %(np.array(task.records["RTmot"][n_testing_trials:]).mean())
		print

		file = folderTfnG + '/Cues' + "%03d" % (i+1) + '.npy'
		np.save(file,task.trials[:n_testing_trials])
		file = folderTfnG + '/Records' + "%03d" % (i+1) + '.npy'
		np.save(file,task.records[:n_testing_trials])
		file = folderTufnG + '/Cues' + "%03d" % (i+1) + '.npy'
		np.save(file,task.trials[n_testing_trials:])
		file = folderTufnG + '/Records' + "%03d" % (i+1) + '.npy'
		np.save(file,task.records[n_testing_trials:])

		#Reactivation of GPi and Testing  changing between familiar and unfamiliar cues every 10 trials
		connections["GPI.cog -> THL.cog"].active = True
		connections["GPI.mot -> THL.mot"].active = True

		task = Task_B(n=n_testing_trials)
		steps = n_testing_trials/10
		print 'Starting   ',
		for j in range(n_testing_trials/10):

			taskf = task[j*10:(j+1)*10]
			learning_trials(taskf, trials = 10, debugging = False)
			print '\b.',
			sys.stdout.flush()
			taskf = task[n_testing_trials+j*10:n_testing_trials+(j+1)*10]
			learning_trials(taskf, trials = 10, debugging = False)
			print '\b.',
			sys.stdout.flush()
		print '   Done!'
		print '\n--------Testing Familiar with GPi--------'
		print "Mean performance	: %.1f %%\n" %(np.array(task.records["best"][:n_testing_trials]).mean()*100)
		print "Mean RT			: %.1f ms\n" %(np.array(task.records["RTmot"][:n_testing_trials]).mean())
		print
		print '--------Testing UnFamiliar with GPi--------'
		print "Mean performance	: %.1f %%\n" %(np.array(task.records["best"][n_testing_trials:]).mean()*100)
		print "Mean RT			: %.1f ms\n" %(np.array(task.records["RTmot"][n_testing_trials:]).mean())
		print

		file = folderTf + '/Cues' + "%03d" % (i+1) + '.npy'
		np.save(file,task.trials[:n_testing_trials])
		file = folderTf + '/Records' + "%03d" % (i+1) + '.npy'
		np.save(file,task.records[:n_testing_trials])
		file = folderTuf + '/Cues' + "%03d" % (i+1) + '.npy'
		np.save(file,task.trials[n_testing_trials:])
		file = folderTuf + '/Records' + "%03d" % (i+1) + '.npy'
		np.save(file,task.records[n_testing_trials:])

