import numpy as np
import matplotlib.pyplot as plt
import colorsys as cs

from theories import *
from midi import *


''' ----------------------------------------------------------------------------------------- '''
''' ********************************** matplotlib settings ********************************** '''
''' ----------------------------------------------------------------------------------------- '''


# assign a style
plt.style.use('seaborn-pastel')

# assign a math font
plt.rc('mathtext', **{'fontset': 'cm'})
plt.rc('text', **{'usetex': False})

# assign a chinese-supporting font
plt.rc('font', **{'sans-serif': 'Consolas-with-Yahei', 'size': 12.0})
plt.rc('axes', **{'unicode_minus': False})


def get_figure(w, h, dpi):
    # figure settings
    fig = plt.figure(figsize=(w, h), dpi=dpi)
    fig.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=1.0, wspace=0.1, hspace=0.1)
    ax = fig.gca()
    ax.set_axis_off()
    ax.margins(x=0.0, y=0.0)
    return ax


''' ----------------------------------------------------------------------------------------- '''
''' *************************************** utilities *************************************** '''
''' ----------------------------------------------------------------------------------------- '''


def hex2oct(hex_string):
    search_obj = re.search(r'(?<=#)(?P<red>[\dabcdef]{2})(?P<green>[\dabcdef]{2})(?P<blue>[\dabcdef]{2})', hex_string)
    red = eval('0x'+search_obj['red'])
    green = eval('0x'+search_obj['green'])
    blue = eval('0x'+search_obj['blue'])
    return red/255, green/255, blue/255


def oct2hex(oct_list):
    red = oct_list[0] * 255
    green = oct_list[1] * 255
    blue = oct_list[2] * 255
    print(red, green, blue)
    digits = [str(k) for k in range(10)] + ['a', 'b', 'c', 'd', 'e', 'f']
    return '#'+f'{digits[int((red-red%16)//16)]}{digits[int(red%16)]}'+\
               f'{digits[int((green-green%16)//16)]}{digits[int(green%16)]}'+\
               f'{digits[int((blue-blue%16)//16)]}{digits[int(blue%16)]}'


def rgb_gradient(t, t_min=0, t_max=1, color1=(0.94, 0.02, 0.55), color2=(0.11, 0.78, 0.72)):
    t = (t-t_min)/(t_max-t_min)
    color1 = cs.rgb_to_yiq(*color1)
    color2 = cs.rgb_to_yiq(*color2)
    return cs.yiq_to_rgb(*[t * c2 + (1.00-t) * c1 for (c1, c2) in zip(color1, color2)])


def hsv_gradient(t, t_min=0, t_max=1, color1=(0.00, 0.80, 0.75), color2=(1.00, 0.80, 0.75)):
    t = (t-t_min)/(t_max-t_min)
    return cs.hsv_to_rgb(*[t * c2 + (1.00-t) * c1 for (c1, c2) in zip(color1, color2)])


def cst_gradient(t, t_min=0, t_max=1, color=(1.00, 0.00, 0.00)):
    return color


def gradient1(t, color1, color2):
    c1 = hex2oct(color1)
    c2 = hex2oct(color2)
    return [[(1-s/(t-1))*c1[k]+s/(t-1)*c2[k] for k in range(3)] for s in range(t)]


def gradient2(t, color1, color2):
    c1 = cs.rgb_to_yiq(*hex2oct(color1))
    c2 = cs.rgb_to_yiq(*hex2oct(color2))
    return [cs.yiq_to_rgb(*[(1-s/(t-1))*c1[k]+s/(t-1)*c2[k] for k in range(3)]) for s in range(t)]


def gradient3(t, color1, color2):
    c1 = color1
    c2 = color2
    return [[(1-s/(t-1))*c1[k]+s/(t-1)*c2[k] for k in range(3)] for s in range(t)]


# a handy length function
def length(a, b):
    return b - a


# a handy middle point function
def middle(a, b):
    return (a + b) / 2


# a handy if-in-range function
def inrange(x, a, b):
    return a <= x < b


''' ----------------------------------------------------------------------------------------- '''
''' *********************************** instrument classes ********************************** '''
''' ----------------------------------------------------------------------------------------- '''


class Guitar(object):
    def __init__(self, notes=None):
        # multiple notes on single string
        self._poly = True
        # default notes
        if notes:
            self._notes = notes
        else:
            self._notes = Chord('C').get_notes()
        # open string notes
        self._open_string_notes = np.array([16, 21, 26, 31, 35, 40])
        self._max_string = self._open_string_notes.shape[0]
        # fret notes
        self._max_fret = 25
        self._fretboard_notes = np.array([self._open_string_notes + i for i in range(0, self._max_fret)])
        # get note information
        self._get_note_information()
        # press
        self._press()

    def _get_note_information(self):
        # fix note names and br357t on fretboard
        self.fretboard_note_names = []
        self.fretboard_note_br357ts = []
        self.fretboard_note_degrees = []
        for fret in self._fretboard_notes:
            tmp_names = []
            tmp_br357ts = []
            tmp_degrees = []
            for note in fret:
                idx_bool = np.array([abs(x)%12 for x in self._notes])==note%12
                if any(idx_bool):
                    idx = np.where(np.array([abs(x)%12 for x in self._notes])==note%12)[0][0]
                    tmp_names.append(self._notes[idx].get_name(show_group=False)+f'{note//12}')
                    tmp_br357ts.append(self._notes[idx].get_message_old())
                    tmp_degrees.append(idx)
                else: tmp_names.append(''); tmp_br357ts.append(''); tmp_degrees.append(-1)
            self.fretboard_note_names.append(tmp_names)
            self.fretboard_note_br357ts.append(tmp_br357ts)
            self.fretboard_note_degrees.append(tmp_degrees)

    def _press(self):
        # pressed strings
        self.pressed = np.zeros((self._max_fret, self._max_string), np.bool)
        for note in self._notes:
            self.pressed[self._fretboard_notes % 12 == abs(note) % 12] = True

        if not self._poly:
            for k in range(self._max_string):
                string_k = self.pressed[:, k]
                idx = np.where(string_k)[0][0]+1
                self.pressed[idx:, k] = False

    def set_notes(self, notes):
        self._notes = notes
        self._get_note_information()
        self._press()
        return self

    def set_poly_on(self, bool):
        self._poly = bool
        return self

    def select(self, selection='x3201p'):
        for string in range(len(selection)):
            if selection[string] == 'p': pass
            elif selection[string] == 'x':
                self.pressed[:, string] = False
            else:
                self.pressed[:, string] = False
                self.pressed[eval('0x'+selection[string]), string] = True
        return self

    def plot1(self, fret_left=0, fret_right=4, ax=None, title=None):
        rotation = 0
        w_scale = 2
        fontsize = 20
        strings = np.arange(self._max_string)
        fret = w_scale * np.arange(0, self._max_fret)
        fingers = np.concatenate([[-1.0], fret[:-1]+fret[1:]]) / 2
        fret_interval = [fret_left, fret_right]

        # new figure
        w = fret[fret_interval[1]] - fret[fret_interval[0]] + 4
        h = strings[-1] - strings[0] + 2
        scale = 0.75
        if not ax:
            fig = plt.figure(figsize=(w*scale, h*scale), dpi=72)
            ax = plt.gca(aspect='equal')
        else:
            fig = plt.gcf()
            ax.set_aspect('equal')
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_axis_off()
        ax.margins(0.0)

        # add title
        if title:
            ax.text(0.5, 0.895, title, fontsize=fontsize*1.5, va='bottom', ha='center', transform=ax.transAxes)

        # plot position blocks
        for i in range(fret_interval[0]+1, fret_interval[1]+1):
            if i in range(12, self._max_fret, 12):
                rect = plt.Rectangle((fingers[i], strings[0]), fret[i]-fingers[i], strings[-1]-strings[0], color='gray', alpha=0.2)
                ax.add_patch(rect)
            elif i % 12 in [3, 5, 7, 9]:
                mid = (strings[-1]-strings[0])/2
                rect = plt.Rectangle((fingers[i], mid), fret[i]-fingers[i], mid, color='gray', alpha=0.2)
                ax.add_patch(rect)
            else: pass

        # plot frets
        ax.set_xlim(fret[fret_interval[0]]-1, fret[fret_interval[1]]+3)
        _ = [ax.plot((fret[i], fret[i]), (strings[0], strings[-1]), c='black', lw=2.0) for i in range(fret_interval[0], fret_interval[1]+1)]
        _ = [ax.annotate(fret[i]//w_scale, (fret[i], -0.5), rotation=rotation, fontsize=fontsize, color='blue', va='center', ha='center') for i in range(fret_interval[0], fret_interval[1]+1)[1:2]]

        # plot strings
        ax.set_ylim(strings[0]-1, strings[-1]+1)
        _ = [ax.plot((fret[fret_interval[0]], fret[fret_interval[1]]), (s, s), c='black', lw=1.0) for s in strings]

        # plot dots
        radius = 0.3
        colors = gradient1(len(self._notes), '#f6b0f0', '#f6deb0')
        for string in strings:

            sp = self.pressed[:, string]

            if any(sp):  # if there exists note on current string
                if self._poly:  # plot all notes
                    circ0 = [plt.Circle((fingers[0]+fret[fret_interval[0]], string), radius, fc='white', ec='black') for _ in range(1) if sp[0]]
                    circs = [plt.Circle((fingers[i+1], string), radius, fc='black', ec='black') for i, k in enumerate(sp[1:]) if k and fret_interval[0]<i+1<=fret_interval[1]]
                    _ = [ax.add_patch(c) for c in circ0 + circs]
                else:  # only plot top note
                    top_idx, = np.where(sp)
                    top_idx = top_idx[-1]
                    if top_idx == 0:
                        circ = plt.Circle((fingers[0]+fret[fret_interval[0]], string), radius, fc='white', ec='black')
                        ax.add_patch(circ)
                    elif fret_interval[0]<top_idx<=fret_interval[1]:
                        circ = plt.Circle((fingers[top_idx], string), radius, fc='black', ec='black')
                        ax.add_patch(circ)
                    else: pass

            else:  # if there isn't any note on current string, add a cross mark on open string position
                cross = [plt.Line2D((fingers[0]+fret[fret_interval[0]]-radius*np.sqrt(2)/2, fingers[0]+fret[fret_interval[0]]+radius*np.sqrt(2)/2),
                                    (string-radius*np.sqrt(2)/2, string+radius*np.sqrt(2)/2), c='black'),
                         plt.Line2D((fingers[0]+fret[fret_interval[0]]+radius*np.sqrt(2)/2, fingers[0]+fret[fret_interval[0]]-radius*np.sqrt(2)/2),
                                    (string-radius*np.sqrt(2)/2, string+radius*np.sqrt(2)/2), c='black')]
                ax.add_line(cross[0]); ax.add_line(cross[1])

        # add string texts (top notes)
        text_names = []
        text_br357ts = []
        text_degrees = []
        for string in strings:

            sp = self.pressed[:, string]

            top_idx, = np.where(sp)
            if sum(top_idx.shape)<=0:
                text_names.append('')
                text_br357ts.append('')
                text_degrees.append('')
                continue
            else:
                top_idx = top_idx[-1]
                text_names.append(self.fretboard_note_names[top_idx][string])
                text_br357ts.append(self.fretboard_note_br357ts[top_idx][string])
                text_degrees.append(self.fretboard_note_degrees[top_idx][string])

        _ = [ax.annotate(text.replace('b', r'$\flat$').replace('#', r'$\sharp$'), (fret[fret_interval[1]]+0.25, strings[i]), rotation=rotation,
                         fontsize=fontsize, va='center', ha='left', bbox=dict(facecolor=colors[0], alpha=0.0)) for i, text in enumerate(text_names)]
        _ = [ax.annotate(text.replace('b', r'$\flat$').replace('#', r'$\sharp$'), (fret[fret_interval[1]]+1.75, strings[i]), rotation=rotation,
                         fontsize=fontsize, va='center', ha='left', bbox=dict(facecolor=colors[-1], alpha=0.2)) for i, text in enumerate(text_br357ts)]

        # plt.savefig('三个和弦的键盘示意图.svg', bbox_inches='tight', pad_inches=0.0)
        # plt.close()

    def plot2(self, fret_left=0, fret_right=4, ax=None, title=None):
        rotation = 0
        w_scale = 2
        fontsize = 12
        strings = np.arange(self._max_string)
        fret = w_scale * np.arange(0, self._max_fret)
        fingers = np.concatenate([[-0.5], fret[:-1]+fret[1:]]) / 2
        fret_interval = [fret_left, fret_right]

        # new figure
        w = fret[fret_interval[1]] - fret[fret_interval[0]] + 2
        h = strings[-1] - strings[0] + 2.4
        scale = 0.75
        if not ax:
            fig = plt.figure(figsize=(w*scale, h*scale), dpi=72)
            ax = plt.gca(aspect='equal')
        else:
            fig = plt.gcf()
            ax.set_aspect('equal')
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_axis_off()
        ax.margins(0.0)

        # add title
        if title:
            ax.text(0.5, 0.895, title, fontsize=fontsize*1.5, va='bottom', ha='center', transform=ax.transAxes)

        # plot position blocks
        for i in range(fret_interval[0]+1, fret_interval[1]+1):
            if i in range(12, self._max_fret, 12):
                rect = plt.Rectangle((fingers[i], strings[0]), fret[i]-fingers[i], strings[-1]-strings[0], color='gray', alpha=0.2)
                ax.add_patch(rect)
            elif i % 12 in [3, 5, 7, 9]:
                mid = (strings[-1]-strings[0])/2
                rect = plt.Rectangle((fingers[i], mid), fret[i]-fingers[i], mid, color='gray', alpha=0.2)
                ax.add_patch(rect)
            else: pass

        # plot frets
        ax.set_xlim(fret[fret_interval[0]]-1, fret[fret_interval[1]]+1)
        _ = [ax.plot((fret[i], fret[i]), (strings[0], strings[-1]), c='black', lw=2.0) for i in range(fret_interval[0], fret_interval[1]+1)]
        _ = [ax.annotate(fret[i]//w_scale, (fret[i], -0.5), rotation=rotation, fontsize=fontsize, color='red', va='center', ha='center') for i in range(fret_interval[0], fret_interval[1]+1)]

        # plot strings
        ax.set_ylim(strings[0]-1.2, strings[-1]+1.2)
        _ = [ax.plot((fret[fret_interval[0]], fret[fret_interval[1]]), (s, s), c='black', lw=1.0) for s in strings]

        # plot texts
        radius = 0.15
        colors = gradient1(len(self._notes), '#f6b0f0', '#f6deb0')
        for string in strings:

            sp = self.pressed[:, string]

            if any(sp):  # if there exists note on current string
                if self._poly:  # plot all notes
                    _ = [ax.annotate(f'({self.fretboard_note_names[0][string]}, {self.fretboard_note_br357ts[0][string]})'.replace('b', r'$\flat$').replace('#', r'$\sharp$'),
                                     (fingers[0]+fret[fret_interval[0]], string), rotation=rotation, color='white', va='center', ha='center',
                                     fontsize=fontsize, bbox=dict(facecolor='#ee5511')) for _ in range(1) if sp[0]]
                    _ = [ax.annotate(f'({self.fretboard_note_names[i+1][string]}, {self.fretboard_note_br357ts[i+1][string]})'.replace('b', r'$\flat$').replace('#', r'$\sharp$'),
                                     (fingers[i+1], string), rotation=rotation, color='black', va='center', ha='center',
                                     fontsize=fontsize, bbox=dict(facecolor=colors[self.fretboard_note_degrees[i+1][string]])) for i, k in enumerate(sp[1:]) if k and fret_interval[0]<i+1<=fret_interval[1]]
                else:  # only plot top note
                    top_idx, = np.where(sp)
                    top_idx = top_idx[-1]
                    if top_idx == 0:
                        ax.annotate(f'({self.fretboard_note_names[0][string]}, {self.fretboard_note_br357ts[0][string]})'.replace('b', r'$\flat$').replace('#', r'$\sharp$'),
                                    (fingers[0]+fret[fret_interval[0]], string), rotation=rotation, va='center', ha='center',
                                    fontsize=fontsize, bbox=dict(facecolor='#ee5511'))
                    elif fret_interval[0]<top_idx<=fret_interval[1]:
                        ax.annotate(f'({self.fretboard_note_names[top_idx][string]}, {self.fretboard_note_br357ts[top_idx][string]})'.replace('b', r'$\flat$').replace('#', r'$\sharp$'),
                                    (fingers[top_idx], string), rotation=rotation, va='center', ha='center',
                                    fontsize=fontsize, bbox=dict(facecolor=colors[self.fretboard_note_degrees[top_idx][string]]))
                    else: pass

            else:  # if there isn't any note on current string, add a cross mark on open string position
                cross = [plt.Line2D((fingers[0]+fret[fret_interval[0]]-radius*np.sqrt(2)/2, fingers[0]+fret[fret_interval[0]]+radius*np.sqrt(2)/2),
                                    (string-radius*np.sqrt(2)/2, string+radius*np.sqrt(2)/2), c='black'),
                         plt.Line2D((fingers[0]+fret[fret_interval[0]]+radius*np.sqrt(2)/2, fingers[0]+fret[fret_interval[0]]-radius*np.sqrt(2)/2),
                                    (string-radius*np.sqrt(2)/2, string+radius*np.sqrt(2)/2), c='black')]
                ax.add_line(cross[0]); ax.add_line(cross[1])

        # fig.savefig('三个和弦的键盘示意图.svg', bbox_inches='tight', pad_inches=0.0)
        # plt.close()


class Piano(object):
    def __init__(self, notes=None):
        # default notes
        if notes:
            self._notes = notes
        else:
            self._notes = Chord('C').get_notes()

        # find range of notes
        self._get_note_range()

    def _get_note_range(self):
        notes = [abs(note) for note in self._notes]
        note_min = min(notes)
        note_max = max(notes)
        self._note_range = (note_min, note_max)
        return self._note_range

    def set_notes(self, notes):
        self._notes = notes
        self._get_note_range()
        return self

    def plot(self, note_range=None, ax=None, title=None):
        # get plot range
        if note_range is None:
            note_range = list(self._note_range)
        else:
            note_range = list(note_range)

        # note to position mappings
        def _note2pos_xy(note):
            group = note // 12
            note = note % 12
            if note in range(5):
                if note in [0, 2, 4]:
                    return 10.5 * group + 1.5 / 2 * note, 0
                else:
                    return 10.5 * group + 1.5 / 2 * (note + 1) - 0.5, 2.5
            else:
                if note in [5, 7, 9, 11]:
                    return 10.5 * group + 1.5 / 2 * (note + 1), 0
                else:
                    return 10.5 * group + 1.5 / 2 * (note + 2) - 0.5, 2.5

        def _note2pos_rect(note):
            if note % 12 in [0, 2, 4, 5, 7, 9, 11]:
                return dict(
                    xy=_note2pos_xy(note),
                    width=1.5,
                    height=6,
                    fc='white',
                    ec='black',
                    ls='-',
                    lw=2,
                    joinstyle='round',
                    zorder=1
                )
            else:
                return dict(
                    xy=_note2pos_xy(note),
                    width=1,
                    height=3.5,
                    fc='black',
                    ec='black',
                    ls='-',
                    lw=2,
                    joinstyle='round',
                    zorder=2
                )

        def _note2pos_mark(note):
            group = note // 12
            note = note % 12
            if note in range(5):
                x = 10.5 * group + 1.5 / 2 * (note + 1)
            else:
                x = 10.5 * group + 1.5 / 2 * (note + 2)
            if note in [0, 2, 4, 5, 7, 9, 11]:
                y = 0.75
            else:
                y = 3.25
            return x, y

        # constants
        expand = 1
        fontsize = 20
        scale = 1
        w = _note2pos_xy(note_range[1]+expand)[0] - _note2pos_xy(note_range[0]-expand)[0]
        h = 6
        margin = 0.2

        # new figure
        if not ax:
            fig = plt.figure(figsize=(w * scale + 2 * margin, h * scale + 2 * margin), dpi=72)
            ax = plt.gca(aspect='equal')
        else:
            fig = plt.gcf()
            ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_axis_off()
        ax.margins(0.0)
        ax.set_xlim(_note2pos_mark(note_range[0]-expand)[0]-margin, _note2pos_mark(note_range[1]+expand)[0]+margin)
        ax.set_ylim(0-margin, h+margin)

        # add title
        if title:
            ax.text(0.5, 0.895, title, fontsize=fontsize * 1.5, va='bottom', ha='center', transform=ax.transAxes)
            ax.set_ylim(0-margin, h+0.75+margin)

        # draw
        rects = [plt.Rectangle(**_note2pos_rect(note)) for note in range(note_range[0]-1-expand, note_range[1]+2+expand)]
        _ = [ax.add_patch(rect) for rect in rects]

        # add annotation
        c2s = ['red' if note.get_message_old() == '[A1]' else
               'orange' if note.get_message_old() == '[A0]' else
               'gold' if note.get_message_old() == '[A2]' else
               'dodgerblue' if note.get_message_old() == '[OK]' else
               'slategrey' if note.get_message_old() == '[TN]' else
               'limegreen' for note in self._notes]
        circs = [plt.Circle(_note2pos_mark(abs(note)), 0.4, ls='-', lw=1, ec=c, fc=c, zorder=3) for note, c in zip(self._notes, c2s)]
        _ = [ax.add_patch(circ) for circ in circs]
        _ = [ax.annotate(note.get_name(show_group=False), _note2pos_mark(abs(note)), color='white', fontsize=fontsize, ha='center', va='center', zorder=4) for note in self._notes]

        # plt.show()


class Pianoroll(object):
    '''

    Generate a pianoroll using matplotlib.

    '''
    def __init__(self, sheet, ticks_per_beat):
        """ pianoroll initialization, extract messages of same kind from sheet """
        # [01] get data
        self._sheet = sheet
        self._ticks_per_beat = ticks_per_beat
        self._max_ticks = max_ticks(sheet)

        self._pianoroll_exists = False

        # [02] get notes
        self._get_notes()

        # [03] get set_tempos
        self._get_set_tempos()

        # [04] get time_signatures
        self._get_time_signatures()

        # [05] get control_changes
        self._get_control_changes()

        # [06] get pitchwheels
        self._get_pitchwheels()

        # [07] set_vector default intervals
        self._set_intervals()

        # [08] set_vector default track colors
        self._set_track_colors()

        # [09] get lyrics
        self._get_lyrics()

    def _get_notes(self):
        self._notes = [[msg for msg in msglist if msg['type'] == 'note'] for msglist in self._sheet]
        # sort by channels, not tracks
        self._notes_c = [[msg for msg in sum(self._sheet, []) if msg['type'] == 'note' and msg['channel'] == k] for k in range(16)]

    def _get_set_tempos(self):
        self._set_tempos = [msg for msg in sum(self._sheet, []) if msg['type'] == 'set_tempo']
        self._set_tempos.sort(key=lambda msg: msg['time'])

        if self._set_tempos == []:
            self._set_tempos.insert(0, dict(type='set_tempo', tempo=500000, time=0))

        tempos = [msg['tempo'] for msg in self._set_tempos]
        self._bpm_range = (round(tempo2bpm(max(tempos))), round(tempo2bpm(min(tempos))))
        if self._bpm_range[1]-self._bpm_range[0]<1e-2:
            self._bpm_is_const = True
        else:
            self._bpm_is_const = False

    def _get_time_signatures(self):
        self._time_signatures = [msg for msg in sum(self._sheet, []) if msg['type'] == 'time_signature']
        self._time_signatures.sort(key=lambda msg: msg['time'])

        if self._time_signatures == [] or self._time_signatures[0]['time'] > 0:
            self._time_signatures.insert(0, dict(type='time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))

    def _get_control_changes(self):
        self._control_changes = [[msg for msg in msglist if msg['type'] == 'control_change'] for msglist in self._sheet]
        _ = [msglist.sort(key=lambda msg: msg['time']) for msglist in self._control_changes]
        self._used_controls = [list({msg['control'] for msg in msglist}) for msglist in self._control_changes]

        print('used controls:')
        for k, msglist in enumerate(self._used_controls):
            print(f'msglist {k}: {msglist}')
        print('')

    def _get_pitchwheels(self):
        self._pitchwheels = [[msg for msg in msglist if msg['type'] == 'pitchwheel'] for msglist in self._sheet]
        _ = [msglist.sort(key=lambda msg: msg['time']) for msglist in self._pitchwheels]

    def _set_intervals(self):
        self._time_interval = None
        self._note_interval = None

    def _set_track_colors(self):
        n_track = len(self._sheet)
        self._track_colors = [hsv_gradient(t, 0, n_track+1) for t in range(n_track)]

    def _get_lyrics(self):
        self._lyrics = [[msg for msg in msglist if msg['type'] == 'lyrics'] for msglist in self._sheet]
        _ = [msglist.sort(key=lambda msg: msg['time']) for msglist in self._lyrics]

    # ---------------------------------------------------------------------------------------------------- #

    def use_default_intervals(self):
        self._time_interval = (0, max(self._max_ticks))
        self._note_interval = (48, 72)
        self._pianoroll_exists = False
        plt.clf()

    def set_intervals(self, time_interval=None, note_interval=None):
        if time_interval:
            if time_interval[0] > time_interval[1]:
                raise ValueError('`time_interval[0]` should not larger than `time_interval[1]`!')
            else:
                self._time_interval = time_interval
        if note_interval:
            if note_interval[0] > note_interval[1]:
                raise ValueError('`note_interval[0]` should not larger than `note_interval[1]`!')
            else:
                self._note_interval = note_interval

        self._pianoroll_exists = False
        plt.clf()

    def set_track_color(self, track, color):
        self._track_colors[track] = color

    def _set_whdpi(self, width, height, dpi):
        pass

    def _set_hadpi(self, height, aspect_note, dpi):
        pass

    def draw_pianoroll(self, height=8, aspect_note=4, dpi=72, splits_per_beat=4, type='piano'):
        """

        Draw pianoroll with meta information.

        * variable's name ending with 's' means it is a list (multi variables)
        * list variable's name ending with '0' means it may contain messages whose time is out of time_interval

        Some abbreviations:

        * note              -> note
        * set_tempo         -> st
        * time_signature    -> ts
        * control_change    -> cc
        * pitchwheel        -> pw

        """

        ''' [00] intervals check '''

        if self._time_interval == None or self._note_interval == None:
            raise ValueError('Please set_vector intervals at first. You can use `use_default_intervals()` or `set_intervals()` to finish this job.')
        else:
            self._pianoroll_exists = True
            plt.clf()

        ''' [01] pianoroll meta params '''

        bottom_lane_h = 5
        self._bottom_lane_h = bottom_lane_h
        top_lane_h = 3

        bottom = self._note_interval[0] - bottom_lane_h
        self._bottom = bottom
        top = self._note_interval[1] + top_lane_h

        aspect_keyboard = {'piano': 4, 'drum': 6, 'agtc': 6}[type]

        width = height * (aspect_keyboard + aspect_note * length(*self._time_interval) / self._ticks_per_beat) / (top - bottom)
        axis_ratio = (aspect_keyboard / aspect_note * self._ticks_per_beat + length(*self._time_interval)) / (aspect_keyboard + aspect_note * length(*self._time_interval) / self._ticks_per_beat)
        keyboard_width = aspect_keyboard * axis_ratio

        left = self._time_interval[0] - keyboard_width
        right = self._time_interval[1]

        fontsize = 49*height/(length(*self._note_interval) + bottom_lane_h + top_lane_h)
        self._fontsize = fontsize
        markersize = 25*height/(length(*self._note_interval) + bottom_lane_h + top_lane_h)
        self._markersize = markersize

        ''' [02] set_tempos parsing '''

        sts0 = [[msg['time'], msg['tempo']] for msg in self._set_tempos]
        k_left = len(sts0)-1- [pw[0] <= self._time_interval[0] for pw in sts0][::-1].index(True)
        k_right = len(sts0)-1- [pw[0] <= self._time_interval[1] for pw in sts0][::-1].index(True)
        sts = [[self._time_interval[0], sts0[k_left][1]]] + [pw for pw in sts0 if self._time_interval[0] < pw[0] < self._time_interval[1]] + [[self._time_interval[1], sts0[k_right][1]]]

        ''' [03] time_signatures parsing '''

        # put all time_signatures into a list and append an end to the list
        tss0 = [[msg['time'], msg['numerator'], msg['denominator']] for msg in self._time_signatures]
        tss0.append([self._time_interval[1], tss0[-1][1], tss0[-1][2]])
        tss = [ts for ts in tss0 if inrange(ts[0], *self._time_interval)]
        # get a list of ticks_per_beat corresponding to time_signatures (because tpb changes with ts denominator)
        tpbs0 = [4 * self._ticks_per_beat // ts[2] for ts in tss0]
        # calculate delta x of three types of vertical line: bar-line, beat-line and split-line
        # step1 and step2 are changing with time_signatures, so they become step1s and step2s
        # step1: bar-line | step2: beat-line | step3: split-line
        # step1[k] = 4*self.ticks_per_beat*(nu[k]/de[k])
        # step2[k] = 4*self.ticks_per_beat*(1/de[k])
        step1s = [tpb*tss0[i][1] for (i, tpb) in enumerate(tpbs0)]
        step2s = tpbs0
        step3 = self._ticks_per_beat // splits_per_beat
        # x1s0 = [range(stt_0, stt_1, step1s[0]), range(stt_1, stt_2, step1s[1]), ..., range(stt_n, self.time_interval[1], step1s[n])]
        # x1s0[n][k] is x of the k-th bar-line after n-th time_signature
        x1s0 = [list(range(tss0[k][0], tss0[k+1][0], step1s[k])) for k in range(len(step1s)-1)]
        x1s = [x1 for x1 in sum(x1s0, []) if inrange(x1, *self._time_interval)]
        x2s0 = [list(range(tss0[k][0], tss0[k+1][0], step2s[k])) for k in range(len(step2s)-1)]
        x2s = [x2 for x2 in sum(x2s0, []) if inrange(x2, *self._time_interval) and x2 not in x1s]
        x3s0 = [k * step3 for k in range(self._time_interval[0] // step3, self._time_interval[1] // step3 + 1)]
        x3s = [x3 for x3 in x3s0 if inrange(x3, *self._time_interval) and x3 not in x1s + x2s]
        # l1s0: bar labels with x coord | l2s0: beat labels with x coord
        l1s0 = list(enumerate(sum(x1s0, [])))
        l1s = [l1[0] for l1 in l1s0 if l1[1] in x1s]
        l2s0 = sum([[[j % tss0[i][1], x2] for (j, x2) in enumerate(x2s0_section)] for (i, x2s0_section) in enumerate(x2s0)], [])
        l2s = [l2[0] for l2 in l2s0 if l2[1] in x2s]

        # ---------------------------------------------------------------------------------------------------- #

        ''' [01] draw pianoroll '''

        # initializing
        ax = get_figure(width, height, dpi)
        # the largest rectangle
        largest_rect = plt.Rectangle((left, bottom), right-left, top-bottom, facecolor='none', edgecolor='#555555', lw=0.75, joinstyle='round', zorder=7)
        ax.add_patch(largest_rect)
        # bottom lane rectangle
        bl_rect = plt.Rectangle((self._time_interval[0], bottom), length(*self._time_interval), bottom_lane_h, facecolor='#ddeeff', lw=0.0, zorder=0)
        self._bl_rect = bl_rect
        ax.add_patch(bl_rect)
        # main area rectangle
        main_rect = plt.Rectangle((self._time_interval[0], self._note_interval[0]), length(*self._time_interval), length(*self._note_interval), facecolor='#ddeeff', lw=0.0, zorder=0)
        self._main_rect = main_rect
        ax.add_patch(main_rect)
        # top lane rectangle
        tl_rect = plt.Rectangle((left, self._note_interval[1]), right - left, top_lane_h, facecolor='#ffffff', lw=0.0, zorder=0)
        ax.add_patch(tl_rect)
        # background keys
        white_notes = [note for note in range(*self._note_interval) if note % 12 in [0, 2, 4, 5, 7, 9, 11]]
        black_notes = [note for note in range(*self._note_interval) if note % 12 in [1, 3, 6, 8, 10]]
        white_bg_rects = [plt.Rectangle((self._time_interval[0], note), length(*self._time_interval), 1, facecolor='#ffffff', lw=0.0, zorder=1) for note in white_notes]
        black_bg_rects = [plt.Rectangle((self._time_interval[0], note), length(*self._time_interval), 1, facecolor='#ddcccc', lw=0.0, zorder=1) for note in black_notes]
        _ = [ax.add_patch(rect) for rect in white_bg_rects+black_bg_rects]
        # left bottom rectangle
        lb_rect = plt.Rectangle((left, bottom), keyboard_width, bottom_lane_h, facecolor='#ffffff', lw=0.0, zorder=4)
        ax.add_patch(lb_rect)
        if self._bpm_is_const:
            text = f'bpm\n{self._bpm_range[0]}\n\nvel\n0..127'
        else:
            text = f'bpm\n{self._bpm_range[0]}..{self._bpm_range[1]}\n\nvel\n0..127'
        plt.annotate(text, (left + keyboard_width / 2, bottom + bottom_lane_h / 2), color='#555555',
                     va='center', ha='center', fontsize=fontsize, zorder=4.1, clip_path=lb_rect)
        # keyboard
        white_kbd_rects = [plt.Rectangle((left, note), keyboard_width, 1, facecolor='#ffffff', lw=0.0, zorder=4) for note in white_notes]
        black_kbd_rects = [plt.Rectangle((left, note), keyboard_width, 1, facecolor='#222222', lw=0.0, zorder=4) for note in black_notes]
        _ = [ax.add_patch(rect) for rect in white_kbd_rects+black_kbd_rects]
        # split lines of keys
        _ = [plt.plot([left, self._time_interval[0]], [note, note], color='#222222', lw=0.5, solid_capstyle='butt', zorder=4.1) for note in range(*self._note_interval)]
        # text on keys
        _ = [plt.annotate(note2label(note, type=type), (left+keyboard_width//16, note+0.5), color='#555555', va='center', fontsize=fontsize, zorder=4.1,
                          clip_path=white_kbd_rects[k]) for (k, note) in enumerate(white_notes)]
        _ = [plt.annotate(note2label(note, type=type), (left+keyboard_width//16, note+0.5), color='#ffffff', va='center', fontsize=fontsize, zorder=4.1,
                          clip_path=black_kbd_rects[k]) for (k, note) in enumerate(black_notes)]
        # horizontal grid lines
        _ = [plt.plot(self._time_interval, [note, note], color='#999999', lw=0.5, solid_capstyle='butt', zorder=2) for note in range(self._note_interval[0] + 1, self._note_interval[1])]
        # vertical grid lines
        _ = [plt.plot([x, x], [bottom, self._note_interval[1]], color='#aaaaaa', lw=0.5, solid_capstyle='butt', zorder=2.1) for x in x3s]
        _ = [plt.plot([x, x], [bottom, self._note_interval[1]], color='#555555', lw=0.5, solid_capstyle='butt', zorder=2.1) for x in x2s]
        _ = [plt.plot([x, x], [bottom, self._note_interval[1]], color='#222222', lw=1.0, solid_capstyle='butt', zorder=2.1) for x in x1s]
        # horizontal split lines
        plt.plot(self._time_interval, [self._note_interval[0], self._note_interval[0]], color='#555555', lw=0.5, solid_capstyle='butt', zorder=6.1)
        plt.plot([left, self._time_interval[1]], [self._note_interval[1], self._note_interval[1]], color='#555555', lw=0.5, solid_capstyle='butt', zorder=6.1)
        plt.plot([left, self._time_interval[1]], [self._note_interval[1] + 1, self._note_interval[1] + 1], color='#555555', lw=0.5, solid_capstyle='butt', zorder=6.1)
        plt.plot([left, self._time_interval[1]], [self._note_interval[1] + 2, self._note_interval[1] + 2], color='#555555', lw=0.5, solid_capstyle='butt', zorder=6.1)
        # vertical split lines
        plt.plot([self._time_interval[0], self._time_interval[0]], [bottom, self._note_interval[1]], color='#555555', lw=0.5, solid_capstyle='butt', zorder=6)

        ''' [02] draw set_tempos '''

        if not self._bpm_is_const:
            def _bpm2vel(bpm):
                bpm_lower = self._bpm_range[0]
                bpm_upper = self._bpm_range[1]
                lam = (bpm_upper - bpm) / (bpm_upper - bpm_lower)
                return lam * (self._note_interval[0] - bottom_lane_h) + (1 - lam) * self._note_interval[0]
            sts_x = [st[0] for st in sts]
            sts_y = [_bpm2vel(tempo2bpm(st[1])) for st in sts]
            plot = plt.step(sts_x, sts_y, color='#ee5511', lw=1.0, solid_capstyle='butt', solid_joinstyle='bevel', where='post', zorder=2.9, label='tempo')
            _ = [p.set_clip_path(bl_rect) for p in plot]

        ''' [03] draw time_signatures '''

        # time_signature labels
        _ = [plt.annotate(f'{ts[1]}/{ts[2]}', (ts[0], self._note_interval[1] + 1.5), color='#555555', va='center', ha='center', fontsize=fontsize) for ts in tss]
        # bar labels
        _ = [plt.annotate(l1, (x1, self._note_interval[1] + 2.5), color='#555555', va='center', ha='center', fontsize=fontsize) for (x1, l1) in zip(x1s, l1s)]
        # beat labels
        _ = [plt.annotate(l2, (x2, self._note_interval[1] + 2.5), fontsize=fontsize * 3 / 4, color='#555555', va='center', ha='center') for (x2, l2) in zip(x2s, l2s)]

    def _draw_notes(self, track=0, shader=rgb_gradient, type='piano', alpha=1.0, lyric=None):
        """ draw notes """

        ''' pianoroll checking '''

        if not self._pianoroll_exists:
            raise ValueError('You should draw a pianoroll first using `draw_pianoroll()` method!')

        ''' notes parsing '''

        # divide notes both in note_interval and time_interval into 3 parts: left, full and right
        notes0 = [note for note in self._notes[track] if inrange(note['note'], *self._note_interval)]
        notes = [note for note in notes0 if inrange(note['time1'], *self._time_interval) or inrange(note['time1'] + note['time2'], *self._time_interval)]
        notes_full = [note for note in notes if inrange(note['time1'], *self._time_interval) and inrange(note['time1'] + note['time2'], *self._time_interval)]
        notes_left = [note for note in notes if note['time1'] < self._time_interval[0] <= note['time1'] + note['time2']]
        notes_right = [note for note in notes if note['time1'] < self._time_interval[1] <= note['time1'] + note['time2']]
        notes_rearranged = notes_full + notes_left + notes_right
        # getting rectangles of notes for pianoroll
        notes_full_rects = [plt.Rectangle((note['time1'], note['note']), note['time2'], 1,
                                          color=shader(note['velocity_on'], 0, 127), joinstyle='round', lw=0.0, alpha=alpha, zorder=5+0.001*track) for note in notes_full]
        notes_left_rects = [plt.Rectangle((self._time_interval[0], note['note']), note['time2'] - self._time_interval[0] + note['time1'], 1,
                                          color=shader(note['velocity_on'], 0, 127), joinstyle='round', lw=0.0, alpha=alpha, zorder=5+0.001*track) for note in notes_left]
        notes_right_rects = [plt.Rectangle((note['time1'], note['note']), self._time_interval[1] - note['time1'], 1,
                                           color=shader(note['velocity_on'], 0, 127), joinstyle='round', lw=0.0, alpha=alpha, zorder=5+0.001*track) for note in notes_right]
        notes_rects = notes_full_rects + notes_left_rects + notes_right_rects

        ''' draw notes '''

        ax = plt.gca()
        _ = [ax.add_patch(rect) for rect in notes_rects]
        # note edge
        _ = [plt.plot([note['time1'], note['time1']+note['time2'], note['time1']+note['time2'], note['time1'], note['time1']],
                      [note['note'], note['note'], note['note']+1, note['note']+1, note['note']],
                      color='#123456', lw=0.5, solid_capstyle='round', alpha=alpha, zorder=5+0.001*(track+0.2)) for note in notes_full]
        _ = [plt.plot([self._time_interval[0], note['time1'] + note['time2'], note['time1'] + note['time2'], self._time_interval[0]],
                      [note['note'], note['note'], note['note']+1, note['note']+1],
                      color='#123456', lw=0.5, solid_capstyle='round', alpha=alpha, zorder=5+0.001*(track+0.2)) for note in notes_left]
        _ = [plt.plot([self._time_interval[1], note['time1'], note['time1'], self._time_interval[1]],
                      [note['note']+1, note['note']+1, note['note'], note['note']],
                      color='#123456', lw=0.5, solid_capstyle='round', alpha=alpha, zorder=5+0.001*(track+0.2)) for note in notes_right]
        # note label
        if type == 'lyric':
            _ = [plt.annotate(note['lyric'], (note['time1'] + self._ticks_per_beat // 16, note['note'] + 0.5),
                              color='#ffffff', va='center', fontsize=self._fontsize, alpha=alpha, zorder=5 + 0.001 * (track + 0.1),
                              clip_path=notes_rects[k]) for (k, note) in enumerate(notes_rearranged)]
        else:
            _ = [plt.annotate(note2label(note['note'], type=type, show_group=False), (note['time1'] + self._ticks_per_beat // 16, note['note'] + 0.5),
                              color='#ffffff', va='center', fontsize=self._fontsize, alpha=alpha, zorder=5 + 0.001 * (track + 0.1),
                              clip_path=notes_rects[k]) for (k, note) in enumerate(notes_rearranged)]
        # on-velocity
        notes_full_vels = [plt.Line2D([note['time1'], note['time1']], [self._bottom, self._bottom + note['velocity_on'] / 127 * self._bottom_lane_h],
                                      color=shader(note['velocity_on'], 0, 127), lw=1.0, solid_capstyle='butt', alpha=alpha, zorder=3+0.001*track,
                                      marker='x', markevery=[1], markersize=self._markersize, mew=1) for note in notes_full + notes_right]
        _ = [ax.add_line(vel) for vel in notes_full_vels]
        _ = [vel.set_clip_path(self._bl_rect) for vel in notes_full_vels]
        # lyric
        if lyric:
            _ = [plt.annotate(lyric[k], (note['time1']+self._ticks_per_beat//16, note['note']-0.5),
                            color='#555555', va='center', fontsize=self._fontsize*3/4, zorder=5+0.001*(track+0.1)) for (k, note) in enumerate(notes) if k<len(lyric)]

    def draw_notes(self, tracks=(0,), color_scheme='velocity', type='piano', alpha=1.0, lyric=None):
        if color_scheme == 'velocity':
            _ = [self._draw_notes(t, rgb_gradient, type, alpha, lyric) for t in tracks]
        elif color_scheme == 'track':
            _ = [self._draw_notes(t, lambda x, x_min, x_max: cst_gradient(x, x_min, x_max, self._track_colors[t]), type, alpha, lyric) for t in tracks]

    def draw_control_changes(self, track=0, controls=(64, ), plot_type='stair', alpha=1.0):
        """ draw control_changes """

        ''' pianoroll checking '''

        if not self._pianoroll_exists:
            raise ValueError('You should draw a pianoroll first using `draw_pianoroll()` method!')

        ''' control_changes parsing '''

        ccs0 = dict.fromkeys(controls, [])
        ccs = dict.fromkeys(controls, [])
        for control in controls:
            ccs0[control] = [[msg['time'], msg['value']] for msg in self._control_changes[track] if msg['control'] == control]
            # add default value
            ccs0[control].insert(0, [0, 0])
            k_left = len(ccs0[control])-1- [cc[0] <= self._time_interval[0] for cc in ccs0[control]][::-1].index(True)
            k_right = len(ccs0[control])-1- [cc[0] <= self._time_interval[1] for cc in ccs0[control]][::-1].index(True)
            ccs[control] = [[self._time_interval[0], ccs0[control][k_left][1]]] + \
                           [cc for cc in ccs0[control] if self._time_interval[0] < cc[0] < self._time_interval[1]] + \
                           [[self._time_interval[1], ccs0[control][k_right][1]]]

        ''' draw control_changes '''

        ccs_stts = dict.fromkeys(controls, [])
        ccs_values = dict.fromkeys(controls, [])
        for i, control in enumerate(controls):
            ccs_stts[control] = [cc[0] for cc in ccs[control]]
            ccs_values[control] = [cc[1] / 127 * length(*self._note_interval) + self._note_interval[0] for cc in ccs[control]]

            color1 = cs.rgb_to_hsv(*self._track_colors[track])
            color2 = [color1[0], color1[1]/10, color1[2]/10]
            color = hsv_gradient(i, 0, len(controls), color1, color2)
            if plot_type == 'piecewise':
                plot = plt.plot(ccs_stts[control], ccs_values[control], color=color, alpha=alpha,
                                lw=0.75, ls='--', dash_capstyle='butt', dash_joinstyle='bevel', zorder=2.9+0.001*(track+0.1*control),
                                clip_path=self._main_rect, label=f'[track {track}] {CC_NAMES[control]}')
                _ = [p.set_clip_path(self._main_rect) for p in plot]
            elif plot_type == 'stair':
                plot = plt.step(ccs_stts[control], ccs_values[control], color=color, alpha=alpha,
                                lw=0.75, ls='--', dash_capstyle='butt', dash_joinstyle='bevel', zorder=2.9+0.001*(track+0.1*control),
                                where='post', clip_path=self._main_rect, label=f'[track {track}] {CC_NAMES[control]}')
                _ = [p.set_clip_path(self._main_rect) for p in plot]
            elif plot_type == 'stair_fill':
                plot = plt.fill_between(ccs_stts[control], ccs_values[control], self._note_interval[0],
                                        color=color, alpha=alpha, step='post', lw=0.75, linestyle='--',
                                        capstyle='butt', joinstyle='bevel', zorder=2.9+0.001*(track+0.1*control),
                                        clip_path=self._main_rect, label=f'[track {track}] {CC_NAMES[control]}')
                plot.set_clip_path(self._main_rect)
            else:
                pass

    def _draw_pitchwheels(self, track=0, shader=cst_gradient, plot_type='stair', alpha=1.0):
        """ draw pitchwheels """

        ''' pianoroll checking '''

        if not self._pianoroll_exists:
            raise ValueError('You should draw a pianoroll first using `draw_pianoroll()` method!')

        ''' pitchwheels parsing '''

        pws0 = [[msg['time'], msg['pitch']] for msg in self._pitchwheels[track]]
        # add default value
        pws0.insert(0, [0, 0])
        k_left = len(pws0)-1- [pw[0] <= self._time_interval[0] for pw in pws0][::-1].index(True)
        k_right = len(pws0)-1- [pw[0] <= self._time_interval[1] for pw in pws0][::-1].index(True)
        pws = [[self._time_interval[0], pws0[k_left][1]]] + [pw for pw in pws0 if self._time_interval[0] < pw[0] < self._time_interval[1]] + [[self._time_interval[1], pws0[k_right][1]]]

        ''' draw pitchwheels '''

        pws_stts = [pw[0] for pw in pws]
        pws_pits = [pw[1] / 16384 * length(*self._note_interval) + middle(*self._note_interval) for pw in pws]
        if plot_type == 'piecewise':
            plot = plt.plot(pws_stts, pws_pits, color=shader(0), lw=1.0, solid_capstyle='butt', solid_joinstyle='bevel', alpha=alpha,
                            zorder=2.9+0.001*track, label=f'[track {track}] pitchwheel')
            _ = [p.set_clip_path(self._main_rect) for p in plot]
        elif plot_type == 'stair':
            plot = plt.step(pws_stts, pws_pits, color=shader(0), lw=1.0, solid_capstyle='butt', solid_joinstyle='bevel', alpha=alpha,
                            where='post', zorder=2.9+0.001*track, label=f'[track {track}] pitchwheel')
            _ = [p.set_clip_path(self._main_rect) for p in plot]
        elif plot_type == 'stair_fill':
            plot = plt.fill_between(pws_stts, pws_pits, middle(*self._note_interval),
                                    color=shader(0), lw=1.0, capstyle='butt', joinstyle='bevel', alpha=alpha, step='post',
                                    zorder=2.9+0.001*track, label=f'[track {track}] pitchwheel')
            plot.set_clip_path(self._main_rect)
        else: pass

    def draw_pitchwheels(self, tracks=(0,), plot_type='stair', alpha=1.0):
        _ = [self._draw_pitchwheels(t, lambda x: cst_gradient(x, 0, 1, self._track_colors[t]), plot_type, alpha) for t in tracks]

    def show_legends(self):
        l = plt.legend(loc='lower right', fontsize=self._fontsize)
        l.set_zorder(20)

    def show_chords(self, times, chords):
        """ show chords """

        ''' pianoroll checking '''

        if not self._pianoroll_exists:
            raise ValueError('You should draw a pianoroll first using `draw_pianoroll()` method!')

        ''' chords parsing '''

        chords0 = list(zip(times, chords))

        ''' show chords '''

        chords = [chord for chord in chords0 if inrange(chord[0], *self._time_interval)]
        _ = [plt.annotate(chord[1], (chord[0], self._note_interval[1] + 0.5), color='#555555', va='center', ha='center', fontsize=self._fontsize) for chord in chords]

    # ---------------------------------------------------------------------------------------------------- #

    def save(self, savepath):
        plt.savefig(Path(savepath))
        plt.close()

    # ---------------------------------------------------------------------------------------------------- #

    def get_tick_range_s(self, track):
        # get tick range (single track)
        return 0, self._max_ticks[track]

    def get_tick_range_m(self, tracks):
        # get tick range (multiple track)
        return 0, max([self._max_ticks[track] for track in tracks])

    def get_tick_range_a(self):
        # get tick range (all tracks)
        return 0, max(self._max_ticks)

    def get_note_range_sg(self, track):
        # get note range (single track, global)
        notes = [note['note'] for note in self._notes[track]]
        note_min = min(notes) - 1 if notes != [] else 48
        note_max = max(notes) + 2 if notes != [] else 72
        return note_min, note_max

    def get_note_range_mg(self, tracks):
        # get note range (multiple track, global)
        ranges = [self.get_note_range_sg(track) for track in tracks]
        note_min = min([r[0] for r in ranges])
        note_max = max([r[1] for r in ranges])
        return note_min, note_max

    def get_note_range_sl(self, track):
        # get note range (single track, local)
        notes = [note['note'] for note in self._notes[track] if inrange(note['time1'], *self._time_interval) or inrange(note['time1'] + note['time2'], *self._time_interval)]
        note_min = min(notes) - 1 if notes != [] else 48
        note_max = max(notes) + 2 if notes != [] else 72
        return note_min, note_max

    def get_note_range_ml(self, tracks):
        # get note range (multiple track, local)
        ranges = [self.get_note_range_sl(track) for track in tracks]
        note_min = min([r[0] for r in ranges])
        note_max = max([r[1] for r in ranges])
        return note_min, note_max

    def get_used_controls(self, track):
        return self._used_controls[track]

    def get_set_tempos(self):
        return [[msg['time'], msg['tempo']] for msg in self._set_tempos]

    def get_key_frames(self, track, note=36, bpm=164, fps=60):
        time1s = [tick2second(msg['time1'], self._ticks_per_beat, bpm2tempo(bpm)) for msg in self._notes[track] if msg['note']==note]
        time2s = [tick2second(2*msg['time2'], self._ticks_per_beat, bpm2tempo(bpm)) for msg in self._notes[track] if msg['note']==note]
        time3s = [time1+time2 for time1, time2 in zip(time1s, time2s)]
        vels = [msg['velocity_on'] for msg in self._notes[track] if msg['note']==note]

        ons = [int(time1//(1/fps)) for time1 in time1s]
        ons.append(-1)
        offs = [int(time3//(1/fps)) for time3 in time3s]
        offs.append(-1)
        print(f'length: {len(ons)} | {ons}')
        print(f'length: {len(offs)} | {offs}')
        print(f'length: {len(vels)} | {vels}')

        return ons, offs, vels


class Clock(object):
    def __init__(self, notes):
        self._notes = notes

    def plot(self, title, tonic=None, margin_anno_type=None, colorize=None, subtitle=None, ax=None):
        import colorsys as cs

        radius = 5
        omega = np.cos(np.pi/6) - 1j*np.sin(np.pi/6)
        offset = (-omega)**3

        texts = ['C', r'C$\sharp$/D$\flat$', 'D', r'D$\sharp$/E$\flat$',
                 'E', 'F', r'F$\sharp$/G$\flat$', 'G',
                 r'G$\sharp$/A$\flat$', 'A', r'A$\sharp$/B$\flat$', 'B']
        for note in self._notes:
            texts[abs(note)%12] = note.get_name(show_group=False).replace('#', r'$\sharp$').replace('b', r'$\flat$') + f'({note.get_message_old()})'
        text_colors = [cs.hls_to_rgb(h, 0.5, 0.75) for h in np.linspace(0, 1.0, 12, endpoint=False)]
        text_colors = [text_color if k in [abs(x)%12 for x in self._notes] else 'gray' for k, text_color in enumerate(text_colors)]
        text_positions = [(1.4*radius*np.real(omega**k*offset), 1.4*radius*np.imag(omega**k*offset)) for k in range(12)]

        hand_colors = [[0.5, 0.5, 0.5]] * 12
        msgs = [note.get_message_old() for note in self._notes]
        if 'R' in msgs: root_pos = abs(self._notes[msgs.index('R')]) % 12
        else: root_pos = -1
        if 'B' in msgs: bass_pos = abs(self._notes[msgs.index('B')]) % 12
        else: bass_pos = -1
        if tonic is not None: tonic_pos = tonic % 12
        else: tonic_pos = -1
        for i in range(12):
            if i in [root_pos, bass_pos, tonic_pos]:
                hand_colors[i] = [0.75*(i==root_pos), 0.75*(i==bass_pos), 0.75*(i==tonic_pos)]
        if colorize:
            for i in colorize:
                hand_colors[i] = 'red'


        ''' new figure '''


        if not ax:
            fig, ax = plt.subplots(1, 1)
            fig.set_figwidth(4); fig.set_figheight(4)
            fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.0, hspace=0.0)
        ax.margins(0.0)
        ax.set_aspect('equal')
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlim(-1.8*radius, 1.8*radius)
        ax.set_ylim(-1.8*radius, 1.8*radius)


        ''' plotting '''


        ks1 = [abs(x) for x in self._notes]

        circ = plt.Circle((0, 0), radius, fc='none', ec='black', lw=2.0)
        hands = [plt.Line2D((0, 0.8*radius*np.real(omega**k*offset)), (0, 0.8*radius*np.imag(omega**k*offset)),
                        lw=1.5, c=hand_colors[k]) for k in range(12)]
        ticks = [plt.Line2D((0.95*radius*np.real(omega**k*offset), radius*np.real(omega**k*offset)), (0.95*radius*np.imag(omega**k*offset), radius*np.imag(omega**k*offset)),
                        lw=1, c='black') for k in range(12)]

        ax.add_patch(circ)
        _ = [ax.add_line(hand) for hand in [hands[k%12] for k in ks1]]
        _ = [ax.add_line(tick) for tick in [ticks[k] for k in range(12)]]
        _ = [ax.annotate(k, (1.1*radius*np.real(omega**k*offset), 1.1*radius*np.imag(omega**k*offset)), ha='center', va='center') for k in range(12)]
        _ = [ax.annotate(texts[k], text_positions[k], va='center', ha='center', bbox=dict(facecolor=text_colors[k], alpha=0.2, edgecolor=text_colors[k])) for k in range(12)]
        ks2 = ks1 + [12+ks1[0]]
        if margin_anno_type == 'degree':
            _ = [ax.annotate(f'{(k2-k1)*30}°', (np.real(0.65*radius*omega**(k1+(k2-k1)/2)*offset), np.imag(0.65*radius*omega**(k1+(k2-k1)/2)*offset)),
                             ha='center', va='center') for k1, k2 in zip(ks2[:-1], ks2[1:])]
        elif margin_anno_type == 'interval':
            notes_appended = self._notes + [self._notes[0]+Interval('P8')]
            _ = [ax.annotate(notes_appended[i+1]-notes_appended[i], (np.real(0.65*radius*omega**(k1+(k2-k1)/2)*offset), np.imag(0.65*radius*omega**(k1+(k2-k1)/2)*offset)),
                             ha='center', va='center') for i, (k1, k2) in enumerate(zip(ks2[:-1], ks2[1:]))]
        else: pass
        ax.text(0.05, 0.95, title, transform=ax.transAxes, ha='left', va='top', bbox=dict(facecolor='none', edgecolor='black'))
        if subtitle:
            ax.text(0.95, 0.05, subtitle, transform=ax.transAxes, ha='right', va='bottom', bbox=dict(facecolor='none', edgecolor='black'))


class ColorScheme(object):
    def __init__(self, notes):
        self._notes = notes

    def plot(self, title, filename=''):
        h = np.linspace(0, 1, 12, endpoint=False)
        hs = [abs(t)%12 for t in self._notes]
        # save_name = ''
        l1 = 0.5; l2 = 0.25
        s1 = 0.95; s2 = 0.5

        n_colors = len(hs)
        n_gradients = 7

        colors = np.zeros((n_colors, n_gradients, 3), 'float')
        for i in range(n_colors):
            colors[i] = gradient3(n_gradients, cs.hls_to_rgb(h[hs[i]], l1, s1), cs.hls_to_rgb(h[hs[i]], l2, s2))


        ax = plt.gca()
        ax.margins(0.0)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_aspect('equal')

        x_margins = 0.5; w = 3
        y_margins = 1.5; h = 1
        h_text = 1
        ax.set_xlim(0, (x_margins+w)*n_gradients-x_margins)
        ax.set_ylim(0-h_text, (y_margins+h)*n_colors-y_margins+h_text)
        for i in range(n_colors):
            for j in range(n_gradients):
                rect = plt.Rectangle(((w+x_margins)*j, (h+y_margins)*i), w, h, color=colors[n_colors-i-1, j])
                ax.add_patch(rect)
                ax.annotate(oct2hex(colors[n_colors-i-1, j]), ((x_margins+w)*j+w/2, (y_margins+h)*i-h_text/2), va='center', ha='center')
        ax.annotate(f'{title} {[k*360//12 for k in hs]}',
                    (((x_margins+w)*n_gradients-x_margins)/2, (y_margins+h)*n_colors-y_margins+h_text/2), ha='center', va='center')
        if filename:
            plt.savefig(f'{filename}.svg', bbox_inches='tight', pad_inches=0.0)


class P5Line(object):
    def __init__(self, chords, names=None):
        self._chords = chords
        self._names = names

    def plot(self):
        color_map = ['salmon', 'darkorange', 'gold', 'yellowgreen', 'mediumaquamarine', 'dodgerblue', 'mediumpurple']
        n_chords = len(self._chords)

        fig, ax = plt.subplots()
        fig.set_figwidth(16)
        fig.set_figheight(16)
        ax.margins(0.0)
        ax.set_axis_off()
        # ax.set_xticks([])
        # ax.set_yticks([])
        ax.set_aspect('equal')

        x_mins = []
        x_maxs = []
        for y, chord in enumerate(self._chords):
            pos_map = dict(((key, value) for value, key in enumerate([5, 0, 7, 2, 9, 4, 11])))
            pos_map_inv = dict(((key, value) for value, key in pos_map.items()))
            def x2text(x): return Note().set_vector(nnrel=pos_map_inv[x%7], accidental=x//7).get_name(show_group=False)

            rect_xs = [pos_map[note.get_vector()[0]]+7*note.get_vector()[1] for note in chord]
            bg_xs = [x for x in range(min(rect_xs), max(rect_xs)+1) if x not in rect_xs]

            rects = [plt.Rectangle((rect_x, y), 1, 1, facecolor=color_map[i], edgecolor='black', lw=2, joinstyle='round', zorder=0) for i, rect_x in enumerate(rect_xs)]
            rects_bg = [plt.Rectangle((bg_x, y), 1, 1, facecolor='gray', edgecolor='black', lw=2, joinstyle='round', zorder=-1) for bg_x in bg_xs]

            _ = [ax.add_patch(rect) for rect in rects+rects_bg]
            _ = [ax.annotate(r'$\mathbf{'+x2text(int(x)).replace('b', r'\flat').replace('#', r'\sharp')+r'}$',
                              (x+1/2, y+1/2), c='white', fontsize=15, ha='center', va='center', zorder=1) for x in rect_xs]
            _ = [ax.annotate(r'$\mathbf{'+x2text(int(x)).replace('b', r'\flat').replace('#', r'\sharp')+r'}$',
                              (x+1/2, y+1/2), c='white', fontsize=15, ha='center', va='center', zorder=1) for x in bg_xs]

            x_mins.append(min(rect_xs))
            x_maxs.append(max(rect_xs))

        x_min = min(x_mins)
        x_max = max(x_maxs)

        left_offset = 3

        if self._names is not None:
            _ = [ax.annotate(self._names[y], (x_min-left_offset, y+1/2),
                              c='black', fontsize=15, ha='left', va='center', zorder=1) for y in range(n_chords)]
        else:
            _ = [ax.annotate(chord.get_name(), (x_min-left_offset, y+1/2),
                              c='black', fontsize=15, ha='left', va='center', zorder=1) for y, chord in enumerate(self._chords)]

        vertical_line_xs = [x for x in range(x_min, x_max+1+1) if x%7==0]
        _ = [ax.plot((x, x), (0, n_chords), 'b', lw=3, solid_capstyle='round') for x in vertical_line_xs]

        ax.set_xlim(x_min-left_offset-1/2, x_max+1+1/2)
        ax.set_ylim(-1/2, n_chords+1/2)


class Tonnetz(object):
    def __init__(self, notes, title=None, enharmonic=False, n_x=11, n_y=11, side_length=3, center_note=Note()):
        self._notes = notes
        if enharmonic:
            self._vectors = [abs(note) % 12 for note in self._notes]
        else:
            self._vectors = [note.get_vector(return_register=False) for note in self._notes]
        self._title = title
        self._enharmonic = enharmonic

        self._n_x = n_x
        self._n_y = n_y

        self._step_x = side_length
        self._step_y = 3 ** (1 / 2) * self._step_x / 2

        self._notes_bg = []
        self._notes_bg_xy = []
        self._links = []

        for i in range(n_x):
            x = i - n_x // 2
            for j in range(n_y):
                y = j - n_y // 2

                cur_note = center_note + x * Interval('P5') + y * Interval('M3')

                if abs(cur_note-center_note) % 3 == 0:
                    cur_note.add_message(tds='T')
                elif abs(cur_note-center_note) % 3 == 1:
                    cur_note.add_message(tds='D')
                else:
                    cur_note.add_message(tds='S')

                if abs(x+y) > 1:
                    cur_note.add_message(alpha=0.25)
                else:
                    cur_note.add_message(alpha=1.0)

                cur_xy = self._step_x * (x + y / 2), y * self._step_y

                self._notes_bg.append(cur_note)
                self._notes_bg_xy.append(cur_xy)

    def plot(self):
        print(self._notes_bg_xy)
        fig, ax = plt.subplots()
        fig.set_figwidth(8)
        fig.set_figheight(8)
        ax.margins(0.0)
        # ax.set_axis_off()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal')

        tds_color_map = {'T': '#D5E8D4', 'D': '#F8CECC', 'S': '#FFF2CC'}
        for cur_note, cur_xy in zip(self._notes_bg, self._notes_bg_xy):
            alpha = cur_note.get_message('alpha')
            circ = plt.Circle(cur_xy, self._step_x / 3, facecolor=tds_color_map[cur_note.get_message('tds')], edgecolor='black', alpha=alpha)
            ax.add_patch(circ)

            if_chosen = abs(cur_note)%12 in self._vectors if self._enharmonic else cur_note.get_vector(return_register=False) in self._vectors
            if if_chosen:
                circ_ = plt.Circle(cur_xy, self._step_x / 4, facecolor='black', edgecolor='black')
                ax.add_patch(circ_)
                ax.annotate(cur_note.get_name(show_register=False), cur_xy, color='white', va='center', ha='center')
            else:
                ax.annotate(cur_note.get_name(show_register=False), cur_xy, color='black', va='center', ha='center', alpha=alpha)

        x_max = self._step_x * (self._n_x - 1 - self._n_x // 2 + (self._n_y - 1 - self._n_y // 2) / 2 + 1)
        y_max = self._step_y * (self._n_y - 1 - self._n_y // 2 + 1)
        ax.set_xlim([-x_max, x_max])
        ax.set_ylim([-y_max, y_max])

        if self._title is not None:
            ax.set_title(self._title)

        plt.show()
