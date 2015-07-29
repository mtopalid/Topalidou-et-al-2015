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

folder = '../Results/C-1-100-Piron'


neverSavedBefore 	= True
SavedBefore			= False

reverses = np.linspace(119,150,32)#np.hstack([np.linspace(101,111,11), np.linspace(126,134,134-126+1)])#np.hstack([np.linspace(55,69,69-55+1), np.linspace(79,91,91-79+1)])#np.linspace(151,159,159-151+1), np.linspace(176,184,184-176+1)])#, np.linspace(79,91,91-79+1)]),#np.linspace(101,111,11), np.linspace(126,134,134-126+1)])#,
P = np.zeros((len(reverses), n_reverse_trials_Piron))
if neverSavedBefore:
	p = np.zeros((simulations, n_reverse_trials_Piron))
	#for j in reverses:#range(1,101):
	for j in range(len(reverses)):
		r = int(reverses[j])
		f = folder + '/Reverse' + "%03d" % (r)
		#f = folder + '/Reverse' + "%03d" % (j)
		print 'Reverse:' + "%03d" % (r)
		for i in range(simulations):
			file = f + '/All-Results' + "%03d" % (i+1) + '.npy'
			temp = np.load(file)
			p[i,:] = temp["P"]
		P[j,:] = p.mean(axis = 0)
		file = folder+ '/MeanPerformanceReverse' + "%03d" % (r) +'.npy'
		np.save(file, P[j,:])
		#P[j-1,:] = p.mean(axis = 0)
		#file = folder+ '/MeanPerformanceReverse' + "%03d" % (j) +'.npy'
		#np.save(file, P[j-1,:])

if SavedBefore:
	#for j in reverses:#range(1,101):
	for j in range(len(reverses)):
		r = int(reverses[j])
		f = folder + '/MeanPerformanceReverse' + "%03d" % (r) +'.npy'
		P[j,:] = np.load(f)

		#f = folder + '/MeanPerformanceReverse' + "%03d" % (j) +'.npy'
		#P[j-1,:] = np.load(f)



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


Num_trials = np.zeros(len(reverses))

for i in range(len(reverses)):
	r = int(reverses[i])
	for j in range(r+1,len(P[1])-30):
		if P[i,j:j+30].mean()>0.9:
			Num_trials[i] = j-r-1
			break
print Num_trials
file = folder+ '/Num_trials_2_recover_0_9_performance119-150.npy'
np.save(file, Num_trials)

X = 1 + np.arange(len(reverses))
z2 = np.polyfit(X, Num_trials, 2)
#print z2
p2 = np.poly1d(z2)
z = np.polyfit(X, Num_trials, 1)
#print z
p = np.poly1d(z)

plt.plot(X, Num_trials, 'bo', lw=1.5, zorder=30, label = "data")
plt.plot(X, p(X), "r", linewidth = 1.5, label = "Fit curve: %.3f" % z[0] + ' x + ' + "%0.3f" % z[1])
plt.plot(X, p2(X), "g", linewidth = 1.5, label = "%0.3f" % z2[0] + ' x^2 + ' + "%0.3f" % z2[1] + ' x + ' + "%0.3f" % z2[2])
plt.legend(loc='lower right', frameon=False, fontsize=20)
plt.ylabel("Number of Trials to obtain Performances over 90%", fontsize=24)
plt.xlabel("Number of Trials before Reverse of Reward Probabilities", fontsize=24)

color = "b"
plt.fill_between([0.,X[-1]+1], [-0.1,-0.1], [500, 500],
                     color=color, alpha=.1, lw=0, zorder=-15)
##plt.xticks([1,10,20,30,40,50,60,70,80,90,100], fontsize=20)
plt.yticks(fontsize=20)
plt.xlim(0.,101)
plt.ylim(50,500)
file = folder + "/Num_trials_2_recover_0_9_performance119-150.pdf"
fig.savefig(file, transparent = True)
plt.show()
