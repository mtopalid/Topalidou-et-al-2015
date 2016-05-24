# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier, Meropi Topalidou
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Generic bandit task using at most 4 cues at 4 different positions.
A task is made of n trials.
A trial is fully described by 4 arrays:
cog:   4 items, indicate which cues are present (A,B,C,D)
mot:   4 items, indicate where cues are present (1,2,3,4)
ass: 4x4 items, indicate the position of cues (A1, A2,..., D3, D4)
rew:   4 items, indicate the reward probability associated with each
                cue for this specific trial
Example
-------
A is in position 3, reward probablity is a
C is in position 2, reward probablity is c
B is not present, D is not present
cue :  [1, 0, 1, 0]
pos :  [0, 1, 1, 0]
rwd :  [a, b, c, d]
ass : [[0, 0, 0, 0],
       [0, 0, 0, 0],
       [0, 0, 1, 0],
       [1, 0, 0, 0]]
Usage
-----
task = Task(n=120)
for trial in task:
    choice = ...
    RT = ...
    reward, best = task.process(trial, choice, RT)
"""
import json
import random
import numpy as np


class Task(object):
    """ A two-armed bandit task """

    def __init__(self, filename="task-guthrie.json"):
        self.index       = None
        self.index_start = None
        self.index_stop  = None

        self.filename = filename
        self.parameters = json.load(open(filename))
        self.setup()


    def block(self,index):
        self.index_start = self.blocks[index][0]-1
        self.index_stop  = self.blocks[index][1]
        self.index = self.index_start
        return self


    def setup(self):

        _ = self.parameters

        blocks = []
        for name in _["session"]:
            blocks.append(_[name])

        # Get total number of trials
        n = 0
        self.blocks = []
        start,stop = 0, 0
        for block in blocks:
            start = stop
            stop += block["n_trial"]
            self.blocks.append((start,stop))
            n += block["n_trial"]

        # Build corresponding arrays
        self.trials = np.zeros(n, [("mot", float, 4),
                                   ("cog", float, 4),
                                   ("ass", float, (4,4)),
                                   ("rwd", float, 4),
                                   ("rnd", float, 1) ] )
        self.records  = np.zeros(n, [("choice", float, 1),
                                     ("best",   float, 1),
                                     ("valid",  float, 1),
                                     ("RT",     float, 1),
                                     ("Values",  float, 4),
                                     ("WeightsStr", float, 4),
                                     ("WeightsCtx", float, 4),
                                     ("CtxCog", float, (3000,4)),
                                     ("CtxMot", float, (3000,4)),
                                     ("reward", float, 1)] )

        # We draw all random probabilities at once (faster)
        self.trials["rnd"] = np.random.uniform(0,1,n)

        # Build actual trials
        index = 0
        for block in blocks:
            n = block["n_trial"]
            cue = np.array(block["cue"],float)
            P_cue = np.cumsum(cue) / np.sum(cue)
            pos = block["pos"]
            P_pos = np.cumsum(pos) / np.sum(pos)
            rwd = block["rwd"]

            for i in range(n):
                c1 = c2 =  np.searchsorted(P_cue, random.uniform(0,1))
                while c1 == c2:
                    c2 = np.searchsorted(P_cue, random.uniform(0,1))

                m1 = m2 =  np.searchsorted(P_pos, random.uniform(0,1))
                while m1 == m2:
                    m2 = np.searchsorted(P_pos, random.uniform(0,1))

                trial = self.trials[index]
                trial["cog"][[c1,c2]] = 1
                trial["mot"][[m1,m2]] = 1
                trial["ass"][c1,m1]   = 1
                trial["ass"][c2,m2]   = 1
                trial["rwd"][...]     = rwd
                index += 1


    def __iter__(self):
        if self.index_start is None:
            self.setup()
            self.index_start = -1
            self.index_stop  = len(self)
            self.index = self.index_start
        return self

    def __next__(self):
        self.index += 1
        if self.index < self.index_stop:
            return self.trials[self.index]

        self.index       = None
        self.index_start = None
        self.index_stop  = None
        raise StopIteration

    def __len__(self):
        return len(self.trials)

    def __getitem__(self, index):
        return self.trials[index]


    def process(self, trial, choice, RT=0.0, debug=False):
        """
        Process a (motor) choice and return the reward and whether this was the
        best choice for this trial.
        """

        # Do we have a choice at least ?
        if choice < 0:
            # No cue chosen
            cue = -1
            # Choice is not valid
            valid = False
            # Not the best move
            best = False
            # No choice, no reward
            reward = 0.0
        else:
            # Check if choice is valid
            valid = (trial["mot"][choice] == 1.0)
            # Get cue corresponding to motor choice
            cue = np.argmax(trial["ass"][:,choice])
            # Get whether this is the best choice
            best = (np.argmax(trial["cog"]*trial["rwd"]) == cue)
            # Get actual reward
            reward = trial["rnd"] < trial["rwd"][cue]

        # Record everything
        self.records[self.index]["RT"] = RT
        self.records[self.index]["best"] = best
        self.records[self.index]["valid"] = valid
        self.records[self.index]["choice"] = choice
        self.records[self.index]["reward"] = reward

        if debug:
            if best: s = " (+)"
            else:    s = " (-)"
            print("Trial %d%s" % ((self.index+1), s))
            P = self.records[:self.index+1]["best"]
            print("  Mean performance: %.3f" % np.array(P).mean())
            R = self.records[:self.index+1]["reward"]
            print("  Mean reward:      %.3f" % np.array(R).mean())

        return reward, cue, best

    def save_learning(self, values=0.5, WStr=0.5, WCtx=0.5):
        """
    	Save the values of the cues in reinforcement learning and
    	both cortical and striatal weights changes through learning
    	"""
        self.records[self.index]["Values"] = values
        self.records[self.index]["WeightsStr"] = WStr
        self.records[self.index]["WeightsCtx"] = WCtx


    def cortical_activity(self, cog, mot):
        """
    	Save the values of the cues in reinforcement learning and
    	both cortical and striatal weights changes through learning
    	"""
        self.records[self.index]["CtxCog"] = cog
        self.records[self.index]["CtxMot"] = mot


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    task = Task()

    for trial in task:
        # Best choice
        best = np.argmax(trial["cog"]*trial["rwd"])
        choice = np.argmax(trial["ass"][best])
        # Random choice
        # n = len(trial["mot"]) - 1 - random.randint(0,trial["mot"].sum()-1)
        # choice = np.argsort(trial["mot"])[n]
        # Process choice
        reward, cue, best = task.process(trial, choice, debug=True)
