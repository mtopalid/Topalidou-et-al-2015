# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
#               Nicolas Rougier (Nicolas.Rougier@inria.fr)
# -----------------------------------------------------------------------------

from c_dana import *
from parameters import *

clamp = Clamp(min=0, max=1000)
sigmoid = Sigmoid(Vmin=Vmin, Vmax=Vmax, Vh=Vh, Vc=Vc)

# Build structures
CTX = AssociativeStructure(
    tau=tau, rest=CTX_rest, noise=Cortex_N, activation=clamp)
STR = AssociativeStructure(
    tau=tau, rest=STR_rest, noise=Striatum_N, activation=sigmoid)
STN = Structure(tau=tau, rest=STN_rest, noise=STN_N, activation=clamp)
GPE = Structure(tau=tau, rest=GPE_rest, noise=GPe_N, activation=clamp)
GPI = Structure(tau=tau, rest=GPI_rest, noise=GPi_N, activation=clamp)
THL = Structure(tau=tau, rest=THL_rest, noise=Thalamus_N, activation=clamp)

structures = (CTX, STR, STN, GPE, GPI, THL)

# Cue vector includes shapes, positions and the shapes' value used in reinforcement learning
CUE = np.zeros(4, dtype=[("mot", float),
                         ("cog", float),
                         ("value", float)])

# Initialization of the values
CUE["mot"] = 0, 1, 2, 3
CUE["cog"] = 0, 1, 2, 3
CUE["value"] = 0.5


# Add noise to weights
def weights(shape, s=0.005, initial=0.5):
    N = np.random.normal(initial, s, shape)
    N = np.minimum(np.maximum(N, 0.0), 1.0)
    return Wmin + (Wmax - Wmin) * N


W1 = (2 * np.eye(4) - np.ones((4, 4))).ravel()
W2 = (2 * np.eye(16) - np.ones((16, 16))).ravel()

# Connectivity 
connections = {
    "CTX.cog -> STR.cog": OneToOne(CTX.cog.V, STR.cog.Isyn, weights(4)),  # plastic (RL)
    "CTX.mot -> STR.mot": OneToOne(CTX.mot.V, STR.mot.Isyn, 0.5 * np.ones(4)),
    "CTX.ass -> STR.ass": OneToOne(CTX.ass.V, STR.ass.Isyn, 0.5 * np.ones(4 * 4)),
    "CTX.cog -> STR.ass": CogToAss(CTX.cog.V, STR.ass.Isyn, 0.5 * np.ones(4)),
    "CTX.mot -> STR.ass": MotToAss(CTX.mot.V, STR.ass.Isyn, 0.5 * np.ones(4)),

    "CTX.cog -> STN.cog": OneToOne(CTX.cog.V, STN.cog.Isyn, np.ones(4)),
    "CTX.mot -> STN.mot": OneToOne(CTX.mot.V, STN.mot.Isyn, np.ones(4)),

    "STR.cog -> GPE.cog": OneToOne(STR.cog.V, GPE.cog.Isyn, np.ones(4)),
    "STR.mot -> GPE.mot": OneToOne(STR.mot.V, GPE.mot.Isyn, np.ones(4)),
    "STR.ass -> GPE.cog": AssToCog(STR.ass.V, GPE.cog.Isyn, np.ones(4)),
    "STR.ass -> GPE.mot": AssToMot(STR.ass.V, GPE.mot.Isyn, np.ones(4)),
    "GPE.cog -> STN.cog": OneToOne(GPE.cog.V, STN.cog.Isyn, np.ones(4)),
    "GPE.mot -> STN.mot": OneToOne(GPE.mot.V, STN.mot.Isyn, np.ones(4)),
    "STN.cog -> GPI.cog": OneToAll(STN.cog.V, GPI.cog.Isyn, np.ones(4)),
    "STN.mot -> GPI.mot": OneToAll(STN.mot.V, GPI.mot.Isyn, np.ones(4)),

    "STR.cog -> GPI.cog": OneToOne(STR.cog.V, GPI.cog.Isyn, np.ones(4)),
    "STR.mot -> GPI.mot": OneToOne(STR.mot.V, GPI.mot.Isyn, np.ones(4)),
    "STR.ass -> GPI.cog": AssToCog(STR.ass.V, GPI.cog.Isyn, np.ones(4)),
    "STR.ass -> GPI.mot": AssToMot(STR.ass.V, GPI.mot.Isyn, np.ones(4)),

    "GPI.cog -> THL.cog": OneToOne(GPI.cog.V, THL.cog.Isyn, np.ones(4)),
    "GPI.mot -> THL.mot": OneToOne(GPI.mot.V, THL.mot.Isyn, np.ones(4)),

    "THL.cog -> CTX.cog": OneToOne(THL.cog.V, CTX.cog.Isyn, np.ones(4)),
    "THL.mot -> CTX.mot": OneToOne(THL.mot.V, CTX.mot.Isyn, np.ones(4)),
    "CTX.cog -> THL.cog": OneToOne(CTX.cog.V, THL.cog.Isyn, np.ones(4)),
    "CTX.mot -> THL.mot": OneToOne(CTX.mot.V, THL.mot.Isyn, np.ones(4)),

    "CTX.mot -> CTX.mot": AllToAll(CTX.mot.V, CTX.mot.Isyn, W1),
    "CTX.cog -> CTX.cog": AllToAll(CTX.cog.V, CTX.cog.Isyn, W1),
    "CTX.ass -> CTX.ass": AllToAll(CTX.ass.V, CTX.ass.Isyn, W2),
    "CTX.ass -> CTX.cog": AssToCog(CTX.ass.V, CTX.cog.Isyn, np.ones(4)),
    "CTX.ass -> CTX.mot": AssToMot(CTX.ass.V, CTX.mot.Isyn, np.ones(4)),
    "CTX.cog -> CTX.ass": CogToAss(CTX.cog.V, CTX.ass.Isyn, weights(4, 0.00005)),  # plastic (HL)
    "CTX.mot -> CTX.ass": MotToAss(CTX.mot.V, CTX.ass.Isyn, weights(4, 0.00005)),  # plastic (HL)
}
for name, gain in gains.items():
    connections[name].gain = gain


def set_trial(task, n=2, trial=0, protocol='Guthrie', familiar=True):
    i1, i2 = (task[trial]["ass"].ravel().argsort())[-2:]
    CUE["mot"][0], CUE["cog"][0] = np.unravel_index(i1, (4, 4))
    CUE["mot"][1], CUE["cog"][1] = np.unravel_index(i2, (4, 4))
    ncues = 2

    CTX.mot.Iext = 0
    CTX.cog.Iext = 0
    CTX.ass.Iext = 0

    for i in range(ncues):
        c, m = CUE["cog"][i], CUE["mot"][i]

        CTX.mot.Iext[m] = Value_cue + np.random.uniform(-noise_cue / 2, noise_cue / 2)
        CTX.cog.Iext[c] = Value_cue + np.random.uniform(-noise_cue / 2, noise_cue / 2)
        CTX.ass.Iext[c * 4 + m] = Value_cue + np.random.uniform(-noise_cue / 2, noise_cue / 2)


def iterate(dt):
    # Flush connections
    for connection in connections.values():
        connection.flush()

    # Propagate activities
    for connection in connections.values():
        connection.propagate()

    # Compute new activities
    for structure in structures:
        structure.evaluate(dt)


def reset():
    CUE["mot"] = 0, 1, 2, 3
    CUE["cog"] = 0, 1, 2, 3
    CUE["value"] = 0.5
    reset_weights()
    reset_activities()


def reset_weights():
    connections["CTX.cog -> CTX.ass"].weights = weights(4, 0.00005)
    connections["CTX.mot -> CTX.ass"].weights = weights(4, 0.00005)
    connections["CTX.cog -> STR.cog"].weights = weights(4)


def reset_activities():
    for structure in structures:
        structure.reset()


def history():
    histor = np.zeros(duration, dtype=dtype)
    histor["CTX"]["mot"] = CTX.mot.history[:duration]
    histor["CTX"]["cog"] = CTX.cog.history[:duration]
    histor["CTX"]["ass"] = CTX.ass.history[:duration]
    histor["STR"]["mot"] = STR.mot.history[:duration]
    histor["STR"]["cog"] = STR.cog.history[:duration]
    histor["STR"]["ass"] = STR.ass.history[:duration]
    histor["STN"]["mot"] = STN.mot.history[:duration]
    histor["STN"]["cog"] = STN.cog.history[:duration]
    histor["GPE"]["mot"] = GPE.mot.history[:duration]
    histor["GPE"]["cog"] = GPE.cog.history[:duration]
    histor["GPI"]["mot"] = GPI.mot.history[:duration]
    histor["GPI"]["cog"] = GPI.cog.history[:duration]
    histor["THL"]["mot"] = THL.mot.history[:duration]
    histor["THL"]["cog"] = THL.cog.history[:duration]
    return histor


def reset_history():
    CTX.mot.history[:duration] = 0
    CTX.cog.history[:duration] = 0
    CTX.ass.history[:duration] = 0
    STR.mot.history[:duration] = 0
    STR.cog.history[:duration] = 0
    STR.ass.history[:duration] = 0
    STN.mot.history[:duration] = 0
    STN.cog.history[:duration] = 0
    GPE.mot.history[:duration] = 0
    GPE.cog.history[:duration] = 0
    GPI.mot.history[:duration] = 0
    GPI.cog.history[:duration] = 0
    THL.mot.history[:duration] = 0
    THL.cog.history[:duration] = 0


def process(task, n=2, learn=True, trial=0, debugging=True, RT=0):
    # A motor decision has been made
    # The actual cognitive choice may differ from the cognitive choice
    # Only the motor decision can designate the chosen cue
    mot_choice = np.argmax(CTX.mot.U)
    reward, best = task.process(task[trial], action=mot_choice, debug=debugging, RT=RT)
    cog_choice = np.argmax(CTX.cog.U)
    task.records["cog_choice"][trial] = cog_choice

    # Find the chosen cue through its position
    for i in range(n):
        if mot_choice == CUE["mot"][:n][i]:
            choice = int(CUE["cog"][:n][i])
    if learn:
        # Compute reward
        reward = int(reward)

        # Compute prediction error
        error = reward - CUE["value"][choice]

        # Update cues values
        CUE["value"][choice] += error * alpha_CUE

        # Reinforcement striatal learning
        lrate = alpha_LTP if error > 0 else alpha_LTD
        dw = error * lrate * STR.cog.V[choice]
        W = connections["CTX.cog -> STR.cog"].weights
        W[choice] += + dw * (Wmax - W[choice]) * (W[choice] - Wmin)
        connections["CTX.cog -> STR.cog"].weights = W

        # Hebbian cortical learning
        dw = alpha_LTP_ctx * CTX.cog.V[choice]
        W = connections["CTX.cog -> CTX.ass"].weights
        W[choice] += + dw * (Wmax - W[choice]) * (W[choice] - Wmin)
        connections["CTX.cog -> CTX.ass"].weights = W

        dw = alpha_LTP_ctx * CTX.mot.V[mot_choice]
        W = connections["CTX.mot -> CTX.ass"].weights
        W[mot_choice] += + dw * (Wmax - W[mot_choice]) * (W[mot_choice] - Wmin)
        connections["CTX.mot -> CTX.ass"].weights = W


def debug_learning(Wcog, Wmot, Wstr, cues_value):
    print "  Cues Values			: ", cues_value
    print "  Cortical Weights Cognitive	: ", Wcog
    print "  Cortical Weights Motor	: ", Wmot
    print "  Striatal Weights		: ", Wstr


def debug_total(P, RT=None, CV=None, Wcog=None, Wmot=None, Wstr=None):
    print "Mean Performance		: ", (P.mean(axis=1)).mean(axis=0) * 100, '%'
    if RT is not None:
        print "Mean Reaction Time	:", (RT.mean(axis=1)).mean(axis=0) * 100, '%'
    if CV is not None:
        print "Mean Cues Values		:" + str(CV.mean(axis=0))
        print 'Mean Cortical Weights Cog	: ' + str(Wcog[:, -1].mean(axis=0))
        print 'Mean Cortical Weights Mot	: ' + str(Wmot[:, -1].mean(axis=0))
        print 'Mean Striatal Weights		: ' + str(Wstr[:, -1].mean(axis=0))

# def debug1ch(cgchoice=None, c1=None, m1=None, P=None, RT=None):
#     if cgchoice is not None:
#         print "Choice:         ",
#         if cgchoice == c1:
#             print " 	[%d]" % c1,
#         else:
#             print " 	Wrong choice"
#
#     if m1 is not None:
#         print "Positions:         	 %d" % (m1)
#     if P is not None:
#         print "Mean performance	 	: %.3f %%" % (np.array(P).mean() * 100)
#
#     if RT is not None:
#         print "Mean Response time		: %.3f ms" % (np.array(RT).mean())

