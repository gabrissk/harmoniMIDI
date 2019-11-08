import mingus.core.notes as Notes
import mingus.core.chords as Chords
import mingus.core.progressions as Progressions
from mingus.containers import Note
from mingus.containers import NoteContainer
from mingus.containers import Bar
from mingus.containers.instrument import Instrument, Piano, Guitar
from mingus.containers import Track
from mingus.containers import Composition
import mingus.core.intervals as Intervals
import mingus.core.keys as Keys

from mingus.midi import fluidsynth

from mingus.midi import midi_file_in as MidiFileIn
from mingus.midi import midi_file_out as MidiFileOut
import random

import mingus.extra.lilypond as LilyPond

import midiToAudio as midi
import sys, os

def note_to_int(note, key):
	if(Notes.note_to_int(note) >= Notes.note_to_int(key)) :
		return Notes.note_to_int(note) - Notes.note_to_int(key)
	else:
		return 12 - (Notes.note_to_int(key) - Notes.note_to_int(note)) 


def harmonize(bars, key, emit, time_sig, mode): 
	prev = '-'
	chords = []
	(bpb, vb) = time_sig
	if mode == 'major':
		ch = 'I'
	else:
		ch = 'vi'
	### PARA CADA COMPASSO, ANALISAR NOTAS PARA DEFINIR A AFINIDADE COM CADA UM DOS 7 ACORDES DO CAMPO HARMONICO. ###
	###	DEPOIS DECIDIR PARA QUAL ACORDE IR, LEVANDO EM CONTA O ACORDE ANTERIOR (CADEIA DE MARKOV) ###
	# for bar in bars:
	for i in range(0, len(bars)):
		notes = []		
		states = {'I':0, 'ii':0, 'iii':0, 'IV':0, 'V':0, 'vi':0, 'vii':0}
		# for note in bars[i]:
		head = 1.1
		if bars[i][0][0] == None:
			chords.append('bbbbbI')
			continue
			# prev = '-'
		for j in range(0, len(bars[i])):
			for state in states:
				# Nota no primeiro tempo (sempre forte) tem mais peso
				if j == 0:
					states[state] += (emit[state][note_to_int(bars[i][j][0], key)] * head)
				else:
					states[state] += (emit[state][note_to_int(bars[i][j][0], key)])
		if i == 0:
			if firstChord(states, ch):
				chords.append(ch)
				prev = (ch)
				continue
		if i == len(bars)-1:
			if lastChord(states, ch):
				chords.append(ch)
				continue
		states[prev] = 0
		curr = bestChord(states, prev)
		chords.append(curr)
		prev = curr
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

def firstChord(states, ch):
	return checkTonic(states, ch)

def lastChord(states, ch):
	return checkTonic(states, ch)

def checkTonic(states, sh):
	sorted_states = sorted(states, key=(lambda key: states[key]))
	ln = len(sorted_states)
	for i in range(ln-1, ln-4, -1):
		if sorted_states[i] == sh:
			return True
	return False

# def avoid(mode):
# 	if mode == "major":
# 		return {
# 		'I': 'iii',
# 		}

def reharmonize(chords, scores, bars, key, mode):
	if mode == 'minor':
		key = Keys.relative_minor(key)
	for i in range(1, len(chords)-1):
		if(chords[i] == 'bbbbbI'): continue
		if random.random() > 0.5:
			subs = Progressions.substitute([chords[i]], 0)
			for j in range(0,5):	
				sub = random.choice(subs)
				if sub != chords[i-1] and sub != chords[i+1] and not (sub.endswith('dim')) and not (sub.endswith('dim7')) and score(sub, bars[i], key):
					chords[i] = sub
					break

def export(melody_track, chords, key, time_sig, bpm, file):
	i = Instrument()
	i.instrument_nr = 1
	t2 = Track()
	for i in range(0, len(chords)):
		b = Bar(key, time_sig)
		if len(chords[i][0]) > 5:
			b.place_notes(None, 1)
		else:
			b.place_notes(NoteContainer(chords[i]), 1)
		t2 + b

	c = Composition()
	c.add_track(melody_track)
	c.add_track(t2)

	out_dir = 'out/'

	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	mid = file.split('/')[-1]
	MidiFileOut.write_Composition(out_dir+'/'+mid, c, bpm)

	file = out_dir + '/' + mid

	sys.argv.append('')
	sys.argv.append('')

	sys.argv[1] = "--midi-file=" + file
	sys.argv[2] = "--out-dir=" + out_dir

	midi.main()
	if os.path.exists(file):
		os.remove(file)

def to_Sheet(bars, chords, track, key, mode, file, out_dir, title,author):
	track = LilyPond.from_Track(track)
	track = track[1:-1]
	track = '\\header {title= "'+ title + '" composer = "' + author +  '"} \nmelody = {\n\\key ' + key.lower() + ' \\' + mode + '\n' + track + '''}
		harmonies = \\chordmode {''' + get_Shorthands(determine_chords(chords)) + '''}\n
		\\score {\n
		<<\n
    	\\new ChordNames {\n 
      	\\set chordChanges = ##t\n''' + determine_clef(bars)+ '''
      	\\harmonies\n 
    	}\n 
    	\\new Staff \\melody 
 		>>\n 
  		\\layout{ } \n 
  		\\midi { }\n 
		}''' 

	file = file.split('/')[-1]
	path = out_dir + '/' + file.split('.')[0]
	LilyPond.to_pdf(track, path)
	if os.path.exists(path + '.midi'):	
		os.remove(path + '.midi')


def get_Shorthands(shorthand):
	ret = ''
	for short in shorthand:
		ret += (short + ' ')
	return ret

def determine_chords(chords):
	sh = []
	for chord in chords:
		if chord[0].endswith('bbb'):
			sh.append('r1')
		else:
			res = {}
			if len(chord) == 4:
				if Intervals.determine(chord[0], chord[3]).split(' ')[0] == 'minor':
					res['seventh'] = ''
				elif Intervals.determine(chord[0], chord[3]).split(' ')[0] == 'major':
					res['seventh'] = 'maj'
			else:
				res['seventh'] = '-'
			if chord[0].find('#') != -1:
				res['acc'] = 'is'
				res['tonic'] = chord[0][0:(chord[0].find('#'))].lower()
			elif chord[0].find('b') != -1:
				res['acc'] = 'es'
				res['tonic'] = chord[0][0:(chord[0].find('b'))].lower()
			else:
				res['acc'] = '-'
				res['tonic'] = chord[0].lower()
			if Intervals.determine(chord[0], chord[2]).split(' ')[0] == 'minor':
				res['fifth'] = 'dim'
			elif Intervals.determine(chord[0], chord[2]).split(' ')[0] == 'augmented':
				res['fifth'] = 'aug'
			else:
				res['fifth'] = '-'
			if Intervals.determine(chord[0], chord[1]).split(' ')[0] == 'major':
				res['mode'] = ''
			elif Intervals.determine(chord[0], chord[1]).split(' ')[0] == 'minor':
				res['mode'] = 'min'
			str = res['tonic']
			if res['acc'] != '-':
				str += res['acc']
			str += '1:'
			if res['fifth'] != '-':
				str += res['fifth']
				sh.append(str)
				continue
			str += res['mode']
			if res['seventh'] != '-':
				str += ('7' + res['seventh'])
			sh.append(str)
	return sh

def determine_clef(bars):
	total = 0
	n = 0
	for bar in bars:
		for note in bar:
			total += note[1]
			n += 1
	octave = int(round(float(total) / n))

	return '\\clef treble' if octave >= 4 else '\\clef bass'  

def score(sub, bar, key):
	sub = Progressions.to_chords([sub], key)[0]
	if len(sub) < 4:
		return True
	else:
		for note in bar:
			if sub[3] == note:
				return True
	return False

def raise_fifth(chords, maj_key):
	print chords
	key = Keys.relative_minor(maj_key)
	for chord in chords:
		if chord == (Chords.dominant(key) or Chords.dominant7(key)):
			chord[1] = Notes.reduce_accidentals(Notes.augment(chord[1]))
	print chords