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

folder = '../Results/A'
title = ''
CuesCog = np.zeros((simulations, n_trials, 2))
CuesMot = np.zeros((simulations, n_trials, 2))
#ChCog = np.zeros((simulations, n_trials))
P = np.zeros((simulations, n_trials))
ChMot = np.zeros((simulations, n_trials))
for i in range(simulations):
	file = folder + '/All-Results' + "%03d" % (i+1) + '.npy'
	temp = np.load(file)
	CuesMot[i,:] = temp["Cues"]["mot"]
	CuesCog[i,:] = temp["Cues"]["cog"]
	ChMot[i,:] = temp["Choice"]["mot"]
	P[i,:] = temp["P"]

X =  1 + np.arange(simulations)
fig = plt.figure(figsize=(18,6), facecolor="w")
ax = fig.gca()
ax.set_xticks(np.arange(1,simulations,1.))
ax.set_yticks(np.arange(0,4.,1.))
#plt.plot(X, CuesCog[:,0,0], 'bo')
#plt.plot(X, CuesCog[:,0,1], 'ro')
#plt.plot(X+0.5, P[0], 'mo')
plt.plot(X, CuesMot[:,0,0]+0.5, 'bo')
plt.plot(X, CuesMot[:,0,1]+0.5, 'ro')
#plt.plot(X+0.5, ChMot[0]+0.5, 'go')
plt.xlim(0,simulations+1)
plt.ylim(-0.5,4)
plt.grid()
plt.show()


#file = folder+ '/MeanPerformance.npy'
#np.save(file, P.mean(axis=0))


