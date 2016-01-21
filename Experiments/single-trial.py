# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
#               Nicolas Rougier (Nicolas.Rougier@inria.fr)
# -----------------------------------------------------------------------------

# Evolution of single trial with Piron protocol
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    # Include to the path files from cython folder
    temp = '../cython/'
    import sys
    sys.path.append(temp)

    # model file build the structures and initialize the model
    from model import *
    from display import *
    from trial import *
    from task import Task

    # 1 if there is presentation of cues else 0
    cues_pres = 1
    # Initialize the system
    reset()

    # Define the shapes and the positions that we'll be used to each trial
    # n should be multiple of 6 because there are 6 valuable combinations of positions
    task = Task(n=6)

    GPi_lesion = True#False#

    # Make GPi lesion
    if GPi_lesion:
        connections["GPI.cog -> THL.cog"].active = False
        connections["GPI.mot -> THL.mot"].active = False

    # Compute a single trial
    trial(task, debugging=True, cues_pres=cues_pres, wholeFig=True)
    # Retrieve the activity history of the structures
    histor = history()

    # Display cortical activity during the single trial
    if 1:
        if GPi_lesion:
            filename = "../Results/single-trial-GPi_lesion.pdf"
        else:
            filename = "../Results/single-trial.pdf"
        display_ctx(histor, 3.0, filename)#, "single-trial-NoBG.pdf")#)#
    if 1:
        if GPi_lesion:
            filename = "../Results/single-trial-GPi_lesion-all.pdf"
        else:
            filename = "../Results/single-trial-all.pdf"
        # Display activity from all structures during the single trial
        display_all(histor, 3.0, filename)
