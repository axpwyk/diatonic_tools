from instruments import *
from time import strftime
from pathlib import Path

# 使用和弦列表
chord_names = ['Em7(9, 11)', 'G7']
chords = [Chord(chord_name) for chord_name in chord_names]

# 显示 chords
print(chords)

# # 创建 Guitar 类并显示和弦图形
# g = Guitar()
# N = len(triples)
# step = 0.4
# offsets = np.arange(-(N/2-1/2)*step, (N/2-1/2)*step+step, step)
# for i in range(N):
#     g.set_pressed_from_triples(triples[i])
#     g.draw_guitar_v2(height=6, hue=0.01+0.075*i, low=-1, high=5, finger_offset=offsets[i], radius_offset=-1)
#
# # 输出
# chords_name_export = ''.join([chd+'-' for chd in chords_name[:-1]]+[chords_name[-1]])
# filename = f'../output/{strftime("%Y%m%d_%H%M%S")}_{chords_name_export}.svg'
# plt.savefig(Path(r'../output/guitar_test.svg'))
# plt.close()
