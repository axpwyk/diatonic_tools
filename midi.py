from mido import MidiFile, MidiTrack
from mido import Message, MetaMessage
from mido import bpm2tempo, tempo2bpm, tick2second, second2tick


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
            cur_time_signature = {'type': 'time_signature', 'stt': cur_tick, 'nu': msg['numerator'], 'de': msg['denominator']}
            msglist.append(cur_time_signature)
        elif msg['type'] == 'control_change':
            cur_control_change = {'type': 'control_change', 'stt': cur_tick, 'cn': msg['control'], 'value': msg['value'], 'ch': msg['channel']}
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
                ticks_.append(msg['stt']+msg['lst'])
            else:
                ticks_.append(msg['stt'])
        ticks.append(max(ticks_))
    return max(ticks)


class Pianoroll(object):
    '''

    Generate a pianoroll using matplotlib.
    Meta messages should be put into msglist[0].
    msglist[1], msglist[2], ... only contain notes.

    '''
    def __init__(self, sheet, nn_interval=(50, 70), tick_interval=(0, 960*4), channel=0):
        ## getting meta params dict
        self.meta_params = {'tick_max': max_tick(sheet),
                            'tick_start': tick_interval[0],
                            'tick_end': tick_interval[1],
                            'nn_start': nn_interval[0],
                            'nn_end': nn_interval[1],
                            'time_signatures': None}

    def add_notelist(self, notelist):
        pass

    def show(self):
        pass
