# -----------------------------------------------------------------------------
# Copyright (c) 2016, Meropi Topalidou
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from experiment import Experiment
# Creation of folders to save the results
import os
folder = "data/"
if not os.path.exists(folder):
    os.makedirs(folder)

folderRes = folder + "results/thomas/"
if not os.path.exists(folderRes):
    os.makedirs(folderRes)

folderRep = folder + "reports/thomas/"
if not os.path.exists(folderRep):
    os.makedirs(folderRep)

folderFig = folder + "figures/thomas/"
if not os.path.exists(folderFig):
    os.makedirs(folderFig)



def session(exp):
    exp.model.setup()
    exp.task.setup()

    # Block 1 : Str ON
    for trial in exp.task.block(0):
        exp.model.process(exp.task, trial)

    # Block 2 : Str OFF

    for trial in exp.task.block(1):
        exp.model.process(exp.task, trial)

    return exp.task.records


mdl = "model-topalidou-thomas.json"
tsk = "tasks/task-thomas.json"
rslt = folderRes + "NoStrAss-control.npy"
rprt = folderRep + "NoStrAss-control.txt"
experiment = Experiment(model = mdl,
						task = tsk,
						result = rslt,
						report = rprt,
                        n_session = 25, n_block = 1, seed = 1)
records = experiment.run(session, "Thomas Protocol without Str Ass Control")
records = np.squeeze(records)



# Textual results
# -----------------------------------------------------------------------------
w = 25
start,end = experiment.task.blocks[0]
P = np.mean(records["best"][:,end-w:end],axis=1)
mean,std = np.mean(P), np.std(P)
print("Performances:")
print("--------------------------------------")
print("Training (HC, GPi On):  %.2f ± %.2f" % (mean,std))

start,end = experiment.task.blocks[1]

P = np.mean(records["best"][:,start:end],axis=1)*100
mean,std = np.mean(P), np.std(P)
print("\nTest all (HC, GPi Off): %.2f ± %.2f" % (mean,std))
P = np.mean(records["best"][:,start:start+w],axis=1)*100
mean,std = np.mean(P), np.std(P)
print("Test start (HC, GPi Off): %.2f ± %.2f" % (mean,std))
P = np.mean(records["best"][:,end-w:end],axis=1)*100
mean,std = np.mean(P), np.std(P)
print("Test end (HC, GPi Off): %.2f ± %.2f" % (mean,std))


start,end = experiment.task.blocks[0]
P = np.mean(records["RT"][:,end-w:end],axis=1)*1000
mean,std = np.mean(P), np.std(P)
print("\n\nReaction time:")
print("--------------------------------------")
print("Training (HC, Str On):  %.2f ± %.2f" % (mean,std))

start,end = experiment.task.blocks[1]
P = np.mean(records["RT"][:,end-w:end],axis=1)*1000
mean,std = np.mean(P), np.std(P)
print("Test (HC, Str Off): %.2f ± %.2f" % (mean,std))


# Graphical results
# -----------------------------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib import lines

start,end = experiment.task.blocks[0]
D1 = records["best"][:,start:end]

start,end = experiment.task.blocks[1]
D2 = records["best"][:,start:end]


sliding_window = 10



plt.figure(figsize=(15,5), facecolor="w")

ax = plt.subplot(111)
ax.patch.set_facecolor("w")
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.yaxis.set_ticks_position('left')
ax.yaxis.set_tick_params(direction="out")
ax.xaxis.set_ticks_position('bottom')
ax.xaxis.set_tick_params(direction="out")


alpha = 0.1

n = D1.shape[1]-1
X = np.arange(1,n+1)
global_mean = np.zeros(n)
local_mean = np.zeros(n)
for j in range(len(D1)):
    for i in range(n):
        imin, imax = max(i+1-sliding_window,0), i+1
        global_mean[i] = D1[:,imin:imax].mean()
        local_mean[i] = D1[j,imin:imax].mean()
    plt.plot(X, local_mean, c='g', lw=1, alpha=alpha)
plt.plot(X, global_mean, c='g', lw=2)

X += n+1
for j in range(len(D2)):
    for i in range(n):
        imin, imax = max(i+1-sliding_window,0), i+1
        global_mean[i] = D2[:,imin:imax].mean()
        local_mean[i] = D2[j,imin:imax].mean()
    plt.plot(X, local_mean, c='m', lw=1, alpha=alpha)
plt.plot(X, global_mean, c='m', lw=2)

ax.axvline(120, linewidth=0.75, c='k', alpha=.75)

plt.xticks([60, 180, 420],
           ["\nHC, 120 trials",
            "\nNC, 120 trials"])
x,y = np.array([[1, 119], [-0.025, -0.025]])
ax.add_line(lines.Line2D(x, y, lw=1, color='k', clip_on=False))
ax.add_line(lines.Line2D(x+120, y, lw=1, color='k', clip_on=False))

plt.ylabel("Mean success rate\n(sliding window of %d trials)" % sliding_window, fontsize=14)
plt.xlim(0,2*(n+1))
plt.ylim(0,1.05)

# plt.title("Piron Protocol without GPi(model, N=%d)" % experiment.n_session)

fl = folderFig + "piron-NoStrAss-control.pdf"
plt.savefig(fl)

plt.show()


