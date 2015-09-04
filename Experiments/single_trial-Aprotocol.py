# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
#               Nicolas Rougier (Nicolas.Rougier@inria.fr)
# -----------------------------------------------------------------------------

# Evolution of single trial with Guthrie protocol
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
    from task_a import Task_A

    # 1 if there is presentation of cues else 0
    cues_pres = 1

    # Initialize the system
    reset()

    # Define the shapes and the positions that we'll be used to each trial
    # n should be multiple of 6 because there are 6 valuable combinations of shapes and positions
    task = Task_A(n=6)

    # Compute a single trial
    time = trial(task, cues_pres=cues_pres, wholeFig=True)

    #retrieve the activity history of the structures
    histor = history()

    # Display cortical activity during the single trial
    if 1: display_ctx(histor, 3.0)#, "single-trial.pdf")

    # Display activity from all structures during the single trial
    if 0: display_all(histor, 3.0)  # , "single-trial-all.pdf")
