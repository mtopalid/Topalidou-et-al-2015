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

folder = '../Results/C-Results'
reverse = 1
reverse_trial = input('After how many trials is the reverse?\n')
reverse_all = input('\nThere is reverse to all probabilities or just the middle ones?\nChoose 1 for all or 0 for middle ones\n')
folder += '-reverse-after' + str(reverse_trial)
folder += 'all' if reverse_all else 'middle cues'#-NoCortLearn-HalfParam
title = 'reverse probabilities of\n'
title += 'all ' if reverse_all else 'middle '
title += 'cues after %s trials' %str(reverse_trial)

file = folder + '/Performance.npy'
P = np.load(file)
file = folder+ '/MeanPerformance.npy'
np.save(file, P)

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
plt.plot(X, P[::,::].mean(axis=0), c='b', lw=1.5, zorder=30)
plt.plot(X, P.mean(axis=0)+P.std(axis=0), c='.5',lw=.5, zorder=20)
plt.plot(X, P.mean(axis=0)-P.std(axis=0), c='.5',lw=.5, zorder=20)
plt.fill_between(X, P.mean(axis=0)+P.std(axis=0),
                    P.mean(axis=0)-P.std(axis=0), color='b', alpha=.05, zorder=10)


plt.ylabel("Proportion of optimum trials")
plt.xlabel("Trial number")
if 0:
	temp_title = 'Mean Performances'
	plt.title(temp_title, fontsize=12)
	plt.title(suptitle, loc='left', fontsize=12)
	plt.title(title, loc='right', fontsize=12)

file = folder + "/Perfomances.png"
fig.savefig(file)

file = folder + '/RT.npy'
RT = np.load(file)
file = folder+ '/RTmean.npy'
np.save(file, RT)

fig = plt.figure(figsize=(18,6), facecolor="w")
ax = plt.subplot()
ax.patch.set_facecolor("w")

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_tick_params(direction="in")
ax.xaxis.set_tick_params(direction="in")
ax.yaxis.set_label_coords(-0.05, 0.5)
ax.xaxis.set_label_coords(0.5, -0.08)
X = 1+np.arange(len(RT[0]))
plt.plot(X, RT[::,::].mean(axis=0), c='b', lw=1.5, zorder=30)
plt.plot(X, RT.mean(axis=0)+RT.std(axis=0), c='.5',lw=.5, zorder=20)
plt.plot(X, RT.mean(axis=0)-RT.std(axis=0), c='.5',lw=.5, zorder=20)
plt.fill_between(X, RT.mean(axis=0)+RT.std(axis=0),
                    RT.mean(axis=0)-RT.std(axis=0), color='b', alpha=.05, zorder=10)


plt.ylabel("Reaction Time (ms)")
plt.xlabel("Trial number")
if 0:
	temp_title = 'Mean Response Time'
	plt.title(temp_title, fontsize=12)
	plt.title(suptitle, loc='left', fontsize=12)
	plt.title(title, loc='right', fontsize=12)
file = folder + "/RT.png"
fig.savefig(file)
plt.show()
