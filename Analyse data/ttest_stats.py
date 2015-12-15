import scipy.stats as sc_st
import sys
import numpy as np
from parameters import *

path = '../cython/'
sys.path.append(path)

folder = '../Results/D'#-half_noise'
folderUf = folder + '/Testing_unfam'
folderUfnG = folder + '/Testing_unfam_NoGPi'
folderTuf_first_day = folder + '/Control/Testing_unfam'
folderTuf_second_day = folder + '/Control/Testing_unfam_2'

n_testing_trials = 100
PUf = np.zeros((simulations, n_testing_trials))
PUfnG = np.zeros((simulations, n_testing_trials))
PUfD1 = np.zeros((simulations, n_testing_trials))
PUfD2 = np.zeros((simulations, n_testing_trials))
for i in range(simulations):
    file = folderUf + '/Records' + "%03d" % (i + 1) + '.npy'
    temp = np.load(file)
    PUf[i, :] = temp["best"]
    file = folderUfnG + '/Records' + "%03d" % (i + 1) + '.npy'
    temp = np.load(file)
    PUfnG[i, :] = temp["best"]
    file = folderTuf_first_day + '/Records' + "%03d" % (i + 1) + '.npy'
    temp = np.load(file)
    PUfD1[i, :] = temp["best"]
    file = folderTuf_second_day + '/Records' + "%03d" % (i + 1) + '.npy'
    temp = np.load(file)
    PUfD2[i, :] = temp["best"]

PUf25f = PUf[:, :25].mean(axis=1)
PUf25l = PUf[:, -25:].mean(axis=1)
PUfnG25f = PUfnG[:, :25].mean(axis=1)
PUfnG25l = PUfnG[:, -25:].mean(axis=1)

PUfD1f = PUfD1[:, :25].mean(axis=1)
PUfD1l = PUfD1[:, -25:].mean(axis=1)
PUfD2f = PUfD2[:, :25].mean(axis=1)
PUfD2l = PUfD2[:, -25:].mean(axis=1)

# sc_st.ttest_ind returns two values: statistic : the calculated t-statistic & the two-tailed p-value.
print(sc_st.ttest_ind(PUfnG25f,PUf25f, equal_var=False))
print(sc_st.ttest_ind(PUfnG25l,PUf25l, equal_var=False))
print()
# print sc_st.ttest_ind(PUf25l,PUf25f, equal_var=False)
# print sc_st.ttest_ind(PUfnG25f,PUfnG25l, equal_var=False)
print()
print((sc_st.ttest_ind(PUfD1f,PUfD2f, equal_var=False)))
print(sc_st.ttest_ind(PUfD1l,PUfD2l, equal_var=False))
print()
print(sc_st.ttest_ind(PUfD1f,PUfD1l, equal_var=False))
print(sc_st.ttest_ind(PUfD2f,PUfD2l, equal_var=False))
