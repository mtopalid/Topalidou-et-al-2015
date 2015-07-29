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

folder = '../Results/C-Results-1-100'

file = folder + '/Performance.npy'
P = np.load(file).mean(axis=1)

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
X = 1+np.arange(len(P[0]))
Num_trials = np.zeros(len(P))
for i in range(len(P)):
	for j in range(24,len(P[1])-25):
		#print i,j
		if P[i,j:j+25].mean()>0.9:
			print i,j
			Num_trials[i] = j
			break
print P[0,:]
print Num_trials
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
