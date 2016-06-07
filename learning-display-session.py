# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from experiment import Experiment


def session(exp):
    exp.model.setup()
    for trial in exp.task:
        exp.model.process(exp.task, trial)
    return exp.task.records


mdl = "model-topalidou.json"
#revr = [10,20,30,40,50,60,70,80,90,100,200,300,400,500]
revr = 200
dt = "data_new"
fdl = "reverse" + str(revr) + "-sessions"

trial = str(revr)
tsk = "tasks/task-topalidou-reverse-" + trial + ".json"
rslt = dt + "/results/reverse-NoCtx/experiment-topalidou-reverse-" + trial + ".npy" #
rprt = dt + "/reports/reverse-NoCtx/experiment-topalidou-reverse-" + trial + ".txt"#
experiment = Experiment(model = mdl,
                        task = tsk,
                        result = rslt,
                        report = rprt,
                        n_session = 25, n_block = 1, seed = 123)#None)
records = experiment.run(session, "Protocol Reverse")
records = np.squeeze(records)

    # -----------------------------------------------------------------------------
for session in range(25):

    xlims = 1000
    #session = 0
    P_mean = records["best"][session,:xlims]

    Rwrd_mean = records["reward"][session,:xlims]

    V_mean = records["Values"][session,:xlims]

    Wstr_mean = records["WeightsStr"][session,:xlims]


    plt.close("all")
    plt.figure(figsize=(18, 10), facecolor="w")

    ax = plt.subplot(411)

    ax.patch.set_facecolor("w")
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.yaxis.set_ticks_position('left')
    ax.yaxis.set_tick_params(direction="in")
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_tick_params(direction="in")
    X = 1 + np.arange(xlims)

    plt.plot(X, P_mean, c='b', lw=2)
    plt.text(xlims + 1, P_mean[-1], "%.2f" % P_mean[-1],
             ha="left", va="center", color="b")

    ax = plt.subplot(412)

    ax.patch.set_facecolor("w")
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.yaxis.set_ticks_position('left')
    ax.yaxis.set_tick_params(direction="in")
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_tick_params(direction="in")
    X = 1 + np.arange(xlims)

    plt.plot(X, Rwrd_mean, 'r.', lw=2)
    plt.text(xlims + 1, Rwrd_mean[-1], "%.2f" % Rwrd_mean[-1],
             ha="left", va="center", color="b")
    plt.ylim(-0.2, 1.2)
    plt.yticks([-0.2, 0., 1., 1.2])

    ax = plt.subplot(413)
    ax.patch.set_facecolor("w")
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.yaxis.set_ticks_position('left')
    ax.yaxis.set_tick_params(direction="in")
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_tick_params(direction="in")

    plt.plot(X, V_mean[:,0], c='b', lw=2)
    plt.text(xlims + 1, V_mean[-1,0], "%.2f" % V_mean[-1,0],
             ha="left", va="center", color="b")

    plt.plot(X, V_mean[:,1], c='r', lw=2)
    plt.text(xlims + 1, V_mean[-1,1], "%.2f" % V_mean[-1,1],
             ha="left", va="center", color="r")

    plt.ylabel("Values\n", fontsize=16)
    plt.xlim(1, xlims)


    ax = plt.subplot(414)

    ax.patch.set_facecolor("w")
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.yaxis.set_ticks_position('left')
    ax.yaxis.set_tick_params(direction="in")
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_tick_params(direction="in")


    plt.plot(X, Wstr_mean[:,0], c='b', lw=2)
    plt.text(xlims + 1, Wstr_mean[-1,0], "%.2f" % Wstr_mean[-1,0],
             ha="left", va="center", color="b")

    plt.plot(X, Wstr_mean[:,1], c='r', lw=2)
    plt.text(xlims + 1, Wstr_mean[-1,1], "%.2f" % Wstr_mean[-1,1],
             ha="left", va="center", color="r")


    plt.ylabel("Striatal Weights\n", fontsize=16)
    plt.xlim(1, xlims)




    plt.xlabel("Trial number", fontsize=16)
    plt.xlim(1, xlims)
    # plt.yticks([400, 500, 600, 700, 800, 1000])
    #
    # plt.text(xlims + 1, RT_mean[-1], "%d ms" % RT_mean[-1],
    #          ha="left", va="center", color="r")
    # plt.text(0, RT_mean[0], "%d" % RT_mean[0],
    #          ha="right", va="center", color="r")

    plt.savefig(dt + "/figures/reverse-NoCtx/" + fdl + "/experiment-topalidou-reverse-" + trial + "-learning-session" + str(session) + ".pdf")#-NoCtx
    # plt.show()
