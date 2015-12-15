import numpy as np

def init_choicesGuth(trials):
	choices  = np.array([[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]])
	cues_cog = np.tile(choices, (trials/6,1))
	cues_mot = np.tile(choices, (trials/6,1))
	return cues_cog, cues_mot

def trials_cues(ntrials):

	cues_cog, cues_mot = init_choicesGuth(trials = ntrials)
	np.random.shuffle(cues_cog)
	np.random.shuffle(cues_mot)
	for i in range(cues_cog.shape[0]):
		np.random.shuffle(cues_cog[i,:])
		np.random.shuffle(cues_mot[i,:])
	return cues_cog, cues_mot

n_trials = 120
cues_cog, cues_mot = trials_cues(ntrials = n_trials)
P = []
for i in range(n_trials):
	print('Task: ', i)
	print('Cog cues: ', cues_cog[i,:])
	print('Mot cues: ', cues_mot[i,:])
	mot_choice = np.random.choice(cues_mot[i,:],1)[0]
	cog_choice = cues_cog[i,0] if mot_choice == cues_mot[i,0] else cues_cog[i,1]
	print('Mot choice: ', mot_choice)
	print('Cog choice: ', cog_choice)
	P.append(1 if cog_choice == np.min(cues_cog[i]) else 0)
	print('Performance : ', P[i])
	print('Mean performance : ', np.array(P).mean())
	print()

print(np.array(P).mean())


