import os; os.chdir('../..')
from midi import *
from pathlib import Path
import numpy as np

NAMED_STR_LST = ['C', 'd', 'D', 'e', 'E', 'F', 'g', 'G', 'a', 'A', 'b', 'B']

sheet, ticks_per_beat, _ = midi2sheet(Path(r'midis/vocal_1.mid'))

hits_per_bar = 16
bars_per_line = 4
hits_per_beat = hits_per_bar / 4
shortening_factor = 2

# 读取 MIDI 音符列表
lrcs = []
t1s = []
t2s = []
for msglist in sheet:
    for msg in msglist:
        if msg['type'] == 'note':
            lrcs.append(NAMED_STR_LST[msg.get('note', 'x') % 12])
            t1s.append(int(msg['time1'] / ticks_per_beat * hits_per_beat))
            t2s.append(int(msg['time2'] / ticks_per_beat * hits_per_beat))

# 处理信息
# lrcs = 'x' * len(lrcs)
# lrcs = lrcs[-14:]
# t1s = t1s[-14:]
# t2s = t2s[-14:]
t1s = [t1 % hits_per_bar + (t1 // hits_per_bar - t1s[0] // hits_per_bar) * hits_per_bar for t1 in t1s]

# 常量
n_bars = (max(t1s) + max(t2s)) // hits_per_bar + 1
n_lines = n_bars // bars_per_line + 1

# 设定输出文本
strs = [' '] * n_bars * hits_per_bar
for lrc, t1, t2 in zip(lrcs, t1s, t2s):
    strs[t1] = lrc
    for v in range(1, t2):
        if v % shortening_factor == 0:
            strs[t1+v] = '-'

print(strs)

# 输出
broken = False
for l in range(n_lines):
    # print(l, end='\t')
    for b in range(bars_per_line):
        for h in range(hits_per_bar):
            try:
                print(strs[l * bars_per_line * hits_per_bar + b * hits_per_bar + h], end='')
            except:
                broken = True
                break
        if not broken:
            print(' | ', end='')
    print()
