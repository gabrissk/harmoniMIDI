import mingus.core.notes as Notes




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
		result.insert(0, v[t+1][prev]["prev"])
		prev = v[t+1][prev]["prev"]

	print result.join()

def note_to_int(note, key):
	if(Notes.note_to_int(note) >= Notes.note_to_int(key)) :
		return Notes.note_to_int(note) - Notes.note_to_int(key)
	else:
		return 12 - (Notes.note_to_int(key) - Notes.note_to_int(note)) 