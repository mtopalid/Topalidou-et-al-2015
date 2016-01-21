#!/usr/bin/env python
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

suptitle = 'Model: Topalidou\n'
path = '../cython/'
import sys
sys.path.append(path)
from performances import *

# -----------------------------------------------------------------------------
if __name__ == "__main__":
    folder = '../Results'
    compute_Performances(folder, normal=True, control=True, reversed=True, printing=True,
                         save=True)
