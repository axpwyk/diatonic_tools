import re
from consts import *


''' note name, interval_name, mode name, chord name, tension name parsers '''


def note_name_parser(note_name):
    # examples: 'C#3', 'Bb1', 'Fbb3', etc.
    search_obj = re.search(r'(?P<note_name>[ABCDEFG])(?P<accidental_str>[b#]*)(?P<group_str>-?\d*)', note_name)
    return search_obj.groupdict()


def interval_name_parser(interval_name):
    # examples: 'm2', 'M3', 'P4', etc.
    search_obj = re.search(r'(?P<neg_str>-?)(?P<type>[dmPMA])(?P<degree_str>[\d]*)', interval_name)
    return search_obj.groupdict()


def mode_name_parser(mode_name):
    # examples: 'C Ionian', 'Bb Dorian', etc.
    search_obj = re.search(r'(?P<key_name>[ABCDEFG][b#]*-?\d*) ?(?P<mode_type>\w+)', mode_name)
    return search_obj.groupdict()


def chord_name_parser(chord_name):
    # examples: 'CM7', 'Dm7(9, 11, 13)', 'Bm7-5/F', etc.
    search_obj = re.search(r'(?P<root_name>[ABCDEFG][b#]*)*(?P<chord_type>\w*-?\d?)(?P<tension_name>\([^ac-z]*\))*/?(?P<bass_name>[ABCDEFG][b#]*)*', chord_name)
    return search_obj.groupdict()


def tension_name_parser(tension_name):
    # examples: '(9)', '(b9, #11)', '(9, 11, 13)', '(9, 13)', etc.
    return re.findall(r'[#b]*\d{1,2}', tension_name)


''' fancy music theory classes '''


class Note(object):
    def __init__(self, note=0, accidental=0, group=0):
        # default: 'C0'
        self._note = note
        self._accidental = accidental
        self._group = group

    def __repr__(self):
        return self.to_name()

    def __str__(self):
        return self.to_name()

    def __sub__(self, other):
        if isinstance(other, Note):
            step1 = NATURAL_NOTES.index(self._note) + self._group * len(NATURAL_NOTES)
            step2 = NATURAL_NOTES.index(other.get_note()) + other.get_group() * len(NATURAL_NOTES)
            return Interval(abs(self) - abs(other), step1 - step2)
        if isinstance(other, Interval):
            return self + (-other)
        else:
            raise TypeError('ClassError: `Note` could only subtract a `Note` or an `Interval`!')

    def __add__(self, other):
        if isinstance(other, Interval):
            delta_note = other.get_delta_note()
            delta_step = other.get_delta_step()
            step = NATURAL_NOTES.index(self._note) + delta_step
            note = NATURAL_NOTES[step % len(NATURAL_NOTES)]
            group = self._group + step // len(NATURAL_NOTES)
            accidental = abs(self) + delta_note - note - len(NOTE_NAMES) * group
            return Note(note, accidental, group)
        else:
            raise TypeError('ClassError: `Note` could only add an `Interval`!')

    def __abs__(self):
        return self._note + self._accidental + self._group * len(NOTE_NAMES)

    def get_note(self):
        return self._note

    def get_accidental(self):
        return self._accidental

    def get_group(self):
        return self._group

    def from_name(self, note_name):
        par = note_name_parser(note_name)

        self._note = NOTE_NAMES.index(par['note_name'])

        accidental = 0
        accidental += par['accidental_str'].count('#')
        accidental -= par['accidental_str'].count('b')
        self._accidental = accidental

        if par['group_str']:
            self._group = eval(par['group_str'])
        else:
            self._group = 0

        return self

    def to_name(self):
        return NOTE_NAMES[self._note] + (self._accidental * '#' if self._accidental > 0 else -self._accidental * 'b') + f'{self._group}'

    def add_sharp(self):
        self._accidental += 1
        return self

    def add_flat(self):
        self._accidental -= 1
        return self


class Interval(object):
    def __init__(self, delta_note=0, delta_step=0):
        # default: 'P1'
        self._delta_note = delta_note
        self._delta_step = delta_step

    def __repr__(self):
        return self.to_name()

    def __str__(self):
        return self.to_name()

    def __add__(self, other):
        if isinstance(other, Note):
            return other + self
        elif isinstance(other, Interval):
            return Interval(self._delta_note + other.get_delta_note(), self._delta_step + other.get_delta_step())
        else:
            raise TypeError('ClassError: `Interval` could only add a `Note` or an `Interval`!')

    def __sub__(self, other):
        if isinstance(other, Interval):
            return Interval(self._delta_note - other.get_delta_note(), self._delta_step - other.get_delta_step())
        else:
            raise TypeError('ClassError: `Interval` could only subtract an `Interval`!')

    def __neg__(self):
        return Interval(-self._delta_note, -self._delta_step)

    def get_delta_note(self):
        return self._delta_note

    def get_delta_step(self):
        return self._delta_step

    def from_name(self, interval_name):
        par = interval_name_parser(interval_name)
        np = -1 if par['neg_str'] else 1
        type = par['type']
        degree = eval(par['degree_str'])
        delta_step = degree - 1
        delta_note = [INTERVAL_TYPES_k[delta_step % len(NATURAL_NOTES)] for INTERVAL_TYPES_k in INTERVAL_TYPES].index(type)
        delta_note = delta_note + delta_step // len(NATURAL_NOTES) * len(NOTE_NAMES)
        self._delta_note, self._delta_step = np * delta_note, np * delta_step
        return self

    def to_name(self):
        type = INTERVAL_TYPES[abs(self._delta_note) % len(NOTE_NAMES)][abs(self._delta_step) % len(NATURAL_NOTES)]
        degree = f'{abs(self._delta_step)+1}'
        return type + degree if self._delta_step >= 0 else '-' + type + degree


class Mode(object):
    """ Mode is a list of Notes """
    def __init__(self, mode_name='C Ionian'):
        par = mode_name_parser(mode_name)
        key = Note().from_name(par['key_name'])
        intervals = MODE_INTERVALS[par['mode_type']]
        self._notes = [key]
        for interval in intervals:
            self._notes.append(self._notes[-1] + Interval().from_name(interval))

    def __repr__(self):
        return f'{self._notes}'

    def __str__(self):
        return f'{self._notes}'


class Chord(object):
    def __init__(self, chord_name):
        pass
