import matplotlib.pyplot as plt
import matplotlib as mpl
# from matplotlib.transforms import TransformedBbox
import colorsys as cs
from mido import MidiFile, MidiTrack
from mido import Message, MetaMessage
from mido import bpm2tempo, tempo2bpm, tick2second, second2tick
from consts import ADD2_NOTE_NAMES, AGTC_NOTE_NAMES, CC_NAMES
from pathlib import Path


''' other functions '''


# a handy length function
def length(a, b):
    return b - a


# a handy middle point function
def middle(a, b):
    return (a + b) / 2


# a handy if-in-range function
def inrange(x, a, b):
    return a <= x < b


''' for matplotlib '''


# assigning a chinese font
plt.rc({'font.sans-serif': 'Consolas-with-Yahei', 'axes.unicode_minus': False, 'font.size': 12.0})
# mpl.rcParams['font.sans-serif'] = ['Consolas-with-Yahei']
# mpl.rcParams['axes.unicode_minus'] = False
# mpl.rcParams['font.size'] = 12.0


def get_figure(w, h, dpi):
    # figure settings
    fig = plt.figure(figsize=(w, h), dpi=dpi)
    fig.subplots_adjust(right=1.0, left=0.0, bottom=0.0, top=1.0, wspace=0.1, hspace=0.1)
    ax = fig.gca()
    ax.set_axis_off()
    ax.margins(x=0.0, y=0.0)
    return ax


def rgb_shader(t, t_min=0, t_max=1, color1=(0.94, 0.02, 0.55), color2=(0.11, 0.78, 0.72)):
    t = (t-t_min)/(t_max-t_min)
    color1 = cs.rgb_to_yiq(*color1)
    color2 = cs.rgb_to_yiq(*color2)
    return cs.yiq_to_rgb(*[t * c2 + (1.00-t) * c1 for (c1, c2) in zip(color1, color2)])


def hsv_shader(t, t_min=0, t_max=1, color1=(0.00, 0.80, 0.75), color2=(1.00, 0.80, 0.75)):
    t = (t-t_min)/(t_max-t_min)
    return cs.hsv_to_rgb(*[t * c2 + (1.00-t) * c1 for (c1, c2) in zip(color1, color2)])


def cst_shader(t, t_min=0, t_max=1, color=(1.00, 0.00, 0.00)):
    return color


''' midi/sheet converters (midi: using delta time | sheet: using absolute time) '''


def track2msglist(track):
    """

    Ideas from Askmyc. Coded by Axpwyk.
    Cannot be used on type 2 midi data.

    Args:

        track : list of midi message dicts using delta time.

        there are several kinds of structure of a midi message dict, and their keys are:

        ['type(=note_on/note_off)', 'time', 'note', 'velocity', 'channel']
        ['type(=set_tempo)', 'time', 'tempo']
        ['type(=time_signature)', 'time', 'numerator', 'denominator']
        ['type(=control_change)', 'time', 'control', 'value', 'channel']
        ['type(=pitchwheel)', 'time', 'pitch', 'channel']
        etc...

        'type' : 'note_on', 'note_off', 'set_tempo', etc...
        'time' : delta time in ticks
        'note' : note number
        'velocity' : velocity
        'channel' : channel
        'tempo': ms per beat
        'control': number of midi cc
        'value': 0..127
        'pitch': -8192..8191

    Outputs:

        msglist : list of midi message dicts using absolute time.
        it means 'note_on' and 'note_off' messages are combined, while time changes to cumtime.

    """
    msglist = []
    cur_tick = 0
    cur_notes = []
    cur_lyrics = []
    for msg in track:
        # Tick accumulation. Find the current tick and record it as time1 or edt.
        cur_tick += msg['time']
        if msg['type'] == 'note_on' and msg['velocity'] > 0:
            # Put a temp note into cur_notes every time meets a 'note_on' message.
            cur_notes.append({'type': 'note', 'time1': cur_tick, 'time2': None, 'note': msg['note'],
                              'velocity_on': msg['velocity'], 'velocity_off': None, 'channel': msg['channel'], 'lyric': None})
        elif msg['type'] == 'lyrics':
            cur_lyrics.append(msg['text'])
        elif msg['type'] == 'note_off' or (msg['type'] == 'note_on' and msg['velocity'] < 1):
            # idx = [note['note'] for note in cur_notes].index(msg['note'])
            idx = 0
            cur_notes[idx]['time2'] = cur_tick - cur_notes[idx]['time1']
            cur_notes[idx]['velocity_off'] = msg['velocity']
            if cur_lyrics != []:
                cur_notes[idx]['lyric'] = cur_lyrics.pop(0)
            cur_note = cur_notes.pop(idx)
            msglist.append(cur_note)
        else:
            msg['time'] = cur_tick
            msglist.append(msg)
    return msglist


def midi2sheet(filename):
    mid = MidiFile(Path(filename))
    ticks_per_beat = mid.ticks_per_beat
    total_time = mid.length

    sheet = []
    for (i, track) in enumerate(mid.tracks):
        print(f'track {i}: {track.name}')
        track_ = []
        for msg in track:
            track_.append(msg.dict())
        sheet.append(track2msglist(track_))

    return sheet, ticks_per_beat, total_time


def msglist2track(msglist):
    pass


def sheet2midi(sheet, savepath):
    pass


''' utilities for sheet '''


def max_ticks(sheet):
    # return max ticks of all tracks
    ticks = []
    for msglist in sheet:
        ticks_ = [0]
        for msg in msglist:
            if msg['type'] == 'note':
                ticks_.append(msg['time1'] + msg['time2'])
            else:
                ticks_.append(msg['time'])
        ticks.append(max(ticks_))
    return ticks


def note2label(note, type='piano', show_group=True, mode='b'):
    if type == 'piano':
        modes = {'b': ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'],
                 '#': ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
                 '2': ['b7', '7', '1', '#1', '2', 'b3', '3', '4', '#4', '5', '#5', '6'],
                 '7b': ['2', 'b3', '3', '4', '#4', '5', '#5', '6', 'b7', '7', '1', '#1']}
        note_names = modes[mode]
        if show_group:
            return f'[{note}]{note_names[note%12]}{note//12-2}'
        else:
            return f'{note_names[note%12]}'
    elif type == 'drum':
        return ADD2_NOTE_NAMES[note]
    elif type == 'agtc':
        return AGTC_NOTE_NAMES[note]
    else:
        return None


''' classes '''


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

        # [07] set default intervals
        self._set_intervals()

        # [08] set default track colors
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

    def _get_pitchwheels(self):
        self._pitchwheels = [[msg for msg in msglist if msg['type'] == 'pitchwheel'] for msglist in self._sheet]
        _ = [msglist.sort(key=lambda msg: msg['time']) for msglist in self._pitchwheels]

    def _set_intervals(self):
        self._time_interval = None
        self._note_interval = None

    def _set_track_colors(self):
        n_track = len(self._sheet)
        self._track_colors = [hsv_shader(t, 0, n_track+1) for t in range(n_track)]

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
            raise ValueError('Please set intervals at first. You can use `use_default_intervals()` or `set_intervals()` to finish this job.')
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

    def _draw_notes(self, track=0, shader=rgb_shader, type='piano', alpha=1.0, lyric=None):
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
            _ = [self._draw_notes(t, rgb_shader, type, alpha, lyric) for t in tracks]
        elif color_scheme == 'track':
            _ = [self._draw_notes(t, lambda x, x_min, x_max: cst_shader(x, x_min, x_max, self._track_colors[t]), type, alpha, lyric) for t in tracks]

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
            color = hsv_shader(i, 0, len(controls), color1, color2)
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

    def _draw_pitchwheels(self, track=0, shader=cst_shader, plot_type='stair', alpha=1.0):
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
        else: pass

    def draw_pitchwheels(self, tracks=(0,), plot_type='stair', alpha=1.0):
        _ = [self._draw_pitchwheels(t, lambda x: cst_shader(x, 0, 1, self._track_colors[t]), plot_type, alpha) for t in tracks]

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
