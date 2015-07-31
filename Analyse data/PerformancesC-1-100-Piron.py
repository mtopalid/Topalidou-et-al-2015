#!/usr/bin/env python
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

suptitle = 'Model: Topalidou\n'
path = '../cython/'
import sys
sys.path.append(path)

from parameters import *

def fitFunc(t, a, b, c):
    return a*np.exp(-b*t) + c

suptitle += 'Protocol: C'

folder = '../Results/C-1-100-Piron'

P = np.zeros((54, n_reverse_trials_Piron))

neverSavedBefore 	= True
SavedBefore			= False

if neverSavedBefore:
	p = np.zeros((simulations, n_reverse_trials_Piron))
	for j in range(1,55):
		f = folder + '/Reverse' + "%03d" % (j)
		print 'Reverse:' + "%03d" % (j)
		for i in range(simulations):
			file = f + '/All-Results' + "%03d" % (i+1) + '.npy'
			temp = np.load(file)
			p[i,:] = temp["P"]
		P[j-1,:] = p.mean(axis = 0)
		file = folder+ '/MeanPerformanceReverse' + "%03d" % (j) +'.npy'
		np.save(file, P[j-1,:])

if SavedBefore:
	for j in range(1,101):
		f = folder + '/MeanPerformanceReverse' + "%03d" % (j) +'.npy'
		P[j-1,:] = np.load(f)



fig = plt.figure(figsize=(18,6), facecolor="w")
ax = plt.subplot()
ax.patch.set_facecolor("w")

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_tick_params(direction="in")
ax.xaxis.set_tick_params(direction="in")
ax.yaxis.set_label_coords(-0.04, 0.5)
ax.xaxis.set_label_coords(0.5, -0.08)


Num_trials = np.zeros(len(P))

for i in range(len(P)):
	r = int(reverse[i])
	for j in range(r+1,len(P[1])-30):
		if P[i,j:j+30].mean()>0.9:
			Num_trials[i] = j-i-1
			break
print Num_trials
file = folder+ '/Num_trials_2_recover_0_9_performance.npy'
np.save(file, Num_trials)

X = 1 + np.arange(54)
plt.plot(X, Num_trials, c='b', lw=1.5, zorder=30)
plt.ylabel("Number of Trials to obtain Performances over 90%")
plt.xlabel("Number of Trials before Reverse of Reward Probabilities")

file = folder + "/Num_trials_2_recover_0_9_performance.png"
fig.savefig(file)
plt.show()
if 0:
	plt.plot(X, P[::,::].mean(axis=0), c='b', lw=1.5, zorder=30)
	plt.plot(X, P.mean(axis=0)+P.std(axis=0), c='.5',lw=.5, zorder=20)
	plt.plot(X, P.mean(axis=0)-P.std(axis=0), c='.5',lw=.5, zorder=20)
	plt.fill_between(X, P.mean(axis=0)+P.std(axis=0),
						P.mean(axis=0)-P.std(axis=0), color='b', alpha=.05, zorder=10)


	plt.ylabel("Proportion of optimum trials")
	plt.xlabel("Trial number")

	file = folder + "/Perfomances.png"
	fig.savefig(file)
	plt.show()
