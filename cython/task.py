# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Nicolas P. Rougier, Meropi Topalidou
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np


# -------------------------------------------------------------------- Task ---
class Task(object):
    """ A two-armed bandit task """

    def __init__(self, n=None, setup=True):
        self.trials = None
        self.records = None
        if setup:
            if n is None:
                self.setup()
            else:
                self.setup(n=n)

    def __iter__(self):
        self.index = -1
        return self

    def __next__(self):
        self.index += 1
        if self.index < len(self.trials):
            return self.trials[self.index]
        raise StopIteration

    def __len__(self):
        return len(self.trials)

    def __getitem__(self, index):

        if isinstance(index, slice):
            task = type(self)(setup=False)
            task.trials = self.trials[index]  # .copy()
            task.records = self.records[index]  # .copy()
            return task
        else:
            self.index = index
            return self.trials[index]

    def build(self, n):
        self.trials = np.zeros(n, [("mot", float, 4),
                                   ("cog", float, 4),
                                   ("ass", float, (4, 4)),
                                   ("rwd", float, 4)])
        self.records = np.zeros(n, [("action", float, 1),
                                    ("shape", float, 1),
                                    ("cog_choice", float, 1),
                                    ("best", float, 1),
                                    ("RTcog", float, 1),
                                    ("RTmot", float, 1),
                                    ("CueValues", float, 4),
                                    ("Wstr", float, 4),
                                    ("Wcog", float, 4),
                                    ("Wmot", float, 4),
                                    ("reward", float, 1)])

    def setup(self, n=120):
        self.n = n

        # Make sure count is a multiple of 6
        n = (n // 6) * 6
        self.build(2 * n)

        # All combinations of cues or positions
        Z = np.array([[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]])

        # n//6 x all combinations of cues
        M = np.repeat(np.arange(6), n // 6)
        np.random.shuffle(M)
        mot = Z[M]
        for i in range(mot.shape[0]):
            np.random.shuffle(mot[i, :])

        Z = np.array([0, 1])
        cogf = np.tile(Z, (n, 1))
        for i in range(cogf.shape[0]):
            np.random.shuffle(cogf[i, :])

        Z = np.array([2, 3])
        cogUf = np.tile(Z, (n, 1))
        for i in range(cogUf.shape[0]):
            np.random.shuffle(cogUf[i, :])

        for i in range(n):
            c1, c2 = cogf[i]
            m1, m2 = mot[i]
            trial = self.trials[i]
            trial["cog"][[c1, c2]] += 1
            trial["mot"][[m1, m2]] += 1
            trial["ass"][m1, c1] += 1
            trial["ass"][m2, c2] += 1
            trial["rwd"][...] = 0.75, 0.25, 0.75, 0.25

            c1, c2 = cogUf[i]
            trial = self.trials[n + i]
            trial["cog"][[c1, c2]] += 1
            trial["mot"][[m1, m2]] += 1
            trial["ass"][m1, c1] += 1
            trial["ass"][m2, c2] += 1
            trial["rwd"][...] = 0.75, 0.25, 0.75, 0.25

    def process(self, trial, action, RT=0, debug=False):

        # Only the associative feature can provide (m1,c1) and (m2,c2)
        i1, i2 = (trial["ass"].ravel().argsort())[-2:]
        m1, c1 = np.unravel_index(i1, (4, 4))
        m2, c2 = np.unravel_index(i2, (4, 4))
        if c2 < c1:
            c1, c2 = c2, c1
            m1, m2 = m2, m1
        r1, r2 = trial["rwd"][c1], trial["rwd"][c2]

        if debug:
            print("Trial %d" % (self.index + 1))
        if action == m1:
            reward = np.random.uniform(0, 1) < trial["rwd"][c1]
            self.records[self.index]["shape"] = c1
            best = r1 > r2
            if debug:
                if best:
                    print("  Choice			: [%d] / %d  (good)" % (c1, c2))
                else:
                    print("  Choice			: [%d] / %d  (bad)" % (c1, c2))
                print("  Reward (p=%.2f)		: %d" % (trial["rwd"][c1], reward))
        elif action == m2:
            reward = np.random.uniform(0, 1) < trial["rwd"][c2]
            self.records[self.index]["shape"] = c2
            best = r2 > r1
            if debug:
                if best:
                    print("  Choice			: %d / [%d] (good)" % (c1, c2))
                else:
                    print("  Choice			: %d / [%d] (bad)" % (c1, c2))
                print("  Reward (p=%.2f)		: %d" % (trial["rwd"][c2], reward))
        else:
            reward = 0.0
            best = False
            if debug:
                print("  Choice			: %d /  %d  (bad)" % (c1, c2))
                print("  No Reward")

        # Record action, best action (was it the best action), reward and RT
        self.records[self.index]["action"] = action
        self.records[self.index]["best"] = best
        self.records[self.index]["RTmot"] = RT
        self.records[self.index]["reward"] = reward

        if debug:
            P = self.records[:self.index + 1]["best"]
            print("  Mean performance		: %.1f %%" % np.array(P * 100).mean())
            R = self.records[:self.index + 1]["reward"]
            print("  Mean reward			: %.3f" % np.array(R).mean())
            rt = self.records[:self.index + 1]["RTmot"]
            print("  Mean Response time	: %.3f ms" % np.array(rt).mean())

        return reward


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import random

    from task import Task

    task = Task(n=6)

    for trial in task:
        # Only the associative group can provide (m1,c1), (m2,c2)
        i1, i2 = (trial["ass"].ravel().argsort())[-2:]
        m1, c1 = np.unravel_index(i1, (4, 4))
        m2, c2 = np.unravel_index(i2, (4, 4))

        # Reward probabilities
        r1, r2 = trial["rwd"][c1], trial["rwd"][c2]

        # Random action
        # if random.uniform(0,1) < 0.5: action = m1
        # else:                         action = m2

        # Best action
        if r1 > r2:
            action = m1
        else:
            action = m2

        reward, best = task.process(trial, action=action, debug=True)
