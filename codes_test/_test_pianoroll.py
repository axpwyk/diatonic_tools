from midi import *

sheet, ticks_per_beat, _ = midi2sheet(r'../midi/test.mid')
pr = Pianoroll(sheet, ticks_per_beat)
pr.draw(tick_interval=(480*20+1, 480*46), nn_interval=(48, 72), channel=0)
