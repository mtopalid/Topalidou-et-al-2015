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
load = np.load(file)
MeanPerformance = load.mean(axis = 0)
mean =  MeanPerformance.mean()*100
file = folder+ '/MeanPerformance.npy'
np.save(file, MeanPerformance)

trials = np.linspace(1,MeanPerformance.shape[0]+1,MeanPerformance.shape[0])
#fitParams, fitCovariances = curve_fit(fitFunc, trials, MeanPerformance)

fig = plt.figure()
axes = fig.add_subplot(1,1,1)
axes.set_autoscale_on(False)
yticks = np.linspace(0,1,11)
axes.set_xbound(0,load.shape[1]+1)
axes.set_ybound(0,1.1)
axes.set_yticks(yticks)
axes.plot(trials, MeanPerformance)
#axes.plot(trials, fitFunc(trials, fitParams[0], fitParams[1], fitParams[2]), "r", linewidth = 3)

plt.ylabel("Proportion of optimum trials")
plt.xlabel("Trial number")
temp_title = 'Mean Performances'
plt.title(temp_title, fontsize=12)
plt.title(suptitle, loc='left', fontsize=12)
plt.title(title, loc='right', fontsize=12)

file = folder + "/Perfomances.png"
fig.savefig(file)

file = folder + '/RT.npy'
load = np.load(file)
RTmean = load.mean(axis = 0)
file = folder+ '/RTmean.npy'
np.save(file, RTmean)

trials = np.linspace(1,RTmean.shape[0],RTmean.shape[0])
#fitParams, fitCovariances = curve_fit(fitFunc, trials, RTmean)

fig = plt.figure()
axes = fig.add_subplot(1,1,1)
axes.set_autoscale_on(True)
axes.plot(trials, RTmean)
#axes.plot(trials, fitFunc(trials, fitParams[0], fitParams[1], fitParams[2]), "r", linewidth = 3)

plt.ylabel("Reaction Time (ms)")
plt.xlabel("Trial number")
temp_title = 'Mean Response Time'
plt.title(temp_title, fontsize=12)
plt.title(suptitle, loc='left', fontsize=12)
plt.title(title, loc='right', fontsize=12)
file = folder + "/RT.png"
fig.savefig(file)
plt.show()
