# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
#               Nicolas Rougier (Nicolas.Rougier@inria.fr)
# -----------------------------------------------------------------------------


# Population size
n = 4
# Simulation size
n_trials = 120

simulations = 100
threshold = 40

# --- Time ---
ms = 0.001
duration = int(3. / ms)
dt = 1 * ms
tau = 10 * ms

# --- Learning ---
alpha_CUE = 0.0075
alpha_LTP = 0.015
alpha_LTD = 0.01125
alpha_LTP_ctx = alpha_LTP  ** 2*2

# --- Sigmoid ---
Vmin = 0
Vmax = 20
Vh = 16
Vc = 3

# --- Model ---
decision_threshold = 40
CTX_rest = -3.0
STR_rest = 0.0
STN_rest = -10.0
GPE_rest = -10.0
GPI_rest = -10.0
THL_rest = -40.0

# Noise level (%)
Cortex_N = 0.01
Striatum_N = 0.01
STN_N = 0.01
GPi_N = 0.01
GPe_N = 0.01
Thalamus_N = 0.01

# --- Cues & Rewards ---
Value_cue = 7
noise_cue = 0.001

rewards_Piron = 0.75, 0.25, 0.75, 0.25

# -- Weight ---
Wmin = 0.25
Wmax = 0.75

gains = {"CTX.cog -> STR.cog": +1.0,
         "CTX.mot -> STR.mot": +1.0,
         "CTX.ass -> STR.ass": +1.0,
         "CTX.cog -> STR.ass": +0.2,
         "CTX.mot -> STR.ass": +0.2,

         "CTX.cog -> STN.cog": +1.0,
         "CTX.mot -> STN.mot": +1.0,

         "STR.cog -> GPE.cog": -2.0,
         "STR.mot -> GPE.mot": -2.0,
         "STR.ass -> GPE.cog": -2.0,
         "STR.ass -> GPE.mot": -2.0,
         "GPE.cog -> STN.cog": -0.25,
         "GPE.mot -> STN.mot": -0.25,
         "STN.cog -> GPI.cog": +1.0,
         "STN.mot -> GPI.mot": +1.0,

         "STR.cog -> GPI.cog": -2.0,
         "STR.mot -> GPI.mot": -2.0,
         "STR.ass -> GPI.cog": -2.0,
         "STR.ass -> GPI.mot": -2.0,

         "GPI.cog -> THL.cog": -0.25,
         "GPI.mot -> THL.mot": -0.25,

         "THL.cog -> CTX.cog": +0.4,
         "THL.mot -> CTX.mot": +0.4,
         "CTX.cog -> THL.cog": +0.1,
         "CTX.mot -> THL.mot": +0.1,

         "CTX.mot -> CTX.mot": +0.5,
         "CTX.cog -> CTX.cog": +0.5,
         "CTX.ass -> CTX.ass": +0.5,

         "CTX.cog -> CTX.ass": +0.01,
         "CTX.mot -> CTX.ass": +0.01,

         "CTX.ass -> CTX.cog": +0.01,
         "CTX.ass -> CTX.mot": +0.01,

         }

dtype = [("CTX", [("mot", float, 4), ("cog", float, 4), ("ass", float, 16)]),
         ("STR", [("mot", float, 4), ("cog", float, 4), ("ass", float, 16)]),
         ("GPE", [("mot", float, 4), ("cog", float, 4)]),
         ("GPI", [("mot", float, 4), ("cog", float, 4)]),
         ("THL", [("mot", float, 4), ("cog", float, 4)]),
         ("STN", [("mot", float, 4), ("cog", float, 4)])]
