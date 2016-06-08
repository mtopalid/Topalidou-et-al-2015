# -----------------------------------------------------------------------------
# Copyright (c) 2016, Meropi Topalidou
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from experiment import Experiment
import os
folder = "data/"
if not os.path.exists(folder):
    os.makedirs(folder)

folderRes = folder + "results/guthrie/"
if not os.path.exists(folderRes):
    os.makedirs(folderRes)

folderRep = folder + "reports/guthrie/"
if not os.path.exists(folderRep):
    os.makedirs(folderRep)

folderFig = folder + "figures/guthrie/"
if not os.path.exists(folderFig):
    os.makedirs(folderFig)


def session(exp):
    exp.model.setup()
    for trial in exp.task:
        exp.model.process(exp.task, trial)
    return exp.task.records


mdl = "model-topalidou.json"

tsk = "tasks/task-guthrie.json"
rslt = folderRes + "control.npy" #-NoCtx
rprt = folderRep + "control.txt"#-NoCtx
experiment = Experiment(model = mdl,
						task = tsk,
						result = rslt,
						report = rprt,
						n_session = 25, n_block = 1, seed = 123)#None)
records = experiment.run(session, "Guthrie Protocol")
records = np.squeeze(records)

# -----------------------------------------------------------------------------

P_mean = np.mean(records["best"], axis=0)
P_std = np.std(records["best"], axis=0)

V_mean = np.mean(records["Values"], axis=0)
V_std = np.std(records["Values"], axis=0)

Wstr_mean = np.mean(records["WeightsStr"], axis=0)
Wstr_std = np.std(records["WeightsStr"], axis=0)

Wctx_mean = np.mean(records["WeightsCtx"], axis=0)
Wctx_std = np.std(records["WeightsCtx"], axis=0)

plt.close("all")
plt.figure(figsize=(18, 10), facecolor="w")
n_trial = len(experiment.task)

ax = plt.subplot(411)

ax.patch.set_facecolor("w")
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.yaxis.set_ticks_position('left')
ax.yaxis.set_tick_params(direction="in")
ax.xaxis.set_ticks_position('bottom')
ax.xaxis.set_tick_params(direction="in")
X = 1 + np.arange(n_trial)

plt.plot(X, P_mean, c='b', lw=2)
plt.plot(X, P_mean + P_std, c='b', lw=.5)
plt.plot(X, P_mean - P_std, c='b', lw=.5)
plt.fill_between(X, P_mean + P_std, P_mean - P_std, color='b', alpha=.1)

plt.text(n_trial+1, P_mean[-1], "%.2f" % P_mean[-1],
		 ha="left", va="center", color="b")

plt.ylabel("Performance\n", fontsize=16)
plt.xlim(1,n_trial)
plt.ylim(-0.25,1.25)
plt.yticks([ 0.0,   0.2,   0.4,  0.6, 0.8,   1.0])
plt.text(n_trial + 1, P_mean[-1], "%.2f" % P_mean[-1],
		 ha="left", va="center", color="b")
plt.text(0, P_mean[0], "%.2f" % P_mean[0],
		 ha="left", va="center", color="b")


ax = plt.subplot(412)
ax.patch.set_facecolor("w")
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.yaxis.set_ticks_position('left')
ax.yaxis.set_tick_params(direction="in")
ax.xaxis.set_ticks_position('bottom')
ax.xaxis.set_tick_params(direction="in")
X = 1 + np.arange(n_trial)
plt.plot(X, V_mean[:,0], c='b', lw=2)
plt.plot(X, V_mean[:,0] + V_std[:,0], c='b', lw=.5)
plt.plot(X, V_mean[:,0] - V_std[:,0], c='b', lw=.5)
plt.fill_between(X, V_mean[:,0] + V_std[:,0], V_mean[:,0] - V_std[:,0], color='b', alpha=.1)

plt.text(n_trial + 1, V_mean[-1,0], "%.2f" % V_mean[-1,0],
		 ha="left", va="center", color="b")
plt.text(0, V_mean[0,0], "%.2f" % V_mean[0,0],
		 ha="left", va="center", color="b")

plt.plot(X, V_mean[:,1], c='r', lw=2)
plt.plot(X, V_mean[:,1] + V_std[:,1], c='r', lw=.5)
plt.plot(X, V_mean[:,1] - V_std[:,1], c='r', lw=.5)
plt.fill_between(X, V_mean[:,1] + V_std[:,1], V_mean[:,1] - V_std[:,1], color='r', alpha=.1)

plt.text(n_trial + 1, V_mean[-1,1], "%.2f" % V_mean[-1,1],
		 ha="left", va="center", color="r")
plt.text(0, V_mean[0,1], "%.2f" % V_mean[0,1],
		 ha="left", va="center", color="r")

plt.plot(X, V_mean[:,2], c='g', lw=2)
plt.plot(X, V_mean[:,2] + V_std[:,2], c='g', lw=.5)
plt.plot(X, V_mean[:,2] - V_std[:,2], c='g', lw=.5)
plt.fill_between(X, V_mean[:,2] + V_std[:,2], V_mean[:,2] - V_std[:,2], color='r', alpha=.1)

plt.text(n_trial + 1, V_mean[-1,2], "%.2f" % V_mean[-1,2],
		 ha="left", va="center", color="g")
plt.text(0, V_mean[0,2], "%.2f" % V_mean[0,2],
		 ha="left", va="center", color="g")

plt.plot(X, V_mean[:,3], c='m', lw=2)
plt.plot(X, V_mean[:,3] + V_std[:,1], c='m', lw=.5)
plt.plot(X, V_mean[:,3] - V_std[:,1], c='m', lw=.5)
plt.fill_between(X, V_mean[:,3] + V_std[:,3], V_mean[:,3] - V_std[:,3], color='m', alpha=.1)

plt.text(n_trial + 1, V_mean[-1,3], "%.2f" % V_mean[-1,3],
		 ha="left", va="center", color="m")
plt.text(0, V_mean[0,3], "%.2f" % V_mean[0,3],
		 ha="left", va="center", color="m")

plt.ylabel("Values\n", fontsize=16)
plt.xlim(1, n_trial)


ax = plt.subplot(413)

ax.patch.set_facecolor("w")
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.yaxis.set_ticks_position('left')
ax.yaxis.set_tick_params(direction="in")
ax.xaxis.set_ticks_position('bottom')
ax.xaxis.set_tick_params(direction="in")


plt.plot(X, Wstr_mean[:,0], c='b', lw=2)
plt.plot(X, Wstr_mean[:,0] + Wstr_std[:,0], c='b', lw=.5)
plt.plot(X, Wstr_mean[:,0] - Wstr_std[:,0], c='b', lw=.5)
plt.fill_between(X, Wstr_mean[:,0] + Wstr_std[:,0], Wstr_mean[:,0] - Wstr_std[:,0], color='b', alpha=.1)

plt.text(n_trial + 1, Wstr_mean[-1,0], "%.2f" % Wstr_mean[-1,0],
		 ha="left", va="center", color="b")
plt.text(0, Wstr_mean[0,0], "%d" % Wstr_mean[0,0],
		 ha="right", va="center", color="r")

plt.plot(X, Wstr_mean[:,1], c='r', lw=2)
plt.plot(X, Wstr_mean[:,1] + Wstr_std[:,1], c='r', lw=.5)
plt.plot(X, Wstr_mean[:,1] - Wstr_std[:,1], c='r', lw=.5)
plt.fill_between(X, Wstr_mean[:,1] + Wstr_std[:,1], Wstr_mean[:,1] - Wstr_std[:,1], color='r', alpha=.1)

plt.text(n_trial + 1, Wstr_mean[-1,1], "%.2f" % Wstr_mean[-1,1],
		 ha="left", va="center", color="r")
plt.text(0, Wstr_mean[0,1], "%d" % Wstr_mean[0,1],
		 ha="right", va="center", color="r")


plt.plot(X, Wstr_mean[:,2], c='g', lw=2)
plt.plot(X, Wstr_mean[:,2] + Wstr_std[:,2], c='g', lw=.5)
plt.plot(X, Wstr_mean[:,2] - Wstr_std[:,2], c='g', lw=.5)
plt.fill_between(X, Wstr_mean[:,2] + Wstr_std[:,2], Wstr_mean[:,2] - Wstr_std[:,2], color='g', alpha=.1)

plt.text(n_trial + 1, Wstr_mean[-1,2], "%.2f" % Wstr_mean[-1,2],
		 ha="left", va="center", color="g")
plt.text(0, Wstr_mean[0,2], "%d" % Wstr_mean[0,2],
		 ha="right", va="center", color="g")


plt.plot(X, Wstr_mean[:,3], c='m', lw=2)
plt.plot(X, Wstr_mean[:,3] + Wstr_std[:,3], c='m', lw=.5)
plt.plot(X, Wstr_mean[:,3] - Wstr_std[:,3], c='m', lw=.5)
plt.fill_between(X, Wstr_mean[:,3] + Wstr_std[:,3], Wstr_mean[:,3] - Wstr_std[:,3], color='m', alpha=.1)

plt.text(n_trial + 1, Wstr_mean[-1,3], "%.2f" % Wstr_mean[-1,3],
		 ha="left", va="center", color="m")
plt.text(0, Wstr_mean[0,3], "%d" % Wstr_mean[0,3],
		 ha="right", va="center", color="m")


plt.ylabel("Striatal Weights\n", fontsize=16)
plt.xlim(1, n_trial)


ax = plt.subplot(414)

ax.patch.set_facecolor("w")
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.yaxis.set_ticks_position('left')
ax.yaxis.set_tick_params(direction="in")
ax.xaxis.set_ticks_position('bottom')
ax.xaxis.set_tick_params(direction="in")

plt.plot(X, Wctx_mean[:,0], c='b', lw=2)
plt.plot(X, Wctx_mean[:,0] + Wctx_std[:,0], c='b', lw=.5)
plt.plot(X, Wctx_mean[:,0] - Wctx_std[:,0], c='b', lw=.5)
plt.fill_between(X, Wctx_mean[:,0] + Wctx_std[:,0], Wctx_mean[:,0] - Wctx_std[:,0], color='b', alpha=.1)

plt.text(n_trial + 1, Wctx_mean[-1,0], "%.2f" % Wctx_mean[-1,0],
		 ha="left", va="center", color="b")
plt.text(0, Wctx_mean[0,0], "%d" % Wctx_mean[0,0],
		 ha="right", va="center", color="r")

plt.plot(X, Wctx_mean[:,1], c='r', lw=2)
plt.plot(X, Wctx_mean[:,1] + Wctx_std[:,1], c='r', lw=.5)
plt.plot(X, Wctx_mean[:,1] - Wctx_std[:,1], c='r', lw=.5)
plt.fill_between(X, Wctx_mean[:,1] + Wctx_std[:,1], Wctx_mean[:,1] - Wctx_std[:,1], color='r', alpha=.1)

plt.text(n_trial + 1, Wctx_mean[-1,1], "%.2f" % Wctx_mean[-1,1],
		 ha="left", va="center", color="r")
plt.text(0, Wctx_mean[0,1], "%d" % Wctx_mean[0,1],
		 ha="right", va="center", color="r")


plt.plot(X, Wctx_mean[:,2], c='g', lw=2)
plt.plot(X, Wctx_mean[:,2] + Wctx_std[:,2], c='g', lw=.5)
plt.plot(X, Wctx_mean[:,2] - Wctx_std[:,2], c='g', lw=.5)
plt.fill_between(X, Wctx_mean[:,2] + Wctx_std[:,2], Wctx_mean[:,2] - Wctx_std[:,2], color='g', alpha=.1)

plt.text(n_trial + 1, Wctx_mean[-1,2], "%.2f" % Wctx_mean[-1,2],
		 ha="left", va="center", color="g")
plt.text(0, Wctx_mean[0,2], "%d" % Wctx_mean[0,2],
		 ha="right", va="center", color="g")


plt.plot(X, Wctx_mean[:,3], c='m', lw=2)
plt.plot(X, Wctx_mean[:,3] + Wctx_std[:,3], c='m', lw=.5)
plt.plot(X, Wctx_mean[:,3] - Wctx_std[:,3], c='m', lw=.5)
plt.fill_between(X, Wctx_mean[:,3] + Wctx_std[:,3], Wctx_mean[:,3] - Wctx_std[:,3], color='m', alpha=.1)

plt.text(n_trial + 1, Wctx_mean[-1,3], "%.2f" % Wctx_mean[-1,3],
		 ha="left", va="center", color="m")
plt.text(0, Wctx_mean[0,3], "%d" % Wctx_mean[0,3],
		 ha="right", va="center", color="m")


plt.xlabel("Trial number", fontsize=16)
plt.ylabel("Cortical Weights\n", fontsize=16)
plt.xlim(1, n_trial)

fl = folderFig + "control-learning.pdf"
plt.savefig(fl)

plt.show()
