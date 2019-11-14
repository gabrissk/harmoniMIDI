from music21 import converter

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
import midiToAudio
import sys, os
from Tkinter import *
from ttk import Progressbar
import time
import threading

class HarmoniMIDI:

	def __init__(self, w, h):

		self.root= Tk()
		self.root.title('HarmoniMIDI')
		self.root.resizable(False, False)

		self.pg = Progressbar(self.root, orient=HORIZONTAL,length=100,  mode='determinate')
		self.pg['maximum'] = 230
		self.pg['value'] = 0

		self.canvas1 = Canvas(self.root, width = w, height = h,  relief = 'raised')
		self.canvas1.pack()

		self.w = []

		self.label1 = Label(self.root, text='HarmoniMIDI')
		self.label1.config(font=('helvetica', 14))
		self.canvas1.create_window(200, 25, window=self.label1)

		self.label2 = Label(self.root, text='Digite o caminho do arquivo .midi: (ex: home/music/in.midi)')
		self.label2.config(font=('helvetica', 10))
		self.canvas1.create_window(200, 70, window=self.label2)
		self.entry1 = Entry (self.root, width=35) 
		self.canvas1.create_window(200, 100, window=self.entry1)
		self.w.append(self.label2)
		self.w.append(self.entry1)

		self.label3 = Label(self.root, text='Deseja exportar o resultado para WAV e/ou gerar partitura? Selecione as opcoes:', wraplength=300)
		self.label3.config(font=('helvetica', 10))
		self.canvas1.create_window(200, 155, window=self.label3)
		self.w.append(self.label3)

		self.CheckVar1 = IntVar()
		self.CheckVar2 = IntVar()
		self.c1 = Checkbutton(self.root, text = "Exportar WAV  ", variable = self.CheckVar1)
		self.canvas1.create_window(200, 195, window=self.c1)                 
		self.c2 = Checkbutton(self.root, text = "Gerar partitura", variable = self.CheckVar2, command=lambda: self.getSheetInfo())
		self.canvas1.create_window(200, 215, window=self.c2) 
		self.w.append(self.c1)
		self.w.append(self.c2)

		self.sheetInfo = Label(self.root, text='Digite, opcionalmente, nome da obra e nome do autor:')
		self.sheetAuthor = Entry(self.root, width=22)
		self.sheetName = Entry(self.root, width=22)
		self.w.append(self.sheetInfo)
		self.w.append(self.sheetName)
		self.w.append(self.sheetAuthor)

		self.button1 = Button(text='HarmoniMIDI-me!', command=lambda: self.validate(), bg='brown', fg='white', font=('helvetica', 9, 'bold'))
		self.b = self.canvas1.create_window(200, 265, window=self.button1)
		self.w.append(self.button1)

		self.labelText = StringVar()
		self.label4 = Label(self.root, textvariable = self.labelText)
		self.canvas1.create_window(200, 125, window=self.label4) 
		self.w.append(self.label4)

		self.name = ""
		self.author = ""

		self.root.mainloop()

	def getSheetInfo(self):
		if self.CheckVar2.get() == 1:
			self.s = self.canvas1.create_window(200, 240, window=self.sheetInfo)
			self.n = self.canvas1.create_window(100, 265, window=self.sheetName)
			self.a = self.canvas1.create_window(300, 265, window=self.sheetAuthor)
			self.canvas1.delete(self.b)
			self.b = self.canvas1.create_window(200, 305, window=self.button1)
		else:
			self.canvas1.delete(self.s)
			self.canvas1.delete(self.n)
			self.canvas1.delete(self.a)
			self.b = self.canvas1.create_window(200, 265, window=self.button1)

	def updt(self, txt):
			self.labelText.set(txt)

	def validate(self):
		if self.entry1.get() == (None or '') or self.entry1.get().strip == '':
			self.updt('Caminho do arquivo .midi nao informado. Tente novamente.')
		elif not os.path.exists(self.entry1.get()):
			self.updt('Arquivo .midi nao encontrado. Tente novamente.')
		else:
			fileN = self.entry1.get()
			self.init(fileN)


	def init(self, fileN):
		self.exp = True if self.CheckVar1.get() == 1 else False
		self.sheet = True if self.CheckVar2.get() == 1 else False
		if self.sheet:
			self.name = self.sheetName.get()
			self.author = self.sheetAuthor.get()
		for wdg in self.w:
			wdg.destroy()
		main(self, fileN)

	def play(self,melody, chords, bpm, scores, bars, key,mode, modeToPass, tra, file, out_dir):
		t2 = Track()
		sh = progressions.to_chords(chords, key)	
		for i in range(0, len(sh)):
			b = Bar(None, (4,4))
			if len(chords[i][0]) > 5:
				b.place_notes(None, 1)
			else:
				b.place_notes(NoteContainer(sh[i]), 1)
			t2 + b
		fluidsynth.pan(1, 25)
		fluidsynth.pan(2, 120)
		fluidsynth.main_volume(2, 50)
		fluidsynth.play_Tracks([melody, t2], [1,2], bpm)

		# sleep(500000)

		button = Button(text='Clique para rearmonizar!', command=lambda: self.checkReharmonize(chords, scores, bars, key, mode, modeToPass, tra, bpm, file, out_dir), bg='brown', fg='white', font=('helvetica', 9, 'bold'))
		self.canvas1.create_window(200, 250, window=button)
		
	def checkReharmonize(self, chords, scores, bars, key, mode, modeToPass, tra, bpm, file, out_dir):
		process = 0
		self.pg['value'] = 0
		self.updt('')
		self.update(0)
		Harmonizer.reharmonize(chords, scores, bars, key, modeToPass)
		chords = progressions.to_chords(chords, key)
		file = "reharmonized_" + file
		if self.exp:
			Harmonizer.export(tra, chords, key, (4,4), bpm, file)
		if self.sheet:
			Harmonizer.to_Sheet(bars, chords, tra, key, mode, file, out_dir, self.name, self.author)

	def update(self, progress):
		progress += 1
		self.pg['value'] = progress
		self.root.update()
		if self.pg['value'] >= self.pg['maximum']:
			self.updt("Sucesso!")
			sleep(200000)
			return 
		sleep(10000)
		self.update(progress)


def main(hMidi, file):

	c2 = MidiFileIn.MIDI_to_Composition(file)

	out_dir = 'out'

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

	score = converter.parse(file)
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

	label1 = Label(hMidi.root, text='Harmonizando!')
	label1.config(font=('helvetica', 14))
	hMidi.canvas1.create_window(200, 100, window=label1)


	pg = Progressbar(hMidi.root, orient=HORIZONTAL,length=100,  mode='determinate')
	pg['maximum'] = 230
	pg['value'] = 0
	hMidi.pg = pg
	hMidi.canvas1.create_window(200, 140, window=pg)
	
	hMidi.updt('')
	label4 = Label(hMidi.root, textvariable = hMidi.labelText)
	hMidi.canvas1.create_window(200, 160, window=label4)

	hMidi.update(0)

	fluidsynth.init("Sounds/soundfont.sf2", "alsa")

	button1 = Button(text='Ouvir resultado', command=lambda: hMidi.play(tra, chords, bpm, scores, bars, key, mode, modeToPass, tra, file, out_dir), bg='brown', fg='white', font=('helvetica', 9, 'bold'))
	hMidi.canvas1.create_window(200, 200, window=button1)
	if hMidi.exp:
		if not os.path.exists(out_dir):
			os.makedirs(out_dir)
		Harmonizer.export(tra, progressions.to_chords(chords, key), key, (4,4), bpm, file)

	if hMidi.sheet:
		if not os.path.exists(out_dir):
			os.makedirs(out_dir)
		Harmonizer.to_Sheet(bars, progressions.to_chords(chords, key), tra, key, mode, file, out_dir, hMidi.name, hMidi.author)

def sleep(n):
	i = 0
	while i < n:
		i += 0.1

if __name__ == "__main__":
	HarmoniMIDI(400, 330)
