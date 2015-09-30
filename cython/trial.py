# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
#				Nicolas Rougier  (Nicolas.Rougier@inria.fr)
# -----------------------------------------------------------------------------
from model import *
from display import *
from parameters import *


def trial(task, cues_pres=True, learn=True, debugging=False, trial_n=0, wholeFig=False):
    reset_activities()
    reset_history()
    ct = None
    cog_time = None
    time = None
    choice_made = False
    for i in xrange(0, 500):
        iterate(dt)
        if CTX.cog.delta > 20 and not ct:
            ct = 1
        if CTX.cog.delta > decision_threshold and not cog_time:
            cog_time = i - 500
    if cues_pres:
        set_trial(task, n=2, trial=trial_n)
    for i in xrange(500, duration):
        iterate(dt)

        if not choice_made:
            # Test if a decision has been made
            if CTX.cog.delta > decision_threshold and not cog_time:
                cog_time = i - 500
                task.records["RTcog"][trial_n] = cog_time
            if CTX.mot.delta > decision_threshold and not time:
                time = i - 500

            if time and cog_time:
                process(task, learn=learn, debugging=debugging, trial=trial_n, RT=time)
                task.records["RTcog"][trial_n] = cog_time
                task.records["CogValues"][trial_n] = CUE["cvalue"]
                task.records["MotValues"][trial_n] = CUE["mvalue"]
                task.records["Wstrc"][trial_n] = connections["CTX.cog -> STR.cog"].weights
                task.records["Wstrm"][trial_n] = connections["CTX.mot -> STR.mot"].weights
                task.records["Wcog"][trial_n] = connections["CTX.cog -> CTX.ass"].weights
                task.records["Wmot"][trial_n] = connections["CTX.mot -> CTX.ass"].weights
                if 0:  # ch[-1] is None:
                    mot_choice = np.argmax(CTX.mot.U)
                    cog_choice = np.argmax(CTX.cog.U)
                    print 'Wrong choice... \nMotor choice: %d\nCognitive choice: %d' % (mot_choice, cog_choice)
                    print CUE["mot"][:n], CUE["cog"][:n]

                if wholeFig:
                    choice_made = True
                else:
                    return time
    time = 2500

    if debugging:
        print 'Trial Failed!'
        print 'NoMove trial: ', trial_n

    return time
