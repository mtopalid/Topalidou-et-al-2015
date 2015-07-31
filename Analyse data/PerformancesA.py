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
P = np.zeros((simulations, n_trials))
for i in range(simulations):
	file = folder + '/Records' + "%03d" % (i+1) + '.npy'
	temp = np.load(file)
	P[i,:] = temp["best"]
file = folder+ '/MeanPerformance.npy'
np.save(file, P.mean(axis=0))

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
X = 1 + np.arange(len(P[0]))
print P.mean(axis=0)[:1].mean(), P.mean(axis=0)[-30:].mean()
Pmean = P.mean(axis=0)
Pstd  = P.std(axis = 0)
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

fig = plt.figure(figsize=(8,6), dpi=72, facecolor="white")
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
width=0.5
p1 = plt.bar(indices, means, width=width,  yerr=stds,
			 color=["1.", ".5"], edgecolor='k', ecolor='k')
plt.xticks(indices+width/2., ('30 first', '30 last') , fontsize=18)
plt.yticks(fontsize=18)


plt.ylabel("Mean Performances", fontsize=22)
plt.xlim(0,2)
#plt.ylim(0,1200)
#plt.tight_layout()

plt.savefig(folder + "/Pmean.pdf", transparent = True)



RTcog = np.zeros((simulations, n_trials))
RTmot = np.zeros((simulations, n_trials))
for i in range(simulations):
	file = folder + '/Records' + "%03d" % (i+1) + '.npy'
	temp = np.load(file)
	RTcog[i,:] = temp["RTcog"]
	RTmot[i,:] = temp["RTmot"]
file = folder+ '/RTmean-cog.npy'
np.save(file, RTcog.mean(axis=0))
file = folder+ '/RTmean-mot.npy'
np.save(file, RTmot.mean(axis=0))


if RTcog_mot:

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

	print RTcog.mean(axis=0)[-30:].mean()
	print RTmot.mean(axis=0)[-30:].mean()
	#X = 1+np.arange(len(RTmean[0]))
	RTmean_cog = RTcog.mean(axis=0)
	RTstd_cog = RTcog.std(axis=0)
	RTmean_mot = RTmot.mean(axis=0)
	RTstd_mot = RTmot.std(axis=0)
	plt.plot(X, RTmean_cog, c='b', lw=1.5, zorder=30, label = "Coginitive Decision")
	plt.plot(X, RTmean_mot, c='r', lw=1.5, zorder=30, label = "Motor Decision")
	plt.legend()
	if 1:
		plt.plot(X, RTmean_cog+RTstd_cog, c='.5',lw=.5, zorder=20)
		plt.plot(X, RTmean_cog-RTstd_cog, c='.5',lw=.5, zorder=20)
		plt.fill_between(X, RTmean_cog+RTstd_cog,
							RTmean_cog-RTstd_cog, color='b', alpha=.05, zorder=10)
		plt.plot(X, RTmean_mot+RTstd_mot, c='.5',lw=.5, zorder=20)
		plt.plot(X, RTmean_mot-RTstd_mot, c='.5',lw=.5, zorder=20)
		plt.fill_between(X, RTmean_mot+RTstd_mot,
							RTmean_mot-RTstd_mot, color='r', alpha=.05, zorder=10)


	plt.ylabel("Reaction Time (ms)")
	plt.xlabel("Trial number")
	if 0:
		temp_title = 'Mean Response Time'
		plt.title(temp_title, fontsize=12)
		plt.title(suptitle, loc='left', fontsize=12)
		plt.title(title, loc='right', fontsize=12)
	file = folder + "/RT.png"
	fig.savefig(file)

if RTdifference:
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

	print RTcog.mean(axis=0)[-30:].mean()
	print RTmot.mean(axis=0)[-30:].mean()
	RTdiff = RTmot - RTcog
	RTmean_diff = RTdiff.mean(axis=0)
	RTstd_diff = RTdiff.std(axis=0)
	plt.plot(X, RTmean_diff, c='b', lw=1.5, zorder=30)
	if 1:
		plt.plot(X, RTmean_diff+RTstd_diff, c='.5',lw=.5, zorder=20)
		plt.plot(X, RTmean_diff-RTstd_diff, c='.5',lw=.5, zorder=20)
		plt.fill_between(X, RTmean_diff+RTstd_diff,
							RTmean_diff-RTstd_diff, color='b', alpha=.05, zorder=10)


	plt.ylabel("Time Difference Between Motor and Cogniitve Decision (ms)")
	plt.xlabel("Trial number")
	if 0:
		temp_title = 'Mean Response Time'
		plt.title(temp_title, fontsize=12)
		plt.title(suptitle, loc='left', fontsize=12)
		plt.title(title, loc='right', fontsize=12)
	file = folder + "/RTdiff.png"
	fig.savefig(file)


if RTboxplot:
	#fig = plt.figure(figsize=(18,12), dpi=72, facecolor="white")
	fig = plt.figure(figsize=(8,6), dpi=72, facecolor="white")
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


	means = [RTcog.mean(axis=0)[:30].mean(), RTcog.mean(axis=0)[-30:].mean()]
	stds  = [ RTcog.std(axis=0)[:30].mean(),  RTcog.std(axis=0)[-30:].mean()]

	indices = 0.25+np.arange(2)
	width=0.5
	p1 = plt.bar(indices, means, width=width,  yerr=stds,
				 color=["1.", ".5"], edgecolor='k', ecolor='k')
	plt.xticks(indices+width/2., ('30 first', '30 last') , fontsize=18)
	plt.yticks(fontsize=18)

	if 0:
		temp_title = 'Mean Reaction time (ms)'
		plt.title(temp_title, fontsize=12)
		plt.title(suptitle, loc='left', fontsize=12)
		plt.title(title, loc='right', fontsize=12)

	plt.ylabel("Mean Cognitive Decision time (ms)", fontsize=22)
	plt.xlim(0,2)
	#plt.ylim(0,1200)
	#plt.tight_layout()

	plt.savefig(folder + "/RTcog-boxplot.pdf", transparent = True)

	#fig = plt.figure(figsize=(18,12), dpi=72, facecolor="white")
	fig = plt.figure(figsize=(8,6), dpi=72, facecolor="white")
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


	means = [RTmot.mean(axis=0)[:30].mean(), RTmot.mean(axis=0)[-30:].mean()]
	stds  = [ RTmot.std(axis=0)[:30].mean(),  RTmot.std(axis=0)[-30:].mean()]

	indices = 0.25+np.arange(2)
	width=0.5
	p1 = plt.bar(indices, means, width=width,  yerr=stds,
				 color=["1.", ".5"], edgecolor='k', ecolor='k')
	plt.xticks(indices+width/2., ('30 first', '30 last') , fontsize=18)
	plt.yticks(fontsize=18)

	if 0:
		temp_title = 'Mean Reaction time (ms)'
		plt.title(temp_title, fontsize=12)
		plt.title(suptitle, loc='left', fontsize=12)
		plt.title(title, loc='right', fontsize=12)

	plt.ylabel("Mean Motor Decision time (ms)", fontsize=22)
	plt.xlim(0,2)
	#plt.ylim(0,1200)
	#plt.tight_layout()

	plt.savefig(folder + "/RTmot-boxplot.pdf", transparent = True)



plt.show()
