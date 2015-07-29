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

suptitle += 'Protocol: B'
folder = '../Results/B-Results'

file = folder + '/Performance-fam.npy'
c1 = np.load(file)
MeanPerformance = c1.mean(axis = 0)
C1 =  MeanPerformance.copy()
file = folder + '/MeanPerformance-fam.npy'
np.save(file, MeanPerformance)

file = folder + '/Performance-unfam.npy'
c3 = np.load(file)
MeanPerformance = c3.mean(axis = 0)
C3 =  MeanPerformance.copy()
file = folder+ '/MeanPerformance-unfam.npy'
np.save(file, MeanPerformance)

file = folder + '/Performance-fam_NoGPi.npy'
c2 = np.load(file)
MeanPerformance = c2.mean(axis = 0)
C2 =  MeanPerformance.copy()
file = folder+ '/MeanPerformance-fam_NoGPi.npy'
np.save(file, MeanPerformance)

file = folder + '/Performance-unfam_NoGPi.npy'
c4 = np.load(file)
MeanPerformance = c4.mean(axis = 0)
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


fig = plt.figure(figsize=(9,6), dpi=72, facecolor="white")
fig.subplots_adjust(bottom=0.25)
fig.subplots_adjust(left=0.15)

ax = plt.subplot(111)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('k')
ax.spines['bottom'].set_color('k')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.yaxis.set_label_coords(-0.15, 0.5)


means = [ c1.mean(axis=0)[:30].mean(), c1.mean(axis=0)[-30:].mean(), c2.mean(axis=0)[:30].mean(), c2.mean(axis=0)[-30:].mean()]
stds  = [ c1.std(axis=0)[:30].std(),  c1.std(axis=0)[-30:].std(), c2.std(axis=0)[:30].std(),  c2.std(axis=0)[-30:].std()]

indices = 0.25+np.arange(4)
width=0.75
p1 = plt.bar(indices, means, width=width,  yerr=stds,
			 color=["1.", ".5", "1.", ".5"], edgecolor='k', ecolor='k')
plt.xticks(indices+width/2., ('30 first', '30 last', '30 first', '30 last') , fontsize=18)
plt.yticks(fontsize=18)


plt.ylabel("Mean Performances HC", fontsize=18)
plt.xlim(0,4.25)
plt.ylim(0.0,1.200)
#plt.tight_layout()

b = 0.025

plt.axhline(-0.2, b,.5-b, clip_on=False, color="k", linewidth = 2.0)
ax.text(1.125,-0.25,"With GPi", clip_on=False, ha="center", va="top", fontsize=18)

plt.axhline(-0.2, .5+b,1-b, clip_on=False, color="k", linewidth = 2.0)
ax.text(3.125,-0.25,"Without GPi", clip_on=False, ha="center", va="top", fontsize=18)

plt.savefig(folder + "/PmeanFam.pdf", transparent = True)


fig = plt.figure(figsize=(9,6), dpi=72, facecolor="white")
fig.subplots_adjust(bottom=0.25)
fig.subplots_adjust(left=0.15)

ax = plt.subplot(111)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('k')
ax.spines['bottom'].set_color('k')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.yaxis.set_label_coords(-0.15, 0.5)


means = [ c3.mean(axis=0)[:30].mean(), c3.mean(axis=0)[-30:].mean(),  c4.mean(axis=0)[:30].mean(), c4.mean(axis=0)[-30:].mean()]
stds  = [ c3.std(axis=0)[:30].std(),  c3.std(axis=0)[-30:].std(), c4.std(axis=0)[:30].std(),  c4.std(axis=0)[-30:].std()]

indices = 0.25+np.arange(4)
width=0.75
p1 = plt.bar(indices, means, width=width,  yerr=stds,
			 color=["1.", ".5", "1.", ".5"], edgecolor='k', ecolor='k')
plt.xticks(indices+width/2., ('30 first', '30 last', '30 first', '30 last') , fontsize=18)
plt.yticks(fontsize=18)


plt.ylabel("Mean Performances NC", fontsize=18)
plt.xlim(0,4.25)
plt.ylim(0,1.200)
#plt.tight_layout()

b = 0.025

plt.axhline(-0.2, b,.5-b, clip_on=False, color="k", linewidth = 2.0)
ax.text(1.125,-0.25,"With GPi", clip_on=False, ha="center", va="top", fontsize=18)

plt.axhline(-0.2, .5+b,1-b, clip_on=False, color="k", linewidth = 2.0)
ax.text(3.125,-0.25,"Without GPi", clip_on=False, ha="center", va="top", fontsize=18)

plt.savefig(folder + "/PmeanUnFam.pdf", transparent = True)



C1 = np.load(folder + "/RT-fam.npy")
C2 = np.load(folder + "/RT-fam_NoGPi.npy")
C3 = np.load(folder + "/RT-unfam.npy")
C4 = np.load(folder + "/RT-unfam_NoGPi.npy")

#fig = plt.figure(figsize=(18,12), dpi=72, facecolor="white")
fig = plt.figure(figsize=(9,6), dpi=72, facecolor="white")
fig.subplots_adjust(bottom=0.25)
fig.subplots_adjust(left=0.15)

ax = plt.subplot(111)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('k')
ax.spines['bottom'].set_color('k')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.yaxis.set_label_coords(-0.15, 0.5)

means = [np.mean(C1), np.mean(C3), np.mean(C2), np.mean(C4)]
stds  = [ np.std(C1),  np.std(C3),  np.std(C2),  np.std(C4)]

indices = 0.25+np.arange(4)
width=0.75
p1 = plt.bar(indices, means, width=width,  yerr=stds,
			 color=["1.", ".5", "1.", ".5"], edgecolor='k', ecolor='k')
plt.xticks(indices+width/2., ('HC', 'NC', 'HC', 'NC') , fontsize=18)
plt.yticks(fontsize=18)

if 0:
	temp_title = 'Mean Reaction time (ms)'
	plt.title(temp_title, fontsize=12)
	plt.title(suptitle, loc='left', fontsize=12)
	plt.title(title, loc='right', fontsize=12)

plt.ylabel("Mean Reaction time (ms)", fontsize=22)
plt.xlim(0,4.25)
#plt.ylim(0,1200)
#plt.tight_layout()

b = 0.025

plt.axhline(-325, b,.5-b, clip_on=False, color="k", linewidth = 2.0)
ax.text(1.125,-350,"With GPi", clip_on=False, ha="center", va="top", fontsize=22)

plt.axhline(-325, .5+b,1-b, clip_on=False, color="k", linewidth = 2.0)
ax.text(3.125,-350,"Without GPi", clip_on=False, ha="center", va="top", fontsize=22)

plt.savefig(folder + "/RT.pdf", transparent = True)



plt.show()
