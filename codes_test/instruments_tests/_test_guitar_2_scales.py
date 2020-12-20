from instruments import *
from time import strftime
from pathlib import Path

# 使用音阶
scales = []
tonality = ['C Ionian', 'D Mixolydian']
for t in tonality:
    s = Mode(t)
    s.add_accidental(0)
    scales.append(s.scale)

# 显示 triples
triples = scales
print(triples)

# 创建 Guitar 类并显示和弦图形
g = Guitar()
N = len(triples)
step = 0.4
offsets = np.arange(-(N/2-1/2)*step, (N/2-1/2)*step+step, step)
for i in range(N):
    g.set_notes(triples[i])
    g.draw_guitar_v2(height=6, hue=0.05+0.10*i, low=-1, high=12, finger_offset=offsets[i], radius_offset=-6)

# 输出
chords_name_export = ''.join([t+'-' for t in tonality[:-1]]+[tonality[-1]])
filename = f'../output/{strftime("%Y%m%d_%H%M%S")}_{chords_name_export}.svg'
plt.savefig(Path(r'../output/guitar_test.svg'))
plt.close()
