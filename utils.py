import math
import numpy as np
import matplotlib.pyplot as plt
import colorsys
import re
from consts import *


# 弃用函数
def note_number_to_frets(note_number, low=0, high=25):
    string_starts = [16, 21, 26, 31, 35, 40]
    return [(i, j) for i in range(low, high) for j in range(0, 6) if string_starts[j]+i == note_number]


def triple_to_frets(triple, low=0, high=25):
    string_starts = [16, 21, 26, 31, 35, 40]
    if triple[2] < 0:
        return [(i, j) for i in range(low, high) for j in range(0, 6) if (string_starts[j]+i-triple[0]-triple[1])%12 == 0]
    else:
        return [(i, j) for i in range(low, high) for j in range(0, 6) if string_starts[j]+i == triple_to_note_number(triple)]


def triple_to_frets_with_group(triple, low=0, high=25):
    # 返回一个三元组列表 [(品数0-24，弦数0-5，音组数1-?), ...]
    string_starts = [16, 21, 26, 31, 35, 40]
    if triple[2] < 0:
        return [(i, j, (string_starts[j] + i) // 12) for i in range(low, high) for j in range(0, 6)
                if (string_starts[j] + i - triple[0] - triple[1]) % 12 == 0]
    else:
        return [(i, j, (string_starts[j] + i) // 12) for i in range(low, high) for j in range(0, 6)
                if string_starts[j] + i == triple_to_note_number(triple)]


def draw_guitar(triples, hue=0.0, low=-1, high=24):
    # 旧版本，新版本见 Guitar 类方法 Guitar.draw_guitar(hue, low, high)
    t = math.pow(1/2, 1/12)
    w_over_h = 610 / 44
    h = 5
    w = h * w_over_h
    # 弦绘图位置（y）
    strings = [h/5*k for k in range(6)]
    # 品柱绘图位置（x）
    frets = [w-w*math.pow(t, k) for k in range(25)]
    # -1 品绘图位置（x）
    frets = [-1.0] + frets
    # 品柱间距（Δx）
    fret_widths = [frets[i+1]-frets[i] for i in range(len(frets)-1)]
    # 手指位置（x+Δx/2）
    finger_pos = [(frets[i+1]+frets[i])/2 for i in range(len(frets)-1)]
    # fig 的大小（同 ax）
    height = h + 1.2
    width = frets[high+1] - frets[low+1] + 0.2

    # 判断是否存在已绘制吉他图形，存在的话则在原图的基础上添加新圆点
    if not plt.fignum_exists(1):
        plt.figure(figsize=(width, height), dpi=200, frameon=False)
        ax = plt.gca(aspect='equal')
        ax.set_xticks([]), ax.set_yticks([])
        ax.set_frame_on(False)
        ax.set_xlim([frets[low+1]-0.1, frets[high+1]+0.1])
        ax.set_ylim([-0.6, h+0.6])

        # 绘制品柱
        # 头部加粗
        ax.plot([-1, -1], [0, h], color='k', linewidth=10, zorder=4)
        # 尾部加粗
        ax.plot([w, w], [0, h], color='k', linewidth=5, zorder=4)
        # 到 high+2 而不是 high+1 是为了把最后一个品柱补上
        for i, k in zip(frets[low+1:high+2], range(len(frets[low+1:high+2]))):
            ax.plot([i, i], [0, h], color='k', linewidth=3, zorder=2)
            ax.text(i, -0.5, '{}'.format(k+low), horizontalalignment='center', verticalalignment='center', color='b', fontsize=20)

        # 绘制弦
        for j, k in zip(strings, range(len(strings))):
            ax.plot([-1, w], [j, j], color='grey', linewidth=3, zorder=3)
            ax.text(frets[low+1]-0.5, j, '{}'.format(6-k), horizontalalignment='center', verticalalignment='center', color='b', fontsize=20)

        # 绘制格子
        r1 = plt.Rectangle((finger_pos[3], 2.5), fret_widths[3]/2, h/2, fill=True, color=[0.8, 0.8, 0.8], zorder=1)
        r2 = plt.Rectangle((finger_pos[5], 2.5), fret_widths[5]/2, h/2, fill=True, color=[0.8, 0.8, 0.8], zorder=1)
        r3 = plt.Rectangle((finger_pos[7], 2.5), fret_widths[7]/2, h/2, fill=True, color=[0.8, 0.8, 0.8], zorder=1)
        r4 = plt.Rectangle((finger_pos[9], 2.5), fret_widths[9]/2, h/2, fill=True, color=[0.8, 0.8, 0.8], zorder=1)
        r5 = plt.Rectangle((finger_pos[12], 0), fret_widths[12]/2, h, fill=True, color=[0.8, 0.8, 0.8], zorder=1)
        r6 = plt.Rectangle((finger_pos[15], 2.5), fret_widths[15]/2, h/2, fill=True, color=[0.8, 0.8, 0.8], zorder=1)
        r7 = plt.Rectangle((finger_pos[17], 2.5), fret_widths[17]/2, h/2, fill=True, color=[0.8, 0.8, 0.8], zorder=1)
        r8 = plt.Rectangle((finger_pos[19], 2.5), fret_widths[19]/2, h/2, fill=True, color=[0.8, 0.8, 0.8], zorder=1)
        r9 = plt.Rectangle((finger_pos[21], 2.5), fret_widths[21]/2, h/2, fill=True, color=[0.8, 0.8, 0.8], zorder=1)
        ax.add_patch(r1), ax.add_patch(r2), ax.add_patch(r3), ax.add_patch(r4)
        ax.add_patch(r5)
        ax.add_patch(r6), ax.add_patch(r7), ax.add_patch(r8), ax.add_patch(r9)

    # 绘制圆点
    def _plot_note(fret, string, text=None, color='r'):
        circ = plt.Circle((finger_pos[fret], strings[string]), color=color, radius=0.4, zorder=5)
        ax.add_patch(circ)
        ax.text(finger_pos[fret], strings[string], text, horizontalalignment='center', verticalalignment='center', color='w', fontsize=16, zorder=6)
    ax = plt.gca()
    for triple, k in zip(triples, range(len(triples))):
        fret_triples = triple_to_frets_with_group(triple, low+1, high+1)
        for pair, c in zip(fret_triples, range(len(fret_triples))):
            _plot_note(pair[0], pair[1], text='{}{}'.format(triple_to_note_name(triple), pair[2]),
                       color=color_gradient(hue, k/len(triples)))


# 用于解析音名、和弦名和调性名称的正则表达式
def note_name_parser(note_name):
    s = note_name
    search_obj = re.search(
        '(?P<name>[ABCDEFG])(?P<acci>[b#]*)(?P<group>-?\d*)', s)
    return search_obj.groupdict()


def chord_name_parser(chord_name):
    s = chord_name
    search_obj = re.search(
        '(?P<bass_name>[ABCDEFG][b#]*) *(?P<chord_type>\w*)(?P<additional>\([^ac-z]*\))*/?(?P<root_name>[ABCDEFG][b#]*)*', s)
    return search_obj.groupdict()


def tonality_parser(tonality):
    s = tonality
    search_obj = re.search('(?P<key_name>[ABCDEFG][b#]*) ?(?P<mode_name>\w+)', s)
    return search_obj.groupdict()


# 常用转换函数
def note_name_to_triple(note_name):
    """ 把音符名称（note_name）转换为三元组（triple）

    输入：
        note_name   音符名称 | python strings | 'Eb3', 'F#', 'G4', etc.

    输出：
        triple      三元组 | python list | [name, acci, group]

    备注：
        name        音名 | integer | range {0, 1, 2, 3, ..., 11}
        acci        变化 | integer | range {-1, 0, 1}
        group       音组 | integer | range {..., -1, 0, 1, 2, ...}
    """
    par = note_name_parser(note_name)
    name = NOTES.index(par['name'])

    acci = 0
    acci += par['acci'].count('#')
    acci -= par['acci'].count('b')

    if par['group']:
        group = eval(par['group'])
    else:
        group = -1
    return [name, acci, group]


def triple_to_note_name(triple):
    note_name = ''
    note_name += NOTES[triple[0]%12]

    if triple[1] > 0:
        note_name += '#'*triple[1]
    elif triple[1] < 0:
        note_name += 'b'*(-triple[1])
    else:
        pass

    if triple[2] >= 0:
        note_name += '{}'.format(triple[2])
    return note_name


def triples_to_note_names(triples):
    return [triple_to_note_name(t) for t in triples]


def triple_to_note_number(triple):
    # note_number represents for midi note number
    return triple[0] + triple[1] + triple[2]*12


def triples_to_note_numbers(triples):
    return [triple_to_note_number(t) for t in triples]


def chord_name_to_triples(chord_name='Cmaj7'):
    par = chord_name_parser(chord_name)
    bass_name = par['bass_name']
    chord_type = par['chord_type']
    scale_type = CHORD_TYPE_SCALES[chord_type]
    choose_list = CHORD_TYPE_CLST[chord_type]
    s = Tonality(bass_name+' '+scale_type)
    return s.chord(choose_list)[0]


# 音乐理论函数
def triple_add5(triple):
    # natural_attractor = [0, 2, 4, 5, 7, 9, 11]
    # diatonic 的特性是升号只在 7 加五度时出现在 4 上成为 #4
    target = triple[0] + 7
    if triple[0] == 11:
        return [target % 12 - 1, triple[1] + 1, triple[2] + target//12]
    else:
        return [target % 12, triple[1], triple[2] + target // 12]


def triple_sub5(triple):
    # natural_attractor = [0, 2, 4, 5, 7, 9, 11]
    # diatonic 的特性是降号只在 4 减五度时出现在 7 上成为 b7
    target = triple[0] - 7
    if triple[0] == 5:
        return [target % 12 + 1, triple[1] - 1, triple[2] - target // 12]
    else:
        return [target % 12, triple[1], triple[2] - target // 12]


class Tonality(object):
    def __init__(self, tonality='C Ionian'):
        par = tonality_parser(tonality)
        self.key = note_name_to_triple(par['key_name'])
        self.mode = MODES.index(par['mode_name'])
        self._build_scale()

    def _build_scale(self):
        if self.mode < 7:
            # 生成中心音，并按照 self.mode 进行向下和向上的五度相生
            self.scale = [self.key]
            for _ in range(self.mode):
                self.scale.insert(0, triple_sub5(self.scale[0]))
            for _ in range(6 - self.mode):
                self.scale.append(triple_add5(self.scale[-1]))
            # 音组归为 -1，排序使得主音在列表首位
            self.scale = [[s[0], s[1], -1] for s in self.scale]
            self.scale.sort()
            key7 = [0, 2, 4, 5, 7, 9, 11].index(self.key[0])
            self.scale = self.scale[key7:] + self.scale[:key7]

        else:
            # 以 Aeolian 为基础调式，后面添加临时升降号变为和声/旋律小调
            base_mode = 4
            self.scale = [self.key]
            for _ in range(base_mode):
                self.scale.insert(0, triple_sub5(self.scale[0]))
            for _ in range(6 - base_mode):
                self.scale.append(triple_add5(self.scale[-1]))
            # 音组归为 -1，排序使得主音在列表首位
            self.scale = [[s[0], s[1], -1] for s in self.scale]
            self.scale.sort()
            key7 = [0, 2, 4, 5, 7, 9, 11].index(self.key[0])
            self.scale = self.scale[key7:] + self.scale[:key7]
            # 添加临时升降号
            if self.mode == 7:
                self.scale[-1][1] += 1
            elif self.mode == 8:
                self.scale[-1][1] += 1
                self.scale[-2][1] += 1

    def add_sharp(self):
        pos = (self.mode * 3) % 7
        self.scale[pos][1] += 1
        self.key = self.scale[0]
        self.mode = (self.mode - 1) % 7

    def add_flat(self):
        pos = (3 + self.mode * 3) % 7
        self.scale[pos][1] -= 1
        self.key = self.scale[0]
        self.mode = (self.mode + 1) % 7

    def tonality(self):
        return triple_to_note_name(self.key) + ' ' + MODES[self.mode]

    def chord(self, choose_list):
        # root 取值为 {0, 1, 2, 3, 4, 5, 6}，表示第几个音级作为根音
        chord = [self.scale[i] for i in choose_list]
        # 把 note number 找到（消去升降号）
        chord_nn = [t[0]+t[1] for t in chord]
        # 求差，推断和弦结构
        diff = [(chord_nn[i+1]-chord_nn[i]) % 12 for i in range(len(chord_nn)-1)]
        diff_s = ''
        for d in diff:
            diff_s += str(d)
        # 返回和弦 triples 和从 CHORDS 中得到的和弦结构名
        return chord, CHORDS[diff_s]


# 绘图函数
def color_gradient(hue, t):
    return colorsys.hsv_to_rgb(hue, t, t)


# 乐器建模
class Guitar(object):
    def __init__(self):
        # 空弦音高
        self._open_strings = np.array([16, 21, 26, 31, 35, 40])
        # 指板各品音高
        self._fretboard = np.array([self._open_strings + i for i in range(0, 25)])
        self._fretboard = np.expand_dims(self._fretboard, -1)
        self._fretboard = np.tile(self._fretboard, (1, 1, 2))
        self._fretboard[:, :, 0] %= 12
        self._fretboard[:, :, 1] //= 12

        self._pressed_initialize()

    def _pressed_initialize(self):
        # pressed strings
        self.pressed = np.zeros((25, 6), np.bool)
        self.accidentals = np.zeros((25, 6), np.int)

    def draw_guitar(self, hue=0.0, low=-1, high=24, pos_offset=0, radius_offset=0):
        t = np.power(1/2, 1/12)
        w_over_h = 610 / 44
        h = 5
        w = h * w_over_h
        # 弦绘图位置（y）
        strings = [h/5*k for k in range(6)]
        # 品柱绘图位置（x）
        frets = [w-w*np.power(t, k) for k in range(25)]
        # -1 品绘图位置（x）
        frets = [-1.0] + frets
        # 品柱间距（Δx）
        fret_widths = [frets[i+1]-frets[i] for i in range(len(frets)-1)]
        # 手指位置（x+Δx/2）
        finger_pos = [(frets[i+1]+frets[i])/2 for i in range(len(frets)-1)]
        # fig 的大小（同 ax）
        height = h + 1.2
        width = frets[high+1] - frets[low+1] + 0.2

        # 判断是否存在已绘制吉他图形，存在的话则在原图的基础上添加新圆点
        if not plt.fignum_exists(1):
            fig = plt.figure(figsize=(width, height), dpi=200, frameon=False)
            # ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], aspect='equal')
            ax = plt.gca(aspect='equal')
            ax.set_xticks([]), ax.set_yticks([])
            ax.set_frame_on(False)
            ax.set_xlim([frets[low+1]-0.1, frets[high+1]+0.1])
            ax.set_ylim([-0.6, h+0.6])

            # 绘制品柱
            # 头部加粗
            ax.plot([-1, -1], [0, h], color='k', linewidth=10, zorder=-1.6)
            # 尾部加粗
            ax.plot([w, w], [0, h], color='k', linewidth=5, zorder=-1.6)
            # 到 high+2 而不是 high+1 是为了把最后一个品柱补上
            for i, k in zip(frets[low+1:high+2], range(len(frets[low+1:high+2]))):
                ax.plot([i, i], [0, h], color='k', linewidth=3, zorder=-1.8)
                ax.text(i, -0.5, '{}'.format(k+low), horizontalalignment='center', verticalalignment='center', color='b', fontsize=20)

            # 绘制弦
            for j, k in zip(strings, range(len(strings))):
                ax.plot([-1, w], [j, j], color='grey', linewidth=3, zorder=-1.7)
                ax.text(frets[low+1]-0.5, j, '{}'.format(6-k), horizontalalignment='center', verticalalignment='center', color='b', fontsize=20)

            # 绘制把位格子
            r1 = plt.Rectangle((finger_pos[3], 2.5), fret_widths[3]/2, h/2, fill=True, color=[0.8, 0.8, 0.8], zorder=-1.9)
            r2 = plt.Rectangle((finger_pos[5], 2.5), fret_widths[5]/2, h/2, fill=True, color=[0.8, 0.8, 0.8], zorder=-1.9)
            r3 = plt.Rectangle((finger_pos[7], 2.5), fret_widths[7]/2, h/2, fill=True, color=[0.8, 0.8, 0.8], zorder=-1.9)
            r4 = plt.Rectangle((finger_pos[9], 2.5), fret_widths[9]/2, h/2, fill=True, color=[0.8, 0.8, 0.8], zorder=-1.9)
            r5 = plt.Rectangle((finger_pos[12], 0), fret_widths[12]/2, h, fill=True, color=[0.8, 0.8, 0.8], zorder=-1.9)
            r6 = plt.Rectangle((finger_pos[15], 2.5), fret_widths[15]/2, h/2, fill=True, color=[0.8, 0.8, 0.8], zorder=-1.9)
            r7 = plt.Rectangle((finger_pos[17], 2.5), fret_widths[17]/2, h/2, fill=True, color=[0.8, 0.8, 0.8], zorder=-1.9)
            r8 = plt.Rectangle((finger_pos[19], 2.5), fret_widths[19]/2, h/2, fill=True, color=[0.8, 0.8, 0.8], zorder=-1.9)
            r9 = plt.Rectangle((finger_pos[21], 2.5), fret_widths[21]/2, h/2, fill=True, color=[0.8, 0.8, 0.8], zorder=-1.9)
            ax.add_patch(r1), ax.add_patch(r2), ax.add_patch(r3), ax.add_patch(r4)
            ax.add_patch(r5)
            ax.add_patch(r6), ax.add_patch(r7), ax.add_patch(r8), ax.add_patch(r9)

        # 绘制按弦位置圆点
        def _plot_note(fret, string, text=None, color=(1.0, 0.0, 0.0)):
            circ = plt.Circle((finger_pos[fret]+pos_offset, strings[string]), color=color, radius=0.4+radius_offset, zorder=1.1+pos_offset)
            ax.add_patch(circ)
            ax.text(finger_pos[fret]+pos_offset, strings[string], text,
                    horizontalalignment='center', verticalalignment='center', color='w', fontsize=16+10*radius_offset, zorder=1.2+pos_offset)
        ax = plt.gca()
        for i in range(low+1, high+1):
            for j in range(0, 6):
                if self.pressed[i, j]:
                    current_note = self._fretboard[i, j, 0] - self.accidentals[i, j]
                    current_accidental = self.accidentals[i, j]
                    current_group = self._fretboard[i, j, 1]
                    current_triple = [current_note, current_accidental, current_group]
                    _plot_note(i, j, triple_to_note_name(current_triple), color_gradient(hue, 0.8))

    def add_pressed_from_triples(self, triples):
        for triple in triples:
            if triple[2] < 0:
                indices = self._fretboard[:, :, 0] == (triple[0] + triple[1]) % 12
                self.pressed[indices] = True
                self.accidentals[indices] = triple[1]
            else:
                indices = np.logical_and(self._fretboard[:, :, 0] == (triple[0] + triple[1]) % 12, self._fretboard[:, :, 1] == triple[2])
                self.pressed[indices] = True
                self.accidentals[indices] = triple[1]

    def set_pressed_from_triples(self, triples):
        self._pressed_initialize()
        self.add_pressed_from_triples(triples)

    def get_triples_from_pressed(self, low=-1, high=24):
        triples = []
        for i in range(low+1, high+1):
            for j in range(0, 6):
                if self.pressed[i, j]:
                    current_note = self._fretboard[i, j, 0] - self.accidentals[i, j]
                    current_accidental = self.accidentals[i, j]
                    current_group = self._fretboard[i, j, 1]
                    current_triple = [current_note, current_accidental, current_group]
                    triples.append(current_triple)
        return triples

    def add_pressed_from_triples_u(self, triples, low=-1, high=24):
        note_numbers = []
        for triple in triples:
            note_numbers.append((triple[0]+triple[1])%12)
        # 在给定区间 [low, high] 中，逐弦从高音到低音进行搜索
        # TODO: 更加有灵性的搜索方式
        for j in range(6):
            for i in range(high+1, low+1, -1):
                if self._fretboard[i, j, 0] in note_numbers:
                    self.pressed[i, j] = True
                    self.accidentals[i, j] = triples[note_numbers.index(self._fretboard[i, j, 0])][1]
                    break

    def set_pressed_from_triples_u(self, triples, low=-1, high=24):
        self._pressed_initialize()
        self.add_pressed_from_triples_u(triples, low, high)
