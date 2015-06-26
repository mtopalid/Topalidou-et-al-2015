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

suptitle += 'Protocol: A'
#reverse = input('\nDo you want to have an reverse of Probabilities during the simulation or stop rewards?\nChoose 2 for Stopping Reward, 1 for reverse of Probabilities or 0 for No change\n')
folder = '../Results/A-Results'
title = ''

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
