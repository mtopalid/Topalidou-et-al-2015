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



RTboxplot 		= True
RTdifference	= True
RTcog_mot		= True


suptitle += 'Protocol: A'
#reverse = input('\nDo you want to have an reverse of Probabilities during the simulation or stop rewards?\nChoose 2 for Stopping Reward, 1 for reverse of Probabilities or 0 for No change\n')
folder = '../Results/A'
title = ''
Wstr = np.zeros((simulations, n_trials, 4))
Wcog = np.zeros((simulations, n_trials, 4))
Wmot = np.zeros((simulations, n_trials, 4))
for i in range(simulations):
	file = folder + '/Records' + "%03d" % (i+1) + '.npy'
	temp = np.load(file)
	Wstr[i,:] = temp["Wstr"]
	Wcog[i,:] = temp["Wcog"]
	Wmot[i,:] = temp["Wmot"]
file = folder+ '/MeanWeights-Str.npy'
np.save(file, Wstr.mean(axis=0))
file = folder+ '/MeanWeights-Cog.npy'
np.save(file, Wcog.mean(axis=0))
file = folder+ '/MeanWeights-Mot.npy'
np.save(file, Wmot.mean(axis=0))

X = 1 + np.arange(n_trials)

fig = plt.figure(figsize=(18,6),facecolor="w")#
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

mean = Wstr.mean(axis=0)
print("striatal	", mean[-1,0], mean[-1,1], mean[-1,2], mean[-1,3])
std  = Wstr.std(axis = 0)
plt.plot(X, mean[:,0], c='b', lw=1.5, zorder=30)
plt.plot(X, mean[:,0]+std[:,0], c='.5',lw=.5, zorder=20)
plt.plot(X, mean[:,0]-std[:,0], c='.5',lw=.5, zorder=20)
plt.fill_between(X, mean[:,0]+std[:,0],
					mean[:,0]-std[:,0], color='b', alpha=.05, zorder=10)

plt.plot(X, mean[:,1], c='r', lw=1.5, zorder=30)
plt.plot(X, mean[:,1]+std[:,1], c='.5',lw=.5, zorder=20)
plt.plot(X, mean[:,1]-std[:,1], c='.5',lw=.5, zorder=20)
plt.fill_between(X, mean[:,1]+std[:,1],
					mean[:,1]-std[:,1], color='r', alpha=.05, zorder=10)

plt.plot(X, mean[:,2], c='g', lw=1.5, zorder=30)
plt.plot(X, mean[:,2]+std[:,2], c='.5',lw=.5, zorder=20)
plt.plot(X, mean[:,2]-std[:,2], c='.5',lw=.5, zorder=20)
plt.fill_between(X, mean[:,2]+std[:,2],
					mean[:,2]-std[:,2], color='g', alpha=.05, zorder=10)

plt.plot(X, mean[:,3], c='m', lw=1.5, zorder=30)
plt.plot(X, mean[:,3]+std[:,3], c='.5',lw=.5, zorder=20)
plt.plot(X, mean[:,3]-std[:,3], c='.5',lw=.5, zorder=20)
plt.fill_between(X, mean[:,3]+std[:,3],
					mean[:,3]-std[:,3], color='m', alpha=.05, zorder=10)


plt.ylabel("Striatal Weights")
plt.xlabel("Trial number")
file = folder + "/Weights-Str.png"
fig.savefig(file)

fig = plt.figure(figsize=(18,6),facecolor="w")#
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

mean = Wcog.mean(axis=0)
print("cognitive	", mean[-1,0], mean[-1,1], mean[-1,2], mean[-1,3])
std  = Wcog.std(axis = 0)
plt.plot(X, mean[:,0], c='b', lw=1.5, zorder=30)
plt.plot(X, mean[:,0]+std[:,0], c='.5',lw=.5, zorder=20)
plt.plot(X, mean[:,0]-std[:,0], c='.5',lw=.5, zorder=20)
plt.fill_between(X, mean[:,0]+std[:,0],
					mean[:,0]-std[:,0], color='b', alpha=.05, zorder=10)

plt.plot(X, mean[:,1], c='r', lw=1.5, zorder=30)
plt.plot(X, mean[:,1]+std[:,1], c='.5',lw=.5, zorder=20)
plt.plot(X, mean[:,1]-std[:,1], c='.5',lw=.5, zorder=20)
plt.fill_between(X, mean[:,1]+std[:,1],
					mean[:,1]-std[:,1], color='r', alpha=.05, zorder=10)

plt.plot(X, mean[:,2], c='g', lw=1.5, zorder=30)
plt.plot(X, mean[:,2]+std[:,2], c='.5',lw=.5, zorder=20)
plt.plot(X, mean[:,2]-std[:,2], c='.5',lw=.5, zorder=20)
plt.fill_between(X, mean[:,2]+std[:,2],
					mean[:,2]-std[:,2], color='g', alpha=.05, zorder=10)

plt.plot(X, mean[:,3], c='m', lw=1.5, zorder=30)
plt.plot(X, mean[:,3]+std[:,3], c='.5',lw=.5, zorder=20)
plt.plot(X, mean[:,3]-std[:,3], c='.5',lw=.5, zorder=20)
plt.fill_between(X, mean[:,3]+std[:,3],
					mean[:,3]-std[:,3], color='m', alpha=.05, zorder=10)


plt.ylabel("Cortical Cognitive Weights")
plt.xlabel("Trial number")
file = folder + "/Weights-Cog.png"
fig.savefig(file)

fig = plt.figure(figsize=(18,6),facecolor="w")#
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

mean = Wmot.mean(axis=0)
print("motor	", mean[-1,0], mean[-1,1], mean[-1,2], mean[-1,3])
std  = Wmot.std(axis = 0)
plt.plot(X, mean[:,0], c='b', lw=1.5, zorder=30)
plt.plot(X, mean[:,0]+std[:,0], c='.5',lw=.5, zorder=20)
plt.plot(X, mean[:,0]-std[:,0], c='.5',lw=.5, zorder=20)
plt.fill_between(X, mean[:,0]+std[:,0],
					mean[:,0]-std[:,0], color='b', alpha=.05, zorder=10)

plt.plot(X, mean[:,1], c='r', lw=1.5, zorder=30)
plt.plot(X, mean[:,1]+std[:,1], c='.5',lw=.5, zorder=20)
plt.plot(X, mean[:,1]-std[:,1], c='.5',lw=.5, zorder=20)
plt.fill_between(X, mean[:,1]+std[:,1],
					mean[:,1]-std[:,1], color='r', alpha=.05, zorder=10)

plt.plot(X, mean[:,2], c='g', lw=1.5, zorder=30)
plt.plot(X, mean[:,2]+std[:,2], c='.5',lw=.5, zorder=20)
plt.plot(X, mean[:,2]-std[:,2], c='.5',lw=.5, zorder=20)
plt.fill_between(X, mean[:,2]+std[:,2],
					mean[:,2]-std[:,2], color='g', alpha=.05, zorder=10)

plt.plot(X, mean[:,3], c='m', lw=1.5, zorder=30)
plt.plot(X, mean[:,3]+std[:,3], c='.5',lw=.5, zorder=20)
plt.plot(X, mean[:,3]-std[:,3], c='.5',lw=.5, zorder=20)
plt.fill_between(X, mean[:,3]+std[:,3],
					mean[:,3]-std[:,3], color='m', alpha=.05, zorder=10)


plt.ylabel("Cortical Motor Weights")
plt.xlabel("Trial number")
file = folder + "/Weights-Mot.png"
fig.savefig(file)
plt.show()
