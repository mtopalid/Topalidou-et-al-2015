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
    records = np.zeros((exp.n_block, exp.n_trial), dtype=exp.task.records.dtype)

    # Day 1 : Str OFF


    g1 = exp.model["CTX:cog → STR:cog"].gain

    exp.model["CTX:cog → STR:cog"].gain = 0


    for trial in exp.task.block(0):
        exp.model.process(exp.task, trial)
    records[0] = exp.task.records

    # Day 2: Str ON
    exp.model["CTX:cog → STR:cog"].gain = g1
    for trial in exp.task.block(0):
        exp.model.process(exp.task, trial)
    records[1] = exp.task.records


    return records


mdl = "model-topalidou-thomas.json"
tsk = "tasks/task-topalidou.json"
rslt = folderRes + "protocol-NoStrCog.npy"
rprt = folderRep + "protocol-NoStrCog.txt"
experiment = Experiment(model = mdl,
						task = tsk,
						result = rslt,
						report = rprt,
                        n_session = 25, n_block = 2, seed=377)
records = experiment.run(session, "Thomas Protocol No Str Cog")


# Textual results
# -----------------------------------------------------------------------------
P = np.squeeze(records["best"][:,0,:25])*100
P = P.mean(axis=len(P.shape)-1)
print("D1 start: %.3f ± %.3f" % (P.mean(), P.std()))
P = np.squeeze(records["best"][:,0,-25:])*100
P = P.mean(axis=len(P.shape)-1)
print("D1 end:   %.3f ± %.3f" % (P.mean(), P.std()))

print()

P = np.squeeze(records["best"][:,1,:25])*100
P = P.mean(axis=len(P.shape)-1)
print("D2 start: %.3f ± %.3f" % (P.mean(), P.std()))
P = np.squeeze(records["best"][:,1,-25:])*100
P = P.mean(axis=len(P.shape)-1)
print("D2 end:   %.3f ± %.3f" % (P.mean(), P.std()))

print()

# Graphical results
# -----------------------------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib import lines

#shape = records.shape
#records = records.reshape(shape[0], shape[1]*shape[2])

D1 = np.squeeze(records["best"][:,0,:])
D2 = np.squeeze(records["best"][:,1,:])
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
    plt.plot(X, local_mean, c='r', lw=1, alpha=alpha)
plt.plot(X, global_mean, c='r', lw=2)

X += n+1
for j in range(len(D2)):
    for i in range(n):
        imin, imax = max(i+1-sliding_window,0), i+1
        global_mean[i] = D2[:,imin:imax].mean()
        local_mean[i] = D2[j,imin:imax].mean()
    plt.plot(X, local_mean, c='b', lw=1, alpha=alpha)
plt.plot(X, global_mean, c='b', lw=2)

ax.axvline(120, linewidth=0.75, c='k', alpha=.75)
ax.axvline(240, linewidth=0.75, c='k', alpha=.75)

plt.xticks([60, 180, 300],
           ["\nDay 1, GPi OFF, 120 trials",
            "\nDay 2, GPi ON, 120 trials"])

x,y = np.array([[1, 119], [-0.025, -0.025]])
ax.add_line(lines.Line2D(x, y, lw=1, color='k', clip_on=False))
ax.add_line(lines.Line2D(x+120, y, lw=1, color='k', clip_on=False))
ax.add_line(lines.Line2D(x+240, y, lw=1, color='k', clip_on=False))

plt.ylabel("Instantaneous performance\n(sliding window of %d trials)" % sliding_window, fontsize=14)
plt.xlim(0,3*(n+1))
plt.ylim(0,1.05)

plt.title("Thomas Protocol (model, N=%d)" % experiment.n_session)

fl = folderFig + "protocol-cog.pdf"
plt.savefig(fl)



import numpy as np
from matplotlib import lines
import matplotlib.pyplot as plt


dpi = 50
# Model

P = np.squeeze(records["best"][:,0,:25])
P = P.mean(axis=len(P.shape)-1)
Dstr = P.mean(), P.std()
P = np.squeeze(records["best"][:,0,-25:])
P = P.mean(axis=len(P.shape)-1)
Dend = P.mean(), P.std()
D1_mean, D1_std = (Dstr[0], Dend[0]), (Dstr[1], Dend[1])

P = np.squeeze(records["best"][:,1,:25])
P = P.mean(axis=len(P.shape)-1)
Dstr = P.mean(), P.std()
P = np.squeeze(records["best"][:,1,-25:])
P = P.mean(axis=len(P.shape)-1)
Dend = P.mean(), P.std()
D2_mean, D2_std = (Dstr[0], Dend[0]), (Dstr[1], Dend[1])



fig = plt.figure(figsize=(6,5), facecolor="w", dpi=dpi)
ax = plt.subplot(111)

ax.tick_params(axis='both', which='major', labelsize=12)

ax.xaxis.set_tick_params(size=0)
ax.yaxis.set_tick_params(width=1)

index = np.array([0,1])
width = 1
color = 'r'

# Pull the formatting out here
bar_kw = {'width': 0.95, 'linewidth':0, 'zorder':5}
err_kw = {'zorder': 10, 'fmt':'none', 'linewidth':0, 'elinewidth':1, 'ecolor':'k'}

def plot(X, mean, sigma, color, alpha):
    plt.bar(X, mean, alpha=alpha, color=color, **bar_kw)
    _,caps,_ = plt.errorbar(X+width/2.0, mean, sigma, **err_kw)
    for cap in caps: cap.set_markeredgewidth(1)

plot(index-width+0.0, D1_mean, D1_std, 'r', 0.45)
plot(index-width+2.5, D2_mean, D2_std, 'b', 0.45)

plt.xlim(-1.5,+6.5)
plt.xticks([-0.5,0.0,0.5, 2.0, 2.5, 3.0, 4.5, 5.0, 5.5],
           ["25 first\ntrials","\n\n\nDay 1 (GPi OFF)\n","25 last\ntrials",
            "25 first\ntrials","\n\n\nDay 2 (GPi ON)\n","25 last\ntrials"])
plt.ylim(0.0,1.2)
plt.ylabel("Ratio of optimum trials")
plt.yticks([0,.25,.5,.75,1.0])

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')

x,y = np.array([[-1.05, 1.0], [-0.15, -0.15]])

ax.add_line(lines.Line2D(x+0.0, y, lw=.5, color='k', clip_on=False))
ax.add_line(lines.Line2D(x+2.5, y, lw=.5, color='k', clip_on=False))
ax.add_line(lines.Line2D(x+5.0, y, lw=.5, color='k', clip_on=False))

x,y = np.array([[-1.05, 1.0], [1.05, 1.05]])
ax.add_line(lines.Line2D(x+0.0, y, lw=.5, color='k', clip_on=False))
ax.add_line(lines.Line2D(x+2.5, y, lw=.5, color='k', clip_on=False))
ax.add_line(lines.Line2D(x+5.0, y, lw=.5, color='k', clip_on=False))

ax.text(0.0, 1.065, "Value acquisition", ha="center", va="bottom", fontsize=12)
ax.text(2.5, 1.065, "Habit acquisition", ha="center", va="bottom", fontsize=12)
ax.text(5.0, 1.065, "Habit expression",  ha="center", va="bottom", fontsize=12)


plt.tight_layout(pad=0)
fl = folderFig + "protocol-histogram-cog.pdf"
plt.savefig(fl, dpi=dpi)
#plt.show()



plt.show()
