#!/usr/bin/env python
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

suptitle = 'Model: Topalidou\n'
path = '../cython/'
import sys
sys.path.append(path)

from parameters import *

def fitFunc(t, a, b, c):
    return a*np.exp(-b*t) + c

suptitle += 'Protocol: C'

folder = '../Results/C-1-100'
reverse = np.hstack((np.linspace(11,25,15),np.linspace(35,50,16), np.linspace(60,75,16), np.linspace(86,100,15)))
for j in reverse:
	f = folder + '/Reverse' + "%03d" % (j)
	print('Reverse:' + "%03d" % (j))
	for i in range(simulations):
		file = f + '/All-Results' + "%03d" % (i+1) + '.npy'
		temp = np.load(file)
		np.save(file, temp[1])
