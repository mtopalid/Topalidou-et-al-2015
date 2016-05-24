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

folderRes = folder + "results/piron/"
if not os.path.exists(folderRes):
    os.makedirs(folderRes)

folderRep = folder + "reports/piron/"
if not os.path.exists(folderRep):
    os.makedirs(folderRep)

folderFig = folder + "figures/piron/"
if not os.path.exists(folderFig):
    os.makedirs(folderFig)



def session(exp):
    exp.model.setup()
    exp.task.setup()

    # Block 1 : GPi ON
    for trial in exp.task.block(0):
        exp.model.process(exp.task, trial)

    # Block 2 : GPi ON
    for trial in exp.task.block(1):
        exp.model.process(exp.task, trial)

    # Block 3 : GPi ON
    for trial in exp.task.block(2):
        exp.model.process(exp.task, trial)

    return exp.task.records


mdl = "model-topalidou.json"
tsk = "tasks/task-piron.json"
rslt = folderRes + "control.npy"
rprt = folderRep + "control.txt"
experiment = Experiment(model = mdl,
						task = tsk,
						result = rslt,
						report = rprt,
                        n_session = 25, n_block = 1, seed = 1)
records = experiment.run(session, "Piron Protocol Control")
records = np.squeeze(records)






#
# # Textual results
# # -----------------------------------------------------------------------------
w = 5
start,end = experiment.task.blocks[0]
P = np.mean(records["best"][:,end-w:end],axis=1)
mean,std = np.mean(P), np.std(P)
print("Performances:")
print("--------------------------------------")
print("Training (HC, GPi On):  %.2f ± %.2f" % (mean,std))

start,end = experiment.task.blocks[1]
P = np.mean(records["best"][:,end-w:end],axis=1)
mean,std = np.mean(P), np.std(P)
print("Test (HC, GPi On): %.2f ± %.2f" % (mean,std))

start,end = experiment.task.blocks[2]
P = np.mean(records["best"][:,start:start+25],axis=1)
mean,std = np.mean(P), np.std(P)
print("Test start(NC, GPi On): %.4f ± %.4f" % (mean,std))
start,end = experiment.task.blocks[2]
P = np.mean(records["best"][:,end-25:end],axis=1)
mean,std = np.mean(P), np.std(P)
print("Test end(NC, GPi On): %.4f ± %.4f" % (mean,std))


start,end = experiment.task.blocks[0]
P = np.mean(records["RT"][:,end-w:end],axis=1)*1000
mean,std = np.mean(P), np.std(P)
print("\n\nReaction time:")
print("--------------------------------------")
print("Training (HC, GPi On):  %.2f ± %.2f" % (mean,std))

start,end = experiment.task.blocks[1]
P = np.mean(records["RT"][:,end-w:end],axis=1)*1000
mean,std = np.mean(P), np.std(P)
print("Test (HC, GPi On): %.2f ± %.2f" % (mean,std))

start,end = experiment.task.blocks[2]
P = np.mean(records["RT"][:,end-w:end],axis=1)*1000
mean,std = np.mean(P), np.std(P)
print("Test (NC, GPi On): %.2f ± %.2f" % (mean,std))

# Graphical results
# -----------------------------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib import lines

start,end = experiment.task.blocks[0]
D1 = records["best"][:,start:end]

start,end = experiment.task.blocks[1]
D2 = records["best"][:,start:end]

start,end = experiment.task.blocks[2]
D3 = records["best"][:,start:end]

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

n = D2.shape[1]-1
X = np.arange(1,n+1)
global_mean = np.zeros(n)
local_mean = np.zeros(n)
for j in range(len(D2)):
    for i in range(n):
        imin, imax = max(i+1-sliding_window,0), i+1
        global_mean[i] = D2[:,imin:imax].mean()
        local_mean[i] = D2[j,imin:imax].mean()
    plt.plot(X, local_mean, c='g', lw=1, alpha=alpha)
plt.plot(X, global_mean, c='g', lw=2)

X += n+1
for j in range(len(D3)):
    for i in range(n):
        imin, imax = max(i+1-sliding_window,0), i+1
        global_mean[i] = D3[:,imin:imax].mean()
        local_mean[i] = D3[j,imin:imax].mean()
    plt.plot(X, local_mean, c='m', lw=1, alpha=alpha)
plt.plot(X, global_mean, c='m', lw=2)

ax.axvline(120, linewidth=0.75, c='k', alpha=.75)

plt.xticks([60, 180, 420],
           ["\nHC, 120 trials",
            "\nNC, 120 trials"])
x,y = np.array([[1, 119], [-0.025, -0.025]])
ax.add_line(lines.Line2D(x, y, lw=1, color='k', clip_on=False))
ax.add_line(lines.Line2D(x+120, y, lw=1, color='k', clip_on=False))

plt.ylabel("Instantaneous performance\n(sliding window of %d trials)" % sliding_window, fontsize=14)
plt.xlim(0,2*(n+1))
plt.ylim(0,1.05)

# plt.title("Piron Protocol control(model, N=%d)" % experiment.n_session)

fl = folderFig + "control.pdf"
plt.savefig(fl)


start,end = experiment.task.blocks[1]
D2 = records["RT"][:,start:end] * 1000

start,end = experiment.task.blocks[2]
D3 = records["RT"][:,start:end] * 1000



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

n = D2.shape[1]-1
X = np.arange(1,n+1)
global_mean = np.zeros(n)
local_mean = np.zeros(n)
for j in range(len(D2)):
    for i in range(n):
        imin, imax = max(i+1-sliding_window,0), i+1
        global_mean[i] = D2[:,imin:imax].mean()
        local_mean[i] = D2[j,imin:imax].mean()
    plt.plot(X, local_mean, c='g', lw=1, alpha=alpha)
plt.plot(X, global_mean, c='g', lw=2)

X += n+1
for j in range(len(D3)):
    for i in range(n):
        imin, imax = max(i+1-sliding_window,0), i+1
        global_mean[i] = D3[:,imin:imax].mean()
        local_mean[i] = D3[j,imin:imax].mean()
    plt.plot(X, local_mean, c='m', lw=1, alpha=alpha)
plt.plot(X, global_mean, c='m', lw=2)

ax.axvline(120, linewidth=0.75, c='k', alpha=.75)

plt.xticks([60, 180],
           ["\nHC, 120 trials",
            "\nNC, 120 trials"])
x,y = np.array([[1, 119], [-0.025, -0.025]])
ax.add_line(lines.Line2D(x, y, lw=1, color='k', clip_on=False))
ax.add_line(lines.Line2D(x+120, y, lw=1, color='k', clip_on=False))

plt.ylabel("Reaction Time\n(sliding window of %d trials)" % sliding_window, fontsize=14)
plt.xlim(0,2*(n+1))
# plt.ylim(0,1.05)

# plt.title("Piron Protocol control(model, N=%d)" % experiment.n_session)

fl = folderFig + "RT-control.pdf"
plt.savefig(fl)


# Histograms


start,end = experiment.task.blocks[1]
P = np.mean(records["best"][:,start:start+25],axis=1)
mean_str,std_str = np.mean(P), np.std(P)
P = np.mean(records["best"][:,end-25:end],axis=1)
mean_end,std_end = np.mean(P), np.std(P)
D2_mean, D2_std = (mean_str, mean_end), (std_str, std_end)

start,end = experiment.task.blocks[2]
P = np.mean(records["best"][:,start:start+25],axis=1)
mean_str,std_str = np.mean(P), np.std(P)
P = np.mean(records["best"][:,end-25:end],axis=1)
mean_end,std_end = np.mean(P), np.std(P)
D3_mean, D3_std = (mean_str, mean_end), (std_str, std_end)



fig = plt.figure(figsize=(6,5), facecolor="w", dpi=50)
ax = plt.subplot(111)

ax.tick_params(axis='both', which='major', labelsize=8)

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

plot(index-width+0.0, D2_mean, D2_std, 'g', 0.45)
plot(index-width+2.5, D3_mean, D3_std, 'm', 0.45)

plt.xlim(-1.5,+4.0)
plt.xticks([-0.5,0.0,0.5, 2.0, 2.5, 3.0, 3.5],
           ["25 first\ntrials","\n\n\nDay 2 (GPi ON)\n","25 last\ntrials",
            "25 first\ntrials","\n\n\nDay 3 (GPi OFF)\n","25 last\ntrials"])
plt.ylim(0.0,1.2)
plt.ylabel("Ratio of optimum trials")
plt.yticks([0,.25,.5,.75,1.0])

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')

x,y = np.array([[-1.05, 1.0], [-0.1, -0.1]])

ax.add_line(lines.Line2D(x+0.0, y, lw=.5, color='k', clip_on=False))
ax.add_line(lines.Line2D(x+2.5, y, lw=.5, color='k', clip_on=False))



# plt.title("Theoretical results (model)")



fl = folderFig + "histogram-control.pdf"
plt.savefig(fl)






start,end = experiment.task.blocks[1]
P = np.mean(records["RT"][:,start:start+25]*1000,axis=1)
mean_str,std_str = np.mean(P), np.std(P)
P = np.mean(records["RT"][:,end-25:end]*1000,axis=1)
mean_end,std_end = np.mean(P), np.std(P)
D2_mean, D2_std = (mean_str, mean_end), (std_str, std_end)

start,end = experiment.task.blocks[2]
P = np.mean(records["RT"][:,start:start+25]*1000,axis=1)
mean_str,std_str = np.mean(P), np.std(P)
P = np.mean(records["RT"][:,end-25:end]*1000,axis=1)
mean_end,std_end = np.mean(P), np.std(P)
D3_mean, D3_std = (mean_str, mean_end), (std_str, std_end)



fig = plt.figure(figsize=(6,5), facecolor="w", dpi=50)
ax = plt.subplot(111)

ax.tick_params(axis='both', which='major', labelsize=8)

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

plot(index-width+0.0, D2_mean, D2_std, 'g', 0.45)
plot(index-width+2.5, D3_mean, D3_std, 'm', 0.45)

plt.xlim(-1.5,+4.0)
plt.xticks([-0.5,0.0,0.5, 2.0, 2.5, 3.0, 3.5],
           ["25 first\ntrials","\n\n\nDay 2 (GPi ON)\n","25 last\ntrials",
            "25 first\ntrials","\n\n\nDay 3 (GPi OFF)\n","25 last\ntrials"])
# plt.ylim(0.0,1.2)
plt.ylabel("Mean Motor Decision Time (ms)")
# plt.yticks([0,.25,.5,.75,1.0])

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')

x,y = np.array([[-1.05, 1.0], [-0.1, -0.1]])

ax.add_line(lines.Line2D(x+0.0, y, lw=.5, color='k', clip_on=False))
ax.add_line(lines.Line2D(x+2.5, y, lw=.5, color='k', clip_on=False))



# plt.title("Theoretical results (model)")



fl = folderFig + "hist-RT-control.pdf"
plt.savefig(fl)

plt.show()
