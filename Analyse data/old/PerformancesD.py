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

suptitle += 'Protocol: D'
folder = '../Results/D-Results'
file = folder + '/Performance-fam.npy'
load = np.load(file)
MeanPerformance = load.mean(axis = 0)
C1 =  MeanPerformance.copy()
file = folder + '/MeanPerformance-fam.npy'
np.save(file, MeanPerformance)

file = folder + '/Performance-unfam.npy'
load = np.load(file)
MeanPerformance = load.mean(axis = 0)
C3 =  MeanPerformance.copy()
file = folder+ '/MeanPerformance-unfam.npy'
np.save(file, MeanPerformance)

file = folder + '/Performance-fam_NoGPi.npy'
load = np.load(file)
MeanPerformance = load.mean(axis = 0)
C2 =  MeanPerformance.copy()
file = folder+ '/MeanPerformance-fam_NoGPi.npy'
np.save(file, MeanPerformance)

file = folder + '/Performance-unfam_NoGPi.npy'
load = np.load(file)
MeanPerformance = load.mean(axis = 0)
C4 =  MeanPerformance.copy()
file = folder+ '/MeanPerformance-unfam_NoGPi.npy'
np.save(file, MeanPerformance)

from matplotlib import rcParams
rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'

plt.figure(figsize=(10,5), dpi=72, facecolor="white")
axes = plt.subplot(111)
axes.spines['right'].set_color('none')
axes.spines['top'].set_color('none')
axes.spines['left'].set_linewidth(2.0)
axes.spines['bottom'].set_linewidth(2.0)
axes.xaxis.set_ticks_position('bottom')
axes.spines['bottom'].set_position(('data',0))
axes.yaxis.set_ticks_position('left')
axes.yaxis.set_label_coords(-0.1, 0.5)
axes.xaxis.set_label_coords(0.5, -0.15)

n = len(C1)

axes.plot(np.arange(n), C1,
		  lw=1.5, c='0.5', linestyle="--", label="HC with GPi", linewidth = 2.0)

axes.plot(np.arange(n), C3,
		  lw=1.5, c='0.0', linestyle=":", label="NC with GPi", linewidth = 2.0)
axes.plot(np.arange(n), C2,
		  lw=1.5, c='0.5', linestyle="-", label="HC without GPi", linewidth = 2.0)
axes.plot(np.arange(n), C4,
		  lw=1.5, c='0.0', linestyle="-", label="NC without GPi", linewidth = 2.0)

plt.legend(loc='lower right', frameon=False, fontsize=16)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
temp_title = 'Mean Performances'
plt.title(temp_title, fontsize=12)
plt.title(suptitle, loc='left', fontsize=12)

plt.xlabel("Number of trials", fontsize=28)
plt.ylabel("Mean success rate", fontsize=28)

plt.xlim(0,n)
plt.ylim(0,1.05)
plt.tight_layout()
plt.savefig(folder + "/Performances.pdf", transparent = True)
plt.show()
