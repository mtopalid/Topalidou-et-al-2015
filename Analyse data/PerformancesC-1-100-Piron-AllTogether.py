#!/usr/bin/env python
import numpy as np
import os
import matplotlib.pyplot as plt

suptitle = 'Model: Topalidou\n'
path = '../cython/'
import sys
sys.path.append(path)

from parameters import *

from scipy.optimize import curve_fit
def fitFunc(t, b):
    return np.exp(b*t)
suptitle += 'Protocol: C'

folder = '../Results/C-1-100-Piron'

t1 = np.load(folder + '/Num_trials_2_recover_0_9_performance1-118.npy')
#t1 = np.load(folder + '/Num_trials_2_recover_0_9_performance1-54.npy')
t2 = np.load(folder + '/Num_trials_2_recover_0_9_performance119-150.npy')
#t3 = np.load(folder + '/Num_trials_2_recover_0_9_performance151-200.npy')
#t4 = np.load(folder + '/Num_trials_2_recover_0_9_performance4.npy')
Num_trials = np.hstack([t1, t2])#, t2, t3])#
file = folder+ '/Num_trials_2_recover_0_9_performance1-150.npy'
np.save(file, Num_trials)

x1 = np.hstack([np.linspace(1,54,54)])
x2 = np.hstack([np.linspace(55,69,69-55+1), np.linspace(79,91,91-79+1)])
x3 = np.hstack([np.linspace(101,111,11), np.linspace(126,134,134-126+1)])
x4 = np.hstack([np.linspace(151,159,159-151+1), np.linspace(176,184,184-176+1)])
X = np.hstack([x1, x2, x3, x4])
X = np.hstack([1 + np.arange(118), np.linspace(126,140, 15)])
X = 1 + np.arange(150)
fitParams, fitCovariances = curve_fit(fitFunc, X[:93], Num_trials[:93])
print(Num_trials.shape, X.shape, Num_trials[119], t1.shape, t2.shape)
z2 = np.polyfit(X[:119], Num_trials[:119], 2)
print(z2)
p2 = np.poly1d(z2)
z = np.polyfit(X[:119], Num_trials[:119], 1)
print(z)
p = np.poly1d(z)
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


plt.plot(X, Num_trials, 'bo', lw=1.5, zorder=30, label = "data")
plt.plot(X[:119], p2(X[:119]), "r", linewidth = 1.5, label = "Fit curve: %0.3f" % z2[0] + ' x^2 + ' + "%0.3f" % z2[1] + ' x + ' + "%0.3f" % z2[2])
plt.plot(X[:119], p(X[:119]), "g", linewidth = 1.5, label = "Fit curve: %0.3f" % z[0] + ' x + ' + "%0.3f" % z[1])
plt.legend(loc='lower right', frameon=False, fontsize=20)
plt.ylabel("Number of Trials to obtain Performances over 90%", fontsize=24)
plt.xlabel("Number of Trials before Reverse of Reward Probabilities", fontsize=24)

color = "b"
plt.fill_between([0.,X[-1]+1], [-0.1,-0.1], [450, 450],
                     color=color, alpha=.1, lw=0, zorder=-15)
plt.xticks([1,10,20,30,40,50,60,70,80,90,100,110,120,130,140], fontsize=20)
plt.yticks(fontsize=20)
plt.xlim(-1.,141)
plt.ylim(-10.,420)
file = folder + "/Num_trials_2_recover_0_9_performance1-150.pdf"
fig.savefig(file, transparent = True)
plt.show()
