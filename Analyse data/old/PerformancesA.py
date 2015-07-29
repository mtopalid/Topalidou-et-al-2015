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
P = np.load(file)
file = folder+ '/MeanPerformance.npy'
np.save(file, P)

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
X = np.linspace(0.,len(P[0])/5,len(P[0])/5+1)*5
X[-1] = X[-1] - 1
X = tuple(X)
print P.mean(axis=0)[:30].mean(), P.mean(axis=0)[-30:].mean()
Pmean = np.take(P.mean(axis=0),X)
Pstd  = np.take(P.std(axis = 0),X)
plt.plot(X, Pmean, c='b', lw=1.5, zorder=30)
plt.plot(X, Pmean+Pstd, c='.5',lw=.5, zorder=20)
plt.plot(X, Pmean-Pstd, c='.5',lw=.5, zorder=20)
plt.fill_between(X, Pmean+Pstd,
                    Pmean-Pstd, color='b', alpha=.05, zorder=10)


plt.ylabel("Proportion of optimum trials")
plt.xlabel("Trial number")
if 0:
	temp_title = 'Mean Performances'
	plt.title(temp_title, fontsize=12)
	plt.title(suptitle, loc='left', fontsize=12)
	plt.title(title, loc='right', fontsize=12)

file = folder + "/Perfomances.png"
fig.savefig(file)

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


means = [ P.mean(axis=0)[:30].mean(), P.mean(axis=0)[-30:].mean()]
stds  = [ P.std(axis=0)[:30].mean(),  P.std(axis=0)[-30:].mean()]

indices = 0.25+np.arange(2)
width=0.75
p1 = plt.bar(indices, means, width=width,  yerr=stds,
			 color=["1.", ".5"], edgecolor='k', ecolor='k')
plt.xticks(indices+width/2., ('30 first', '30 last') , fontsize=18)
plt.yticks(fontsize=18)


plt.ylabel("Mean Performances", fontsize=22)
plt.xlim(0,4.25)
#plt.ylim(0,1200)
#plt.tight_layout()

plt.savefig(folder + "/Pmean.pdf", transparent = True)





file = folder + '/RT.npy'
RT = np.load(file)
#file = folder+ '/RTmean.npy'
#np.save(file, RT)


fig = plt.figure(figsize=(18,6),facecolor="w")#
ax = plt.subplot()
ax.patch.set_facecolor("w")

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_tick_params(direction="in")
ax.xaxis.set_tick_params(direction="in")
ax.yaxis.set_label_coords(-0.06, 0.5)
ax.xaxis.set_label_coords(0.5, -0.08)

print RT.mean(axis=0)[-25:].mean()
#X = 1+np.arange(len(RTmean[0]))
RTmean = np.take(RT.mean(axis=0),X)
RTstd = np.take(RT.std(axis=0),X)
plt.plot(X, RTmean, c='b', lw=1.5, zorder=30)
if 1:
	plt.plot(X, RTmean+RTstd, c='.5',lw=.5, zorder=20)
	plt.plot(X, RTmean-RTstd, c='.5',lw=.5, zorder=20)
	plt.fill_between(X, RTmean+RTstd,
						RTmean-RTstd, color='b', alpha=.05, zorder=10)

plt.ylabel("Reaction Time (ms)")
plt.xlabel("Trial number")
if 0:
	temp_title = 'Mean Response Time'
	plt.title(temp_title, fontsize=12)
	plt.title(suptitle, loc='left', fontsize=12)
	plt.title(title, loc='right', fontsize=12)
file = folder + "/RT.png"
fig.savefig(file)

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


means = [RT.mean(axis=0)[:30].mean(), RT.mean(axis=0)[-30:].mean()]
stds  = [ RT.std(axis=0)[:30].mean(),  RT.std(axis=0)[-30:].mean()]

indices = 0.25+np.arange(2)
width=0.75
p1 = plt.bar(indices, means, width=width,  yerr=stds,
			 color=["1.", ".5"], edgecolor='k', ecolor='k')
plt.xticks(indices+width/2., ('30 first', '30 last') , fontsize=18)
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

plt.savefig(folder + "/RTmean.pdf", transparent = True)



plt.show()
