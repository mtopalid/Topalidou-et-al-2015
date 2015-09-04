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


folder = '../Results/B-Dlearning'
folderf = folder + '/Testing_fam'
folderUf = folder + '/Testing_unfam'
folderfnG = folder + '/Testing_fam_NoGPi'
folderUfnG = folder + '/Testing_unfam_NoGPi'
Pf = np.zeros((simulations, n_testing_trials))
PUf = np.zeros((simulations, n_testing_trials))
PfnG = np.zeros((simulations, n_testing_trials))
PUfnG = np.zeros((simulations, n_testing_trials))
for i in range(simulations):
    file = folderf + '/Records' + "%03d" % (i + 1) + '.npy'
    temp = np.load(file)
    Pf[i, :] = temp["best"]
    file = folderUf + '/Records' + "%03d" % (i + 1) + '.npy'
    temp = np.load(file)
    PUf[i, :] = temp["best"]
    file = folderfnG + '/Records' + "%03d" % (i + 1) + '.npy'
    temp = np.load(file)
    PfnG[i, :] = temp["best"]
    file = folderUfnG + '/Records' + "%03d" % (i + 1) + '.npy'
    temp = np.load(file)
    PUfnG[i, :] = temp["best"]
file = folder + '/MeanPerformanceF.npy'
np.save(file, Pf.mean(axis=0))
file = folder + '/MeanPerformanceUf.npy'
np.save(file, PUf.mean(axis=0))
file = folder + '/MeanPerformancefnG.npy'
np.save(file, PfnG.mean(axis=0))
file = folder + '/MeanPerformanceUfnG.npy'
np.save(file, PUfnG.mean(axis=0))

print "HC with GPi: ", Pf.mean(axis=0).mean()
print "HC without GPi: ", PfnG.mean(axis=0).mean()

print "NC with GPi start: ", PUf.mean(axis=0)[:30].mean()
print "NC with GPi last: ", PUf.mean(axis=0)[-30:].mean()

print "NC without GPi: ", PUfnG.mean(axis=0).mean()

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

n = len(Pf[0])

axes.plot(np.arange(n), Pf.mean(axis=0),
          lw=1.5, c='0.5', linestyle="--", label="HC with GPi", linewidth=2.0)

axes.plot(np.arange(n), PUf.mean(axis=0),
          lw=1.5, c='0.0', linestyle="--", label="NC with GPi", linewidth=2.0)
axes.plot(np.arange(n), PfnG.mean(axis=0),
          lw=1.5, c='0.5', linestyle="-", label="HC without GPi", linewidth=2.0)
axes.plot(np.arange(n), PUfnG.mean(axis=0),
          lw=1.5, c='0.0', linestyle="-", label="NC without GPi", linewidth=2.0)

plt.legend(loc='lower right', frameon=False, fontsize=16)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)

plt.xlabel("Number of trials", fontsize=28)
plt.ylabel("Mean success rate", fontsize=28)

plt.xlim(0, n)
plt.ylim(0, 1.05)
plt.tight_layout()
plt.savefig(folder + "/Performances.pdf", transparent=True)

plt.figure(figsize=(16, 5), dpi=72, facecolor="white")
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
axes.patch.set_facecolor('b')
axes.patch.set_alpha(0.1)
n = len(Pf[0])

axes.plot(np.arange(n), Pf.mean(axis=0),
          lw=1.5, c='0.5', linestyle="--", label="With GPi", linewidth=2.0)
axes.plot(np.arange(n), PfnG.mean(axis=0),
          lw=1.5, c='0.5', linestyle="-", label="Without GPi", linewidth=2.0)

plt.legend(loc='lower right', frameon=False, fontsize=20)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
temp_title = 'Habitual Condition'  # Mean Performances in
plt.title(temp_title, fontsize=28)

plt.xlabel("Number of trials", fontsize=28)
plt.ylabel("Mean success rate", fontsize=28)

plt.xlim(0, n)
plt.ylim(0, 1.05)
plt.tight_layout()
plt.savefig(folder + "/Performances-HC.pdf")  # , transparent = True)

plt.figure(figsize=(16, 5), dpi=72, facecolor="white")
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
axes.patch.set_facecolor('b')
axes.patch.set_alpha(0.1)
n = len(PUf[0])

axes.plot(np.arange(n), PUf.mean(axis=0),
          lw=1.5, c='0.0', linestyle="--", label="With GPi", linewidth=2.0)
axes.plot(np.arange(n), PUfnG.mean(axis=0),
          lw=1.5, c='0.0', linestyle="-", label="Without GPi", linewidth=2.0)

plt.legend(loc='lower right', frameon=False, fontsize=20)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
temp_title = 'Novel Condition'  # Mean Performances in
plt.title(temp_title, fontsize=28)

plt.xlabel("Number of trials", fontsize=28)
plt.ylabel("Mean success rate", fontsize=28)

plt.xlim(0, n)
plt.ylim(0, 1.05)
plt.tight_layout()
plt.savefig(folder + "/Performances-NC.pdf")  # , transparent = True)

fig = plt.figure(figsize=(9, 6), dpi=72, facecolor="white")
fig.subplots_adjust(bottom=0.25)
fig.subplots_adjust(left=0.15)

ax = plt.subplot(111)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('k')
ax.spines['bottom'].set_color('k')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data', 0))
ax.yaxis.set_ticks_position('left')
ax.yaxis.set_label_coords(-0.15, 0.5)

means = [Pf.mean(axis=0)[:30].mean(), Pf.mean(axis=0)[-30:].mean(), PfnG.mean(axis=0)[:30].mean(),
         PfnG.mean(axis=0)[-30:].mean()]
stds = [Pf.std(axis=0)[:30].std(), Pf.std(axis=0)[-30:].std(), PfnG.std(axis=0)[:30].std(),
        PfnG.std(axis=0)[-30:].std()]

indices = 0.25 + np.arange(4)
width = 0.75
p1 = plt.bar(indices, means, width=width, yerr=stds,
             color=["1.", ".5", "1.", ".5"], edgecolor='k', ecolor='k')
plt.xticks(indices + width / 2., ('30 first', '30 last', '30 first', '30 last'), fontsize=18)
plt.yticks(fontsize=18)

plt.ylabel("Mean Performances HC", fontsize=18)
plt.xlim(0, 4.25)
plt.ylim(0.0, 1.200)
# plt.tight_layout()

b = 0.025

plt.axhline(-0.2, b, .5 - b, clip_on=False, color="k", linewidth=2.0)
ax.text(1.125, -0.25, "With GPi", clip_on=False, ha="center", va="top", fontsize=18)

plt.axhline(-0.2, .5 + b, 1 - b, clip_on=False, color="k", linewidth=2.0)
ax.text(3.125, -0.25, "Without GPi", clip_on=False, ha="center", va="top", fontsize=18)

plt.savefig(folder + "/PmeanFam.pdf", transparent=True)

fig = plt.figure(figsize=(9, 6), dpi=72, facecolor="white")
fig.subplots_adjust(bottom=0.25)
fig.subplots_adjust(left=0.15)

ax = plt.subplot(111)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('k')
ax.spines['bottom'].set_color('k')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data', 0))
ax.yaxis.set_ticks_position('left')
ax.yaxis.set_label_coords(-0.15, 0.5)

means = [PUf.mean(axis=0)[:30].mean(), PUf.mean(axis=0)[-30:].mean(), PUfnG.mean(axis=0)[:30].mean(),
         PUfnG.mean(axis=0)[-30:].mean()]
stds = [PUf.std(axis=0)[:30].std(), PUf.std(axis=0)[-30:].std(), PUfnG.std(axis=0)[:30].std(),
        PUfnG.std(axis=0)[-30:].std()]

indices = 0.25 + np.arange(4)
width = 0.75
p1 = plt.bar(indices, means, width=width, yerr=stds,
             color=["1.", ".5", "1.", ".5"], edgecolor='k', ecolor='k')
plt.xticks(indices + width / 2., ('30 first', '30 last', '30 first', '30 last'), fontsize=18)
plt.yticks(fontsize=18)

plt.ylabel("Mean Performances NC", fontsize=18)
plt.xlim(0, 4.25)
plt.ylim(0, 1.200)
# plt.tight_layout()

b = 0.025

plt.axhline(-0.2, b, .5 - b, clip_on=False, color="k", linewidth=2.0)
ax.text(1.125, -0.25, "With GPi", clip_on=False, ha="center", va="top", fontsize=18)

plt.axhline(-0.2, .5 + b, 1 - b, clip_on=False, color="k", linewidth=2.0)
ax.text(3.125, -0.25, "Without GPi", clip_on=False, ha="center", va="top", fontsize=18)

plt.savefig(folder + "/PmeanUnFam.pdf", transparent=True)

RTf = np.zeros((simulations, n_testing_trials))
RTUf = np.zeros((simulations, n_testing_trials))
RTfnG = np.zeros((simulations, n_testing_trials))
RTUfnG = np.zeros((simulations, n_testing_trials))
for i in range(simulations):
    f = '/Records' + "%03d" % (i + 1) + '.npy'
    file = folderf + f
    temp = np.load(file)
    RTf[i, :] = temp["RTmot"]
    file = folderUf + f
    temp = np.load(file)
    RTUf[i, :] = temp["RTmot"]
    file = folderfnG + f
    temp = np.load(file)
    RTfnG[i, :] = temp["RTmot"]
    file = folderUfnG + f
    temp = np.load(file)
    RTUfnG[i, :] = temp["RTmot"]
file = folder + '/MeanRTF.npy'
np.save(file, RTf.mean(axis=0))
file = folder + '/MeanRTUf.npy'
np.save(file, RTUf.mean(axis=0))
file = folder + '/MeanRTfnG.npy'
np.save(file, RTfnG.mean(axis=0))
file = folder + '/MeanRTUfnG.npy'
np.save(file, RTUfnG.mean(axis=0))

print "RT HC with GPi: ", RTf.mean(axis=0).mean()
print "RT HC without GPi: ", RTfnG.mean(axis=0).mean()

print "RT NC with GPi start: ", RTUf.mean(axis=0)[:30].mean()
print "RT NC with GPi last: ", RTUf.mean(axis=0)[-30:].mean()
print "RT NC with GPi : ", RTUf.mean(axis=0).mean()

print "RT NC without GPi: ", RTUfnG.mean(axis=0).mean()
# fig = plt.figure(figsize=(18,12), dpi=72, facecolor="white")
fig = plt.figure(figsize=(9, 6), dpi=72, facecolor="white")
fig.subplots_adjust(bottom=0.25)
fig.subplots_adjust(left=0.15)

ax = plt.subplot(111)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('k')
ax.spines['bottom'].set_color('k')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data', 0))
ax.yaxis.set_ticks_position('left')
ax.yaxis.set_label_coords(-0.15, 0.5)

means = [np.mean(RTf), np.mean(RTUf), np.mean(RTfnG), np.mean(RTUfnG)]
stds = [np.std(RTf), np.std(RTUf), np.std(RTfnG), np.std(RTUfnG)]

indices = 0.25 + np.arange(4)
width = 0.75
p1 = plt.bar(indices, means, width=width, yerr=stds,
             color=["1.", ".5", "1.", ".5"], edgecolor='k', ecolor='k')
plt.xticks(indices + width / 2., ('HC', 'NC', 'HC', 'NC'), fontsize=18)
plt.yticks(fontsize=18)

plt.ylabel("Mean Reaction time (ms)", fontsize=22)
plt.xlim(0, 4.25)
# plt.ylim(0,1200)
# plt.tight_layout()

b = 0.025

plt.axhline(-325, b, .5 - b, clip_on=False, color="k", linewidth=2.0)
ax.text(1.125, -350, "With GPi", clip_on=False, ha="center", va="top", fontsize=22)

plt.axhline(-325, .5 + b, 1 - b, clip_on=False, color="k", linewidth=2.0)
ax.text(3.125, -350, "Without GPi", clip_on=False, ha="center", va="top", fontsize=22)

plt.savefig(folder + "/RTmot.pdf", transparent=True)

plt.show()
