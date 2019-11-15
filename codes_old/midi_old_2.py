import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.transforms import TransformedBbox
import colorsys as cs
from mido import MidiFile, MidiTrack
from mido import Message, MetaMessage
from mido import bpm2tempo, tempo2bpm, tick2second, second2tick
from consts import ADD2_NOTE_NAMES

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


def rgb_shader(t, t_min=0, t_max=127):
    t = (t_max-t)/(t_max-t_min)
    color1 = [240/255, 53/255, 140/255]
    color2 = [27/255, 200/255, 184/255]
    color1 = cs.rgb_to_yiq(*color1)
    color2 = cs.rgb_to_yiq(*color2)
    return cs.yiq_to_rgb(*[t * c2 + (1-t) * c1 for (c1, c2) in zip(color1, color2)])


def hsv_shader(t, t_min=0, t_max=15):
    t = (t_max-t)/(t_max-t_min)
    color1 = [0, 0.8, 0.75]
    color2 = [1, 0.8, 0.75]
    return cs.hsv_to_rgb(*[t * c2 + (1-t) * c1 for (c1, c2) in zip(color1, color2)])


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
    else:
        return None


''' classes '''


class Pianoroll(object):
    '''

    Generate a pianoroll using matplotlib.

    * list variable's name ending with '0' means it may contain messages whose time1 is out of tick_interval
    * variable's name ending with 's' means it is a list (multi variables)

    Some abbreviations:

    * note              -> note
    * set_tempo         -> st
    * time_signature    -> ts
    * control_change    -> cc
    * pitchwheel        -> pw

    '''
    def __init__(self, sheet, ticks_per_beat):
        """ pianoroll initialization, extract messages of same kind from sheet """
        # [01] get data
        self.sheet = sheet
        self.ticks_per_beat = ticks_per_beat
        self.max_tick = max_tick(sheet)

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
        self.chds0 = [[2*1920, 'Cm'], [4*1920, 'Ab'], [5*1920-240, 'Gm'],
                      [6*1920, 'Cm'], [8*1920, 'Ab'], [9*1920-240, 'Gm'], [10*1920, 'X']]

    def _get_notes(self):
        self.notes = [[msg for msg in msglist if msg['type'] == 'note'] for msglist in self.sheet]

    def _get_set_tempos(self):
        self.set_tempos = [msg for msg in sum(self.sheet, []) if msg['type'] == 'set_tempo']
        self.set_tempos.sort(key=lambda msg: msg['time'])

        if self.set_tempos == []:
            self.set_tempos.insert(0, dict(type='set_tempo', tempo=500000, time=0))

        tempos = [msg['tempo'] for msg in self.set_tempos]
        self.bpm_range = (round(tempo2bpm(max(tempos))), round(tempo2bpm(min(tempos))))

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

    # ---------------------------------------------------------------------------------------------------- #

    def _draw_pianoroll_whdpi(self):
        pass

    def _draw_pianoroll_hadpi(self, height=8, aspect_note=2, dpi=36, note_interval=(48, 72), tick_interval=(0, 1920*2), type='piano'):
        # aspect_note and aspect_keyboard mean visual width-to-height ratio
        # [01] get pianoroll meta parameters
        aspect_keyboard = 4
        self.note_interval = note_interval
        self.tick_interval = tick_interval

        self.velocity_lane_height = 5
        self.top_lane_numbers = 3
        self.right_panel_width = 0

        self.bottom = self.note_interval[0] - self.velocity_lane_height
        self.top = self.note_interval[1] + self.top_lane_numbers
        total_beats = length(*self.tick_interval)/self.ticks_per_beat
        width = height*(aspect_keyboard+aspect_note*total_beats)/(self.top-self.bottom)
        axis_ratio = (aspect_keyboard/aspect_note*self.ticks_per_beat+length(*self.tick_interval))/(aspect_keyboard+aspect_note*total_beats)
        self.keyboard_width = aspect_keyboard*axis_ratio

        self.left = self.tick_interval[0] - self.keyboard_width
        self.right = self.tick_interval[1] + self.right_panel_width

        self.fontsize = 45*height/(length(*self.note_interval)+8)

        # ---------------------------------------------------------------------------------------------------- #

        # [02] draw pianoroll
        ## get axes
        ax = get_figure(width, height, dpi)
        ## draw the largest rectangle
        largest_rect = plt.Rectangle((self.left, self.bottom), self.right-self.left, self.top-self.bottom, facecolor='none', edgecolor='#555555', lw=0.75, joinstyle='round', zorder=7)
        ax.add_patch(largest_rect)
        ## draw velocity lane rectangle
        vel_rect = plt.Rectangle((self.tick_interval[0], self.bottom), length(*self.tick_interval), self.velocity_lane_height, facecolor='#ddeeff', lw=0.0, zorder=0)
        ax.add_patch(vel_rect)
        ## draw main area rectangle
        main_rect = plt.Rectangle((self.tick_interval[0], self.note_interval[0]), length(*self.tick_interval), length(*self.note_interval), facecolor='#ddeeff', lw=0.0, zorder=0)
        ax.add_patch(main_rect)
        ## draw top lane rectangle
        ruler_rect = plt.Rectangle((self.left, self.note_interval[1]), self.right-self.left, 3, facecolor='#ffffff', lw=0.0, zorder=0)
        ax.add_patch(ruler_rect)
        ## draw background keys
        white_notes = [notes for notes in range(*self.note_interval) if notes % 12 in [0, 2, 4, 5, 7, 9, 11]]
        black_notes = [notes for notes in range(*self.note_interval) if notes % 12 in [1, 3, 6, 8, 10]]
        white_bg_rects = [plt.Rectangle((self.tick_interval[0], notes), length(*self.tick_interval), 1, facecolor='#ffffff', lw=0.0, zorder=1) for notes in white_notes]
        black_bg_rects = [plt.Rectangle((self.tick_interval[0], notes), length(*self.tick_interval), 1, facecolor='#ddcccc', lw=0.0, zorder=1) for notes in black_notes]
        _ = [ax.add_patch(rect) for rect in white_bg_rects+black_bg_rects]
        ## draw left bottom rectangle
        left_bottom_rect = plt.Rectangle((self.left, self.bottom), self.keyboard_width, self.velocity_lane_height, facecolor='#ffffff', lw=0.0, zorder=4)
        ax.add_patch(left_bottom_rect)
        ## draw keys
        white_kbd_rects = [plt.Rectangle((self.left, nn), self.keyboard_width, 1, facecolor='#ffffff', lw=0.0, zorder=4) for nn in white_notes]
        black_kbd_rects = [plt.Rectangle((self.left, nn), self.keyboard_width, 1, facecolor='#222222', lw=0.0, zorder=4) for nn in black_notes]
        _ = [ax.add_patch(rect) for rect in white_kbd_rects+black_kbd_rects]
        ### draw split lines of keys
        _ = [plt.plot([self.left, self.tick_interval[0]], [nn, nn], color='#222222', lw=0.5, solid_capstyle='butt', zorder=4.1) for nn in range(*self.note_interval)]
        plt.plot([self.left, self.tick_interval[0]], [self.note_interval[1], self.note_interval[1]], color='#222222', lw=0.5, solid_capstyle='butt', zorder=4.1)
        ### show text on keys
        _ = [plt.annotate(note2label(note, type=type), (self.left+self.keyboard_width//16, note+0.5), color='#555555', va='center', fontsize=self.fontsize, zorder=4.1,
                          clip_box=TransformedBbox(white_kbd_rects[k].get_bbox(), ax.transData)) for (k, note) in enumerate(white_notes)]
        _ = [plt.annotate(note2label(note, type=type), (self.left+self.keyboard_width//16, note+0.5), color='#ffffff', va='center', fontsize=self.fontsize, zorder=4.1,
                          clip_box=TransformedBbox(black_kbd_rects[k].get_bbox(), ax.transData)) for (k, note) in enumerate(black_notes)]
        ## split lines
        ### horizontal
        plt.plot(self.tick_interval, [self.note_interval[0], self.note_interval[0]], color='#555555', lw=0.5, solid_capstyle='butt', zorder=2)
        plt.plot(self.tick_interval, [self.note_interval[1], self.note_interval[1]], color='#555555', lw=0.5, solid_capstyle='butt', zorder=2)
        plt.plot([self.left, self.tick_interval[1]], [self.note_interval[1]+1, self.note_interval[1]+1], color='#555555', lw=0.5, solid_capstyle='butt', zorder=2)
        plt.plot([self.left, self.tick_interval[1]], [self.note_interval[1]+2, self.note_interval[1]+2], color='#555555', lw=0.5, solid_capstyle='butt', zorder=2)
        ### vertical
        plt.plot([self.tick_interval[0], self.tick_interval[0]], [self.bottom, self.note_interval[1]], color='#ee2222', lw=1.0, solid_capstyle='butt', zorder=6.1)

    def _show_grid_and_time_signature(self, splits_per_beat=4):
        # [02] time_signature parsing
        ## put all time_signatures into a list and append an end to the list
        tss0 = [[msg['time1'], msg['nu'], msg['de']] for msg in self.time_signatures]
        tss0.append([self.tick_interval[1], tss0[-1][1], tss0[-1][2]])
        ## get a list of ticks_per_beat corresponding to time_signatures (because tpb changes with ts denominator)
        tpbs0 = [4*self.ticks_per_beat//ts[2] for ts in tss0]
        ## calculate delta x of three types of vertical line: bar-line, beat-line and split-line
        ## step1 and step2 are changing with time_signatures, so they become step1s and step2s
        ## step1: bar-line | step2: beat-line | step3: split-line
        ## step1[k] = 4*self.ticks_per_beat*(nu[k]/de[k])
        ## step2[k] = 4*self.ticks_per_beat*(1/de[k])
        step1s = [tpb*tss0[i][1] for (i, tpb) in enumerate(tpbs0)]
        step2s = tpbs0
        step3 = self.ticks_per_beat//splits_per_beat
        ## x1s0 = [range(time1_0, time1_1, step1s[0]), range(time1_1, time1_2, step1s[1]), ..., range(time1_n, self.tick_interval[1], step1s[n])]
        ## x1s0[n][k] is x of the k-th bar-line after n-th time_signature
        x1s0 = [list(range(tss0[k][0], tss0[k+1][0], step1s[k])) for k in range(len(step1s)-1)]
        x1s = [x1 for x1 in sum(x1s0, []) if inrange(x1, *self.tick_interval)]
        x2s0 = [list(range(tss0[k][0], tss0[k+1][0], step2s[k])) for k in range(len(step2s)-1)]
        x2s = [x2 for x2 in sum(x2s0, []) if inrange(x2, *self.tick_interval) and x2 not in x1s]
        x3s0 = [k*step3 for k in range(self.tick_interval[0]//step3, self.tick_interval[1]//step3+1)]
        x3s = [x3 for x3 in x3s0 if inrange(x3, *self.tick_interval) and x3 not in x1s+x2s]
        ## l1s0: bar labels with x coord | l2s0: beat labels with x coord
        l1s0 = list(enumerate(sum(x1s0, [])))
        l1s = [l1[0] for l1 in l1s0 if l1[1] in x1s]
        l2s0 = sum([[[j % tss0[i][1], x2] for (j, x2) in enumerate(x2s0_section)] for (i, x2s0_section) in enumerate(x2s0)], [])
        l2s = [l2[0] for l2 in l2s0 if l2[1] in x2s]

        ## draw horizontal lines

        _ = [plt.plot(self.tick_interval, [note, note], color='#999999', lw=0.5, solid_capstyle='butt', zorder=2)
             for note in range(self.note_interval[0]+1, self.note_interval[1])]

        ## draw vertical lines

        _ = [plt.plot([x, x], [self.bottom, self.note_interval[1]], color='#aaaaaa', lw=0.5, solid_capstyle='butt', zorder=2.1) for x in x3s]
        _ = [plt.plot([x, x], [self.bottom, self.note_interval[1]], color='#555555', lw=0.5, solid_capstyle='butt', zorder=2.1) for x in x2s]
        _ = [plt.plot([x, x], [self.bottom, self.note_interval[1]], color='#222222', lw=1.0, solid_capstyle='butt', zorder=2.1) for x in x1s]

    def _draw_notes(self):
        pass

    def _draw_set_tempos(self):
        text = f'bpm\n\n{self.bpm_range[0]}..{self.bpm_range[1]}'
        plt.annotate(text, (self.left+self.keyboard_width/2, self.bottom+self.velocity_lane_height/2), color='#555555', va='center', ha='center', fontsize=self.fontsize, zorder=4.1,
                     clip_box=TransformedBbox(left_bottom_rect.get_bbox(), ax.transData))

    def _show_time_signatures(self):


        # [04] draw time_signatures
        ## time_signature changes
        tss = [ts for ts in tss0 if inrange(ts[0], *self.tick_interval)]
        _ = [plt.annotate(f'{ts[1]}/{ts[2]}', (ts[0], self.note_interval[1]+1.5), color='#555555', va='center', ha='center', fontsize=fontsize) for ts in tss]
        ## bar labels
        _ = [plt.annotate(l1, (x1, self.note_interval[1]+2.5), color='#555555', va='center', ha='center', fontsize=fontsize) for (x1, l1) in zip(x1s, l1s)]
        ## beat labels
        _ = [plt.annotate(l2, (x2, self.note_interval[1]+2.5), fontsize=fontsize*3/4, color='#555555', va='center', ha='center') for (x2, l2) in zip(x2s, l2s)]

    def _show_chords(self):
        chds = [chd for chd in self.chds0 if inrange(chd[0], *self.self.tick_interval)]
        _ = [plt.annotate(chd[1], (chd[0], self.note_interval[1]+0.5), color='#555555', va='center', ha='center', fontsize=self.fontsize) for chd in chds]

    def _draw_control_changes(self):
        pass

    def _draw_pitchwheels(self):
        pass

    # ---------------------------------------------------------------------------------------------------- #

    def get_tick_range(self):
        return 0, self.max_tick

    def get_nn_range(self, number_of_msglist):
        nns = [note['note'] for note in self.notes[number_of_msglist]]
        nn_min = min(nns) - 1
        nn_max = max(nns) + 2
        return nn_min, nn_max

    def draw(self):
        self._draw_pianoroll_hadpi()
        self._show_grid()