# -----------------------------------------------------------------------------
# Copyright (c) 2016, Meropi Topalidou
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from experiment import Experiment # Creation of folders to save the results
import os
folder = "data/"
if not os.path.exists(folder):
    os.makedirs(folder)

folderRes = folder + "results/reverse/"
if not os.path.exists(folderRes):
    os.makedirs(folderRes)

folderRep = folder + "reports/reverse/"
if not os.path.exists(folderRep):
    os.makedirs(folderRep)

folderFig = folder + "figures/reverse/"
if not os.path.exists(folderFig):
    os.makedirs(folderFig)


def session(exp):
    exp.model.setup()
    exp.task.setup()

    # Normal
    for trial in exp.task.block(0):
        exp.model.process(exp.task, trial)

    # Reverse
    for trial in exp.task.block(1):
        exp.model.process(exp.task, trial)

    return exp.task.records

mdl = "model-topalidou.json"

revr = [600,700,800,900,1100,1200,1300,1400,1500]#10,50,50, 100,200,300,
# revr = [300]
for i in revr:
    trial = str(i)
    tsk = "tasks/task-topalidou-reverse-" + trial + ".json"
    rslt = folderRes + trial + ".npy"
    rprt = folderRep + trial + ".txt"
    experiment = Experiment(model = mdl,
                            task = tsk,
                            result = rslt,
                            report = rprt,
                            n_session = 25, n_block = 1, seed = 123)#None)
    records = experiment.run(session, "Protocol Reverse")
    records = np.squeeze(records)

    # -----------------------------------------------------------------------------
    w = 5
    start,end = experiment.task.blocks[0]
    P = np.mean(records["best"][:,end-w:end],axis=1)
    mean,std = np.mean(P), np.std(P)
    print("Acquisition (HC):  %.2f ± %.2f" % (mean,std))

    start,end = experiment.task.blocks[1]
    P = np.mean(records["best"][:,end-w:end],axis=1)
    mean,std = np.mean(P), np.std(P)
    print("Test (HC, GPi On): %.2f ± %.2f" % (mean,std))



    # -----------------------------------------------------------------------------
    P_mean, P_std = [], []

    for i in range(records.shape[1]-w):
        P = np.mean(records["best"][:,i:i+w],axis=1)
        P_mean.append(np.mean(P))
        P_std.append(np.std(P))

    P_mean  = np.array(P_mean)
    P_std   = np.array(P_std)
    X       = w + np.arange(len(P_mean))

    plt.close("all")
    plt.figure(figsize=(16,10), facecolor="w")
    n_trial = len(experiment.task)

    ax = plt.subplot(111)
    ax.patch.set_facecolor("w")
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.yaxis.set_ticks_position('left')
    ax.yaxis.set_tick_params(direction="in")
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_tick_params(direction="in")

    # X = 1+np.arange(n_trial)


    plt.plot(X, P_mean, c='b', lw=2)
    plt.plot(X, P_mean + P_std, c='b', lw=.5)
    plt.plot(X, P_mean - P_std, c='b', lw=.5)
    plt.fill_between(X, P_mean + P_std, P_mean - P_std, color='b', alpha=.1)

    plt.text(n_trial+1, P_mean[-1], "%.2f" % P_mean[-1],
             ha="left", va="center", color="b")

    plt.ylabel("Performance\n", fontsize=16)
    plt.xlim(1,n_trial)
    plt.ylim(0,1.25)

    plt.yticks([ 0.0,   0.2,   0.4,  0.6, 0.8,   1.0])
    plt.text(0, P_mean[0], "%.2f" % P_mean[0],
             ha="right", va="center", color="b")

    fl = folderFig + trial + ".pdf"
    plt.savefig(fl)
    # plt.show()




