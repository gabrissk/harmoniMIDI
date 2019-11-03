#import mingus.core.diatonic as diatonic
import mingus.core.chords as Chords
import mingus.core.notes as Notes
import mingus.core.intervals as intervals
import mingus.core.scales as scales
import mingus.core.value as value
import mingus.core.progressions as progressions

from mingus.containers import Note
from mingus.containers import NoteContainer
from mingus.containers import Bar
from mingus.containers.instrument import Instrument, Piano, Guitar
from mingus.containers import Track
from mingus.containers import Composition

from mingus.midi import fluidsynth

from mingus.midi import midi_file_in as MidiFileIn
from mingus.midi import midi_file_out as MidiFileOut
import mido
import mingus.extra.lilypond as LilyPond
import algorithm as Harmonizer
import music21
import midiToAudio
import sys



# fluidsynth.init("GeneralUser_GS_1.471/soundfont.sf2","alsa")

c = Composition()
c2 = MidiFileIn.MIDI_to_Composition(sys.argv[2])

tra = Track()
notes = list()
bars = []
for x in c2:
	if(x.__class__.__name__ == "Composition"):
		for track in x.tracks:
			i = 0;
			for bar in track.bars:
				if len(bar.get_note_names()) > 0:
					tra + bar
				notesB = list()
				for y in bar:
					# notes + Note(String(NoteContainer(y[-1]))) ### CADA NOTA DA MELODIA ESTA AQUI
					if(len(NoteContainer(y[-1]).get_note_names()) > 0):
						notes.append(NoteContainer(y[-1]).get_note_names()[0])
						notesB.append(NoteContainer(y[-1]).get_note_names()[0])
				bars.append(notesB)
				i = i +1
			key = x.tracks[0][0].key.key
			meter = x.tracks[0][0].meter
bars = bars[:-1]

bpm = c2[1]

### DESCOBRIR TONALIDADE MELODIA -> 1o GRAU ###
key_and_mode = scales.determine(notes)[0]
if key_and_mode != None:
	key = key_and_mode.split(" ")[0]
	mode = key_and_mode.split(" ")[1]
	print (key, mode)
else:
	score = music21.converter.parse("test.midi")
	parse = score.analyze('key')
	key = parse.tonic.name
	mode = parse.key.mode


### TRANSFORMAR AS NOTAS EM NUMEROS REFERENTES A TONALIDADE
notesInt = []
for note in notes:
	notesInt.append(Harmonizer.note_to_int(note, key))

### PREENCHER VETOR DE PROBABILIDADES INICIAIS (1 NO PRIMEIRO ACORDE, 0 NO RESTO) ###
# startProb = {"I": 1, "ii": 0, "iii": 0, "IV": 0, "V": 0, "vi": 0, "vii": 0}

### BOLAR TRANSICOES DE ACORDES/NOTAS/GRAUS ###
emissionProbs = {
	'I':   {0: 0.5,   1: -0.2,  2: 0,     3: 0,     4: 0.35,  5: 0,     6: 0,     7: 0.35,  8: 0,     9: 0,     10: 0,     11: 0.1},
	'ii':  {0: 0,     1: 0.1,   2: 0.5,   3: -0.2,  4: 0,     5: 0,     6: 0.35,  7: 0,     8: 0,     9: 0.35,  10: 0,     11: 0},
	'iii': {0: 0,     1: 0,     2: 0,     3: 0.1,   4: 0.5,   5: -0.2,  6: 0,     7: 0,     8: 0.35,  9: 0,     10: 0,     11: 0.35},
	'IV':  {0: 0.35,  1: 0,     2: 0,     3: 0,     4: 0.1,   5: 0.5,   6: -0.2,  7: 0,     8: 0,     9: 0.35,  10: 0,     11: 0},
	'V':   {0: 0,     1: 0,     2: 0.35,  3: 0,     4: 0,     5: 0,     6: 0.1,   7: 0.5,   8: -0.2,  9: 0,     10: 0,     11: 0.35},
	'vi':  {0: 0,     1: 0.35,  2: 0,     3: 0,     4: 0.35,  5: 0,     6: 0,     7: 0,     8: 0.1,   9: 0.5,   10: -0.2,  11: 0},
	'vii': {0: -0.2,  1: 0,     2: 0,     3: 0.35,  4: 0,     5: 0,     6: 0.35,  7: 0,     8: 0,     9: 0,     10: 0.11,  11: 0.5}
}


states = ('I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii')

chords = Harmonizer.harmonize(bars, notesInt, key, states, emissionProbs, (4,4), mode)
# print chords
Harmonizer.reharmonize(chords)
# print chords
chords = progressions.to_chords(chords, key)

Harmonizer.export(tra, chords, key, (4,4), bpm)

# MidiFileOut.write_Composition("/home/gabriel.morais/Downloads/test3.midi", c2[0], 100)
shorthand = []
for chord in chords:
	shorthand.append(Chords.determine_triad(chord, True))
print shorthand 
track = LilyPond.from_Track(tra)
track = track[1:-1]
track = 'melody = \\relative d {\n\\key ' + key.lower() + ' \\' + mode + '\n' + track + '''}
		harmonies = \\chordmode {d a g d}\n
		\\score {\n
		<<\n
    	\\new ChordNames {\n 
      	\\set chordChanges = ##t\n 
      	\\harmonies\n 
    	}\n 
    	\\new Staff \\melody 
 		>>\n 
  		\\layout{ } \n 
  		\\midi { }\n 
		}''' 
		
print track
LilyPond.to_pdf(track, "test")



# statesMin = ('i', 'ii', 'III', 'iv', 'V', 'VI', 'VII')

# majTransitionProbs = {
# 	'I':   {'I': 0,  'ii': 0.166,  'iii': 0.166, 'IV': 0.166,  'V': 0.166,  'vi': 0.166,  'vii': 0.166},
# 	'ii':  {'I': 0,      'ii': 0,      'iii': 0,     'IV': 0.1428, 'V': 0.8572, 'vi': 0,      'vii': 0},
# 	'iii': {'I': 0,      'ii': 0,      'iii': 0,     'IV': 0,      'V': 0.1428, 'vi': 0.8572, 'vii': 0},
# 	'IV':  {'I': 0.1428, 'ii': 0,      'iii': 0,     'IV': 0,      'V': 0.8572, 'vi': 0,      'vii': 0},
# 	'V':   {'I': 0.8572, 'ii': 0,      'iii': 0,     'IV': 0,      'V': 0, 'vi': 0,      'vii': 0},
# 	'vi':  {'I': 0,      'ii': 0.8572, 'iii': 0,     'IV': 0,      'V': 0.1428, 'vi': 0,      'vii': 0},
# 	'vii': {'I': 0.8572, 'ii': 0,      'iii': 0,     'IV': 0,      'V': 0.1428, 'vi': 0,      'vii': 0}
# }
# b = Bar()
# b2 = Bar('Ab', (3, 4))
# n = NoteContainer(['A', 'C', 'E'])
# t = Track()
# b + n
# b + []
# b + n
# b + n
# b2 + n
# b2 + n
# b2 + []
# t + b
# t + b
# t.name = 'Track Name Test'
# MidiFileOut.write_NoteContainer('/home/gabriel.morais/Downloads/test1.mid', n)
# MidiFileOut.write_Bar('/home/gabriel.morais/Downloads/test2.mid', b)
# MidiFileOut.write_Bar('/home/gabriel.morais/Downloads/test3.mid', b, 200)
# MidiFileOut.write_Bar('/home/gabriel.morais/Downloads/test4.mid', b2, 200, 2)
# MidiFileOut.write_Track('/home/gabriel.morais/Downloads/test5.mid', t, 120)
