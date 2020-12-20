import matplotlib.pyplot as plt
import colorsys as cs
import copy
from mido import MidiFile, MidiTrack
from mido import Message, MetaMessage
from mido import bpm2tempo, tempo2bpm, tick2second, second2tick
from pathlib import Path
from consts import ADD2_NOTE_NAMES, AGTC_NOTE_NAMES, CC_NAMES


''' ----------------------------------------------------------------------------------------- '''
''' ********************************* midi/sheet converters ********************************* '''
''' ----------------------------------------------------------------------------------------- '''
''' midi:  using delta time, based on 'note_on' and 'note_off' events                         '''
''' sheet: using absolute time, based on 'note' event                                         '''
''' ----------------------------------------------------------------------------------------- '''


def track2msglist(track):
    """

    Ideas from Askmyc. Coded by Axpwyk.
    Cannot be used on type 2 midi data.

    Args:

        track : list of midi message dicts using delta time.

        there are several kinds of midi message dict, and their keys are:

        <meta message>
        ['type(=track_name)', 'name', 'time']
        ['type(=set_tempo)', 'tempo', 'time']
        ['type(=time_signature)', 'numerator', 'denominator', 'clocks_per_click', 'notated_32nd_notes_per_beat', 'time']
        ['type(=marker)', 'text', 'time']
        ['type(=end_of_track)', 'time']
        etc...

        <message>
        ['type(=note_on/note_off)', 'channel', 'note', 'velocity', 'time']
        ['type(=control_change)', 'channel', 'control', 'value', 'time']
        ['type(=pitchwheel)', 'channel', 'pitch', 'time']
        etc...

        their values are:

        'type' : 'note_on', 'note_off', 'set_tempo', etc...
        'name' : text
        'tempo': milliseconds per beat
        'numerator', 'denominator': integer
        'time' : delta time in ticks
        'channel' : channel number
        'note' : note number
        'velocity' : velocity
        'control': control change number
        'value': 0..127
        'pitch': -8192..8191

    Outputs:

        msglist : list of midi message dicts using absolute time.
        it means 'note_on' and 'note_off' messages are combined, while time changes to cumtime.
        'velocity' breaks into 'velocity_on' and 'velocity_off'.

    """
    msglist = []
    cur_tick = 0
    tmp_notes = []
    tmp_lyrics = []
    for msg in track:
        # tick accumulation, find the current tick and record it as time1 or edt
        cur_tick += msg['time']
        # note message detection
        if msg['type'] == 'note_on' and msg['velocity'] > 0:
            # put a temp note into tmp_notes every time meets a 'note_on' message
            tmp_notes.append({'type': 'note',
                              'channel': msg['channel'],
                              'note': msg['note'],
                              'velocity_on': msg['velocity'],
                              'velocity_off': None,
                              'lyric': None,
                              'time1': cur_tick,
                              'time2': None})
        # lyrics message detection
        elif msg['type'] == 'lyrics':
            tmp_lyrics.append(msg['text'])
        # sometime in real applications velocity 0 note_on is an alternative of note_off
        elif msg['type'] == 'note_off' or (msg['type'] == 'note_on' and msg['velocity'] < 1):
            idx = [note['note'] for note in tmp_notes].index(msg['note'])
            # idx = 0
            tmp_notes[idx]['time2'] = cur_tick - tmp_notes[idx]['time1']
            tmp_notes[idx]['velocity_off'] = msg['velocity']
            if tmp_lyrics != []:
                tmp_notes[idx]['lyric'] = tmp_lyrics.pop(0)
            cur_note = tmp_notes.pop(idx)
            msglist.append(cur_note)
        # other message and meta messages detection
        else:
            msg = copy.copy(msg)
            msg['time'] = cur_tick
            msglist.append(msg)

    return msglist


def midi2sheet(filename):
    # `ticks_per_beat` is `resolution` in cubase
    mid = MidiFile(Path(filename))
    ticks_per_beat = mid.ticks_per_beat
    total_time = mid.length

    sheet = []
    print('used tracks:')
    for i, track in enumerate(mid.tracks):
        print(f'track {i}: {track.name}')
        track_ = []
        for msg in track:
            track_.append(msg.dict())
        sheet.append(track2msglist(track_))
    print('')

    return sheet, ticks_per_beat, total_time


def msglist2track(msglist):
    msglist = copy.deepcopy(msglist)
    track = []
    # 'note' message splitting
    while len(msglist) > 0:
        msg = msglist.pop(0)
        if msg['type'] == 'note':
            msg1 = dict(type='note_on', channel=msg['channel'], note=msg['note'], velocity=msg['velocity_on'], time=msg['time1'])
            msg2 = dict(type='note_off', channel=msg['channel'], note=msg['note'], velocity=msg['velocity_off'], time=msg['time1']+msg['time2'])
            track.append(msg1)
            track.append(msg2)
        else:
            track.append(msg)
    # sort `track` with respect to 'time'
    track = sorted(track, key=lambda x: x['time'])
    # convert cumtime to delta time
    for i in reversed(range(len(track)-1)):
        track[i+1]['time'] = track[i+1]['time'] - track[i]['time']
    # convert `track` to `mido.MidiTrack` object
    msg_obj_list = []
    for msg in track:
        # meta messages
        if msg['type'] in ['track_name', 'set_tempo', 'time_signature', 'marker', 'end_of_track']:
            msg_obj_list.append(MetaMessage(**msg))
        else:
            msg_obj_list.append(Message(**msg))

    return MidiTrack(msg_obj_list)


def sheet2midi(sheet, ticks_per_beat, filename='untitled.mid'):
    mid = MidiFile(type=1, ticks_per_beat=ticks_per_beat)
    for i, msglist in enumerate(sheet):
        # if not contains 'track_name' message, add default 'track_name' message
        track_name = f'Track {i}'
        if_track_name_contains = False
        for msg in msglist:
            if msg['type'] == 'track_name':
                track_name = msg['name']
                if_track_name_contains = True
        if not if_track_name_contains:
            msglist.insert(0, dict(type='track_name', name=track_name, time=0))
        # add tracks to `mido.MidiFile`
        mid.tracks.append(msglist2track(msglist))
    mid.save(filename)


''' ----------------------------------------------------------------------------------------- '''
''' ********************************** utilities for sheet ********************************** '''
''' ----------------------------------------------------------------------------------------- '''


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


def note2label(note, type='piano', show_group=True, mode='Ab Ionian'):
    # note: midi note number
    if type == 'piano':
        modes = {'b': ['C', r'D$\flat$', 'D', r'E$\flat$', 'E', 'F', r'G$\flat$', 'G', r'A$\flat$', 'A', r'B$\flat$', 'B'],
                 '#': ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
                 '2': ['♭7', '7', '1', '#1', '2', '♭3', '3', '4', '#4', '5', '#5', '6'],
                 '7b': ['2', '♭3', '3', '4', '#4', '5', '#5', '6', '♭7', '7', '1', '#1'],
                 'A phrygian(#3)': ['C', r'C$\sharp$', 'D', r'$D\sharp$', 'E', 'F', r'F$\sharp$', 'G', r'G$\sharp$', 'A', r'B$\flat$', 'B'],
                 'Ab Ionian': ['3', '4', '4$\sharp$', '5', '5$\sharp$', '6', '7$\\flat$', '7', '1', '2$\\flat$', '2', '3$\\flat$']}
        note_names = modes[mode]
        if show_group:
            return f'[{note}]{note_names[note%12]}{note//12-2}'
        else:
            return f'{note_names[note%12]}'
    elif type == 'drum':
        return ADD2_NOTE_NAMES[note]
    elif type == 'agtc':
        return AGTC_NOTE_NAMES[note]
    elif type == 'null':
        return ''
    else:
        return None
