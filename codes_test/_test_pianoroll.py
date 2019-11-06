from midi import *

sheet, ticks_per_beat, _ = midi2sheet(r'../midi/test2.mid')
pr = Pianoroll(sheet, ticks_per_beat)
pr.set_default_ts(4, 4)
pr.set_default_st(bpm2tempo(164))
ch = 0
pr.draw(4, 2, 36, nn_interval=pr.get_nn_range(ch), tick_interval=(0*1920, pr.max_tick), splits_per_beat=4, channel=ch, is_drum=False)
