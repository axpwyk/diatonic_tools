from theories import *
import os

chord_types = ['M7+5sus4', 'M7sus4', 'sus4', 'augM7', 'aug7', 'aug', 'M7', '7', '6', '', 'M7-5', '7-5', '-5', 'm7+5', 'mM7', 'm7', 'm6', 'm', 'mM7-5', 'm7-5', 'dim7', 'dim', '7sus2', '7-5sus2', '6-5sus2', 'sus2', '-5sus2']

for ct in chord_types:
    ch = Chord('F' + ct)
    print(ch, '\t', ch.get_name())
