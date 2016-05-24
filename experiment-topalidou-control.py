# -----------------------------------------------------------------------------
# Copyright (c) 2016, Meropi Topalidou
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------

import numpy as np
from experiment import Experiment
# Creation of folders to save the results
import os
folder = "data/"
if not os.path.exists(folder):
    os.makedirs(folder)

folderRes = folder + "results/topalidou/"
if not os.path.exists(folderRes):
    os.makedirs(folderRes)

folderRep = folder + "reports/topalidou/"
if not os.path.exists(folderRep):
    os.makedirs(folderRep)

folderFig = folder + "figures/topalidou/"
if not os.path.exists(folderFig):
    os.makedirs(folderFig)


def session(exp):
    exp.model.setup()
    records = np.zeros((exp.n_block, exp.n_trial), dtype=exp.task.records.dtype)

    # Day 1 : GPi ON
    for trial in exp.task.block(0):
        exp.model.process(exp.task, trial)
    records[0] = exp.task.records

    # Day 2: GPi ON
    for trial in exp.task.block(0):
        exp.model.process(exp.task, trial)
    records[1] = exp.task.records

    return records


mdl = "model-topalidou.json"
tsk = "tasks/task-topalidou.json"
rslt = folderRes + "control.npy"
rprt = folderRep + "control.txt"
experiment = Experiment(model = mdl,
						task = tsk,
						result = rslt,
						report = rprt,
                        n_session = 25, n_block = 2, seed = 123)
records = experiment.run(session, "Topalidou Control")

# Textual results
# -----------------------------------------------------------------------------
P = np.squeeze(records["best"][:,0,:25])
P = P.mean(axis=len(P.shape)-1)
print("D1 start: %.3f ± %.3f" % (P.mean(), P.std()))
P = np.squeeze(records["best"][:,0,-25:])
P = P.mean(axis=len(P.shape)-1)
print("D1 end:   %.3f ± %.3f" % (P.mean(), P.std()))

print()

P = np.squeeze(records["best"][:,1,:25])
P = P.mean(axis=len(P.shape)-1)
print("D2 start: %.3f ± %.3f" % (P.mean(), P.std()))
P = np.squeeze(records["best"][:,1,-25:])
P = P.mean(axis=len(P.shape)-1)
print("D2 end:   %.3f ± %.3f" % (P.mean(), P.std()))
print("-"*30)


# Graphical results
# -----------------------------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib import lines

D1 = np.squeeze(records["best"][:,0,:])
D2 = np.squeeze(records["best"][:,1,:])
sliding_window = 10

plt.figure(figsize=(10,5), facecolor="w")

ax = plt.subplot(111)
ax.patch.set_facecolor("w")
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.yaxis.set_ticks_position('left')
ax.yaxis.set_tick_params(direction="out")
ax.xaxis.set_ticks_position('bottom')
ax.xaxis.set_tick_params(direction="out")


n = D1.shape[1]-1
X = np.arange(1,n+1)
global_mean = np.zeros(n)
local_mean = np.zeros(n)
alpha = 0.1

for j in range(len(D1)):
    for i in range(n):
        imin, imax = max(i+1-sliding_window,0), i+1
        global_mean[i] = D1[:,imin:imax].mean()
        local_mean[i] = D1[j,imin:imax].mean()
    plt.plot(X, local_mean, c='b', lw=1, alpha=alpha)
plt.plot(X, global_mean, c='b', lw=2)

X += n+1
for j in range(len(D2)):
    for i in range(n):
        imin, imax = max(i+1-sliding_window,0), i+1
        global_mean[i] = D2[:,imin:imax].mean()
        local_mean[i] = D2[j,imin:imax].mean()
    plt.plot(X, local_mean, c='b', lw=1, alpha=alpha)
plt.plot(X, global_mean, c='b', lw=2)


ax.axvline(120, linewidth=0.75, c='k', alpha=.75)

plt.xticks([60, 180],
           ["\nDay 1, GPi ON, 120 trials",
            "\nDay 2, GPi ON, 120 trials"])

x,y = np.array([[1, 119], [-0.025, -0.025]])
ax.add_line(lines.Line2D(x, y, lw=1, color='k', clip_on=False))
ax.add_line(lines.Line2D(x+120, y, lw=1, color='k', clip_on=False))

plt.ylabel("Instantaneous performance\n(sliding window of %d trials)" % sliding_window, fontsize=14)
plt.xlim(0,2*(n+1))
plt.ylim(0,1.05)

plt.title("Control (model, N=%d)" % experiment.n_session)
fl = folderFig + "control.pdf"
plt.savefig(fl)
plt.show()
