from mido import MidiFile
from mido import Message
from mido import bpm2tempo, tempo2bpm, tick2second, second2tick


# sheet = [ts (starting time in seconds), tl (lasting time in seconds), note, velocity, channel]


def msgd_list_to_note_list(msgd_list, ticks_per_beat):
    """
    Ideas from Askmyc. Coded by Axpwyk.

    Args:

        msgd_list : list of midi message dicts.
        the structure of a midi message dict: ['type', 'time', 'note', 'velocity', 'channel']
        ‘type' : 'note_on', 'note_off', 'set_tempo', etc...
        'time' : delta time in ticks
        'note' : note number
        'velocity' : velocity
        'channel' : channel

    Outputs:

        note_list : list of notes.
        the structure of a note : [ts, te, nn, vel, ch]
        ts : starting time in ticks
        tl : lasting time in ticks
        te : ending time in ticks, not used, te = ts + tl
        nn : note number
        vel : velocity
        ch : channel
    """
    note_list = []
    cur_tick = 0
    cur_notes = []
    for msgd in msgd_list:
        # Tick accumulation. Find the current tick and record it as ts or te.
        cur_tick += msgd['time']
        cur_tempo = 600000
        if msgd['type'] == 'set_tempo':
            cur_tempo = msgd['tempo']
        if msgd['type'] == 'note_on':
            # Put a temp note into cur_notes every time meets a 'note_on' message.
            cur_notes.append([cur_tick, 0] + [msgd['note'], msgd['velocity'], msgd['channel']])
        if msgd['type'] == 'note_off':
            idx = [note[2] for note in cur_notes].index(msgd['note'])
            cur_notes[idx][1] = cur_tick
            cur_note = cur_notes.pop(idx)
            cur_note[1] -= cur_note[0]
            cur_note[0] = tick2second(cur_note[0], ticks_per_beat, cur_tempo)
            cur_note[1] = tick2second(cur_note[1], ticks_per_beat, cur_tempo)
            note_list.append(cur_note)


    return note_list


def midi_to_note_list(filename):
    mid = MidiFile(filename)
    ticks_per_beat = mid.ticks_per_beat

    sheet = []
    msgd_list = []
    for i, track in enumerate(mid.tracks):
        print(f'Track {i}: {track.name}')
        for msg in track:
            if msg.dict()['type'] == 'set_tempo':
                msgd_list.append(msg.dict())
            if msg.dict()['type'] == 'note_on' or msg.dict()['type'] == 'note_off':
                msgd_list.append(msg.dict())

        sheet.append(msgd_list_to_note_list(msgd_list, ticks_per_beat))

    return sheet


def pianoroll(note_list):
    pass
