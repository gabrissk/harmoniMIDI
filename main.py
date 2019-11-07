import mingus.core.chords as Chords
import mingus.core.notes as Notes
import mingus.core.intervals as intervals
import mingus.core.scales as scales
import mingus.core.value as value
import mingus.core.progressions as progressions
import mingus.core.keys as keys

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
import harmonizer as Harmonizer
import music21
import midiToAudio
import sys, os
from Tkinter import *
import Tkinter as tk

def main(file, exp, sheet):

	c2 = MidiFileIn.MIDI_to_Composition(file)

	out_dir = 'out/'

	tra = Track()
	notes = list()
	bars = []
	for x in c2:
		if(x.__class__.__name__ == "Composition"):
			for track in x.tracks:
				i = 0;
				for bar in track.bars:
					notesB = []
					if len(bar.get_note_names()) == 0:
						bar.empty()
						bar.place_rest(1)
						tra + bar
						notesB.append(None)
						bars.append(notesB)
						i = i +1
						continue
					tra + bar
					for y in bar:
						if(len(NoteContainer(y[-1]).get_note_names()) > 0):
							notes.append(NoteContainer(y[-1]).get_note_names()[0])
							notesB.append((y[2][0].name, y[2][0].octave))
					bars.append(notesB)
					i = i +1

	bars = bars[:-1]
	tra.bars = tra.bars[:-1]
	bpm = c2[1]

	### DESCOBRIR TONALIDADE MELODIA -> 1o GRAU ###
	key_and_mode = scales.determine(notes)[0]
	if key_and_mode != None:
		key = key_and_mode.split(" ")[0]
		mode = key_and_mode.split(" ")[1]

	score = music21.converter.parse(file)
	parse = score.analyze('key')
	keym = parse.tonic.name
	modem = parse.mode

	flag = False
	if mode == ('harmonic' or 'minor'):
		key = keys.relative_major(key.lower())
		mode = 'major'
		flag = True
	elif mode != modem:
		Flag = True


	scores = {
		'I':   {0: 0.5,   1: -0.2,  2: 0,     3: 0,     4: 0.35,  5: 0,     6: 0,     7: 0.35,  8: 0,     9: 0,     10: 0,     11: 0.1},
		'ii':  {0: 0,     1: 0.1,   2: 0.5,   3: -0.2,  4: 0,     5: 0,     6: 0.35,  7: 0,     8: 0,     9: 0.35,  10: 0,     11: 0},
		'iii': {0: 0,     1: 0,     2: 0,     3: 0.1,   4: 0.5,   5: -0.2,  6: 0,     7: 0,     8: 0.35,  9: 0,     10: 0,     11: 0.35},
		'IV':  {0: 0.35,  1: 0,     2: 0,     3: 0,     4: 0.1,   5: 0.5,   6: -0.2,  7: 0,     8: 0,     9: 0.35,  10: 0,     11: 0},
		'V':   {0: 0,     1: 0,     2: 0.35,  3: 0,     4: 0,     5: 0,     6: 0.1,   7: 0.5,   8: -0.2,  9: 0,     10: 0,     11: 0.35},
		'vi':  {0: 0,     1: 0.35,  2: 0,     3: 0,     4: 0.35,  5: 0,     6: 0,     7: 0,     8: 0.1,   9: 0.5,   10: -0.2,  11: 0},
		'vii': {0: -0.2,  1: 0,     2: 0,     3: 0.35,  4: 0,     5: 0,     6: 0.35,  7: 0,     8: 0,     9: 0,     10: 0.11,  11: 0.5}
	}

	scoresMin = {
		'I':   {0: 0,     1: 0.35,  2: 0,     3: 0,     4: 0.35,  5: 0,     6: 0,     7: 0,     8: 0.1,   9: 0.5,   10: -0.2,  11: 0},
		'ii':  {0: -0.2,  1: 0,     2: 0,     3: 0.35,  4: 0,     5: 0,     6: 0.35,  7: 0,     8: 0,     9: 0,     10: 0.11,  11: 0.5},
		'iii': {0: 0.5,   1: -0.2,  2: 0,     3: 0,     4: 0.35,  5: 0,     6: 0,     7: 0.35,  8: 0,     9: 0,     10: 0,     11: 0.1},
		'IV':  {0: 0,     1: 0.1,   2: 0.5,   3: -0.2,  4: 0,     5: 0,     6: 0.35,  7: 0,     8: 0,     9: 0.35,  10: 0,     11: 0},
		'V':   {0: 0,     1: 0,     2: 0,     3: 0.1,   4: 0.5,   5: -0.2,  6: 0,     7: 0,     8: 0.35,  9: 0,     10: 0,     11: 0.35},
		'vi':  {0: 0.35,  1: 0,     2: 0,     3: 0,     4: 0.1,   5: 0.5,   6: -0.2,  7: 0,     8: 0,     9: 0.35,  10: 0,     11: 0},
		'vii': {0: 0,     1: 0,     2: 0.35,  3: 0,     4: 0,     5: 0,     6: 0.1,   7: 0.5,   8: -0.2,  9: 0,     10: 0,     11: 0.35}
	}

	if flag:
		scores = scoresMin

	modeToPass = 'minor' if flag else 'major'
	chords = Harmonizer.harmonize(bars, key, scores, (4,4), modeToPass)
	# print chords
	Harmonizer.reharmonize(chords, scores, bars, key, modeToPass)
	# print chords
	chords = progressions.to_chords(chords, key)

	if exp: 
		Harmonizer.export(tra, chords, key, (4,4), bpm, file)

	# if len(sys.argv) > 3:
	# 	title = sys.argv[3]
	# if title == None: title = "Musical piece"
	# if len(sys.argv) > 4:
	# 	author = sys.argv[4]
	# if author == None: author = "Usuario"

	if sheet:
		Harmonizer.to_Sheet(bars, chords, tra, key, mode, file, out_dir, "Musica", "Eu")


root= tk.Tk()
root.title('HarmoniMIDI')
root.resizable(False, False)

canvas1 = tk.Canvas(root, width = 400, height = 330,  relief = 'raised')
canvas1.pack()

label1 = tk.Label(root, text='HarmoniMIDI')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Digite o caminho do arquivo .midi: (ex: home/music/in.midi)')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 70, window=label2)
entry1 = tk.Entry (root, width=35) 
canvas1.create_window(200, 100, window=entry1)

label3 = tk.Label(root, text='Deseja exportar o resultado para WAV e/ou gerar partitura? Selecione as opcoes:', wraplength=300)
label3.config(font=('helvetica', 10))
canvas1.create_window(200, 150, window=label3)

CheckVar1 = IntVar()
CheckVar2 = IntVar()
c1 = tk.Checkbutton(root, text = "Exportar WAV  ", variable = CheckVar1)#, \
canvas1.create_window(200, 190, window=c1)                 
c2 = tk.Checkbutton(root, text = "Gerar partitura", variable = CheckVar2)#, \
canvas1.create_window(200, 210, window=c2) 

button1 = tk.Button(text='HarmoniMIDI-me!', command=lambda: validate(), bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 260, window=button1)

labelText = StringVar()
label4 = tk.Label(root, textvariable = labelText)
canvas1.create_window(200, 290, window=label4) 

def updt(txt):
	labelText.set(txt)

def validate():
	if entry1.get() == (None or '') or entry1.get().strip == '':
		updt('Caminho do arquivo .midi nao informado. Tente novamente.')
	elif not os.path.exists(entry1.get()):
		updt('Arquivo .midi nao encontrado. Tente novamente.')
	else:
		fileN = entry1.get()
		init(fileN)


def init(fileN):
	canvas1.destroy()
	exp = True if CheckVar1.get() == 1 else False
	sheet = True if CheckVar2.get() == 1 else False
	main(fileN, exp, sheet)


root.mainloop()

