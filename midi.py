import matplotlib.pyplot as plt
import matplotlib as mpl
from mido import MidiFile, MidiTrack
from mido import Message, MetaMessage
from mido import bpm2tempo, tempo2bpm, tick2second, second2tick


''' other functions '''


# a handy length function
def length(a, b):
    return b - a


def inrange(x, a, b):
    return a <= x < b


''' for matplotlib '''

# assigning a chinese font
mpl.rcParams['font.sans-serif'] = ['STKaiti']
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['font.size'] = 8.0


def get_figure(w, h, dpi):
    # figure settings
    fig = plt.figure(figsize=(w, h), dpi=dpi)
    fig.subplots_adjust(right=0.97, left=0.03, bottom=0.03, top=0.97, wspace=0.1, hspace=0.1)
    ax = fig.gca()
    ax.set_axis_off()
    return fig, ax


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
    for i, track in enumerate(mid.tracks):
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
    ticks = []
    for msglist in sheet:
        ticks_ = []
        for msg in msglist:
            if msg['type'] == 'note':
                ticks_.append(msg['stt'] + msg['lst'])
            else:
                ticks_.append(msg['stt'])
        ticks.append(max(ticks_))
    return max(ticks)


class Pianoroll(object):
    '''

    Generate a pianoroll using matplotlib.

    '''

    def __init__(self, sheet, ticks_per_beat):
        self.sheet = sheet
        self.ticks_per_beat = ticks_per_beat
        self.max_tick = max_tick(sheet)
        # meta-messages
        self.msglist_tpo = [msg for msg in sum(sheet, []) if msg['type'] == 'set_tempo']
        self.msglist_tpo = sorted(self.msglist_tpo, key=lambda msg: msg['stt'])
        self.msglist_ts = [msg for msg in sum(sheet, []) if msg['type'] == 'time_signature']
        self.msglist_ts = sorted(self.msglist_ts, key=lambda msg: msg['stt'])
        # ccs and pitchwheels (sorted by channels)
        self.sheet_cc = [[msg for msg in sum(sheet, []) if msg['type'] == 'control_change' and msg['ch'] == k] for k in
                         range(16)]
        _ = [self.sheet_cc[k].sort(key=lambda msg: msg['stt']) for k in range(16)]
        self.sheet_pw = [[msg for msg in sum(sheet, []) if msg['type'] == 'pitchwheel' and msg['ch'] == k] for k in
                         range(16)]
        _ = [self.sheet_pw[k].sort(key=lambda msg: msg['stt']) for k in range(16)]
        # notes (sorted by channels)
        self.sheet_note_c = [[msg for msg in sum(sheet, []) if msg['type'] == 'note' and msg['ch'] == k] for k in
                             range(16)]
        # notes (sorted by tracks)
        self.sheet_note_t = [[msg for msg in sheet[k] if msg['type'] == 'note'] for k in range(len(sheet))]

    def _clean(self):
        self.sheet = []

    def add_msg(self, msg):
        pass

    def add_msglist(self, msglist):
        pass

    def set_msglist(self, msglist):
        self.clean()
        pass

    def clean(self):
        self._clean()

    def draw(self, nn_interval=(48, 72), tick_interval=(0, 960*4), splits_per_beat=4, channel=0):
        # getting meta params
        note_names = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        velocity_lane_h = 5
        keyboard_w = 480
        bottom = nn_interval[0] - velocity_lane_h
        left = tick_interval[0] - keyboard_w
        # finding vertical lines' position (bar_line, beat_line, split_line)
        ## TODO: this part was not good
        ## time signature list
        tss = [[msg['stt'], msg['nu'], msg['de']] for msg in self.msglist_ts] + [[tick_interval[1], -1, -1]]
        ## ticks per beat list (tpb changes with ts denominator)
        tpbs = [[ts[0], self.ticks_per_beat*4//ts[2]] for ts in tss]
        ## delta xs of three types of vertical line
        step1s = [[tpb[0], tpb[1]*tss[i][1]] for i, tpb in enumerate(tpbs)]
        step2s = tpbs
        step3 = self.ticks_per_beat//splits_per_beat
        ## x coords of three types of vertical line
        x1s0 = sum([list(range(step1s[k][0], step1s[k+1][0], step1s[k][1])) for k in range(len(step1s)-1)], [])
        x1s = [x for x in x1s0 if inrange(x, *tick_interval)]
        x2s0 = sum([list(range(step2s[k][0], step2s[k+1][0], step2s[k][1])) for k in range(len(step2s)-1)], [])
        x2s = [x for x in x2s0 if inrange(x, *tick_interval) and x not in x1s]
        x3s0 = [k*step3 for k in range(tick_interval[0]//step3, tick_interval[1]//step3+1)]
        x3s = [x for x in x3s0 if x in range(*tick_interval) and x not in x1s+x2s]
        ## beat_line labels
        l1s0 = list(enumerate(x1s0))
        l1s = [l[0] for l in l1s0 if l[1] in range(*tick_interval)]
        # initializing pianoroll
        get_figure(12, 5, 144)
        # main area bounding box
        _ = plt.plot([left, tick_interval[1], tick_interval[1], left, left],
                     [bottom, bottom, nn_interval[1], nn_interval[1], bottom],
                     c='#555555', linewidth=0.75, solid_capstyle='round', zorder=7)
        # main area face color
        plt.fill([tick_interval[0], tick_interval[1], tick_interval[1], tick_interval[0]],
                 [nn_interval[0], nn_interval[0], nn_interval[1], nn_interval[1]], c='#ddeeff', lw=0.0, zorder=0)
        # velocity lane face color
        plt.fill([tick_interval[0], tick_interval[1], tick_interval[1], tick_interval[0]],
                 [bottom, bottom, nn_interval[0], nn_interval[0]], c='#ccddee', lw=0.0, zorder=0)
        # background keys
        _ = [plt.fill([tick_interval[0], tick_interval[1], tick_interval[1], tick_interval[0]],
                      [nn, nn, nn+1, nn+1], c='#ffffff', lw=0.0, zorder=1) for nn in range(*nn_interval) if nn % 12 in [0, 2, 4, 5, 7, 9, 11]]
        _ = [plt.fill([tick_interval[0], tick_interval[1], tick_interval[1], tick_interval[0]],
                      [nn, nn, nn+1, nn+1], c='#ddcccc', lw=0.0, zorder=1) for nn in range(*nn_interval) if nn % 12 in [1, 3, 6, 8, 10]]
        # keyboard
        plt.fill([left, tick_interval[0], tick_interval[0], left],
                 [bottom, bottom, nn_interval[0], nn_interval[0]], c='#ffffff', lw=0.0, zorder=4)
        _ = [plt.fill([tick_interval[0], left, left, tick_interval[0]],
                      [nn, nn, nn+1, nn+1], c='#ffffff', lw=0.0, zorder=1) for nn in range(*nn_interval) if nn % 12 in [0, 2, 4, 5, 7, 9, 11]]
        _ = [plt.fill([tick_interval[0], left, left, tick_interval[0]],
                      [nn, nn, nn+1, nn+1], c='#222222', lw=0.0, zorder=1) for nn in range(*nn_interval) if nn % 12 in [1, 3, 6, 8, 10]]
        _ = [plt.plot([left, tick_interval[0]], [nn, nn], c='#222222', linewidth=0.5, zorder=2) for nn in range(nn_interval[0]+1, nn_interval[1])]
        ## texts
        _ = [plt.text(left+keyboard_w//8, nn+0.5, f'[{nn}]{note_names[nn%12]}{nn//12-1}',
                      color='#555555', va='center', zorder=1.1) for nn in range(*nn_interval) if nn % 12 in [0, 2, 4, 5, 7, 9, 11]]
        _ = [plt.text(left+keyboard_w//8, nn+0.5, f'[{nn}]{note_names[nn%12]}{nn//12-1}',
                      color='#ffffff', va='center', zorder=1.1) for nn in range(*nn_interval) if nn % 12 in [1, 3, 6, 8, 10]]
        # horizontal lines
        plt.plot([left, tick_interval[1]], [nn_interval[0], nn_interval[0]], c='#555555', linewidth=0.5, solid_capstyle='butt', zorder=6)
        _ = [plt.plot(tick_interval, [nn, nn], c='#999999', linewidth=0.5, solid_capstyle='butt', zorder=2) for nn in range(nn_interval[0]+1, nn_interval[1])]
        # vertical lines
        plt.plot([tick_interval[0], tick_interval[0]], [bottom, nn_interval[1]], c='#ee2222', linewidth=1.0, solid_capstyle='butt', zorder=6.1)
        _ = [plt.plot([x, x], [bottom, nn_interval[1]], c='#aaaaaa', linewidth=0.5, solid_capstyle='butt', zorder=2.1) for x in x3s]
        _ = [plt.plot([x, x], [bottom, nn_interval[1]], c='#555555', linewidth=0.5, solid_capstyle='butt', zorder=2.1) for x in x2s]
        _ = [plt.plot([x, x], [bottom, nn_interval[1]], c='#222222', linewidth=1.0, solid_capstyle='butt', zorder=2.1) for x in x1s]
        ## texts
        _ = [plt.text(x, nn_interval[1]+0.5, l, color='#555555', va='center', ha='center') for (x, l) in zip(x1s, l1s)]
        # notes
        notes = [note for note in self.sheet_note_c[channel] if note['stt'] in range(*tick_interval) or note['stt']+note['lst'] in range(*tick_interval)]
        notes_full = [note for note in notes if note['stt'] in range(*tick_interval) and note['stt']+note['lst'] in range(*tick_interval)]
        notes_left = [note for note in notes if note['stt'] < tick_interval[0] <= note['stt'] + note['lst']]
        notes_right = [note for note in notes if note['stt'] < tick_interval[1] <= note['stt'] + note['lst']]
        ## note interior
        ax = plt.gca()
        notes_full_rects = [plt.Rectangle((note['stt'], note['nn']), note['lst'], 1,
                                          color='#aa3322', joinstyle='round', lw=0.0, zorder=5) for note in notes_full]
        notes_left_rects = [plt.Rectangle((tick_interval[0], note['nn']), note['lst']-tick_interval[0]+note['stt'], 1,
                                          color='#aa3322', joinstyle='round', lw=0.0, zorder=5) for note in notes_left]
        notes_right_rects = [plt.Rectangle((note['stt'], note['nn']), tick_interval[1]-note['stt'], 1,
                                           color='#aa3322', joinstyle='round', lw=0.0, zorder=5) for note in notes_right]
        _ = [ax.add_patch(rect) for rect in notes_full_rects+notes_left_rects+notes_right_rects]
        ## note edge
        _ = [plt.plot([note['stt'], note['stt']+note['lst'], note['stt']+note['lst'], note['stt'], note['stt']],
                      [note['nn'], note['nn'], note['nn']+1, note['nn']+1, note['nn']],
                      c='#123456', linewidth=0.5, solid_capstyle='round', zorder=5.1) for note in notes_full]
        _ = [plt.plot([tick_interval[0], note['stt']+note['lst'], note['stt']+note['lst'], tick_interval[0]],
                      [note['nn'], note['nn'], note['nn']+1, note['nn']+1],
                      c='#123456', linewidth=0.5, solid_capstyle='round', zorder=5.1) for note in notes_left]
        _ = [plt.plot([tick_interval[1], note['stt'], note['stt'], tick_interval[1]],
                      [note['nn']+1, note['nn']+1, note['nn'], note['nn']],
                      c='#123456', linewidth=0.5, solid_capstyle='round', zorder=5.1) for note in notes_right]
        ## note text
        _ = [plt.text(note['stt']+self.ticks_per_beat//16, note['nn']+0.5, note_names[note['nn']%12],
                      c='#ffffff', va='center', zorder=5.2) for note in notes_full+notes_left+notes_right]
        ## note on-velocity
        ax = plt.gca()
        marker = 'x'
        notes_full_vels = [plt.Line2D([note['stt'], note['stt']], [bottom, bottom+note['vel_on']/127*velocity_lane_h],
                                      color='#aa3322', linewidth=0.75, zorder=3,
                                      marker=marker, markevery=[1], markersize=4, mew=0.75) for note in notes_full+notes_right]
        _ = [ax.add_line(vel) for vel in notes_full_vels]
        # pitchwheels
        pw = [[msg['stt'] for msg in self.sheet_pw[channel] if msg['stt'] in range(*tick_interval)],
              [msg['pit']/8192*length(*nn_interval)+nn_interval[0] for msg in self.sheet_pw[channel] if msg['stt'] in range(*tick_interval)]]
        plt.plot(pw[0], pw[1], c='#55ddee', zorder=8)
        # save figure
        plt.savefig(r'../output/pianoroll_test.svg')

    def show(self):
        pass
