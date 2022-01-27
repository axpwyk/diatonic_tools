import re
import os
import unicodedata
import matplotlib.pyplot as plt


# 累积求和
def cumsum(lst): return [sum(lst[:k]) for k in range(1, len(lst) + 1)]
def cumsum_0(lst): cs = cumsum(lst); return [x - cs[0] for x in cs]

# 全半角判定
def is_fw(character): return True if unicodedata.east_asian_width(character) in ['F', 'W'] else False


# 参数设定
filename = 'chords_with_lyrics/shiro_no_kisetsu.txt'
export_ext = 'svg'
sans_serif = {
    'svg': 'Yu Gothic',
    'pdf': 'FOT-TsukuARdGothic Std'
}.get(export_ext, 'Consolas-with-Yahei')
fontsize = 8
scale = 4
scale_x = 1

# matplotlib 默认值设定
plt.style.use('seaborn-pastel')
plt.rc('pdf', **{'fonttype': 42})
plt.rc('ps', **{'fonttype': 42})
plt.rc('svg', **{'fonttype': 'none'})
plt.rc('font', **{'sans-serif': sans_serif})
plt.rc('axes', **{'unicode_minus': False})

# 读取格式化歌词文本
with open(f'{filename}', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    lines[i] = line.strip()

# 求取 每行的 y 的坐标值，以及和弦的字符位置
ys_delta = []
chords_pos = []
chords_text = []
for i, line in enumerate(lines):
    # 查找每一行的和弦数目
    find_all = re.findall(r'<[\w(), /#-.]+>', line)
    n_chords = len(find_all)
    # 如果有和弦，就使用 1.5 倍行距，否则单倍行距
    y_delta = -1.5 * scale if n_chords > 0 else -1 * scale
    ys_delta.append(y_delta)
    # 从文本中删除和弦，并记录其位置
    x_chord = []
    chord = []
    for _ in range(n_chords):
        search_obj = re.search(r'<[\w(), /#-.]+>', line)
        chord_start = search_obj.start()
        chord_end = search_obj.end()
        x_chord.append(chord_start - 1)
        chord.append(search_obj.group())
        line = line[:chord_start] + line[chord_end:]
    lines[i] = line
    chords_pos.append(x_chord)
    chords_text.append(chord)
ys = cumsum_0(ys_delta)

# 求取 每行每个文字的 x 坐标值（分全半角设置不同宽度）
xs = [cumsum_0([is_fw(c) * scale * scale_x + (not is_fw(c)) / 2 * scale * scale_x for c in line]) for line in lines]

# 定义域和值域
xlim = max(sum(xs, start=[]))
ylim = -min(ys)

# 创建新图形并控制格式
plt.gca().set_xlim(0 - 1 / 2 * scale, xlim + 1 / 2 * scale)
plt.gca().set_ylim(-ylim - 1 / 2 * scale, 0 + 1 / 2 * scale)
plt.gca().autoscale_view()
plt.gca().set_aspect('equal')
plt.gca().margins(0, 0)
plt.gca().set_axis_off()

# 绘制文字
fontcolor = 'slateblue'
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        plt.annotate(c, (xs[i][j], ys[i]), ha='center', va='center', fontsize=fontsize)
    for chord_text, chord_pos in zip(chords_text[i], chords_pos[i]):
        patch = {
            'rect': plt.Rectangle((xs[i][chord_pos], ys[i] - 2 / 3 * scale), scale, scale, 45, ec='none', fc=fontcolor, alpha=0.25, capstyle='round'),
            'circ': plt.Circle((xs[i][chord_pos], ys[i]), 1 / 2.1 * scale, ec='none', fc=fontcolor, alpha=0.25)
        }.get('circ', plt.Circle((0, 0), 0))
        plt.gca().add_patch(patch)
        plt.annotate(chord_text[1:-1], (xs[i][chord_pos], ys[i] + 2 / 3 * scale), ha='center', va='center', fontsize=fontsize / 2, color=fontcolor)

# 输出图像
plt.gcf().set_dpi(144)
plt.gcf().set_figheight(72)
plt.savefig(f'{os.path.splitext(filename)[0]}.{export_ext}', bbox_inches='tight', pad_inches=0.1)
plt.close()
