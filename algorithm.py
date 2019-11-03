import mingus.core.notes as Notes
import mingus.core.chords as Chords
import mingus.core.progressions as Progressions
from random import seed
from random import randint
from random import shuffle

def note_to_int(note, key):
	if(Notes.note_to_int(note) >= Notes.note_to_int(key)) :
		return Notes.note_to_int(note) - Notes.note_to_int(key)
	else:
		return 12 - (Notes.note_to_int(key) - Notes.note_to_int(note)) 


def harmonize(bars, melody, key, states, emit, time_sig, mode): 
	prev = '-'
	chords = []
	# chords.append(Progressions.to_chords("I", key))
	print melody
	(bpb, vb) = time_sig

	### PARA CADA COMPASSO, ANALISAR NOTAS PARA DEFINIR A AFINIDADE COM CADA UM DOS 7 ACORDES DO CAMPO HARMONICO. ###
	###	DEPOIS DECIDIR PARA QUAL ACORDE IR, LEVANDO EM CONTA O ACORDE ANTERIOR (CADEIA DE MARKOV) ###
	# for bar in bars:
	for i in range(0, len(bars)):
		notes = []		
		states = {'I':0, 'ii':0, 'iii':0, 'IV':0, 'V':0, 'vi':0, 'vii':0}
		# for note in bars[i]:
		head = 1.1
		if len(bars[i]) == 0:
			chords.append(prev)

		for j in range(0, len(bars[i])):
			for state in states:
				# Nota no primeiro tempo (sempre forte) tem mais peso
				if j == 0:
					states[state] += (emit[state][note_to_int(bars[i][j], key)] * head)
				else:
					states[state] += (emit[state][note_to_int(bars[i][j], key)])
		# print states
		if i == 0:
			if firstChord(states):
				chords.append("I")
				prev = ("I")
				continue
		states[prev] = 0
		# curr = max(states.iterkeys(), key=(lambda key: states[key]))
		curr = bestChord(states, prev)
		print curr
		chords.append(curr)
		prev = curr
		print "\n"
	return chords

cadences = {
	'ii': 'V',
	'V': 'I',
	'IV': 'V',
	'vii': 'I'
}

def bestChord(states, prev):
	best = ('-', 0)
	for state in states:
		curr = states.get(state)
		if curr > best[1]:
			best = (state, curr)
		elif curr == best[1]: # Caso haja empate, confere cadencias
			if cadences.has_key(prev) and cadences[prev] == state:
				best = (state, curr)
				print 'cadencia' 
				print best
	return best[0]

def firstChord(states):
	sorted_states = sorted(states, key=(lambda key: states[key]))
	ln = len(sorted_states)
	for i in range(ln-1, ln-4, -1):
		if sorted_states[i] == 'I':
			return True
	return False

def avoid(mode):
	if mode == "major":
		return {
		'I': 'iii',
		}

def reharmonize(chords):
	seed(1)
	for i in range(1, len(chords)-1):
		if randint(1,10) > 5:
			subs = Progressions.substitute([chords[i]], 0)
			for sub in subs:
				if sub != chords[i-1] and sub != chords[i+1]:
					chords[i] = sub
					break