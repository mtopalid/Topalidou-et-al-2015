# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Nicolas P. Rougier, Meropi Topalidou
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Task A (Guthrie et al. (2013) protocol)
=======================================

Trials:

 - n trials with random uniform sampling of cues and positions
   Reward probabilities: A=1.00, B=0.33, C=0.66, D=0.00

"""
import numpy as np
from task import Task



class Task_A(Task):

    def setup(self, n=180):

        # Make sure count is a multiple of 6
        n = (n//6) * 6
        self.build(n)

        # All combinations of cues or positions
        Z = np.array([[0,1], [0,2], [0,3], [1,2], [1,3], [2,3]])

        # n//6 x all combinations of positions
        M = np.repeat(np.arange(6),n//6)
        np.random.shuffle(M)
        mot = Z[M]
        for i in range(mot.shape[0]):
        	np.random.shuffle(mot[i,:])

        # n//6 x all combinations of cues
        C = np.repeat(np.arange(6),n//6)
        np.random.shuffle(C)
        cog = Z[C]
        for i in range(cog.shape[0]):
        	np.random.shuffle(cog[i,:])

        for i in range(n):
            c1,c2 = cog[i]
            m1,m2 = mot[i]
            trial = self.trials[i]

            trial["cog"][[c1,c2]] += 1
            trial["mot"][[m1,m2]] += 1
            trial["ass"][m1,c1]   += 1
            trial["ass"][m2,c2]   += 1
            trial["rwd"][...] = 1.00,0.66,0.33,0.00
