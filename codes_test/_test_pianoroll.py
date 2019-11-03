from midi import *

sheet, ticks_per_beat, _ = midi2sheet(r'../midi/drum_funk.mid')
pr = Pianoroll(sheet, ticks_per_beat)
pr.set_default_ts(4, 4)
ch = 0
pr.draw(whdpi=(72, 8, 36), nn_interval=pr.get_nn_range(ch), tick_interval=(0, 16*1920), splits_per_beat=4, channel=ch, is_drum=True)
# pr.draw(tick_interval=(0, pr.get_max_tick()), nn_interval=(0, 10), splits_per_beat=4, channel=0)
