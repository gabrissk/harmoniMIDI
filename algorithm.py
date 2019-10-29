import mingus.core.notes as Notes
import mingus.core.chords as Chords

def algorithm(obs, states, start_p, trans_p, emit_p):
	v = [{}]
	for state in states:	
		v[0][state] = {"prob": start_p[state] * emit_p[state][obs[0]], "prev": None}
	for t in range(1, len(obs)):
		v.append({})
		for state in states:
			max_tr_prob = v[t-1][states[0]]["prob"] * trans_p[states[0]][state]
			prev_sel = states[0]
			for prev_state in states[1:]:
				prob = v[t-1][prev_state]["prob"] * trans_p[prev_state][state]
				if prob > max_tr_prob:
					max_tr_prob = prob
					prev_sel = prev_state
			max_prob = max_tr_prob * emit_p[state][obs[t]]
			v[t][state] = {"prob": max_prob, "prev": prev_sel}

	result = []
	max_prob = max(value["prob"] for value in v[-1].values())
	prev = None
	for state, data in v[-1].items():
		if data["prob"] == max_prob:
			result.append(state)
			prev = state
			break
	for i in range(len(v) -2, -1, -1):
		result.insert(0, v[i+1][prev]["prev"])
		prev = v[i+1][prev]["prev"]

	print result

def note_to_int(note, key):
	if(Notes.note_to_int(note) >= Notes.note_to_int(key)) :
		return Notes.note_to_int(note) - Notes.note_to_int(key)
	else:
		return 12 - (Notes.note_to_int(key) - Notes.note_to_int(note)) 

def algorithm2(obs, states, start_p, trans_p, emit_p):
	# v = [{}]
	# b = [{}]
	v = [[0 for _ in range(len(obs))] for _ in range(len(states))]
	b = [ [0 for _ in range(len(obs))] for _ in range(len(states))]
	print v
	for i in range(len(states)):
		v[0][i] = start_p[i] * emit_p[i][obs[0]]
	
	for i in range(1, len(obs)):
		for j in states:
			print len(v)
			print len(obs)
			print len(trans_p["I"])
			print len(states)
			v[i][j] = emit_p[j][obs[i]] * max(v[i-1][k] * trans_p[k][j] for k in states)
			b[j][k] = max(enumerate([v[k][i-1] * trans_p[k][j] for k in range(len(states))]), key = operator.itemgetter(1))

	z, max_prob = max(enumerate([v[k][-1] for k in range(len(states))]), key = operator.itemgetter(1))
	path = [None for _ in range(len(obs))]
	path[-1] = states[z]

	for i in range(len(obs)-1, 0 , -1):
		z = b[z][i]
		path[i-1] = states[z]

	print path




