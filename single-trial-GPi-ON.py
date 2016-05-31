# -----------------------------------------------------------------------------
# Copyright (c) 2016, Meropi Topalidou
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------

import random
import numpy as np
import matplotlib.pyplot as plt
from task_single import Task
from model_single import Model

import os

folder = "data/figures/"
if not os.path.exists(folder):
    os.makedirs(folder)

seed = random.randint(0,1000)
np.random.seed(seed)
random.seed(seed)
# seed = 448,380,325
model = Model("model-topalidou.json")
task  = Task("tasks/task-topalidou.json")

print("-"*30)
print("Seed:     %d" % seed)
print("Model:    %s" % model.filename)
print("Task:     %s" % task.filename)
print("-"*30)


trial = task[0]
model.process(task, trial, stop=False, debug=False, cortical_activity=True)

cog = model["CTX"]["cog"].history[:3000]
mot = model["CTX"]["mot"].history[:3000]
init_cog = model["INP"]["cog"].history[:3000]
init_mot = model["INP"]["mot"].history[:3000]


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


plt.plot(timesteps, init_cog[:,0], c='r', label="Cognitive Cortex")
plt.plot(timesteps, init_cog[:,1], c='r')
plt.plot(timesteps, init_cog[:,2], c='r')
plt.plot(timesteps, init_cog[:,3], c='r')
plt.plot(timesteps, init_mot[:,0], c='b', label="Motor Cortex")
plt.plot(timesteps, init_mot[:,1], c='b')
plt.plot(timesteps, init_mot[:,2], c='b')
plt.plot(timesteps, init_mot[:,3], c='b')

# plt.title("Single trial (GPi ON)")
plt.xlabel("Time (seconds)")
plt.ylabel("Activity (Hz)")
plt.legend(frameon=False, loc='upper left')
plt.xlim(0.0,duration)
plt.ylim(-10.0,60.0)
plt.xticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
           ['0.0','0.5\n(Trial start)','1.0','1.5', '2.0','2.5','3.0'])
file = folder + "single-trial-GPi-ON.pdf"
plt.savefig(file)




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
file = folder + "single-trial-GPi-ON.pdf"
plt.savefig(file)







histor = model.history(3000)


fig = plt.figure(figsize=(20,14))
fig.patch.set_facecolor('1.0')

# fig.suptitle('Single trial (GPi ON)', fontsize=24)


timesteps = np.linspace(0,duration, len(histor))

def subplot(rows,cols,n, alpha=0.0):
    ax = plt.subplot(rows,cols,n)
    ax.patch.set_facecolor("k")
    ax.patch.set_alpha(alpha)

    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.yaxis.set_ticks_position('left')
    ax.yaxis.set_tick_params(direction="outward")
    return ax

ax = subplot(6,3,1)
ax.set_title("Motor", fontsize=24)
ax.set_ylabel("STN", fontsize=24)
for i in range(4):
    plt.plot(timesteps, histor["STN"]["mot"][:,i], c='k', lw=.5)
ax.set_xticks([])

ax = subplot(6,3,2)
ax.set_title("Cognitive", fontsize=24)
for i in range(4):
    plt.plot(timesteps, histor["STN"]["cog"][:,i], c='k', lw=.5)
ax.set_xticks([])

ax = subplot(6,3,3,alpha=0)
ax.set_title("Associative", fontsize=24)
ax.set_xticks([])
ax.set_yticks([])
ax.spines['left'].set_color('none')


ax = subplot(6,3,4)
ax.set_ylabel("Cortex", fontsize=24)
for i in range(4):
    plt.plot(timesteps, histor["CTX"]["mot"][:,i], c='k', lw=.5)
ax.set_xticks([])

ax = subplot(6,3,5)
for i in range(4):
    plt.plot(timesteps, histor["CTX"]["cog"][:,i], c='k', lw=.5)
ax.set_xticks([])

ax = subplot(6,3,6)
for i in range(16):
    plt.plot(timesteps, histor["CTX"]["ass"][:,i], c='k', lw=.5)
ax.set_xticks([])

ax = subplot(6,3,7)
ax.set_ylabel("Striatum", fontsize=24)
for i in range(4):
    plt.plot(timesteps, histor["STR"]["mot"][:,i], c='k', lw=.5)
ax.set_xticks([])

ax = subplot(6,3,8)
for i in range(4):
    plt.plot(timesteps, histor["STR"]["cog"][:,i], c='k', lw=.5)
ax.set_xticks([])

ax = subplot(6,3,9)
for i in range(16):
    plt.plot(timesteps, histor["STR"]["ass"][:,i], c='k', lw=.5)
ax.set_xticks([])

ax = subplot(6,3,10)
ax.set_ylabel("GPe", fontsize=24)
for i in range(4):
    plt.plot(timesteps, histor["GPE"]["mot"][:,i], c='k', lw=.5)
ax.set_xticks([])

ax = subplot(6,3,11)
for i in range(4):
    plt.plot(timesteps, histor["GPE"]["cog"][:,i], c='k', lw=.5)
ax.set_xticks([])

ax = subplot(6,3,13)
ax.set_ylabel("GPi", fontsize=24)
for i in range(4):
    plt.plot(timesteps, histor["GPI"]["mot"][:,i], c='k', lw=.5)
ax.set_xticks([])

ax = subplot(6,3,14)
for i in range(4):
    plt.plot(timesteps, histor["GPI"]["cog"][:,i], c='k', lw=.5)
ax.set_xticks([])
ax = subplot(6,3,16)
ax.set_ylabel("Thalamus", fontsize=24)
for i in range(4):
    plt.plot(timesteps, histor["THL"]["mot"][:,i], c='k', lw=.5)
ax.set_xticks([])

ax = subplot(6,3,17)
for i in range(4):
    plt.plot(timesteps, histor["THL"]["cog"][:,i], c='k', lw=.5)
ax.set_xticks([])

#
# file = folder + "single-trial-GPi-ON-all.pdf"
# plt.savefig(file)

plt.show()
