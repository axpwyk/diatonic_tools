import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.transforms import TransformedBbox
import colorsys as cs
from mido import MidiFile, MidiTrack
from mido import Message, MetaMessage
from mido import bpm2tempo, tempo2bpm, tick2second, second2tick
from consts import NOTE_NAMES

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


''' midi/sheet converters '''


def track2msglist(track):
    """

    Ideas from Askmyc. Coded by Axpwyk.
    Cannot be used on type 2 midi data.

    Args:

        track : list of midi message dicts.

        there are several kinds of structure of a midi message dict, and their keys are:

        ['type(=note_on/note_off)', 'time', 'note', 'velocity', 'channel']
        ['type(=set_tempo)', 'time', 'tempo']
        ['type(=time_signature)', 'time', 'numerator', 'denominator']
        ['type(=control_change)', 'time', 'control', 'value', 'channel']
        ['type(=pitchwheel)', 'time', 'pitch', 'channel']

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

        msglist : list of notes, set_tempos, time_signatures, ccs and pitchwheels.

        dict keys of a note : ['type', 'stt', 'lst', 'nn', 'vel_on', 'vel_off', 'ch']
        dict keys of a set_tempo: ['type', 'stt', 'tpo']
        dict keys of a time_signature: ['type', 'stt', 'nu', 'de']
        dict keys of a control_change: ['type', 'stt', 'cn', 'value', 'ch']
        dict keys of a pitchwheel: ['type', 'stt', 'pit', 'ch']

        'stt' : starting time in ticks
        'lst' : lasting time in ticks
        'edt' : ending time in ticks (not in the note structure)
        'nn' : note number
        'vel_on' : on velocity
        'vel_off' : off velocity
        'ch' : channel
        'tpo' : new tempo in mspb
        'cn' : control number
        'value' : new control change value
        'pit' : new pitch

    """
    msglist = []
    cur_tick = 0
    cur_notes = []
    for msg in track:
        # Tick accumulation. Find the current tick and record it as stt or edt.
        cur_tick += msg['time']
        if msg['type'] == 'note_on':
            # Put a temp note into cur_notes every time meets a 'note_on' message.
            cur_notes.append({'type': 'note', 'stt': cur_tick, 'lst': None,
                              'nn': msg['note'], 'vel_on': msg['velocity'], 'vel_off': None, 'ch': msg['channel']})
        elif msg['type'] == 'note_off':
            idx = [note['nn'] for note in cur_notes].index(msg['note'])
            cur_notes[idx]['lst'] = cur_tick - cur_notes[idx]['stt']
            cur_notes[idx]['vel_off'] = msg['velocity']
            cur_note = cur_notes.pop(idx)
            msglist.append(cur_note)
        elif msg['type'] == 'set_tempo':
            cur_set_tempo = {'type': 'set_tempo', 'stt': cur_tick, 'tpo': msg['tempo']}
            msglist.append(cur_set_tempo)
        elif msg['type'] == 'time_signature':
            cur_time_signature = {'type': 'time_signature', 'stt': cur_tick, 'nu': msg['numerator'],
                                  'de': msg['denominator']}
            msglist.append(cur_time_signature)
        elif msg['type'] == 'control_change':
            cur_control_change = {'type': 'control_change', 'stt': cur_tick, 'cn': msg['control'],
                                  'value': msg['value'], 'ch': msg['channel']}
            msglist.append(cur_control_change)
        elif msg['type'] == 'pitchwheel':
            cur_pitchwheel = {'type': 'pitchwheel', 'stt': cur_tick, 'pit': msg['pitch'], 'ch': msg['channel']}
            msglist.append(cur_pitchwheel)
        else:
            pass
    return msglist


def midi2sheet(filename):
    mid = MidiFile(filename)
    ticks_per_beat = mid.ticks_per_beat
    total_time = mid.length

    sheet = []
    for (i, track) in enumerate(mid.tracks):
        print(f'Track {i}: {track.name}')
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


def meta_to_msglist0(sheet):
    nmsglists = len(sheet)


def max_tick(sheet):
    # return max tick of all tracks
    ticks = []
    for msglist in sheet:
        ticks_ = [0]
        for msg in msglist:
            if msg['type'] == 'note':
                ticks_.append(msg['stt'] + msg['lst'])
            else:
                ticks_.append(msg['stt'])
        ticks.append(max(ticks_))
    return max(ticks)


def nn2label(nn, is_drum=False, show_group=True):
    if is_drum:
        return NOTE_NAMES[nn]
    else:
        modes = {'b': ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'],
                 '#': ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
                 '2': ['x', '7', '1', 'x', '2', 'x', '3', '4', 'x', '5', 'x', '6'],
                 '7b': ['2', 'x', '3', '4', 'x', '5', 'x', '6', 'x', '7', '1', '']}
        note_names = modes['b']
        if show_group:
            return f'[{nn}]{note_names[nn%12]}{nn//12-2}'
        else:
            return f'{note_names[nn%12]}'


class Pianoroll(object):
    '''

    Generate a pianoroll using matplotlib.

    * list variable's name ending with '0' means it may contain messages whose stt is out of tick_interval
    * variable's name ending with 's' means it is a list (multi variables)

    Some abbreviations:

    * note              -> note
    * set_tempo         -> st
    * time_signature    -> ts
    * control_change    -> cc
    * pitchwheel        -> pw

    '''
    def __init__(self, sheet, ticks_per_beat):
        # [01] getting data
        self.sheet = sheet
        self.ticks_per_beat = ticks_per_beat
        self.max_tick = max_tick(sheet)

        # [02] getting notes
        ## (sorted by channels)
        self.notes_c = [[msg for msg in sum(sheet, []) if msg['type'] == 'note' and msg['ch'] == k] for k in range(16)]
        ## (sorted by tracks)
        self.notes_t = [[msg for msg in sheet[k] if msg['type'] == 'note'] for k in range(len(sheet))]

        # [03] getting set_tempos
        self.set_tempos = [msg for msg in sum(sheet, []) if msg['type'] == 'set_tempo']
        self.set_tempos.sort(key=lambda msg: msg['stt'])

        # [04] getting time_signatures
        self.time_signatures = [msg for msg in sum(sheet, []) if msg['type'] == 'time_signature']
        self.time_signatures.sort(key=lambda msg: msg['stt'])

        # [05] getting control_changes (sorted by channels)
        self.control_changes = [[msg for msg in sum(sheet, []) if msg['type'] == 'control_change' and msg['ch'] == k] for k in range(16)]
        _ = [self.control_changes[k].sort(key=lambda msg: msg['stt']) for k in range(16)]
        self.controls = list({cc['cn'] for cc in sum(self.control_changes, [])})
        for k in range(16):
            for control in self.controls:
                self.control_changes[k].insert(0, dict(type='control_change', stt=0, cn=control, value=0, ch=k))
                self.control_changes[k].append(dict(type='control_change', stt=self.max_tick, cn=control, value=0, ch=k))
        print(f'used controls: {self.controls}')

        # [06] getting pitchwheels (sorted by channels)
        self.pitchwheels = [[msg for msg in sum(sheet, []) if msg['type'] == 'pitchwheel' and msg['ch'] == k] for k in range(16)]
        _ = [self.pitchwheels[k].sort(key=lambda msg: msg['stt']) for k in range(16)]
        for k in range(16):
            self.pitchwheels[k].insert(0, dict(type='pitchwheel', stt=0, pit=0, ch=k))
            self.pitchwheels[k].append(dict(type='pitchwheel', stt=self.max_tick, pit=0, ch=k))

    def get_max_tick(self):
        return self.max_tick

    def get_tick_range(self):
        return 0, self.max_tick

    def get_nn_range(self, channel):
        nns = [note['nn'] for note in self.notes_c[channel]]
        nn_min = min(nns) - 1
        nn_max = max(nns) + 2
        return nn_min, nn_max

    def set_default_ts(self, numerator=4, denominator=4):
        self.time_signatures.insert(0, dict(type='time_signature', stt=0, nu=numerator, de=denominator))

    def set_default_st(self, tempo=500000):
        self.set_tempos.insert(0, dict(type='set_tempo', stt=0, tpo=tempo))

    def show_meta(self):
        print(f'set_tempos: {self.set_tempos}\ntime_signatures: {self.time_signatures}')

    def draw(self, whdpi=(12, 5, 144), nn_interval=(48, 72), tick_interval=(0, 960*4), splits_per_beat=4, channel=0, is_drum=False):
        # [01] pianoroll meta params
        fontsize = 45*whdpi[1]/(length(*nn_interval)+8)
        velocity_h = 5
        if is_drum:
            keyboard_w = 2
        else:
            keyboard_w = 1
        keyboard_w = keyboard_w*length(*tick_interval)//(whdpi[0]-keyboard_w)
        bottom = nn_interval[0] - velocity_h
        left = tick_interval[0] - keyboard_w
        top = nn_interval[1] + 3
        right = tick_interval[1]
        chds0 = [[2*1920, 'Cm'], [4*1920, 'Ab'], [5*1920-240, 'Gm'],
                 [6*1920, 'Cm'], [8*1920, 'Ab'], [9*1920-240, 'Gm'], [10*1920, 'X']]

        # [02] note parsing
        ## divide notes both in nn_interval and tick_interval into 3 parts: left, full and right
        notes = [note for note in self.notes_c[channel] if inrange(note['nn'], *nn_interval)]
        notes = [note for note in notes if inrange(note['stt'], *tick_interval) or inrange(note['stt']+note['lst'], *tick_interval)]
        notes_full = [note for note in notes if inrange(note['stt'], *tick_interval) and inrange(note['stt']+note['lst'], *tick_interval)]
        notes_left = [note for note in notes if note['stt'] < tick_interval[0] <= note['stt'] + note['lst']]
        notes_right = [note for note in notes if note['stt'] < tick_interval[1] <= note['stt'] + note['lst']]
        notes_rearranged = notes_full + notes_left + notes_right
        ## getting rectangles of notes for pianoroll
        notes_full_rects = [plt.Rectangle((note['stt'], note['nn']), note['lst'], 1,
                                          color=rgb_shader(note['vel_on']), joinstyle='round', lw=0.0, zorder=5) for note in notes_full]
        notes_left_rects = [plt.Rectangle((tick_interval[0], note['nn']), note['lst']-tick_interval[0]+note['stt'], 1,
                                          color=rgb_shader(note['vel_on']), joinstyle='round', lw=0.0, zorder=5) for note in notes_left]
        notes_right_rects = [plt.Rectangle((note['stt'], note['nn']), tick_interval[1]-note['stt'], 1,
                                           color=rgb_shader(note['vel_on']), joinstyle='round', lw=0.0, zorder=5) for note in notes_right]
        notes_rects = notes_full_rects + notes_left_rects + notes_right_rects

        # [03] set_tempo parsing
        # TODO: set_tempo parsing

        # [04] time_signature parsing
        ## put all time_signatures into a list and append an end to the list
        tss0 = [[msg['stt'], msg['nu'], msg['de']] for msg in self.time_signatures]
        tss0.append([tick_interval[1], tss0[-1][1], tss0[-1][2]])
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
        ## x1s0 = [range(stt_0, stt_1, step1s[0]), range(stt_1, stt_2, step1s[1]), ..., range(stt_n, tick_interval[1], step1s[n])]
        x1s0 = [list(range(tss0[k][0], tss0[k+1][0], step1s[k])) for k in range(len(step1s)-1)]
        x1s = [x1 for x1 in sum(x1s0, []) if inrange(x1, *tick_interval)]
        x2s0 = [list(range(tss0[k][0], tss0[k+1][0], step2s[k])) for k in range(len(step2s)-1)]
        x2s = [x2 for x2 in sum(x2s0, []) if inrange(x2, *tick_interval) and x2 not in x1s]
        x3s0 = [k*step3 for k in range(tick_interval[0]//step3, tick_interval[1]//step3+1)]
        x3s = [x3 for x3 in x3s0 if inrange(x3, *tick_interval) and x3 not in x1s+x2s]
        ## l1s0: bar labels | l2s0: beat labels
        l1s0 = list(enumerate(sum(x1s0, [])))
        l1s = [l[0] for l in l1s0 if inrange(l[1], *tick_interval)]
        l2s0 = [[x2 % tss0[i][1] for x2 in range(len(x2s0_section)) if x2 % tss0[i][1] != 0] for (i, x2s0_section) in enumerate(x2s0)]
        l2s = sum(l2s0, [])

        # [05] control_change parsing
        # TODO: control_change parsing

        # [06] pitchwheel parsing
        # TODO: pitchwheel parsing

        # ---------------------------------------------------------------------------------------------------- #

        # [01] draw pianoroll
        ## initializing
        ax = get_figure(*whdpi)
        ## the largest bounding box
        largest_rect = plt.Rectangle((left, bottom), right-left, top-bottom, facecolor='none', edgecolor='#555555', lw=0.75, joinstyle='round', zorder=7)
        ax.add_patch(largest_rect)
        ## main area facecolor
        main_rect = plt.Rectangle((tick_interval[0], nn_interval[0]), length(*tick_interval), length(*nn_interval), facecolor='#ddeeff', lw=0.0, zorder=0)
        ax.add_patch(main_rect)
        ## velocity lane facecolor
        vel_rect = plt.Rectangle((tick_interval[0], bottom), length(*tick_interval), velocity_h, facecolor='#ccddee', lw=0.0, zorder=0)
        ax.add_patch(vel_rect)
        ## ruler facecolor
        ruler_rect = plt.Rectangle((left, nn_interval[1]), right-left, 3, facecolor='#ffffff', lw=0.0, zorder=0)
        ax.add_patch(ruler_rect)
        ## background keys
        white_nns = [nn for nn in range(*nn_interval) if nn % 12 in [0, 2, 4, 5, 7, 9, 11]]
        black_nns = [nn for nn in range(*nn_interval) if nn % 12 in [1, 3, 6, 8, 10]]
        white_bg_rects = [plt.Rectangle((tick_interval[0], nn), length(*tick_interval), 1, facecolor='#ffffff', lw=0.0, zorder=1) for nn in white_nns]
        black_bg_rects = [plt.Rectangle((tick_interval[0], nn), length(*tick_interval), 1, facecolor='#ddcccc', lw=0.0, zorder=1) for nn in black_nns]
        _ = [ax.add_patch(rect) for rect in white_bg_rects+black_bg_rects]
        ## keys
        white_kbd_rects = [plt.Rectangle((left, nn), keyboard_w, 1, facecolor='#ffffff', lw=0.0, zorder=4) for nn in white_nns]
        black_kbd_rects = [plt.Rectangle((left, nn), keyboard_w, 1, facecolor='#222222', lw=0.0, zorder=4) for nn in black_nns]
        _ = [ax.add_patch(rect) for rect in white_kbd_rects+black_kbd_rects]
        left_bottom_rect = plt.Rectangle((left, bottom), keyboard_w, velocity_h, facecolor='#ffffff', lw=0.0, zorder=4)
        ax.add_patch(left_bottom_rect)
        ### line between keys
        _ = [plt.plot([left, tick_interval[0]], [nn, nn], color='#222222', lw=0.5, solid_capstyle='butt', zorder=4.1) for nn in range(*nn_interval)]
        plt.plot([left, tick_interval[0]], [nn_interval[1], nn_interval[1]], color='#222222', lw=0.5, solid_capstyle='butt', zorder=4.1)
        ### text on keys
        _ = [plt.annotate(nn2label(nn, is_drum=is_drum), (left+keyboard_w//16, nn+0.5), color='#555555', va='center', fontsize=fontsize, zorder=4.1,
                          clip_box=TransformedBbox(white_kbd_rects[k].get_bbox(), ax.transData)) for (k, nn) in enumerate(white_nns)]
        _ = [plt.annotate(nn2label(nn, is_drum=is_drum), (left+keyboard_w//16, nn+0.5), color='#ffffff', va='center', fontsize=fontsize, zorder=4.1,
                          clip_box=TransformedBbox(black_kbd_rects[k].get_bbox(), ax.transData)) for (k, nn) in enumerate(black_nns)]
        ## horizontal lines
        plt.plot(tick_interval, [nn_interval[0], nn_interval[0]], color='#555555', lw=0.5, solid_capstyle='butt', zorder=2)
        _ = [plt.plot(tick_interval, [nn, nn], color='#999999', lw=0.5, solid_capstyle='butt', zorder=2) for nn in range(nn_interval[0]+1, nn_interval[1])]
        plt.plot(tick_interval, [nn_interval[1], nn_interval[1]], color='#555555', lw=0.5, solid_capstyle='butt', zorder=2)
        plt.plot([left, tick_interval[1]], [nn_interval[1]+1, nn_interval[1]+1], color='#555555', lw=0.5, solid_capstyle='butt', zorder=2)
        plt.plot([left, tick_interval[1]], [nn_interval[1]+2, nn_interval[1]+2], color='#555555', lw=0.5, solid_capstyle='butt', zorder=2)
        ## vertical lines
        plt.plot([tick_interval[0], tick_interval[0]], [bottom, nn_interval[1]], color='#ee2222', lw=1.0, solid_capstyle='butt', zorder=6.1)
        _ = [plt.plot([x, x], [bottom, nn_interval[1]], color='#aaaaaa', lw=0.5, solid_capstyle='butt', zorder=2.1) for x in x3s]
        _ = [plt.plot([x, x], [bottom, nn_interval[1]], color='#555555', lw=0.5, solid_capstyle='butt', zorder=2.1) for x in x2s]
        _ = [plt.plot([x, x], [bottom, nn_interval[1]], color='#222222', lw=1.0, solid_capstyle='butt', zorder=2.1) for x in x1s]

        ### chords
        chds = [chd for chd in chds0 if inrange(chd[0], *tick_interval)]
        _ = [plt.annotate(chd[1], (chd[0], nn_interval[1]+0.5), color='#555555', va='center', ha='center', fontsize=fontsize) for chd in chds]

        # [02] draw notes
        _ = [ax.add_patch(rect) for rect in notes_rects]
        ## note edge
        _ = [plt.plot([note['stt'], note['stt']+note['lst'], note['stt']+note['lst'], note['stt'], note['stt']],
                      [note['nn'], note['nn'], note['nn']+1, note['nn']+1, note['nn']],
                      color='#123456', lw=0.5, solid_capstyle='round', zorder=5.2) for note in notes_full]
        _ = [plt.plot([tick_interval[0], note['stt']+note['lst'], note['stt']+note['lst'], tick_interval[0]],
                      [note['nn'], note['nn'], note['nn']+1, note['nn']+1],
                      color='#123456', lw=0.5, solid_capstyle='round', zorder=5.2) for note in notes_left]
        _ = [plt.plot([tick_interval[1], note['stt'], note['stt'], tick_interval[1]],
                      [note['nn']+1, note['nn']+1, note['nn'], note['nn']],
                      color='#123456', lw=0.5, solid_capstyle='round', zorder=5.2) for note in notes_right]
        ## note label
        _ = [plt.annotate(nn2label(note['nn'], is_drum=is_drum, show_group=False), (note['stt']+self.ticks_per_beat//16, note['nn']+0.5),
                          color='#ffffff', va='center', fontsize=fontsize, zorder=5.1,
                          clip_box=TransformedBbox(notes_rects[k].get_bbox(), ax.transData)) for (k, note) in enumerate(notes_rearranged)]
        # on-velocity
        notes_full_vels = [plt.Line2D([note['stt'], note['stt']], [bottom, bottom+note['vel_on']/127*velocity_h],
                                      color=rgb_shader(note['vel_on']), lw=1.0, solid_capstyle='butt', zorder=3,
                                      marker='x', markevery=[1], markersize=4, mew=1) for note in notes_full+notes_right]
        _ = [ax.add_line(vel) for vel in notes_full_vels]

        # [03] draw set_tempos
        # TODO: draw set_tempos

        # [04] draw time_signatures
        ## time_signature changes
        tss = [ts for ts in tss0 if inrange(ts[0], *tick_interval)]
        _ = [plt.annotate(f'{ts[1]}/{ts[2]}', (ts[0], nn_interval[1]+1.5), color='#555555', va='center', ha='center', fontsize=fontsize) for ts in tss]
        ## bar labels
        _ = [plt.annotate(l1, (x1, nn_interval[1]+2.5), color='#555555', va='center', ha='center', fontsize=fontsize) for (x1, l1) in zip(x1s, l1s)]
        ## beat labels
        _ = [plt.annotate(l2, (x2, nn_interval[1]+2.5), fontsize=fontsize*3/4, color='#555555', va='center', ha='center') for (x2, l2) in zip(x2s, l2s)]

        # [05] draw control_changes
        # TODO: draw control_changes

        # [06] draw pitchwheels
        pws0 = [[msg['stt'] for msg in self.pitchwheels[channel]], [msg['pit']/16384*length(*nn_interval)+middle(*nn_interval) for msg in self.pitchwheels[channel]]]
        x1 = [k for k in range(len(pws0[0])) if pws0[0][k]<=tick_interval[0]]
        if x1 == []: x1 = 0
        else: x1 = x1[-1]
        x2 = [k for k in range(len(pws0[0])) if pws0[0][k]>=tick_interval[1]]
        if x2 == []: x2 = len(pws0[0])-1
        else: x2 = x2[0]
        pws = [[pws0[0][k] for k in range(x1+1, x2)], [pws0[1][k] for k in range(x1+1, x2)]]
        pws[0].insert(0, tick_interval[0])
        pws[0].append(tick_interval[1])
        pws[1].insert(0, pws0[1][x1])
        pws[1].append(pws0[1][x2])
        plot_type = ['piecewise', 'stair', 'none'][1]
        if plot_type == 'piecewise':
            plt.plot(pws[0], pws[1], color='#1155ee', solid_capstyle='butt', solid_joinstyle='bevel', zorder=4.2, label='pitch')
        elif plot_type == 'stair':
            plt.step(pws[0], pws[1], color='#1155ee', solid_capstyle='butt', zorder=4.2, label='pitch')
        else: pass
        if plot_type in ['piecewise', 'stair']:
            plt.legend(loc='lower right', fontsize=24)

        # [07]save figure
        plt.savefig(r'../output/pianoroll_test.svg')
