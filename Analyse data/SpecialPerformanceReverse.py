#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

path = '../cython/'
import sys
sys.path.append(path)

from parameters import *

folder = '../Results/C-Piron'
reverse = 1
reverse_all = 1
reverse_trial = input('After how many trials is the reverse?\n')
folder += '/' + str(reverse_trial)
title = 'reverse probabilities of\n'
title += 'all ' if reverse_all else 'middle '
title += 'cues after %s trials' %str(reverse_trial)

file = folder + '/Performances.npy'
P = np.load(file)

#areas = [("A",    0, reverse_trial),
#         ("B",  reverse_trial, 140),
#         ("C",  140, 600),
#         ("D",  600,960)]

areas = [("A",    0, 500),
         ("B",  500,1200)]

fig = plt.figure(figsize=(20,8), facecolor="w", dpi = 72)
ax = plt.subplot(111, aspect=250)
ax.patch.set_facecolor("w")
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.yaxis.set_ticks_position('left')
ax.yaxis.set_tick_params(direction="in")
ax.xaxis.set_ticks_position('bottom')
ax.xaxis.set_tick_params(direction="in")

ax.yaxis.set_label_coords(-0.07, 0.5)
ax.xaxis.set_label_coords(0.5, -0.15)
X = 1+np.arange(len(P[0]))
plt.plot(X, P[::,::].mean(axis=0), c='k', lw=1.5, zorder=30)
plt.plot(X, P.mean(axis=0)+P.var(axis=0), c='.5',lw=.5, zorder=20)
plt.plot(X, P.mean(axis=0)-P.var(axis=0), c='.5',lw=.5, zorder=20)
plt.fill_between(X, P.mean(axis=0)+P.var(axis=0),
                    P.mean(axis=0)-P.var(axis=0), color='k', alpha=.05, zorder=10)


color = "b"
for (name,xmin,xmax) in areas:
    plt.fill_between([xmin,xmax], [-0.1,-0.1], [1.1, 1.1],
                     color=color, alpha=.1, lw=0, zorder=-15)
    plt.axvline(xmax, lw=1, color="w", zorder=-10)
    plt.text(xmin+(xmax-xmin)/2, .5, name,
             fontsize=64, color=color, alpha=.1, zorder=-5,
             verticalalignment="center", horizontalalignment="center")

x = reverse_trial
ax.annotate('Reward switch\n(trial #%d)' % x,
            xy=(x,+1.1), xycoords='data', xytext=(x, 1.2),
#            arrowprops=dict(arrowstyle="->", color='k'),
            horizontalalignment="center", fontsize=28)

plt.xlabel("Trial number", fontsize=28)
plt.ylabel("Performance", fontsize=28)
plt.ylim(-0.1,1.1)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlim(0,len(P[0])+10)
fig.savefig(folder + '/Performances-DiffAreas.pdf', transparent = True)
plt.show()
sys.exit()
