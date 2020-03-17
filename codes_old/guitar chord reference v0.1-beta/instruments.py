import numpy as np
import matplotlib.pyplot as plt
import colorsys as cs
from theories import *


''' instrument modelling '''


class Guitar(object):
    def __init__(self):
        # open string notes
        self._open_strings = np.array([16, 21, 26, 31, 35, 40])
        # fret notes
        self._fretboard = np.array([self._open_strings + i for i in range(0, 25)])
        self._fretboard = np.expand_dims(self._fretboard, -1)
        self._fretboard = np.tile(self._fretboard, (1, 1, 2))
        self._fretboard[:, :, 0] %= 12
        self._fretboard[:, :, 1] //= 12

        self._initialize()

    def _initialize(self):
        # pressed strings
        self.pressed = np.zeros((25, 6), np.bool)
        self.accidentals = np.zeros((25, 6), np.int)
        self.r357 = np.zeros((25, 6), np.chararray)

    def draw_guitar(self, height=5, hue=0.0, low=-1, high=24, finger_offset=0, radius_offset=0, wh_ratio=610/44):
        t = np.power(1/2, 1/12)
        h = height / 1.2
        w = h*wh_ratio
        dpi = 72
        # string positions (y)
        strings = [h/5*k for k in range(6)]
        # fret positions (x)
        frets = [w-w*np.power(t, k) for k in range(25)]
        # -1 fret position (x)
        frets = [-h/5] + frets
        # delta positions of frets (Δx)
        fret_widths = [frets[i+1]-frets[i] for i in range(len(frets)-1)]
        # finger positions (x+Δx/2)
        fingers = [(frets[i+1]+frets[i])/2 for i in range(len(frets)-1)]
        # fig size
        width = frets[high+1] - frets[low+1] + 0.2*h
        # ax size
        x_range = [frets[low+1], frets[high+1]]
        y_range = [0-0.1*h, h+0.1*h]


        if not plt.fignum_exists(1):
            plt.figure(figsize=(width, height), dpi=dpi)
            ax = plt.gca(aspect='equal')
            ax.set_frame_on(False)
            ax.set_axis_off()
            ax.margins(x=0.0, y=0.0)
            ax.set_xlim(x_range)
            ax.set_ylim(y_range)
            plt.subplots_adjust(right=1.0, left=0.0, bottom=0.0, top=1.0, wspace=0.1, hspace=0.1)


            ax.plot([frets[1], frets[1]], [0, h], color='k', linewidth=10, solid_capstyle='butt', zorder=-1.8)
            ax.plot([w, w], [0, h], color='k', linewidth=5, solid_capstyle='butt', zorder=-1.8)
            for i, k in zip(frets[low+1:high+2], range(len(frets[low+1:high+2]))):
                ax.plot([i, i], [0, h], color='k', linewidth=3, solid_capstyle='butt', zorder=-1.8)
                ax.text(i, -h/13, '{}'.format(k+low), horizontalalignment='center', verticalalignment='center', color='b', fontsize=42*h/(-radius_offset+11))


            for j, k in zip(strings, range(len(strings))):
                settings = 1
                if settings == 0:
                    ax.plot([frets[low+1], frets[high+1]], [j, j], color='grey', linewidth=3, zorder=-1.7)
                elif settings == 1:
                    ax.plot([-h/5, w], [j, j], color='grey', linewidth=3, zorder=-1.7)
                elif settings == 2:
                    ax.plot([-h/5, w], [j, j], color='grey', linewidth=3, zorder=-1.7)
                    ax.text(frets[low+1]-h/13, j, '{}'.format(6-k), horizontalalignment='center', verticalalignment='center', color='b', fontsize=42*h/(-radius_offset+11))
                else: pass


            r1 = plt.Rectangle((fingers[3], h/2), fret_widths[3]/2, h/2, facecolor=[0.8, 0.8, 0.8], zorder=-1.9)
            r2 = plt.Rectangle((fingers[5], h/2), fret_widths[5]/2, h/2, facecolor=[0.8, 0.8, 0.8], zorder=-1.9)
            r3 = plt.Rectangle((fingers[7], h/2), fret_widths[7]/2, h/2, facecolor=[0.8, 0.8, 0.8], zorder=-1.9)
            r4 = plt.Rectangle((fingers[9], h/2), fret_widths[9]/2, h/2, facecolor=[0.8, 0.8, 0.8], zorder=-1.9)
            r5 = plt.Rectangle((fingers[12], 0), fret_widths[12]/2, h, facecolor=[0.8, 0.8, 0.8], zorder=-1.9)
            r6 = plt.Rectangle((fingers[15], h/2), fret_widths[15]/2, h/2, facecolor=[0.8, 0.8, 0.8], zorder=-1.9)
            r7 = plt.Rectangle((fingers[17], h/2), fret_widths[17]/2, h/2, facecolor=[0.8, 0.8, 0.8], zorder=-1.9)
            r8 = plt.Rectangle((fingers[19], h/2), fret_widths[19]/2, h/2, facecolor=[0.8, 0.8, 0.8], zorder=-1.9)
            r9 = plt.Rectangle((fingers[21], h/2), fret_widths[21]/2, h/2, facecolor=[0.8, 0.8, 0.8], zorder=-1.9)
            ax.add_patch(r1), ax.add_patch(r2), ax.add_patch(r3), ax.add_patch(r4)
            ax.add_patch(r5)
            ax.add_patch(r6), ax.add_patch(r7), ax.add_patch(r8), ax.add_patch(r9)


        def _plot_note(fret, string, text=None, color=(1.0, 0.0, 0.0)):
            circ = plt.Circle((fingers[fret] + finger_offset*fret_widths[fret]/2, strings[string]),
                              clip_on=False, color=color, radius=h/(-radius_offset+11), zorder=10.001 + finger_offset)
            ax.add_patch(circ)
            ax.text(fingers[fret] + finger_offset*fret_widths[fret]/2, strings[string], text,
                    horizontalalignment='center', verticalalignment='center', color='w', fontsize=32*h/(-radius_offset+11), zorder=10.002 + finger_offset)
        ax = plt.gca()
        for i in range(low+1, high+1):
            for j in range(0, 6):
                if self.pressed[i, j]:
                    current_note = self._fretboard[i, j, 0] - self.accidentals[i, j]
                    current_accidental = self.accidentals[i, j]
                    current_group = self._fretboard[i, j, 1]
                    current_triple = [current_note, current_accidental, current_group]
                    _plot_note(i, j, Note().set_vector(*current_triple).__str__() + f'({self.r357[i, j]})', cs.hsv_to_rgb(hue, 0.65, 0.85))

    def add_notes(self, notes):
        for i, note in enumerate(notes.get_notes()):
            if True:
                indices = self._fretboard[:, :, 0] == (note.get_note() + note.get_accidental()) % 12
                self.pressed[indices] = True
                self.accidentals[indices] = note.get_accidental()
                self.r357[indices] = notes._r357[i]
            else:
                indices = np.logical_and(self._fretboard[:, :, 0] == (note.get_note() + note.get_accidental()) % 12, self._fretboard[:, :, 1] == note.get_group())
                self.pressed[indices] = True
                self.accidentals[indices] = note.get_accidental()
                self.r357[indices] = i

    def set_notes(self, notes):
        self._initialize()
        self.add_notes(notes)

    def get_notes(self, low=-1, high=24):
        notes = []
        for i in range(low+1, high+1):
            for j in range(0, 6):
                if self.pressed[i, j]:
                    current_note = self._fretboard[i, j, 0] - self.accidentals[i, j]
                    current_accidental = self.accidentals[i, j]
                    current_group = self._fretboard[i, j, 1]
                    current_triple = [current_note, current_accidental, current_group]
                    notes.append(Note().set_vector(*current_triple))
        return notes
