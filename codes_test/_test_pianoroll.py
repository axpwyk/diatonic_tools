from midi import *

sheet, ticks_per_beat, _ = midi2sheet(r'../midi/test2.mid')
pr = Pianoroll(sheet, ticks_per_beat)
pr.set_default_ts(4, 4)
ch = 0
pr.draw(whdpi=(16, 6, 36), nn_interval=pr.get_nn_range(ch), tick_interval=(2*1920, pr.max_tick), splits_per_beat=4, channel=ch, is_drum=False)
