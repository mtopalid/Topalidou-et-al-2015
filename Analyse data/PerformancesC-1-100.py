#!/usr/bin/env python
import numpy as np
import os
import matplotlib.pyplot as plt

suptitle = 'Model: Topalidou\n'
path = '../cython/'
import sys
sys.path.append(path)

from parameters import *

suptitle += 'Protocol: C'

folder = '../Results/C-1-100'

P = np.zeros((100, n_reverse_trials))

neverSavedBefore 	= False
SavedBefore			= True

if neverSavedBefore:
	p = np.zeros((simulations, n_reverse_trials))
	for j in range(1,101):
		f = folder + '/Reverse' + "%03d" % (j)
		print('Reverse:' + "%03d" % (j))
		for i in range(simulations):
			file = f + '/All-Results' + "%03d" % (i+1) + '.npy'
			temp = np.load(file)
			p[i,:] = temp["P"]
		P[j-1,:] = p.mean(axis = 0)
		file = folder+ '/MeanPerformanceReverse' + "%03d" % (j) +'.npy'
		np.save(file, P[j-1,:])

if SavedBefore:
	for j in range(1,101):
		f = folder + '/MeanPerformanceReverse' + "%03d" % (j) +'.npy'
		P[j-1,:] = np.load(f)



fig = plt.figure(figsize=(20,10), facecolor="w", dpi = 72)
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


Num_trials = np.zeros(len(P))

for i in range(len(P)):
	for j in range(i+2,len(P[1])-30):
		if P[i,j:j+30].mean()>0.9:
			Num_trials[i] = j-i-1
			break
print(Num_trials)
file = folder+ '/Num_trials_2_recover_0_9_performance.npy'
np.save(file, Num_trials)

X = 1 + np.arange(100)
z2 = np.polyfit(X, Num_trials, 2)
#print z2
p2 = np.poly1d(z2)
z = np.polyfit(X, Num_trials, 1)
#print z
p = np.poly1d(z)

plt.plot(X, Num_trials, 'bo', lw=1.5, zorder=30, label = "data")
#plt.plot(X, p(X), "g", linewidth = 1.5, label = "Fit curve: %.3f" % z[0] + ' x + ' + "%0.3f" % z[1])
plt.plot(X, p2(X), "r", linewidth = 1.5, label = "Fit curve: %0.3f" % z2[0] + ' x^2 + ' + "%0.3f" % z2[1] + ' x + ' + "%0.3f" % z2[2])
plt.legend(loc='lower right', frameon=False, fontsize=20)
plt.ylabel("Number of Trials to obtain Performances over 90%", fontsize=24)
plt.xlabel("Number of Trials before Reverse of Reward Probabilities", fontsize=24)

color = "b"
plt.fill_between([0.,X[-1]+1], [-0.1,-0.1], [500, 500],
                     color=color, alpha=.1, lw=0, zorder=-15)
plt.xticks([1,10,20,30,40,50,60,70,80,90,100], fontsize=20)
plt.yticks(fontsize=20)
plt.xlim(0.,101)
plt.ylim(50,500)
file = folder + "/Num_trials_2_recover_0_9_performance.pdf"
fig.savefig(file, transparent = True)
plt.show()
if 0:
	plt.plot(X, P[::,::].mean(axis=0), c='b', lw=1.5, zorder=30)
	plt.plot(X, P.mean(axis=0)+P.std(axis=0), c='.5',lw=.5, zorder=20)
	plt.plot(X, P.mean(axis=0)-P.std(axis=0), c='.5',lw=.5, zorder=20)
	plt.fill_between(X, P.mean(axis=0)+P.std(axis=0),
						P.mean(axis=0)-P.std(axis=0), color='b', alpha=.05, zorder=10)


	plt.ylabel("Proportion of optimum trials")
	plt.xlabel("Trial number")

	file = folder + "/Perfomances.png"
	fig.savefig(file)
	plt.show()
