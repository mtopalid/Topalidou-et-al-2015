# -----------------------------------------------------------------------------
# Copyright (c) 2016, Meropi Topalidou
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from experiment_single import Experiment # Creation of folders to save the results
import os
folder = "data/"
if not os.path.exists(folder):
    os.makedirs(folder)

folderRes = folder + "results/"
if not os.path.exists(folderRes):
    os.makedirs(folderRes)

folderRep = folder + "reports/"
if not os.path.exists(folderRep):
    os.makedirs(folderRep)

folderFig = folder + "figures/"
if not os.path.exists(folderFig):
    os.makedirs(folderFig)


def session(exp):

    exp.model.setup()
    exp.task.setup()

    # Block 1 : GPi ON
    for trial in exp.task.block(0):
        exp.model.process(exp.task, trial, stop=False, cortical_activity=True)

    # Block 2 : GPi ON
    for trial in exp.task.block(1):
        exp.model.process(exp.task, trial, stop=False, cortical_activity=True)

    # Block 3 : GPi ON
    for trial in exp.task.block(2):
        exp.model.process(exp.task, trial, stop=False, cortical_activity=True)

    return exp.task.records
mdl = "model-topalidou.json"
tsk = "tasks/task-piron.json"
rslt = folderRes + "single-session-piron.npy"
rprt = folderRep + "single-session-piron.txt"
experiment = Experiment(model = mdl,
                        task = tsk,
                        result = rslt,
                        report = rprt,
                        n_session = 1, n_block = 1, seed = 123)#None)
records = experiment.run(session, "Piron Protocol")
records = np.squeeze(records)
print(records["best"])


cog = records["CtxCog"][-1]
mot = records["CtxMot"][-1]


duration = 3.0
timesteps = np.linspace(0, duration, 3000)
fig = plt.figure(figsize=(9,7), facecolor="w")
ax = plt.subplot(111)
ax.patch.set_facecolor("w")
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.yaxis.set_ticks_position('left')
ax.yaxis.set_tick_params(direction="in")
ax.xaxis.set_ticks_position('bottom')
ax.xaxis.set_tick_params(direction="in")


plt.plot(timesteps, cog[:,0], c='r', label="Cognitive Cortex")
plt.plot(timesteps, cog[:,1], c='r')
plt.plot(timesteps, cog[:,2], c='r')
plt.plot(timesteps, cog[:,3], c='r')
plt.plot(timesteps, mot[:,0], c='b', label="Motor Cortex")
plt.plot(timesteps, mot[:,1], c='b')
plt.plot(timesteps, mot[:,2], c='b')
plt.plot(timesteps, mot[:,3], c='b')

# plt.title("Single trial (GPi ON)")
plt.xlabel("Time (seconds)")
plt.ylabel("Activity (Hz)")
plt.legend(frameon=False, loc='upper left')
plt.xlim(0.0,duration)
plt.ylim(-10.0,60.0)
plt.xticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
           ['0.0','0.5\n(Trial start)','1.0','1.5', '2.0','2.5','3.0'])
file = folderFig + "single-session-activity-piron.pdf"
plt.savefig(file)
plt.show()
