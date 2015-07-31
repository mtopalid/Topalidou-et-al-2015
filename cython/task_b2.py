# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Nicolas P. Rougier, Meropi Topalidou
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Task B (Piron et al. (2015) protocol)
=====================================

Trials:

  - n trials with A & B at random uniform positions
    Reward probabilities: A=0.75, B=0.25

  - n trials with C & D at random uniform positions
    Reward probabilities: C=0.75, D=0.25
"""
import numpy as np
from task import Task


class Task_B(Task):

    def setup(self, n=120):

        # Make sure count is a multiple of 6
        n = (n//6) * 6
        self.build(2*n)

        # All combinations of cues or positions
        Z = np.array([[0,1], [0,2], [0,3], [1,2], [1,3], [2,3]])

        # n//6 x all combinations of cues
        M = np.repeat(np.arange(6),n//6)
        np.random.shuffle(M)
        mot = Z[M]

        trial = self.trials["rwd"] = 0.75, 0.25, 0.75, 0.25

        for i in range(n):
            m1,m2 = mot[i]

            trial = self.trials[i]
            trial["cog"][[0,1]]   += 1
            trial["mot"][[m1,m2]] += 1
            trial["ass"][m1,0]    += 1
            trial["ass"][m2,1]    += 1

            trial = self.trials[n+i]
            trial["cog"][[2,3]]   += 1
            trial["mot"][[m1,m2]] += 1
            trial["ass"][m1,2]    += 1
            trial["ass"][m2,3]    += 1
