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

import algorithm as Harmonizer

import music21

import midiToAudio

n = NoteContainer(chords.triad("C", "C"))

b = Bar(None, (4,4))
b.place_notes(NoteContainer(chords.triad("C", "C")),8)
b.place_notes(NoteContainer(chords.triad("C", "C")),8)
b.place_notes(NoteContainer(chords.triad("A", "C")),4)
b.place_notes(NoteContainer(chords.triad("F", "C")),4)
b.place_notes(NoteContainer(chords.triad("G", "C")),4)

t = Track()
t.name = "Teste"

b1 = Bar(None, (4,4))
b1.place_notes(Note("D-3"), 4)
b1.place_notes(Note("E-3"), 4)
b1.place_notes(Note("F#-3"), 4)
b1.place_notes(Note("G-3"), 4)
t + b1
b1 = Bar(None, (4,4))
b1.place_notes(Note("A-3"), 2)
b1.place_notes(Note("D-3"), 2)
t + b1
b1 = Bar(None, (4,4))
b1.place_notes(Note("B-3"), 4)
b1.place_notes(Note("G-3"), 4)
b1.place_notes(Note("D-4"), 4)
b1.place_notes(Note("B-3"), 4)
t + b1
b1 = Bar(None, (4,4))
b1.place_notes(Note("A-3"), 2)
b1.place_notes(Note("A-3"), 2)
# b1.place_rest(2)
# b1.place_rest(2)
# print b1
t + b1
b1 = Bar(None, (4,4))
b1.place_notes(Note("B-3"), 4)
b1.place_notes(Note("G-3"), 4)
b1.place_notes(Note("D-4"), 4)
b1.place_notes(Note("B-3"), 4)
t + b1
b1 = Bar(None, (4,4))
b1.place_notes(Note("A-3"), 4)
b1.place_notes(Note("F#-3"), 4)
b1.place_notes(Note("D-4"), 4)
b1.place_notes(Note("F#-3"), 4)
t + b1
b1 = Bar(None, (4,4))
b1.place_notes(Note("E-3"), 4)
b1.place_notes(Note("F#-3"), 4)
b1.place_notes(Note("G-3"), 4)
b1.place_notes(Note("C#-3"), 4)
t+b1
b1 = Bar(None, (4,4))
b1.place_notes(Note("D-3"), 2)
b1.place_notes(Note("D-3"), 2)
t+b1

MidiFileOut.write_Track("test.midi", t, 150)

# b2 = Bar(None, (4,4))
# b2.place_notes(NoteContainer(chords.triad("D", "D")), 1)
# t1 = Track()
# t1+b2
# b2 = Bar(None, (4,4))
# b2.place_notes(NoteContainer(chords.triad("E", "D")), 1)
# t1+b2
# b2 = Bar(None, (4,4))
# b2.place_notes(NoteContainer(chords.triad("G", "D")), 1)
# t1+b2
# b2 = Bar(None, (4,4))
# b2.place_notes(NoteContainer(chords.triad("D", "D")), 1)
# t1+b2
# MidiFileOut.write_Track("out.midi", t1, 150)