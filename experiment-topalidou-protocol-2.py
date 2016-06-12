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

    # Day 1 : GPi OFF
    g1 = exp.model["GPi:cog → THL:cog"].gain
    g2 = exp.model["GPi:mot → THL:mot"].gain
    exp.model["GPi:cog → THL:cog"].gain = 0
    exp.model["GPi:mot → THL:mot"].gain = 0
    for trial in exp.task.block(0):
        exp.model.process(exp.task, trial)
    records[0] = exp.task.records

    # Day 2: GPi ON
    exp.model["GPi:cog → THL:cog"].gain = g1
    exp.model["GPi:mot → THL:mot"].gain = g2
    for trial in exp.task.block(0):
        exp.model.process(exp.task, trial)
    records[1] = exp.task.records

    # Day 1 : GPi OFF
    exp.model["GPi:cog → THL:cog"].gain = 0
    exp.model["GPi:mot → THL:mot"].gain = 0
    for trial in exp.task.block(0):
        exp.model.process(exp.task, trial)
    records[2] = exp.task.records

    return records


mdl = "model-topalidou.json"
tsk = "tasks/task-topalidou.json"
rslt = folderRes + "protocol-2.npy"
rprt = folderRep + "protocol-2.txt"
experiment = Experiment(model = mdl,
						task = tsk,
						result = rslt,
						report = rprt,
                        n_session = 25, n_block = 3, seed=927)
records = experiment.run(session, "Topalidou Protocol 2")


# Textual results
# -----------------------------------------------------------------------------
P = np.squeeze(records["best"][:,0,:25])
P = P.mean(axis=len(P.shape)-1)
print("D1 start: %.3f ± %.3f" % (P.mean(), P.std()))
P = np.squeeze(records["best"][:,0,-25:])
P = P.mean(axis=len(P.shape)-1)
print("D1 end:   %.3f ± %.3f" % (P.mean(), P.std()))

P = np.squeeze(records["RT"][:,0])
print("D1 mean RT: %.3f ± %.3f" % (P.mean(), P.std()))

print()

P = np.squeeze(records["best"][:,1,:25])
P = P.mean(axis=len(P.shape)-1)
print("D2 start: %.3f ± %.3f" % (P.mean(), P.std()))
P = np.squeeze(records["best"][:,1,-25:])
P = P.mean(axis=len(P.shape)-1)
print("D2 end:   %.3f ± %.3f" % (P.mean(), P.std()))

P = np.squeeze(records["RT"][:,1])
print("D2 mean RT: %.3f ± %.3f" % (P.mean(), P.std()))

print()

P = np.squeeze(records["best"][:,2,:25])
P = P.mean(axis=len(P.shape)-1)
print("D3 start: %.3f ± %.3f" % (P.mean(), P.std()))
P = np.squeeze(records["best"][:,2,-25:])
P = P.mean(axis=len(P.shape)-1)
print("D3 end:   %.3f ± %.3f" % (P.mean(), P.std()))

P = np.squeeze(records["RT"][:,2])
print("D3 mean RT: %.3f ± %.3f" % (P.mean(), P.std()))

print("-"*30)



# Graphical results
# -----------------------------------------------------------------------------
from figures import *
# figure_H_P(records, [0,1,0], "Protocol 2", "data/experiment-topalidou-protocol-2-H-P.pdf")
# figure_H_RT(records, [0,1,0], "Protocol 2", "data/experiment-topalidou-protocol-2-H-RT.pdf")
fl = folderFig + "protocol-2-P.pdf"
figure_P(records, [0,1,0], "Protocol 2", fl)
# figure_RT(records, [0,1,0], "Protocol 2", "data/experiment-topalidou-protocol-2-RT.pdf")
