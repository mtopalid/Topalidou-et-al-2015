# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
# -----------------------------------------------------------------------------

# Testing learning for each model under Guthrie protocol
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    temp = '../cython/'
    import sys

    sys.path.append(temp)
    from model import *
    from display import *
    from learning import *
    from task_b import Task_B

    if 1:
        reset()
        taskl = Task_B(n=n_learning_trials)
        taskl = taskl[:n_learning_trials]
        learning_trials(taskl, trials=n_learning_trials, debugging=False)
        print()
        print("Mean performance of learning trials: %.1f %%\n" % (np.array(taskl.records["best"]).mean() * 100))

    if 1:
        task = Task_B(n=n_testing_trials)
        task_f = task[:n_testing_trials]
        task_uf = task[n_testing_trials:]
        connections["GPI.cog -> THL.cog"].active = False
        connections["GPI.mot -> THL.mot"].active = False
        learning_trials(task_f, trials=n_testing_trials)
        print("\n\n\n\n\n\n\n\n\n")
        # learning_trials(task_uf, trials=n_testing_trials)
        print()
        print("Mean performance of learning trials: %.1f %%\n" % (np.array(taskl.records["best"]).mean() * 100))
        print("Mean performance of Familiar trials: %.1f %%" % (np.array(task_f.records["best"]).mean() * 100))
        print("Mean performance of Unfamiliar trials: %.1f %%" % (np.array(task_uf.records["best"]).mean() * 100))

    if 0:
        bad_learning = True
        check_at = 180
        print("Initial learning")
        while bad_learning:
            reset()
            task = Task_B(n=n_learning_trials)
            task = task[:n_learning_trials]
            initial_task = task[:check_at]
            learning_trials(initial_task, trials=check_at)
            if np.array(initial_task.records["best"][-30:]).mean() > 0.75:
                bad_learning = False
                print(np.array(initial_task.records["best"][-30:]).mean() * 100)
                print()
                print()
        print("Remain learning")
        remain_task = task[check_at:n_learning_trials]
        learning_trials(remain_task, trials=n_learning_trials - check_at)
        print()
        print("Mean performance of learning trials: %.1f %%\n" % (np.array(remain_task.records["best"]).mean() * 100))

    if 0:
        P = learning_trials(trials=n_testing_trials, protocol='Piron', trained=True)
        P = learning_trials(trials=n_testing_trials, protocol='Piron', trained=True, familiar=False)

        connections["CTX.cog -> CTX.ass"].weights[2:] = weights(2, 0.00005)  # 0.5*np.ones(4)
        connections["CTX.cog -> STR.cog"].weights[2:] = weights(2)
        CUE["value"][2:] = 0.5

    if 0:
        print()
        print("Mean performance of Familiar trials: %.1f %%" % (
        np.array(task[:n_testing_trials].records["best"]).mean() * 100))
        print("Mean performance of Unfamiliar trials: %.1f %%" % (
        np.array(task[n_testing_trials:].records["best"]).mean() * 100))
    if 0: display_all(hist, 3.0)  # , "single-trial-all.pdf")
    if 0: display_ctx(hist, 3.0)
    if 0: display_all(hist, 3.0)  # , "single-trial-all.pdf")
