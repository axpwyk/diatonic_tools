import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.transforms import TransformedBbox
import colorsys as cs
from mido import MidiFile, MidiTrack
from mido import Message, MetaMessage
from mido import bpm2tempo, tempo2bpm, tick2second, second2tick
from consts import ADD2_NOTE_NAMES, AGTC_NOTE_NAMES


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
mpl.rcParams['font.sans-serif'] = ['Consolas-with-Yahei']
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['font.size'] = 12.0


def get_figure(w, h, dpi):
    # figure settings
    fig = plt.figure(figsize=(w, h), dpi=dpi)
    fig.subplots_adjust(right=1.0, left=0.0, bottom=0.0, top=1.0, wspace=0.1, hspace=0.1)
    ax = fig.gca()
    ax.set_axis_off()
    ax.margins(x=0.0, y=0.0)
    return ax


def rgb_shader(t, t_min=0, t_max=127, color1=(0.94, 0.02, 0.55), color2=(0.11, 0.78, 0.72)):
    t = (t_max-t)/(t_max-t_min)
    color1 = cs.rgb_to_yiq(*color1)
    color2 = cs.rgb_to_yiq(*color2)
    return cs.yiq_to_rgb(*[t * c2 + (1-t) * c1 for (c1, c2) in zip(color1, color2)])


def hsv_shader(t, t_min=0, t_max=127, color1=(0.00, 0.80, 0.75), color2=(1.00, 0.80, 0.75)):
    t = (t_max-t)/(t_max-t_min)
    return cs.hsv_to_rgb(*[t * c2 + (1-t) * c1 for (c1, c2) in zip(color1, color2)])


def const_shader(t, t_min=0, t_max=127, color=(1.0, 0.0, 0.0)):
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
    for msg in track:
        # Tick accumulation. Find the current tick and record it as time1 or edt.
        cur_tick += msg['time']
        if msg['type'] == 'note_on':
            # Put a temp note into cur_notes every time meets a 'note_on' message.
            cur_notes.append({'type': 'note', 'time1': cur_tick, 'time2': None,
                              'note': msg['note'], 'velocity_on': msg['velocity'], 'velocity_off': None, 'channel': msg['channel']})
        elif msg['type'] == 'note_off':
            idx = [note['note'] for note in cur_notes].index(msg['note'])
            cur_notes[idx]['time2'] = cur_tick - cur_notes[idx]['time1']
            cur_notes[idx]['velocity_off'] = msg['velocity']
            cur_note = cur_notes.pop(idx)
            msglist.append(cur_note)
        else:
            msg['time'] = cur_tick
            msglist.append(msg)
    return msglist


def midi2sheet(filename):
    mid = MidiFile(filename)
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


def max_tick(sheet):
    # return max tick of all tracks
    ticks = []
    for msglist in sheet:
        ticks_ = [0]
        for msg in msglist:
            if msg['type'] == 'note':
                ticks_.append(msg['time1'] + msg['time2'])
            else:
                ticks_.append(msg['time'])
        ticks.append(max(ticks_))
    return max(ticks)


def note2label(note, type='piano', show_group=True):
    if type == 'piano':
        modes = {'b': ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'],
                 '#': ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
                 '2': ['x', '7', '1', 'x', '2', 'x', '3', '4', 'x', '5', 'x', '6'],
                 '7b': ['2', 'x', '3', '4', 'x', '5', 'x', '6', 'x', '7', '1', '']}
        note_names = modes['b']
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
        self.sheet = sheet
        self.ticks_per_beat = ticks_per_beat
        self.max_tick = max_tick(sheet)
        self._set_intervals((0, self.max_tick), (48, 72))

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

        # [07] msglists to show
        self.msglist_numbers = [0]

        # [08] define chords
        self.chords0 = [[2*1920, 'Cm'], [4*1920, 'Ab'], [5*1920-240, 'Gm'],
                      [6*1920, 'Cm'], [8*1920, 'Ab'], [9*1920-240, 'Gm'], [10*1920, 'X']]

    def _get_notes(self):
        self.notes = [[msg for msg in msglist if msg['type'] == 'note'] for msglist in self.sheet]

    def _get_set_tempos(self):
        self.set_tempos = [msg for msg in sum(self.sheet, []) if msg['type'] == 'set_tempo']
        self.set_tempos.sort(key=lambda msg: msg['time'])

        if self.set_tempos == []:
            self.set_tempos.insert(0, dict(type='set_tempo', tempo=500000, time=0))

        tempos = [msg['tempo'] for msg in self.set_tempos]
        self.bpm_range = (round(tempo2bpm(max(tempos)))-1, round(tempo2bpm(min(tempos)))+1)

    def _get_time_signatures(self):
        self.time_signatures = [msg for msg in sum(self.sheet, []) if msg['type'] == 'time_signature']
        self.time_signatures.sort(key=lambda msg: msg['time'])

        if self.time_signatures == []:
            self.time_signatures.insert(0, dict(type='time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))

    def _get_control_changes(self):
        self.control_changes = [[msg for msg in msglist if msg['type'] == 'control_change'] for msglist in self.sheet]
        _ = [msglist.sort(key=lambda msg: msg['time']) for msglist in self.control_changes]
        self.used_controls = [list({msg['control'] for msg in msglist}) for msglist in self.control_changes]

        print('used controls:')
        for k, msglist in enumerate(self.used_controls):
            print(f'msglist {k}: {msglist}')

    def _get_pitchwheels(self):
        self.pitchwheels = [[msg for msg in msglist if msg['type'] == 'pitchwheel'] for msglist in self.sheet]
        _ = [msglist.sort(key=lambda msg: msg['time']) for msglist in self.pitchwheels]

    def _set_intervals(self, tick_interval, note_interval):
        self.tick_interval = tick_interval
        self.note_interval = note_interval

    # ---------------------------------------------------------------------------------------------------- #

    def set_intervals(self, tick_interval, note_interval):
        self._set_intervals(tick_interval, note_interval)
        plt.clf()

    def draw_pianoroll(self, height=8, aspect_note=4, dpi=36, splits_per_beat=4, type='piano'):
        """

        Draw pianoroll with meta information.

        * variable's name ending with 's' means it is a list (multi variables)
        * list variable's name ending with '0' means it may contain messages whose time is out of tick_interval

        Some abbreviations:

        * note              -> note
        * set_tempo         -> st
        * time_signature    -> ts
        * control_change    -> cc
        * pitchwheel        -> pw

        """

        ''' [01] pianoroll meta params '''

        bottom_lane_h = 5
        self.bottom_lane_h = bottom_lane_h
        top_lane_h = 3

        bottom = self.note_interval[0] - bottom_lane_h
        self.bottom = bottom
        top = self.note_interval[1] + top_lane_h

        aspect_keyboard = {'piano': 4, 'drum': 6, 'agtc': 6}[type]

        width = height*(aspect_keyboard+aspect_note*length(*self.tick_interval)/self.ticks_per_beat)/(top-bottom)
        axis_ratio = (aspect_keyboard/aspect_note*self.ticks_per_beat+length(*self.tick_interval))/(aspect_keyboard+aspect_note*length(*self.tick_interval)/self.ticks_per_beat)
        keyboard_width = aspect_keyboard * axis_ratio

        left = self.tick_interval[0] - keyboard_width
        right = self.tick_interval[1]

        fontsize = 49*height/(length(*self.note_interval)+bottom_lane_h+top_lane_h)
        self.fontsize = fontsize
        markersize = 25*height/(length(*self.note_interval)+bottom_lane_h+top_lane_h)
        self.markersize = markersize

        ''' [02] set_tempos parsing '''

        sts0 = [[msg['time'], msg['tempo']] for msg in self.set_tempos]
        k_left = len(sts0)-1-[pw[0]<=self.tick_interval[0] for pw in sts0][::-1].index(True)
        k_right = len(sts0)-1-[pw[0]<=self.tick_interval[1] for pw in sts0][::-1].index(True)
        sts = [[self.tick_interval[0], sts0[k_left][1]]] + [pw for pw in sts0 if self.tick_interval[0]<pw[0]<self.tick_interval[1]] + [[self.tick_interval[1], sts0[k_right][1]]]

        ''' [03] time_signatures parsing '''

        # put all time_signatures into a list and append an end to the list
        tss0 = [[msg['time'], msg['numerator'], msg['denominator']] for msg in self.time_signatures]
        tss0.append([self.tick_interval[1], tss0[-1][1], tss0[-1][2]])
        tss = [ts for ts in tss0 if inrange(ts[0], *self.tick_interval)]
        # get a list of ticks_per_beat corresponding to time_signatures (because tpb changes with ts denominator)
        tpbs0 = [4*self.ticks_per_beat//ts[2] for ts in tss0]
        # calculate delta x of three types of vertical line: bar-line, beat-line and split-line
        # step1 and step2 are changing with time_signatures, so they become step1s and step2s
        # step1: bar-line | step2: beat-line | step3: split-line
        # step1[k] = 4*self.ticks_per_beat*(nu[k]/de[k])
        # step2[k] = 4*self.ticks_per_beat*(1/de[k])
        step1s = [tpb*tss0[i][1] for (i, tpb) in enumerate(tpbs0)]
        step2s = tpbs0
        step3 = self.ticks_per_beat//splits_per_beat
        # x1s0 = [range(stt_0, stt_1, step1s[0]), range(stt_1, stt_2, step1s[1]), ..., range(stt_n, self.tick_interval[1], step1s[n])]
        # x1s0[n][k] is x of the k-th bar-line after n-th time_signature
        x1s0 = [list(range(tss0[k][0], tss0[k+1][0], step1s[k])) for k in range(len(step1s)-1)]
        x1s = [x1 for x1 in sum(x1s0, []) if inrange(x1, *self.tick_interval)]
        x2s0 = [list(range(tss0[k][0], tss0[k+1][0], step2s[k])) for k in range(len(step2s)-1)]
        x2s = [x2 for x2 in sum(x2s0, []) if inrange(x2, *self.tick_interval) and x2 not in x1s]
        x3s0 = [k*step3 for k in range(self.tick_interval[0]//step3, self.tick_interval[1]//step3+1)]
        x3s = [x3 for x3 in x3s0 if inrange(x3, *self.tick_interval) and x3 not in x1s+x2s]
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
        bl_rect = plt.Rectangle((self.tick_interval[0], bottom), length(*self.tick_interval), bottom_lane_h, facecolor='#ddeeff', lw=0.0, zorder=0)
        ax.add_patch(bl_rect)
        # main area rectangle
        main_rect = plt.Rectangle((self.tick_interval[0], self.note_interval[0]), length(*self.tick_interval), length(*self.note_interval), facecolor='#ddeeff', lw=0.0, zorder=0)
        ax.add_patch(main_rect)
        # top lane rectangle
        tl_rect = plt.Rectangle((left, self.note_interval[1]), right-left, 3, facecolor='#ffffff', lw=0.0, zorder=0)
        ax.add_patch(tl_rect)
        # background keys
        white_notes = [note for note in range(*self.note_interval) if note % 12 in [0, 2, 4, 5, 7, 9, 11]]
        black_notes = [note for note in range(*self.note_interval) if note % 12 in [1, 3, 6, 8, 10]]
        white_bg_rects = [plt.Rectangle((self.tick_interval[0], note), length(*self.tick_interval), 1, facecolor='#ffffff', lw=0.0, zorder=1) for note in white_notes]
        black_bg_rects = [plt.Rectangle((self.tick_interval[0], note), length(*self.tick_interval), 1, facecolor='#ddcccc', lw=0.0, zorder=1) for note in black_notes]
        _ = [ax.add_patch(rect) for rect in white_bg_rects+black_bg_rects]
        # left bottom rectangle
        lb_rect = plt.Rectangle((left, bottom), keyboard_width, bottom_lane_h, facecolor='#ffffff', lw=0.0, zorder=4)
        ax.add_patch(lb_rect)
        plt.annotate(f'bpm\n{self.bpm_range[0]}..{self.bpm_range[1]}\n\nvel\n0..127', (left+keyboard_width/2, bottom+bottom_lane_h/2), color='#555555',
                     va='center', ha='center', fontsize=fontsize, zorder=4.1, clip_box=TransformedBbox(lb_rect.get_bbox(), ax.transData))
        # keyboard
        white_kbd_rects = [plt.Rectangle((left, note), keyboard_width, 1, facecolor='#ffffff', lw=0.0, zorder=4) for note in white_notes]
        black_kbd_rects = [plt.Rectangle((left, note), keyboard_width, 1, facecolor='#222222', lw=0.0, zorder=4) for note in black_notes]
        _ = [ax.add_patch(rect) for rect in white_kbd_rects+black_kbd_rects]
        # split lines of keys
        _ = [plt.plot([left, self.tick_interval[0]], [note, note], color='#222222', lw=0.5, solid_capstyle='butt', zorder=4.1) for note in range(*self.note_interval)]
        # text on keys
        _ = [plt.annotate(note2label(note, type=type), (left+keyboard_width//16, note+0.5), color='#555555', va='center', fontsize=fontsize, zorder=4.1,
                          clip_box=TransformedBbox(white_kbd_rects[k].get_bbox(), ax.transData)) for (k, note) in enumerate(white_notes)]
        _ = [plt.annotate(note2label(note, type=type), (left+keyboard_width//16, note+0.5), color='#ffffff', va='center', fontsize=fontsize, zorder=4.1,
                          clip_box=TransformedBbox(black_kbd_rects[k].get_bbox(), ax.transData)) for (k, note) in enumerate(black_notes)]
        # horizontal grid lines
        _ = [plt.plot(self.tick_interval, [note, note], color='#999999', lw=0.5, solid_capstyle='butt', zorder=2) for note in range(self.note_interval[0]+1, self.note_interval[1])]
        # vertical grid lines
        _ = [plt.plot([x, x], [bottom, self.note_interval[1]], color='#aaaaaa', lw=0.5, solid_capstyle='butt', zorder=2.1) for x in x3s]
        _ = [plt.plot([x, x], [bottom, self.note_interval[1]], color='#555555', lw=0.5, solid_capstyle='butt', zorder=2.1) for x in x2s]
        _ = [plt.plot([x, x], [bottom, self.note_interval[1]], color='#222222', lw=1.0, solid_capstyle='butt', zorder=2.1) for x in x1s]
        # horizontal split lines
        plt.plot(self.tick_interval, [self.note_interval[0], self.note_interval[0]], color='#555555', lw=0.5, solid_capstyle='butt', zorder=2)
        plt.plot([left, self.tick_interval[1]], [self.note_interval[1], self.note_interval[1]], color='#555555', lw=0.5, solid_capstyle='butt', zorder=6.1)
        plt.plot([left, self.tick_interval[1]], [self.note_interval[1]+1, self.note_interval[1]+1], color='#555555', lw=0.5, solid_capstyle='butt', zorder=6.1)
        plt.plot([left, self.tick_interval[1]], [self.note_interval[1]+2, self.note_interval[1]+2], color='#555555', lw=0.5, solid_capstyle='butt', zorder=6.1)
        # vertical split lines
        plt.plot([self.tick_interval[0], self.tick_interval[0]], [bottom, self.note_interval[1]], color='#555555', lw=0.5, solid_capstyle='butt', zorder=6)
        # chords
        chords = [chord for chord in self.chords0 if inrange(chord[0], *self.tick_interval)]
        _ = [plt.annotate(chord[1], (chord[0], self.note_interval[1]+0.5), color='#555555', va='center', ha='center', fontsize=fontsize) for chord in chords]

        ''' [02] draw set_tempos '''

        def _bpm2vel(bpm):
            bpm_lower = self.bpm_range[0]
            bpm_upper = self.bpm_range[1]
            lam = (bpm_upper - bpm) / (bpm_upper - bpm_lower)
            return lam*(self.note_interval[0]-bottom_lane_h)+(1-lam)*self.note_interval[0]
        sts_x = [st[0] for st in sts]
        sts_y = [_bpm2vel(tempo2bpm(st[1])) for st in sts]
        plt.plot(sts_x, sts_y, color='#ee5511', lw=1.0, solid_capstyle='butt', solid_joinstyle='bevel', zorder=2.9, label='tempo')

        ''' [03] draw time_signatures '''

        # time_signature labels
        _ = [plt.annotate(f'{ts[1]}/{ts[2]}', (ts[0], self.note_interval[1]+1.5), color='#555555', va='center', ha='center', fontsize=fontsize) for ts in tss]
        # bar labels
        _ = [plt.annotate(l1, (x1, self.note_interval[1]+2.5), color='#555555', va='center', ha='center', fontsize=fontsize) for (x1, l1) in zip(x1s, l1s)]
        # beat labels
        _ = [plt.annotate(l2, (x2, self.note_interval[1]+2.5), fontsize=fontsize*3/4, color='#555555', va='center', ha='center') for (x2, l2) in zip(x2s, l2s)]

    def draw_notes(self, track=0, shader=rgb_shader, type='piano', channel=0):
        """ draw notes """

        ''' notes parsing '''

        # divide notes both in note_interval and tick_interval into 3 parts: left, full and right
        notes0 = [note for note in self.notes[track] if inrange(note['note'], *self.note_interval)]
        notes = [note for note in notes0 if inrange(note['time1'], *self.tick_interval) or inrange(note['time1']+note['time2'], *self.tick_interval)]
        notes_full = [note for note in notes if inrange(note['time1'], *self.tick_interval) and inrange(note['time1']+note['time2'], *self.tick_interval)]
        notes_left = [note for note in notes if note['time1'] < self.tick_interval[0] <= note['time1'] + note['time2']]
        notes_right = [note for note in notes if note['time1'] < self.tick_interval[1] <= note['time1'] + note['time2']]
        notes_rearranged = notes_full + notes_left + notes_right
        # getting rectangles of notes for pianoroll
        notes_full_rects = [plt.Rectangle((note['time1'], note['note']), note['time2'], 1,
                                          color=shader(note['velocity_on']), joinstyle='round', lw=0.0, zorder=5+0.001*track) for note in notes_full]
        notes_left_rects = [plt.Rectangle((self.tick_interval[0], note['note']), note['time2']-self.tick_interval[0]+note['time1'], 1,
                                          color=shader(note['velocity_on']), joinstyle='round', lw=0.0, zorder=5+0.001*track) for note in notes_left]
        notes_right_rects = [plt.Rectangle((note['time1'], note['note']), self.tick_interval[1]-note['time1'], 1,
                                           color=shader(note['velocity_on']), joinstyle='round', lw=0.0, zorder=5+0.001*track) for note in notes_right]
        notes_rects = notes_full_rects + notes_left_rects + notes_right_rects

        ''' draw notes '''

        ax = plt.gca()
        _ = [ax.add_patch(rect) for rect in notes_rects]
        # note edge
        _ = [plt.plot([note['time1'], note['time1']+note['time2'], note['time1']+note['time2'], note['time1'], note['time1']],
                      [note['note'], note['note'], note['note']+1, note['note']+1, note['note']],
                      color='#123456', lw=0.5, solid_capstyle='round', zorder=5+0.001*(track+0.2)) for note in notes_full]
        _ = [plt.plot([self.tick_interval[0], note['time1']+note['time2'], note['time1']+note['time2'], self.tick_interval[0]],
                      [note['note'], note['note'], note['note']+1, note['note']+1],
                      color='#123456', lw=0.5, solid_capstyle='round', zorder=5+0.001*(track+0.2)) for note in notes_left]
        _ = [plt.plot([self.tick_interval[1], note['time1'], note['time1'], self.tick_interval[1]],
                      [note['note']+1, note['note']+1, note['note'], note['note']],
                      color='#123456', lw=0.5, solid_capstyle='round', zorder=5+0.001*(track+0.2)) for note in notes_right]
        # note label
        _ = [plt.annotate(note2label(note['note'], type='piano', show_group=False), (note['time1']+self.ticks_per_beat//16, note['note']+0.5),
                          color='#ffffff', va='center', fontsize=self.fontsize, zorder=5+0.001*(track+0.1),
                          clip_box=TransformedBbox(notes_rects[k].get_bbox(), ax.transData)) for (k, note) in enumerate(notes_rearranged)]
        # note channel
        # if channel:
        #     _ = [plt.annotate(note['channel'], (note['time1']+self.ticks_per_beat//16, note['note']+1.5),
        #                       color='#555555', va='center', fontsize=self.fontsize, zorder=5+0.001*(track+0.1)) for (k, note) in enumerate(notes_rearranged)]
        # note lyric
        # lrc = list(range(1000))
        # _ = [plt.annotate(lrc[k%1000], (note['time1']+self.ticks_per_beat//16, note['note']-0.5),
        #                   color='#555555', va='center', fontsize=self.fontsize, zorder=5+0.001*(track+0.1)) for (k, note) in enumerate(notes_rearranged)]
        # on-velocity
        notes_full_vels = [plt.Line2D([note['time1'], note['time1']], [self.bottom, self.bottom+note['velocity_on']/127*self.bottom_lane_h],
                                      color=shader(note['velocity_on']), lw=1.0, solid_capstyle='butt', zorder=3+0.001*track,
                                      marker='x', markevery=[1], markersize=self.markersize, mew=1) for note in notes_full+notes_right]
        _ = [ax.add_line(vel) for vel in notes_full_vels]

    def draw_control_changes(self, track=0, shader=hsv_shader, channel=0):
        """ draw control_changes """

        ''' control_changes parsing '''

        ccs0 = dict.fromkeys(self.used_controls[track], [])
        ccs = dict.fromkeys(self.used_controls[track], [])
        for control in self.used_controls[track]:
            ccs0[control] = [[msg['time'], msg['value']] for msg in self.control_changes[track] if msg['control'] == control]
            # add default value
            ccs0[control].insert(0, [0, 0])
            k_left = len(ccs0[control])-1-[cc[0]<=self.tick_interval[0] for cc in ccs0[control]][::-1].index(True)
            k_right = len(ccs0[control])-1-[cc[0]<=self.tick_interval[1] for cc in ccs0[control]][::-1].index(True)
            ccs[control] = [[self.tick_interval[0], ccs0[control][k_left][1]]] + \
                           [cc for cc in ccs0[control] if self.tick_interval[0]<cc[0]<self.tick_interval[1]] + \
                           [[self.tick_interval[1], ccs0[control][k_right][1]]]

        ''' draw control_changes '''

        ccs_stts = dict.fromkeys(self.used_controls[track], [])
        ccs_values = dict.fromkeys(self.used_controls[track], [])
        for i, control in enumerate(self.used_controls[track]):
            ccs_stts[control] = [cc[0] for cc in ccs[control]]
            ccs_values[control] = [cc[1]/128*length(*self.note_interval)+self.note_interval[0] for cc in ccs[control]]
            plt.plot(ccs_stts[control], ccs_values[control], color=shader(i, 1, len(self.used_controls[track])+1),
                     lw=0.75, ls='--', solid_capstyle='butt', solid_joinstyle='bevel', zorder=2.9+0.001*(track+0.1*control), label=f'[track {track}] cc{control}')

    def draw_pitchwheels(self, track=0, shader=const_shader, channel=0):
        """ draw pitchwheels """

        ''' [06] pitchwheels parsing '''
        pws0 = [[msg['time'], msg['pitch']] for msg in self.pitchwheels[track]]
        # add default value
        pws0.insert(0, [0, 0])
        k_left = len(pws0)-1-[pw[0]<=self.tick_interval[0] for pw in pws0][::-1].index(True)
        k_right = len(pws0)-1-[pw[0]<=self.tick_interval[1] for pw in pws0][::-1].index(True)
        pws = [[self.tick_interval[0], pws0[k_left][1]]] + [pw for pw in pws0 if self.tick_interval[0]<pw[0]<self.tick_interval[1]] + [[self.tick_interval[1], pws0[k_right][1]]]

        ''' [06] draw pitchwheels '''

        pws_stts = [pw[0] for pw in pws]
        pws_pits = [pw[1]/16384*length(*self.note_interval)+middle(*self.note_interval) for pw in pws]
        plot_type = ['piecewise', 'stair', 'none'][1]
        if plot_type == 'piecewise':
            plt.plot(pws_stts, pws_pits, color=shader(1), lw=1.0, solid_capstyle='butt', solid_joinstyle='bevel', zorder=2.9+0.001*track, label=f'[track {track}] pitchwheel')
        elif plot_type == 'stair':
            plt.step(pws_stts, pws_pits, color=shader(1), lw=1.0, solid_capstyle='butt', zorder=2.9+0.001*track, label=f'[track {track}] pitchwheel')
        else: pass

    def show_legends(self):
        plt.legend(loc='lower right', fontsize=self.fontsize)

    # ---------------------------------------------------------------------------------------------------- #

    def get_tick_range(self):
        return 0, self.max_tick

    def get_note_range(self, track):
        notes = [note['note'] for note in self.notes[track]]
        note_min = min(notes) - 1 if notes != [] else 48
        note_max = max(notes) + 2 if notes != [] else 72
        return note_min, note_max
