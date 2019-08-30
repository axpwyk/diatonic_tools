import numpy as np
import matplotlib.pyplot as plt
import colorsys
from theories import *


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
        h, w = 5, 610/44*5
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
            fig = plt.figure(figsize=(width, height), dpi=50, frameon=False)
            ax = plt.gca(aspect='equal')
            ax.set_frame_on(False)
            ax.axis('off')
            ax.set_xlim([frets[low+1]-0.1, frets[high+1]+0.1])
            ax.set_ylim([-0.6, h+0.6])
            plt.subplots_adjust(right=0.97, left=0.03, bottom=0.03, top=0.97, wspace=0.1, hspace=0.1)

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