# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Meropi Topalidou
# Distributed under the (new) BSD License.
#
# Contributors: Meropi Topalidou (Meropi.Topalidou@inria.fr)
# -----------------------------------------------------------------------------
from c_dana import *
from parameters import *

clamp   = Clamp(min=0, max=1000)
sigmoid = Sigmoid(Vmin=Vmin, Vmax=Vmax, Vh=Vh, Vc=Vc)

CTX = AssociativeStructure(
                 tau=tau, rest=CTX_rest, noise=Cortex_N, activation=clamp )
STR = AssociativeStructure(
                 tau=tau, rest=STR_rest, noise=Striatum_N, activation=sigmoid )
STN = Structure( tau=tau, rest=STN_rest, noise=STN_N, activation=clamp )
GPE = Structure( tau=tau, rest=GPE_rest, noise=GPe_N, activation=clamp )
GPI = Structure( tau=tau, rest=GPI_rest, noise=GPi_N, activation=clamp )
THL = Structure( tau=tau, rest=THL_rest, noise=Thalamus_N, activation=clamp )

structures = (CTX, STR, STN, GPE, GPI, THL)

CUE = np.zeros(4, dtype=[("mot", float),
                         ("cog", float),
                         ("value" , float),
                         ("reward", float)])

# shapes and positions choices for the whole simulation
# each pair out of the 6 possible is presented equal times
def init_choicesGuth(trials = n_trials):
	choices  = np.array([[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]])
	cues_cog = np.tile(choices, (trials/6,1))
	cues_mot = np.tile(choices, (trials/6,1))
	return cues_cog, cues_mot
def init_choicesPiron(ltrials = n_learning_trials, ttrials = n_testing_trials):
	choices  = np.array([0,1])
	learning_cues_cog = np.tile(choices, (ltrials,1))
	testing_cues_cog_fam = np.tile(choices, (ttrials,1))
	choices  = np.array([2,3])
	testing_cues_cog_unfam = np.tile(choices, (ttrials,1))
	return learning_cues_cog, testing_cues_cog_fam, testing_cues_cog_unfam
def init_choicesMot(trials = n_trials):
	choices  = np.array([[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]])
	cues_mot = np.tile(choices, (trials/6,1))
	return cues_mot
def init_1ch(trials = n_trials, perc1 = 0.25, perc2 = 0.75):
	choice1  = np.array([0])
	choice2  = np.array([1])
	choice1 = np.tile(choice1, trials*perc1)
	choice2 = np.tile(choice2, trials*perc2)
	choices = np.hstack((choice1,choice2))
	return choices
def trials_cues(protocol = 'Guthrie', ntrials = n_trials, ltrials = n_learning_trials, ttrials = n_testing_trials, perc1 = 0.25, perc2 = 0.75):

    global cues_cog,cues_mot, learning_cues_cog, testing_cues_cog_fam, testing_cues_cog_unfam, learning_cues_mot, testing_cues_mot_fam, testing_cues_mot_unfam

    if protocol == 'Guthrie':
    	CUE["reward"] = rewards_Guthrie
    	cues_cog, cues_mot = init_choicesGuth(trials = ntrials)
    	np.random.shuffle(cues_cog)
    	np.random.shuffle(cues_mot)
    	for i in range(cues_cog.shape[0]):
			np.random.shuffle(cues_cog[i,:])
			np.random.shuffle(cues_mot[i,:])
    	return cues_cog, cues_mot
    elif protocol == 'Piron':
    	CUE["reward"] = rewards_Piron
    	learning_cues_cog, testing_cues_cog_fam, testing_cues_cog_unfam = init_choicesPiron(ltrials = ltrials, ttrials = ttrials)
    	learning_cues_mot = init_choicesMot(ltrials)
    	testing_cues_mot_fam = init_choicesMot(ttrials)
    	testing_cues_mot_unfam = init_choicesMot(ttrials)
    	np.random.shuffle(learning_cues_cog)
    	np.random.shuffle(testing_cues_cog_fam)
    	np.random.shuffle(testing_cues_cog_unfam)
    	np.random.shuffle(learning_cues_mot)
    	np.random.shuffle(testing_cues_mot_fam)
    	np.random.shuffle(testing_cues_mot_unfam)
    	for i in range(learning_cues_cog.shape[0]):
			np.random.shuffle(learning_cues_cog[i,:])
    	for i in range(testing_cues_cog_fam.shape[0]):
			np.random.shuffle(testing_cues_cog_fam[i,:])
			np.random.shuffle(testing_cues_cog_unfam[i,:])
    	for i in range(learning_cues_mot.shape[0]):
			np.random.shuffle(learning_cues_mot[i,:])
    	for i in range(testing_cues_mot_fam.shape[0]):
			np.random.shuffle(testing_cues_mot_fam[i,:])
			np.random.shuffle(testing_cues_mot_unfam[i,:])
    	return learning_cues_cog, testing_cues_cog_fam, testing_cues_cog_unfam, learning_cues_mot, testing_cues_mot_fam, testing_cues_mot_unfam
    elif protocol == 'OneChoice':
    	CUE["reward"] = rewards_Piron
    	cues_cog = init_1ch(trials = ntrials, perc1 = perc1, perc2 = perc2)
    	cues_mot = init_choicesMot()
    	np.random.shuffle(cues_cog)
    	np.random.shuffle(cues_mot)
    	for i in range(cues_mot.shape[0]):
			np.random.shuffle(cues_mot[i,:])
    	return cues_cog, cues_mot


CUE["mot"]    = 0,1,2,3
CUE["cog"]    = 0,1,2,3
CUE["value"]  = 0.5
#CUE["reward"] = rewards

def weights(shape, s = 0.0005, initial = 0.5):
    N = np.random.normal(initial, s, shape)
    N = np.minimum(np.maximum(N, 0.0),1.0)
    return (Wmin+(Wmax-Wmin)*N)#initial*np.ones(shape)#

W1 = (2*np.eye(4) - np.ones((4,4))).ravel()
W2 = (2*np.eye(16) - np.ones((16,16))).ravel()

connections = {
    "CTX.cog -> STR.cog" : OneToOne( CTX.cog.V, STR.cog.Isyn, weights(4)  ), # plastic (RL)
    "CTX.mot -> STR.mot" : OneToOne( CTX.mot.V, STR.mot.Isyn, 0.5*np.ones(4)  ),#, weights(4)  ),
    "CTX.ass -> STR.ass" : OneToOne( CTX.ass.V, STR.ass.Isyn, 0.5*np.ones(4*4)  ),#, weights(4*4)),
    "CTX.cog -> STR.ass" : CogToAss( CTX.cog.V, STR.ass.Isyn, 0.5*np.ones(4)  ),#, weights(4)  ),
    "CTX.mot -> STR.ass" : MotToAss( CTX.mot.V, STR.ass.Isyn, 0.5*np.ones(4)  ),#, weights(4)  ),
    "CTX.cog -> STN.cog" : OneToOne( CTX.cog.V, STN.cog.Isyn, np.ones(4)  ),
    "CTX.mot -> STN.mot" : OneToOne( CTX.mot.V, STN.mot.Isyn, np.ones(4)  ),
    "STR.cog -> GPE.cog" : OneToOne( STR.cog.V, GPE.cog.Isyn, np.ones(4)  ),
    "STR.mot -> GPE.mot" : OneToOne( STR.mot.V, GPE.mot.Isyn, np.ones(4)  ),
    "STR.ass -> GPE.cog" : AssToCog( STR.ass.V, GPE.cog.Isyn, np.ones(4)  ),
    "STR.ass -> GPE.mot" : AssToMot( STR.ass.V, GPE.mot.Isyn, np.ones(4)  ),
    "STN.cog -> GPI.cog" : OneToAll( STN.cog.V, GPI.cog.Isyn, np.ones(4)  ),
    "STN.mot -> GPI.mot" : OneToAll( STN.mot.V, GPI.mot.Isyn, np.ones(4)  ),
    "STR.cog -> GPI.cog" : OneToOne( STR.cog.V, GPI.cog.Isyn, np.ones(4)  ),
    "STR.mot -> GPI.mot" : OneToOne( STR.mot.V, GPI.mot.Isyn, np.ones(4)  ),
    "STR.ass -> GPI.cog" : AssToCog( STR.ass.V, GPI.cog.Isyn, np.ones(4)  ),
    "STR.ass -> GPI.mot" : AssToMot( STR.ass.V, GPI.mot.Isyn, np.ones(4)  ),
    "STN.cog -> GPI.cog" : OneToAll( STN.cog.V, GPI.cog.Isyn, np.ones(4)  ),
    "STN.mot -> GPI.mot" : OneToAll( STN.mot.V, GPI.mot.Isyn, np.ones(4)  ),
    "STN.cog -> GPE.cog" : OneToAll( STN.cog.V, GPE.cog.Isyn, np.ones(4)  ),#new#
    "STN.mot -> GPE.mot" : OneToAll( STN.mot.V, GPE.mot.Isyn, np.ones(4)  ),#new#
    "THL.cog -> CTX.cog" : OneToOne( THL.cog.V, CTX.cog.Isyn, np.ones(4)  ),
    "THL.mot -> CTX.mot" : OneToOne( THL.mot.V, CTX.mot.Isyn, np.ones(4)  ),
    "CTX.cog -> THL.cog" : OneToOne( CTX.cog.V, THL.cog.Isyn, np.ones(4)  ),
    "CTX.mot -> THL.mot" : OneToOne( CTX.mot.V, THL.mot.Isyn, np.ones(4)  ),
    "GPE.cog -> STN.cog" : OneToOne( GPE.cog.V, STN.cog.Isyn, np.ones(4) ),
    "GPE.mot -> STN.mot" : OneToOne( GPE.mot.V, STN.mot.Isyn, np.ones(4) ),
    "GPE.cog -> GPI.cog" : OneToOne( GPE.cog.V, GPI.cog.Isyn, np.ones(4)  ),#new#
    "GPE.mot -> GPI.mot" : OneToOne( GPE.mot.V, GPI.mot.Isyn, np.ones(4)  ),#new#
    "GPI.cog -> THL.cog" : OneToOne( GPI.cog.V, THL.cog.Isyn, np.ones(4) ),
    "GPI.mot -> THL.mot" : OneToOne( GPI.mot.V, THL.mot.Isyn, np.ones(4) ),
    "THL.cog -> GPI.cog" : OneToOne( THL.cog.V, GPI.cog.Isyn, np.ones(4)  ),#new#
    "THL.mot -> GPI.mot" : OneToOne( THL.mot.V, GPI.mot.Isyn, np.ones(4)  ),#new#
    "CTX.mot -> CTX.mot" : AllToAll( CTX.mot.V, CTX.mot.Isyn, W1         ),
    "CTX.cog -> CTX.cog" : AllToAll( CTX.cog.V, CTX.cog.Isyn, W1         ),
    "CTX.ass -> CTX.ass" : AllToAll( CTX.ass.V, CTX.ass.Isyn, W2         ),
    "CTX.ass -> CTX.cog" : AssToCog( CTX.ass.V, CTX.cog.Isyn, np.ones(4) ),
    "CTX.ass -> CTX.mot" : AssToMot( CTX.ass.V, CTX.mot.Isyn, np.ones(4) ),
    "CTX.cog -> CTX.ass" : CogToAss( CTX.cog.V, CTX.ass.Isyn, weights(4, 0.0005)  ),
    "CTX.mot -> CTX.ass" : MotToAss( CTX.mot.V, CTX.ass.Isyn, weights(4, 0.00005) ),
}
for name,gain in gains.items():
    connections[name].gain = gain

# -----------------------------------------------------------------------------
def set_trial(n=2, cog_shuffle=True, mot_shuffle=True, noise=noise, trial = 0, protocol = 'Guthrie', familiar = True, Piron_learning = False):
    global cues_cog,cues_mot, learning_cues_cog, testing_cues_cog_fam, testing_cues_cog_unfam, learning_cues_mot, testing_cues_mot_fam, testing_cues_mot_unfam
    if protocol == 'Guthrie':
		CUE["cog"][0], CUE["cog"][1] = cues_cog[trial,:]
		CUE["mot"][0], CUE["mot"][1] = cues_mot[trial,:]
		ncues = 2

    elif protocol == 'Piron':#if protocol == 'Piron':
    	if Piron_learning:
			CUE["cog"][0], CUE["cog"][1] = learning_cues_cog[trial,:]
			CUE["mot"][0], CUE["mot"][1] = learning_cues_mot[trial,:]
    	else:
			if familiar:
				CUE["cog"][0], CUE["cog"][1] = testing_cues_cog_fam[trial,:]
				CUE["mot"][0], CUE["mot"][1] = testing_cues_mot_fam[trial,:]
			else:
				CUE["cog"][0], CUE["cog"][1] = testing_cues_cog_unfam[trial,:]
				CUE["mot"][0], CUE["mot"][1] = testing_cues_mot_unfam[trial,:]
    	ncues = 2

    elif protocol == 'OneChoice':
		CUE["cog"][0] = cues_cog[trial]
		CUE["mot"][0], CUE["mot"][1] = cues_mot[trial,:]
		ncues = 1

    CTX.mot.Iext = 0
    CTX.cog.Iext = 0
    CTX.ass.Iext = 0

    for i in range(ncues):
        c, m = CUE["cog"][i], CUE["mot"][i]

        CTX.mot.Iext[m]     = V_cue + np.random.uniform(-noise/2,noise/2)
        CTX.cog.Iext[c]     = V_cue + np.random.uniform(-noise/2,noise/2)
        CTX.ass.Iext[c*4+m] = V_cue + np.random.uniform(-noise/2,noise/2)


def iterate(dt):
    # Flush connections
    for connection in connections.values():
        connection.flush()

    # Propagate activities
    for connection in connections.values():
        connection.propagate()

    # Compute new activities
    for structure in structures:
        structure.evaluate(dt)


def reset(protocol = 'Guthrie', ntrials = n_trials, W_COG = None, W_MOT = None, W_STR = None):
    CUE["mot"]    = 0,1,2,3
    CUE["cog"]    = 0,1,2,3
    CUE["value"]  = 0.5
    reset_weights(W_COG = W_COG, W_MOT = W_MOT, W_STR = W_STR)
    reset_activities()
def reset_weights(W_COG = None, W_MOT = None, W_STR = None):
    if W_COG is not None:
		connections["CTX.cog -> CTX.ass"].weights = W_COG
		connections["CTX.mot -> CTX.ass"].weights = W_MOT
		connections["CTX.cog -> STR.cog"].weights = W_STR
    else:
		connections["CTX.cog -> CTX.ass"].weights = weights(4, 0.00005)#0.5*np.ones(4)
		connections["CTX.mot -> CTX.ass"].weights = weights(4, 0.00005)#0.5*np.ones(4)
		connections["CTX.cog -> STR.cog"].weights = weights(4)
def reset_activities():
    for structure in structures:
        structure.reset()
def history():
	history = np.zeros(duration, dtype=dtype)
	history["CTX"]["mot"] = CTX.mot.history[:duration]
	history["CTX"]["cog"] = CTX.cog.history[:duration]
	history["CTX"]["ass"] = CTX.ass.history[:duration]
	history["STR"]["mot"] = STR.mot.history[:duration]
	history["STR"]["cog"] = STR.cog.history[:duration]
	history["STR"]["ass"] = STR.ass.history[:duration]
	history["STN"]["mot"] = STN.mot.history[:duration]
	history["STN"]["cog"] = STN.cog.history[:duration]
	history["GPE"]["mot"] = GPE.mot.history[:duration]
	history["GPE"]["cog"] = GPE.cog.history[:duration]
	history["GPI"]["mot"] = GPI.mot.history[:duration]
	history["GPI"]["cog"] = GPI.cog.history[:duration]
	history["THL"]["mot"] = THL.mot.history[:duration]
	history["THL"]["cog"] = THL.cog.history[:duration]
	return history

def reset_history():
	CTX.mot.history[:duration] = 0
	CTX.cog.history[:duration] = 0
	CTX.ass.history[:duration] = 0
	STR.mot.history[:duration] = 0
	STR.cog.history[:duration] = 0
	STR.ass.history[:duration] = 0
	STN.mot.history[:duration] = 0
	STN.cog.history[:duration] = 0
	GPE.mot.history[:duration] = 0
	GPE.cog.history[:duration] = 0
	GPI.mot.history[:duration] = 0
	GPI.cog.history[:duration] = 0
	THL.mot.history[:duration] = 0
	THL.cog.history[:duration] = 0

def results(n_trials = n_trials):
	result = np.zeros(n_trials, dtype=dtype2)
	return result

def process(result, n = 2, learn = True, reverse = False, reverse_all = True):
    # A motor decision has been made
    # The actual cognitive choice may differ from the cognitive choice
    # Only the motor decision can designate the chosen cue
    mot_choice = np.argmax(CTX.mot.U)
    result["Choice"]["mot"]  = mot_choice
    cog_choice = np.argmax(CTX.cog.U)
    result["Choice"]["cog"]  = cog_choice

    # The actual cognitive choice may differ from the cognitive choice
    # Only the motor decision can designate the chosen cue
    for i in range(n):
        #print mot_choice, CUE["mot"][:n][i]
        if mot_choice == CUE["mot"][:n][i]:
            choice = int(CUE["cog"][:n][i])
            result["Choice"]["ch"] = choice
    if not reverse:
		if n == 1:
			if choice == CUE["cog"][0]:
				result["P"] = 1
			else:
				result["P"] = 0
		else:
			if choice == min(CUE["cog"][:n][0],CUE["cog"][:n][1]):
				result["P"] = 1
			else:
				result["P"] = 0
    else:
		if reverse_all:
			if choice == max(CUE["cog"][:n][0],CUE["cog"][:n][1]):
				result["P"] = 1
			else:
				result["P"] = 0
		else:
			c1, c2 = np.sort(CUE["cog"][:n])
			if np.array_equal([c1, c2], [1,2]):
				if choice == max(CUE["cog"][:n][0],CUE["cog"][:n][1]):
					result["P"] = 1
				else:
					result["P"] = 0
			elif choice == min(CUE["cog"][:n][0],CUE["cog"][:n][1]):
				result["P"] = 1
			else:
				result["P"] = 0
    if learn:
		# Compute reward
		reward = float(np.random.uniform(0,1) < CUE["reward"][choice])
		result["R"] = reward

		# Compute prediction error
		error = reward - CUE["value"][choice]

		# Update cues values
		CUE["value"][choice] += error* alpha_CUE

        # Reinforcement striatal learning
		lrate = alpha_LTP if error > 0 else alpha_LTD
		dw = error * lrate * STR.cog.V[choice]
		W = connections["CTX.cog -> STR.cog"].weights
		W[choice] = W[choice] + dw * (Wmax-W[choice]) * (W[choice]-Wmin)
		connections["CTX.cog -> STR.cog"].weights = W

		# Hebbian cortical learning
		dw = alpha_LTP_ctx * CTX.cog.V[choice]
		W = connections["CTX.cog -> CTX.ass"].weights
		W[choice] = W[choice] + dw * (Wmax-W[choice]) * (W[choice]-Wmin)
		connections["CTX.cog -> CTX.ass"].weights = W

		dw = alpha_LTP_ctx * CTX.mot.V[mot_choice]
		W = connections["CTX.mot -> CTX.ass"].weights
		W[mot_choice] = W[mot_choice] + dw * (Wmax-W[mot_choice]) * (W[mot_choice]-Wmin)
		connections["CTX.mot -> CTX.ass"].weights = W



def debug_learning(Wcog, Wmot, Wstr, cues_value):
		print "Cues Values			: ", cues_value
		print "Cortical Weights Cognitive	: ", Wcog
		print "Cortical Weights Motor		: ", Wmot
		print "Striatal Weights		: ", Wstr

def debug(cgchoice = None, c1 = None, c2 = None, m1 = None, m2 = None, reverse = False, reverse_all = True, P = None, reward = None, RT = None):

	if cgchoice is not None:
		print "Choice:         ",
		if cgchoice == c1:
			print " 	[%d]" % c1,
		else:
			print " 	%d" % c1,
		if cgchoice == c2:
			print " [%d]" % c2,
		else:
			print " %d" % c2,
		if not reverse:
			if cgchoice == np.minimum(c1,c2):
				print " (good)"
			else:
				print " (bad)"
		else:
			if reverse_all:
				if cgchoice == np.maximum(c1,c2):
					print " (good)"
				else:
					print " (bad)"
			else:
				temp1, temp2 = np.sort([c1,c2])
				if np.array_equal([temp1, temp2],[1,2]):
					if cgchoice == np.maximum(c1,c2):
						print " (good)"
					else:
						print " (bad)"
				elif cgchoice == np.minimum(c1,c2):
					print " (good)"

				else:
					print " (bad)"

	if m1 is not None:
		print "Positions:         	 %d   %d" %(m1, m2)
	if P is not None:
		print "Mean performance	 	: %.3f %%" % (P.mean()*100)

	if RT is not None:
		print "Mean Response time		: %.3f ms" % (RT.mean())
	if reward is not None:
		print "Reward	  		 	: %d" % (reward)
		print "Mean reward		 	: %.3f %%" % (R.mean()*100)

def debug1ch(cgchoice = None, c1 = None, m1 = None, P = None, RT = None):

	if cgchoice is not None:
		print "Choice:         ",
		if cgchoice == c1:
			print " 	[%d]" % c1,
		else:
			print " 	Wrong choice"


	if m1 is not None:
		print "Positions:         	 %d" %(m1)
	if P is not None:
		print "Mean performance	 	: %.3f %%" % (np.array(P).mean()*100)

	if RT is not None:
		print "Mean Response time		: %.3f ms" % (np.array(RT).mean())


def debug_total(P, RT = None, CV = None, Wcog = None, Wmot = None, Wstr = None):

	print "Mean Performance		: " , (P.mean(axis=1)).mean(axis = 0)*100, '%'
	if RT is not None:
		print "Mean Reaction Time	:" ,(RT.mean(axis=1)).mean(axis = 0)*100, '%'
	if CV is not None:
		print "Mean Cues Values		:" + str(CV.mean(axis = 0))
		print 'Mean Cortical Weights Cog	: ' + str(Wcog[:,-1].mean(axis = 0))
		print 'Mean Cortical Weights Mot	: ' + str(Wmot[:,-1].mean(axis = 0))
		print 'Mean Striatal Weights		: ' + str(Wstr[:,-1].mean(axis = 0))

def save_files(folder, i, cues_cog, cues_mot, P, Cvalues, wCog, wMot, wStr, RT_cg, RT_mot, R, ch, ch_cog, ch_mot):
		file = folder + '/Performances' + str(i) + '.npy'
		np.save(file,P)
		file = folder + '/Trials_cues_cog' + str(i) + '.npy'
		np.save(file,cues_cog)
		file = folder + '/Trials_cues_mot' + str(i) + '.npy'
		np.save(file,cues_mot)
		file = folder + '/Cvalues' + str(i) + '.npy'
		np.save(file,Cvalues)
		file = folder + '/wCog' + str(i) + '.npy'
		np.save(file,wCog)
		file = folder + '/wMot' + str(i) + '.npy'
		np.save(file,wMot)
		file = folder + '/wStr' + str(i) + '.npy'
		np.save(file,wStr)
		file = folder + '/RT_cg' + str(i) + '.npy'
		np.save(file,RT_cg)
		file = folder + '/RT_mot' + str(i) + '.npy'
		np.save(file,RT_mot)
		file = folder + '/R' + str(i) + '.npy'
		np.save(file,R)
		file = folder + '/choice' + str(i) + '.npy'
		np.save(file,ch)
		file = folder + '/ch_cog' + str(i) + '.npy'
		np.save(file,ch_cog)
		file = folder + '/ch_mot' + str(i) + '.npy'
		np.save(file,ch_mot)
