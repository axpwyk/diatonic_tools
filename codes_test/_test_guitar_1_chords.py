from instruments import *
from time import strftime
from pathlib import Path

# 使用和弦列表
chords_name = ['Cm7', 'Ab6', 'Gm7']
chords = [chord_name_to_triples(chord_name) for chord_name in chords_name]

# 使用音阶
# scales = []
# tonality = 'C Ionian'
# s = Tonality(tonality)
# scales.append(s.scale)
# s = Tonality(tonality)
# s.add_sharp()
# scales.append(s.scale)

# 显示 triples
triples = chords
print(triples)

# 创建 Guitar 类并显示和弦图形
g = Guitar()
offsets = [0.3*(i-(len(triples)-1)/2) for i in range(len(triples))]
for i in range(len(triples)):
    g.set_pressed_from_triples(triples[i])
    g.draw_guitar(i/len(triples), -1, 15, offsets[i])

# 输出
chords_name_export = ''.join([chd+'-' for chd in chords_name[:-1]]+[chords_name[-1]])
plt.savefig(Path(f'../output/{strftime("%Y%m%d_%H%M%S")}_{chords_name_export}.svg'))
plt.close()
