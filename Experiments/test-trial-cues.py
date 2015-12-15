# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
# -----------------------------------------------------------------------------

# Simulate number of experiments that is given in parameters.py of the different
# models. Each simulation is a number of trials under Guthrie protocol.
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    temp = '../cython/'
    import sys

    sys.path.append(temp)
    import numpy as np
    import os
    from model import *
    from learning import *
    from testing import *
    from parameters import *

    global cues_cog, cues_mot
    if 1:
        cues_cog, cues_mot = trials_cues(protocol='Guthrie', ntrials=n_reverse_trials)
        set_trial(protocol='Guthrie')
    if 0:
        cues_cog, cues_mot = trials_cues(protocol='OneChoice', ntrials=n_reverse_trials)
        set_trial(protocol='OneChoice')
    if 0:
        np.set_printoptions(threshold=np.nan)
        print('cues_cog : ', cues_cog)
        print('cues_mot: ', cues_mot)
    if 0:
        global learning_cues_cog, testing_cues_cog_fam, testing_cues_cog_unfam, learning_cues_mot, testing_cues_mot_fam, testing_cues_mot_unfam
        learning_cues_cog, testing_cues_cog_fam, testing_cues_cog_unfam, learning_cues_mot, testing_cues_mot_fam, testing_cues_mot_unfam = trials_cues(
            protocol='Piron', ntrials=n_reverse_trials)
        print('learning_cues_cog: ', learning_cues_cog)
        print('testing_cues_cog_fam: ', testing_cues_cog_fam)
        print('testing_cues_cog_unfam: ', testing_cues_cog_unfam)
        print('learning_cues_mot: ', learning_cues_mot)
        print('testing_cues_mot_fam: ', testing_cues_mot_fam)
        print('testing_cues_mot_unfam: ', testing_cues_mot_unfam)
        # set_trial(protocol = 'Piron', familiar = True, learning = True)
        # set_trial(protocol = 'Piron', familiar = True, learning = False)
        set_trial(protocol='Piron', familiar=False, learning=False)

    print(CUE["cog"], CUE["mot"])
