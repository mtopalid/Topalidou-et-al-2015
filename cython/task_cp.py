# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Nicolas P. Rougier, Meropi Topalidou
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Task C (Topalidou et al. (2015) protocol)
=========================================

Trials:

    - n trials with uniform sampling of cues and positions
      Reward probabilities: A=0.75, B=0.25

    - 10*n trials with uniform sampling of cues and positions
      Reward probabilities: A=0.25, B=0.75

"""
import numpy as np
from task import Task


class Task_C(Task):
    def __init__(self, n=30, r=6, setup=True):
        self.trials = None
        self.records = None
        if setup:
            self.setup(n=n, r=r)

    def setup(self, n=30, r=6):

        n = (n // 6) * 6
        r = (r // 6) * 6
        n1 = r
        n2 = n - r

        self.build(n1 + n2)

        # All combinations of cues or positions
        Z = np.array([[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]])

        # n//6 x all combinations of cues
        M = np.repeat(np.arange(6), n1 // 6)
        np.random.shuffle(M)
        mot = Z[M]

        C = np.array([0, 1])
        cog = np.tile(C, (n1, 1))
        for i in range(cog.shape[0]):
            np.random.shuffle(cog[i, :])

        for i in range(n1):
            c1, c2 = cog[i]
            m1, m2 = mot[i]
            trial = self.trials[i]
            trial["cog"][[c1, c2]] += 1
            trial["mot"][[m1, m2]] += 1
            trial["ass"][m1, c1] += 1
            trial["ass"][m2, c2] += 1
            trial["rwd"][...] = 0.75, 0.25, 0.75, 0.25

        # n//6 x all combinations of cues
        M = np.repeat(np.arange(6), n2 // 6)
        np.random.shuffle(M)
        mot = Z[M]
        for i in range(mot.shape[0]):
            np.random.shuffle(mot[i, :])

        #
        C = np.array([0, 1])
        cog = np.tile(C, (n2, 1))
        for i in range(cog.shape[0]):
            np.random.shuffle(cog[i, :])

        for i in range(n1, n1 + n2):
            c1, c2 = cog[i - n1]
            m1, m2 = mot[i - n1]
            trial = self.trials[i]
            trial["cog"][[c1, c2]] += 1
            trial["mot"][[m1, m2]] += 1
            trial["ass"][m1, c1] += 1
            trial["ass"][m2, c2] += 1
            trial["rwd"][...] = 0.25, 0.75, 0.25, 0.75
