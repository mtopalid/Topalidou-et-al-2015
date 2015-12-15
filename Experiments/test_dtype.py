import numpy as np
temp = '../cython/'
import sys
sys.path.append(temp)
from model import *
from display import *
from trial import *
from parameters import *


result = results()
global cues_cog, cues_mot
cues_cog, cues_mot = trials_cues(protocol = 'Guthrie', ntrials = n_reverse_trials)

def tt(result):
	result["W"]["STR"] = 5
if 0:
	tt(result[1])
	print(result["W"]["STR"])
	print(result["W"]["STR"][1])
	print(result[1]["W"]["STR"])
#histor, time = trial(result = result[0], hist = True, debugging = True, protocol = 'Guthrie', wholeFig = True)
