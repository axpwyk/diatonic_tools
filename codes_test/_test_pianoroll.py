from midi import *

sheet, ticks_per_beat, _ = midi2sheet(r'../midi/rolling_girl_uta.mid')
pr = Pianoroll(sheet, ticks_per_beat)
pr.set_default_time_signature()
pr.draw(tick_interval=(480*20, 480*120), nn_interval=(60, 80), channel=0)
pr.show_meta()
