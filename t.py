#import mingus.core.diatonic as diatonic
import mingus.core.chords as chords
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

import algorithm as Algo

import music21


n = NoteContainer(chords.triad("C", "C"))

b = Bar(None, (4,4))
b.place_notes(NoteContainer(chords.triad("C", "C")),8)
b.place_notes(NoteContainer(chords.triad("C", "C")),8)
b.place_notes(NoteContainer(chords.triad("A", "C")),4)
b.place_notes(NoteContainer(chords.triad("F", "C")),4)
b.place_notes(NoteContainer(chords.triad("G", "C")),4)

t = Track()
# print(t)
t.name = "Teste"

b1 = Bar(None, (4,4))
# b1.place_notes(NoteContainer(chords.triad("C", "C")), 4)
b1.place_notes(Note("D-3"), 4)
b1.place_notes(Note("E-3"), 4)
b1.place_notes(Note("F#-3"), 4)
b1.place_notes(Note("D-3"), 4)
t + b1
b1 = Bar(None, (4,4))
b1.place_notes(Note("G-3"), 2)
b1.place_notes(Note("G-3"), 2)
t + b1
b1 = Bar(None, (4,4))
b1.place_notes(Note("A-3"), 4)
b1.place_notes(Note("G-3"), 4)
b1.place_notes(Note("F#-3"), 4)
b1.place_notes(Note("E-3"), 4)
t + b1
b1 = Bar(None, (4,4))
b1.place_notes(Note("C#-3"), 2)
b1.place_notes(Note("D-3"), 2)
t + b1

# b + n
# b1 + n
# n = NoteContainer(chords.triad("F", "C"))
# b+n
# b1 + n
# n = NoteContainer(chords.triad("G", "C"))
# # b+n
# b1+n
# n = NoteContainer(chords.triad("A", "C"))
# # b+n
# b1+n

fluidsynth.init("GeneralUser_GS_1.471/soundfont.sf2","alsa")
# nc = NoteContainer(chords.triad("C", "C"))
# # for x in xrange(1,128):
# # 	fluidsynth.set_instrument(1, x)
# # 	fluidsynth.play_Bar(b,1,5000)
# # 	#nc + c
# print(t)
# fluidsynth.play_Track(t,1,100)
MidiFileOut.write_Track("test.midi", t, 150)


mid = mido.MidiFile("test.midi")
# print(mid)

# for msg in mid.play():
# 	print(msg)

### ACHANDO O BPM ###
# print(mid.length)
for msg in mid.tracks[0]:
	# print(msg)
	if(msg.type == "set_tempo"):
		bpm = mido.bpm2tempo(msg.tempo) 
		break

# beat = 60.0 / bpm ### DURACAO DO BEAT EH 60 / BPM ACHADO ACIMA ###
# print bpm, beat

# bars = round(mid.length / beat / 4) ### QNTD DE COMPASSOS ###
# print int(bars)

track = Track()


c = Composition()
c = MidiFileIn.MIDI_to_Composition("mel.mid")
c2 = MidiFileIn.MIDI_to_Composition("test.midi")
# print c.__class__.__name__
# print c
# print "\n"
tra = Track()
notes = list()
for x in c2:
	# print x
	print x.__class__.__name__
	if(x.__class__.__name__ == "Composition"):
		for track in x.tracks:
			# print "Track:"
			# print track
			for bar in track.bars:
				# print "bars:"
				# bar.set_meter((3,4))
				# print bar
				# print bar.key.key
				# print bar.meter
				tra + bar
				for y in bar:
					# notes + Note(String(NoteContainer(y[-1]))) ### CADA NOTA DA MELODIA ESTA AQUI
					if(len(NoteContainer(y[-1]).get_note_names()) > 0):
						notes.append(NoteContainer(y[-1]).get_note_names()[0])
					# print y
					# print "\n"
				# print "\n"
			# print "\n"
			key = x.tracks[0][0].key.key
			meter = x.tracks[0][0].meter

# 	print "\n"

print key
print meter

# print(c[0])
#fluidsynth.play_Composition(c[0],1,100)

print c[1]
print c2[1]
print notes
# MidiFileOut.write_Composition("/home/gabriel.morais/Downloads/test3.midi", c[0], 100)
# track = LilyPond.from_Track(tra)
# LilyPond.to_pdf(track, "test")

### DESCOBRIR PRIMEIRO ACORDE -> 1o GRAU ###
score = music21.converter.parse("test.midi")
key = score.analyze('key')
print(key.tonic.name, key.mode)

major = key.mode == "major"

### TRANSFORMAR AS NOTAS EM NUMEROS REFERENTES A TONALIDADE

### PREENCHER VETOR DE PROBABILIDADES INICIAIS (1 NO PRIMEIRO ACORDE, 0 NO RESTO) ###
startProb = {"I": 1, "ii": 0, "iii": 0, "IV": 0, "V": 0, "vi": 0, "vii": 0}

### BOLAR TRANSICOES DE ACORDES/NOTAS/GRAUS ###

notesInt = []
for note in notes:
	notesInt.append(Algo.note_to_int(note, key.tonic.name))
print notesInt

statesMaj = ('I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii')
statesMin = ('i', 'ii', 'III', 'iv', 'V', 'VI', 'VII')

majTransitionProbs = {
	'I':   {'I': 0,  'ii': 0.166,  'iii': 0.166, 'IV': 0.166,  'V': 0.166,  'vi': 0.166,  'vii': 0.166},
	'ii':  {'I': 0,      'ii': 0,      'iii': 0,     'IV': 0.1428, 'V': 0.8572, 'vi': 0,      'vii': 0},
	'iii': {'I': 0,      'ii': 0,      'iii': 0,     'IV': 0,      'V': 0.1428, 'vi': 0.8572, 'vii': 0},
	'IV':  {'I': 0.1428, 'ii': 0,      'iii': 0,     'IV': 0,      'V': 0.8572, 'vi': 0,      'vii': 0},
	'V':   {'I': 0.8572, 'ii': 0,      'iii': 0,     'IV': 0,      'V': 0, 'vi': 0,      'vii': 0},
	'vi':  {'I': 0,      'ii': 0.8572, 'iii': 0,     'IV': 0,      'V': 0.1428, 'vi': 0,      'vii': 0},
	'vii': {'I': 0.8572, 'ii': 0,      'iii': 0,     'IV': 0,      'V': 0.1428, 'vi': 0,      'vii': 0}
}

majEmissionProbs = {
	'I':   {0: 0.278, 1: 0,     2: 0,     3: 0,     4: 0.278, 5: 0,     6: 0,     7: 0.278, 8: 0,     9: 0,     10: 0,     11: 0.166},
	'ii':  {0: 0,     1: 0.166, 2: 0.278, 3: 0,     4: 0,     5: 0,     6: 0.278, 7: 0,     8: 0,     9: 0.278, 10: 0,     11: 0},
	'iii': {0: 0,     1: 0,     2: 0,     3: 0.166, 4: 0.278, 5: 0,     6: 0,     7: 0,     8: 0.278, 9: 0,     10: 0,     11: 0.278},
	'IV':  {0: 0.278, 1: 0,     2: 0,     3: 0,     4: 0.166, 5: 0.278, 6: 0,     7: 0,     8: 0,     9: 0.278, 10: 0,     11: 0},
	'V':   {0: 0,     1: 0,     2: 0.278, 3: 0,     4: 0,     5: 0,     6: 0.166, 7: 0.278, 8: 0,     9: 0,     10: 0,     11: 0.278},
	'vi':  {0: 0,     1: 0.278, 2: 0,     3: 0,     4: 0.278, 5: 0,     6: 0,     7: 0,     8: 0.166, 9: 0.278, 10: 0,     11: 0},
	'vii': {0: 0,     1: 0,     2: 0,     3: 0.278, 4: 0,     5: 0,     6: 0.278, 7: 0,     8: 0,     9: 0,     10: 0.166, 11: 0.278}
}

bars = c2[0].tracks[0].bars
firstBar = bars[0].get_note_names()

Algo.algorithm(notesInt, statesMaj, startProb, majTransitionProbs, majEmissionProbs)


# minTransitionProbs = {
# 	'i': {'i': , 'ii': , 'III': , 'iv': , 'V': , 'VI': , 'VII': },
# 	'ii': {'i': , 'ii': , 'III': , 'iv': , 'V': , 'VI': , 'VII': },
# 	'III': {'i': , 'ii': , 'III': , 'iv': , 'V': , 'VI': , 'VII': },
# 	'iv': {'i': , 'ii': , 'III': , 'iv': , 'V': , 'VI': , 'VII': },
# 	'V': {'i': , 'ii': , 'III': , 'iv': , 'V': , 'VI': , 'VII': },
# 	'VI': {'i': , 'ii': , 'III': , 'iv': , 'V': , 'VI': , 'VII': },
# 	'VII': {'i': , 'ii': , 'III': , 'iv': , 'V': , 'VI': , 'VII': }
# }


# minEmissionProbs = {
# 	'i': {1: , 2: , 3: , 4: , 5: , 6: , 7: , 8: , 9: , 10: ,11: , 12: },
# 	'ii': {1: , 2: , 3: , 4: , 5: , 6: , 7: , 8: , 9: , 10: ,11: , 12: },
# 	'III': {1: , 2: , 3: , 4: , 5: , 6: , 7: , 8: , 9: , 10: ,11: , 12: },
# 	'iv': {1: , 2: , 3: , 4: , 5: , 6: , 7: , 8: , 9: , 10: ,11: , 12: },
# 	'V': {1: , 2: , 3: , 4: , 5: , 6: , 7: , 8: , 9: , 10: ,11: , 12: },
# 	'VI': {1: , 2: , 3: , 4: , 5: , 6: , 7: , 8: , 9: , 10: ,11: , 12: },
# 	'VII': {1: , 2: , 3: , 4: , 5: , 6: , 7: , 8: , 9: , 10: ,11: , 12: }
# }


### PARA CADA COMPASSO, ANALISAR NOTAS PARA DEFINIR A AFINIDADE COM CADA UM DOS 7 ACORDES DO CAMPO HARMONICO. ###

###	DEPOIS DECIDIR PARA QUAL ACORDE IR, LEVANDO EM CONTA O ACORDE ANTERIOR (CADEIA DE MARKOV) ###


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
