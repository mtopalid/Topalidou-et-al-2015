#!/usr/bin/env python
import sys
import numpy as np
path = '../cython/'
sys.path.append(path)
from parameters import *


def compute_Performances(folder, normal=False, control=False, reversed=False, printing=True, save=True):
    if normal:
        folderUfnG = folder + '/D1'
        folderUf = folder + '/D2'
        folderTufnG2 = folder + '/D3'
        PUf = np.zeros((simulations, n_trials))
        PUfnG = np.zeros((simulations, n_trials))
        PUfnG2 = np.zeros((simulations, n_trials))
    if control:
        folderD1 = folder + '/Control/D1'
        folderD2 = folder + '/Control/D2'
        folderD3 = folder + '/Control/D3'
        PUfD1 = np.zeros((simulations, n_trials))  # 1200
        PUfD2 = np.zeros((simulations, n_trials))
        PUfD3 = np.zeros((simulations, n_trials))
    if reversed:
        folderUfRev = folder + '/Reversed/D1'
        folderUfnGRev = folder + '/Reversed/D2'
        PUfRev = np.zeros((simulations, n_trials))  # 1200
        PUfnGRev = np.zeros((simulations, n_trials))

    for i in range(simulations):
        if normal:
            file = folderUf + '/Records' + "%03d" % (i + 1) + '.npy'
            temp = np.load(file)
            PUf[i, :] = temp["best"]
            file = folderUfnG + '/Records' + "%03d" % (i + 1) + '.npy'
            temp = np.load(file)
            PUfnG[i, :] = temp["best"]
            file = folderTufnG2 + '/Records' + "%03d" % (i + 1) + '.npy'
            temp = np.load(file)
            PUfnG2[i, :] = temp["best"]
        if control:
            file = folderD1 + '/Records' + "%03d" % (i + 1) + '.npy'
            temp = np.load(file)
            PUfD1[i, :] = temp["best"]
            file = folderD2 + '/Records' + "%03d" % (i + 1) + '.npy'
            temp = np.load(file)
            PUfD2[i, :] = temp["best"]
            file = folderD3 + '/Records' + "%03d" % (i + 1) + '.npy'
            temp = np.load(file)
            PUfD3[i, :] = temp["best"]
        if reversed:
            file = folderUfRev + '/Records' + "%03d" % (i + 1) + '.npy'
            temp = np.load(file)
            PUfRev[i, :] = temp["best"]
            file = folderUfnGRev + '/Records' + "%03d" % (i + 1) + '.npy'
            temp = np.load(file)
            PUfnGRev[i, :] = temp["best"]

    if normal:
        file = folder + '/MeanPerformanceUf.npy'
        np.save(file, PUf.mean(axis=0))
        file = folder + '/MeanPerformanceUfnG.npy'
        np.save(file, PUfnG.mean(axis=0))
        file = folder + '/MeanPerformanceUfnG.npy'
        np.save(file, PUfnG2.mean(axis=0))
    if control:
        file = folder + '/MeanPerformanceUfD1.npy'
        np.save(file, PUfD1.mean(axis=0))
        file = folder + '/MeanPerformanceUfD2.npy'
        np.save(file, PUfD2.mean(axis=0))
        file = folder + '/MeanPerformanceUfD3.npy'
        np.save(file, PUfD3.mean(axis=0))
    if reversed:
        file = folder + '/MeanPerformanceUfRev.npy'
        np.save(file, PUfRev.mean(axis=0))
        file = folder + '/MeanPerformanceUfnGRev.npy'
        np.save(file, PUfnGRev.mean(axis=0))
    if printing:
        if normal:
            PUf = PUf.mean(axis=0)
            PUfnG = PUfnG.mean(axis=0)
            PUfnG2 = PUfnG2.mean(axis=0)
            print('              NoGPi     ->      GPi      ->     NoGPi')
            print('First 25:  %.2f ± %.2f	    %.2f ± %.2f 	 %.2f ± %.2f' % (PUfnG[:25].mean(),PUfnG[:25].std(), PUf[:25].mean(), PUf[:25].std(), PUfnG2[:25].mean(), PUfnG2[:25].std()))
            print('Last 25:   %.2f ± %.2f	    %.2f ± %.2f 	 %.2f ± %.2f\n' % (PUfnG[-25:].mean(), PUfnG[-25:].std(), PUf[-25:].mean(), PUf[-25:].std(), PUfnG2[-25:].mean(), PUfnG2[-25:].std()))
        if control:
            PUfD1 = PUfD1.mean(axis=0)
            PUfD2 = PUfD2.mean(axis=0)
            PUfD3 = PUfD3.mean(axis=0)
            print('               GPi      ->      GPi      ->      GPi')
            print('First 25:  %.2f ± %.2f	    %.2f ± %.2f	     %.2f ± %.2f' % (PUfD1[:25].mean(), PUfD1[:25].std(), PUfD2[:25].mean(), PUfD2[:25].std(), PUfD3[:25].mean(), PUfD3[:25].std()))
            print('Last 25:   %.2f ± %.2f	    %.2f ± %.2f	     %.2f ± %.2f\n' % (PUfD1[-25:].mean(), PUfD1[-25:].std(), PUfD2[-25:].mean(), PUfD2[-25:].std(), PUfD3[-25:].mean(), PUfD3[-25:].std()))
        if reversed:
            PUfRev = PUfRev.mean(axis=0)
            PUfnGRev = PUfnGRev.mean(axis=0)
            print('               GPi      ->     NoGPi')
            print('First 25:  %.2f ± %.2f	    %.2f ± %.2f' % (PUfRev[:25].mean(), PUfRev[:25].std(), PUfnGRev[:25].mean(), PUfnGRev[:25].std()))
            print('Last 25:   %.2f ± %.2f	    %.2f ± %.2f\n\n' % (PUfRev[-25:].mean(), PUfRev[-25:].std(), PUfnGRev[-25:].mean(), PUfnGRev[-25:].std()))

    if save:
        if normal and control and reversed:
            filename = folder + '/Performances_Results.txt'
        elif normal:
            filename = folder + '/Performances_Results_normal.txt'
        elif control:
            filename = folder + '/Performances_Results_control.txt'
        elif reversed:
            filename = folder + '/Performances_Results_reversed.txt'
        else:
            filename = folder + '/Performances_Results.txt'
        out_file = open(filename, "wt")
        out_file.write('Mean\n')
        if normal:
            out_file.write('             NoGPi     ->      GPi      ->     NoGPi\n')
            out_file.write(
                    str('First 25: %.2f ± %.2f      %.2f ± %.2f	    %.2f ± %.2f\n' % (
                    PUfnG[:25].mean(), PUfnG[:25].std(), PUf[:25].mean(), PUf[:25].std(), PUfnG2[:25].mean(),
                    PUfnG2[:25].std())))
            out_file.write(
                    str('Last 25:  %.2f ± %.2f      %.2f ± %.2f	    %.2f ± %.2f\n' % (
                    PUfnG[-25:].mean(), PUfnG[-25:].std(), PUf[-25:].mean(), PUf[-25:].std(), PUfnG2[-25:].mean(),
                    PUfnG2[-25:].std())))
            out_file.write('\n')
        if control:
            out_file.write('              GPi      ->      GPi      ->      GPi\n')
            out_file.write(
                    str('First 25: %.2f ± %.2f      %.2f ± %.2f	    %.2f ± %.2f\n' % (
                    PUfD1[:25].mean(), PUfD1[:25].std(), PUfD2[:25].mean(), PUfD2[:25].std(), PUfD3[:25].mean(),
                    PUfD3[:25].std())))
            out_file.write(
                    str('Last 25:  %.2f ± %.2f      %.2f ± %.2f	    %.2f ± %.2f\n' % (
                    PUfD1[-25:].mean(), PUfD1[-25:].std(), PUfD2[-25:].mean(), PUfD2[-25:].std(), PUfD3[-25:].mean(), PUfD3[-25:].std())))
            out_file.write('\n')
        if reversed:
            out_file.write('              GPi      ->     NoGPi\n')
            out_file.write(str('First 25: %.2f ± %.2f      %.2f ± %.2f\n' % (PUfRev[:25].mean(),
             PUfRev[:25].std(), PUfnGRev[:25].mean(), PUfnGRev[:25].std())))
            out_file.write(str('Last 25:  %.2f ± %.2f      %.2f ± %.2f\n' % (PUfRev[-25:].mean(), PUfRev[-25:].std(), PUfnGRev[-25:].mean(), PUfnGRev[-25:].std())))
        out_file.close()


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    compute_Performances('../Results/D-D1_D2_D3-120a1.75', normal=True, control=True, reversed=True, printing=True,
                         save=True)
