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
    return a * np.exp(-b * t) + c

folder = '../Results/D'#-half_noise'
folderUf = folder + '/Testing_unfam'
folderUfnG = folder + '/Testing_unfam_NoGPi'
folderTuf_first_day = folder + '/Control/Testing_unfam'
folderTuf_second_day = folder + '/Control/Testing_unfam_2'

n_testing_trials = 100
PUf = np.zeros((simulations, n_testing_trials))
PUfnG = np.zeros((simulations, n_testing_trials))
PUfD1 = np.zeros((simulations, n_testing_trials))
PUfD2 = np.zeros((simulations, n_testing_trials))
for i in range(simulations):
    file = folderUf + '/Records' + "%03d" % (i + 1) + '.npy'
    temp = np.load(file)
    PUf[i, :] = temp["best"]
    file = folderUfnG + '/Records' + "%03d" % (i + 1) + '.npy'
    temp = np.load(file)
    PUfnG[i, :] = temp["best"]
    file = folderTuf_first_day + '/Records' + "%03d" % (i + 1) + '.npy'
    temp = np.load(file)
    PUfD1[i, :] = temp["best"]
    file = folderTuf_second_day + '/Records' + "%03d" % (i + 1) + '.npy'
    temp = np.load(file)
    PUfD2[i, :] = temp["best"]
file = folder + '/MeanPerformanceUf.npy'
np.save(file, PUf.mean(axis=0))
file = folder + '/MeanPerformanceUfnG.npy'
np.save(file, PUfnG.mean(axis=0))
file = folder + '/MeanPerformanceUfD1.npy'
np.save(file, PUfD1.mean(axis=0))
file = folder + '/MeanPerformanceUfD2.npy'
np.save(file, PUfD2.mean(axis=0))

PUf = PUf.mean(axis=0)
PUfnG = PUfnG.mean(axis=0)
PUfD1 = PUfD1.mean(axis=0)
PUfD2 = PUfD2.mean(axis=0)
print 'Mean'
print 'NoGPi -> GPi'
print 'First 25: ', PUfnG[:25].mean(), PUf[:25].mean()
print 'Last 25: ', PUfnG[-25:].mean(), PUf[-25:].mean(),
print
print 'GPi -> GPi'
print 'First 25: ',  PUfD1[:25].mean(), PUfD2[:25].mean()
print 'Last 25: ', PUfD1[-25:].mean(), PUfD2[-25:].mean()
print
print 'Std'
print 'NoGPi -> GPi'
print 'First 25: ', PUfnG[:25].std(), PUf[:25].std()
print 'Last 25: ', PUfnG[-25:].std(), PUf[-25:].std(),
print
print 'GPi -> GPi'
print 'First 25: ',  PUfD1[:25].std(), PUfD2[:25].std()
print 'Last 25: ', PUfD1[-25:].std(), PUfD2[-25:].std()
'''
from matplotlib import rcParams

rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'

plt.figure(figsize=(10, 5), dpi=72, facecolor="white")
axes = plt.subplot(111)
axes.spines['right'].set_color('none')
axes.spines['top'].set_color('none')
axes.spines['left'].set_linewidth(2.0)
axes.spines['bottom'].set_linewidth(2.0)
axes.xaxis.set_ticks_position('bottom')
axes.spines['bottom'].set_position(('data', 0))
axes.yaxis.set_ticks_position('left')
axes.yaxis.set_label_coords(-0.1, 0.5)
axes.xaxis.set_label_coords(0.5, -0.15)

n = len(PUf[0])

axes.plot(np.arange(n), PUf.mean(axis=0),
          lw=1.5, c='0.0', linestyle="--", label="NC with GPi", linewidth=2.0)

axes.plot(np.arange(n), PUfnG.mean(axis=0),
          lw=1.5, c='0.0', linestyle="-", label="NC without GPi", linewidth=2.0)
axes.plot(np.arange(n), PUfnG2.mean(axis=0),
          lw=1.5, c='0.0', linestyle="*", label="NC without GPi2", linewidth=2.0)

plt.legend(loc='lower right', frameon=False, fontsize=16)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)

plt.xlabel("Number of trials", fontsize=28)
plt.ylabel("Mean success rate", fontsize=28)

plt.xlim(0, n)
plt.ylim(0, 1.05)
plt.tight_layout()
plt.savefig(folder + "/Performances.pdf", transparent=True)

PUf = PUf.mean(axis=0)
PUfnG = PUfnG.mean(axis=0)
plt.figure()
print 'Mean: ', PUfnG[:25].mean(), PUf[:25].mean(), PUfnG[:25].mean(), PUfnG[-25:].mean(), PUf[-25:].mean(), \
    PUfnG[-25:].mean()
print 'Std: ', PUfnG[:25].std(), PUf[:25].std(), PUfnG[:25].std(), PUfnG[-25:].std(), PUf[-25:].std(),PUfnG[-25:].std()
Means = [PUfnG[:25].mean(), PUf[:25].mean(), PUfnG[:25].mean(), PUfnG[-25:].mean(), PUf[-25:].mean(),PUfnG[-25:].mean()]
ind = np.arange(6)    # the x locations for the groups
width = 0.35
plt.bar(ind, Means,   width)
plt.ylabel('Proportion of optimum trials')
plt.title('Half learning')
plt.xticks(ind+width/2., ('25 first trials\nno GPi', '25 first trials\nGPi', '25 first trials\nno GPi2',
                          '25 last trials\nno GPi',
           '25 last trials\nGPi', '25 last trials\nno GPi2') )

plt.savefig(folder + "/BarPerformances.pdf", transparent=True)
plt.show()
'''