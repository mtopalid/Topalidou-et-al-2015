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

folder = '../Results/C-1-100-Piron'
neverSavedBefore 	= False
SavedBefore			= True
NumTrialsBefore		= True

if NumTrialsBefore:
	step = 5
	file = folder+ '/Num_trials_2_recover_0_9_performance3.npy'
	Num_trials = np.load(file)
else:
	last_reverse = 125
	start = 5
	step = 5
	finish = 500
	n = (finish - start + step) / step
	#P = np.zeros((last_reverse, n_reverse_trials_Piron))
	P = np.zeros((n, n_reverse_trials_Piron))
	if neverSavedBefore:
		p = np.zeros((simulations, n_reverse_trials_Piron))
		for j in range(1,last_reverse+1):
		#for k in range(n):
			j = k * 5 + start
			f = folder + '/Reverse' + "%03d" % (j)
			print('Reverse:' + "%03d" % (j))
			for i in range(simulations):
				file = f + '/Records' + "%03d" % (i+1) + '.npy'
				temp = np.load(file)
				p[i,:] = temp["best"]
			P[j-1,:] = p.mean(axis = 0)
			#P[k,:] = p.mean(axis = 0)
			file = folder+ '/MeanPerformanceReverse' + "%03d" % (j) +'.npy'
			np.save(file, P[j-1,:])
			#np.save(file, P[k,:])
	if SavedBefore:
		for j in range(1,last_reverse):
		#for k in range(n):
			#j = k * 5 + start
			#if (j) % 5 != 0:#1:#
			f = folder + '/MeanPerformanceReverse' + "%03d" % (j) +'.npy'
			P[j-1,:] = np.load(f)
			#P[k,:] = np.load(f)

	Num_trials = np.zeros(last_reverse)
	#Num_trials = np.zeros(n)

	for i in range(last_reverse):
	#for i in range(n):
		if (i+1) % 5 == 0:#0:#
			pos = (i+1)/5 - 1
			Num_trials[i] = Num_trials2[pos]
		else:
			#for k in range(n):
				#i = k * 5 + start
				for j in range(i,len(P[1])-30):
					if P[i,j:j+30].mean()>0.9:
					#if P[k,j:j+30].mean()>0.9:
						#Num_trials[k] = j-i-1
						Num_trials[i] = j-i-1
						break
	#print Num_trials
	file = folder+ '/Num_trials_2_recover_0_9_performance1-125.npy'
	np.save(file, Num_trials)



fig = plt.figure(figsize=(20,10), facecolor="w")
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



#X = 1 + np.arange(last_reverse)
X = (1 + np.arange(len(Num_trials)))*step

nozero_till = np.where(Num_trials == 0)[0][0]

#fitParams, fitCovariances = curve_fit(fitFunc, X[:nozero_till], Num_trials[:nozero_till])
#z2 = np.polyfit(X[:nozero_till], Num_trials[:nozero_till], 2)
#print z2
#p2 = np.poly1d(z2)
z = np.polyfit(X[:nozero_till], Num_trials[:nozero_till], 1)
#print z
p = np.poly1d(z)
#fig = plt.figure(figsize=(20,10), facecolor="w", dpi = 72)

#z = np.polyfit(X, Num_trials, 1)
#p = np.poly1d(z)
plt.plot(X, Num_trials, 'bo', lw=1.5, zorder=30, label = "data")
#plt.plot(X[:nozero_till], p2(X[:nozero_till]), "g", linewidth = 1.5, label = "Fit curve: %0.3f" % z2[0] + ' x^2 + ' + "%0.3f" % z2[1] + ' x + ' + "%0.3f" % z2[2])
plt.plot(X[:nozero_till], p(X[:nozero_till]), "r", linewidth = 1.5, label = "Fit curve: %0.3f" % z[0] + ' x + ' + "%0.3f" % z[1])
#plt.plot(X, p(X), "r", linewidth = 1.5, label = "Fit curve: %0.3f" % z[0] + ' x + ' + "%0.3f" % z[1])
plt.legend(loc='right', frameon=False, fontsize=20)
plt.ylabel("Number of Trials to obtain Performances over 90%", fontsize=20)
plt.xlabel("Number of Trials before Reverse of Reward Probabilities", fontsize=20)

color = "b"
plt.fill_between([0.0,X[-1]+1], [-1,-1], [870, 870],
                     color=color, alpha=.1, lw=0, zorder=-15)
#plt.fill_between([0.0,X[-1]+1], [0.0,0.0], [300, 300],
#                    color=color, alpha=.1, lw=0, zorder=-15)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
#plt.xlim(-1.,127)
#plt.ylim(-1.,300)
plt.xlim(-5.,505)
plt.ylim(-5.,880)
file = folder + "/Num_trials_2_recover_0_9_performance5-500.png"#1-125.png"#
fig.savefig(file)
plt.show()
