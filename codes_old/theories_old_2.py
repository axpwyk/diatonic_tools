import re
from consts import *


''' note_name, interval_name, mode_name, chord_name, tension_type parsers '''


def note_name_parser(note_name):
    # examples: 'C#3', 'Bb1', 'Fbb3', etc.
    search_obj = re.search(r'(?P<note_name>[ABCDEFG])(?P<accidental_str>[b#]*)(?P<group_str>-?\d+)?', note_name)
    return search_obj.groupdict()


def interval_name_parser(interval_name):
    # examples: 'm2', 'M3', 'P4', etc.
    search_obj = re.search(r'(?P<neg_str>-)?(?P<interval_type>[dmPMA])(?P<degree_str>[\d]+)', interval_name)
    return search_obj.groupdict()


def mode_name_parser(mode_name):
    # examples: 'C Ionian', 'Bb Dorian', etc.
    search_obj = re.search(r'(?P<key_name>[ABCDEFG][b#]*-?\d*) ?(?P<mode_type>\w+)', mode_name)
    return search_obj.groupdict()


def chord_name_parser(chord_name):
    # examples: 'CM7', 'Dm7(9, 11, 13)', 'Bm7-5/F', etc.
    search_obj = re.search(r'(?P<root_name>[ABCDEFG][b#]*)(?P<chord_type>\w*[-+]?\d?)(?P<tension_type>(\([^ac-z]*\)))?(/(?P<bass_name>[ABCDEFG][b#]*))?', chord_name)
    return search_obj.groupdict()


def tension_type_parser(tension_name):
    # examples: '(9)', '(b9, #11)', '(9, 11, 13)', '(9, 13)', etc.
    return re.findall(r'[#b]*\d{1,2}', tension_name)


''' fancy music theory classes '''


class Note(object):
    def __init__(self, note_name='C0'):
        # default: 'C0'
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

    def __repr__(self):
        return self._get_name()

    def __str__(self):
        return self._get_name()

    def __sub__(self, other):
        if isinstance(other, Note):
            step1 = NATURAL_NOTES.index(self._note) + self._group * len(NATURAL_NOTES)
            step2 = NATURAL_NOTES.index(other.get_note()) + other.get_group() * len(NATURAL_NOTES)
            return Interval().set_vector(abs(self) - abs(other), step1 - step2)
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
            return Note().set_vector(note, accidental, group)
        else:
            raise TypeError('ClassError: `Note` could only add an `Interval`!')

    def __abs__(self):
        return self._note + self._accidental + self._group * len(NOTE_NAMES)

    def from_vector(self, note=0, accidental=0, group=1):
        self._note = note
        self._accidental = accidental
        self._group = group
        return self

    def _get_name_without_group(self):
        return NOTE_NAMES[self._note] + (self._accidental * '#' if self._accidental > 0 else -self._accidental * 'b')

    def _get_name(self):
        return NOTE_NAMES[self._note] + (self._accidental * '#' if self._accidental > 0 else -self._accidental * 'b') + f'{self._group}'

    def get_name_without_group(self):
        return self._get_name_without_group()

    def get_name(self):
        return self._get_name()

    def set_vector(self, note=None, accidental=None, group=None):
        if note:
            self._note = note
        if accidental:
            self._accidental = accidental
        if group:
            self._group = group
        return self

    def get_note(self):
        return self._note

    def get_accidental(self):
        return self._accidental

    def get_group(self):
        return self._group

    def add_sharp(self):
        self._accidental += 1
        return self

    def add_flat(self):
        self._accidental -= 1
        return self

    def add_oct(self):
        self._group += 1
        return self

    def sub_oct(self):
        self._group -= 1
        return self


class Interval(object):
    def __init__(self, interval_name='P1'):
        # default: 'P1'
        par = interval_name_parser(interval_name)
        np = -1 if par['neg_str'] else 1
        type = par['interval_type']
        degree = eval(par['degree_str'])
        delta_step = degree - 1
        delta_note = [INTERVAL_TYPES_k[delta_step % len(NATURAL_NOTES)] for INTERVAL_TYPES_k in INTERVAL_TYPES].index(type)
        delta_note = delta_note + delta_step // len(NATURAL_NOTES) * len(NOTE_NAMES)
        self._delta_note, self._delta_step = np * delta_note, np * delta_step

    def __repr__(self):
        return self._get_name()

    def __str__(self):
        return self._get_name()

    def __add__(self, other):
        if isinstance(other, Note):
            return other + self
        elif isinstance(other, Interval):
            return Interval().set_vector(self._delta_note + other.get_delta_note(), self._delta_step + other.get_delta_step())
        else:
            raise TypeError('ClassError: `Interval` could only add a `Note` or an `Interval`!')

    def __sub__(self, other):
        if isinstance(other, Interval):
            return Interval().set_vector(self._delta_note - other.get_delta_note(), self._delta_step - other.get_delta_step())
        else:
            raise TypeError('ClassError: `Interval` could only subtract an `Interval`!')

    def __neg__(self):
        return Interval().set_vector(-self._delta_note, -self._delta_step)

    def from_vector(self, delta_note=0, delta_step=0):
        self._delta_note = delta_note
        self._delta_step = delta_step
        return self

    def _get_name(self):
        type = INTERVAL_TYPES[abs(self._delta_note) % len(NOTE_NAMES)][abs(self._delta_step) % len(NATURAL_NOTES)]
        degree = f'{abs(self._delta_step)+1}'
        return type + degree if self._delta_step >= 0 else '-' + type + degree

    def get_name(self):
        return self._get_name()

    def set_vector(self, delta_note=None, delta_step=None):
        if delta_note:
            self._delta_note = delta_note
        if delta_step:
            self._delta_step = delta_step
        return self

    def get_delta_note(self):
        return self._delta_note

    def get_delta_step(self):
        return self._delta_step


class DiatonicMode(object):
    def __init__(self, scale_name='C Ionian'):
        par = mode_name_parser(scale_name)
        key_name = par['key_name']
        mode_type = par['mode_type']
        tonic = TONIC_NOTE_ENCODER[key_name]
        mode = SCALE_TYPE_ENCODER[mode_type]



''' old music theory classes '''


class Notes(object):
    """ Notes is a list of Note, also the base of Mode and Chord """
    def __init__(self, notes=None):
        self._notes = notes

    def __repr__(self):
        return f'{self._notes}'

    def __str__(self):
        return f'{self._notes}'

    def get_notes(self):
        return self._notes


class Mode(Notes):
    """ Mode is a subclass of Notes. """
    def __init__(self, mode_name='C Ionian'):
        super().__init__()
        par = mode_name_parser(mode_name)
        key = Note(par['key_name'])
        intervals = MODE_INTERVALS[par['mode_type']]
        self._notes = [key]
        self._steps = [0]
        for step, interval in enumerate(intervals):
            self._notes.append(self._notes[-1] + Interval(interval))
            self._steps.append(step + 1)

    def get_type(self):
        notes = [abs(note) for note in self._notes]
        deltas = [str(note2-note1) for note1, note2 in zip(notes[:-1], notes[1:])]
        deltas = ''.join(deltas)
        mode_type = INTERVALS_TO_MODE_TYPE[deltas]
        return mode_type

    def get_name(self):
        mode_type = self.get_type()
        return f'{self._notes[0]._get_name_without_group()} {mode_type}'

    def add_sharp(self):
        major_tonic_position = MAJOR_POSITION[self.get_type()]
        sharp_position = (major_tonic_position + 3) % 7
        self._notes[sharp_position].add_sharp()
        return self

    def add_flat(self):
        major_tonic_position = MAJOR_POSITION[self.get_type()]
        flat_position = (major_tonic_position - 1) % 7
        self._notes[flat_position].add_flat()
        return self

    def get_full_chord(self, step):
        steps = [((step+2*k)%7, (step+2*k)//7) for k in range(7)]
        notes = [self._notes[step[0]] + sum(step[1]*[Interval('P8')], Interval('P1')) for step in steps]
        return Chord().set_notes(notes)


class Chord(Notes):
    """ Chord is also a subclass of Notes """
    def __init__(self, chord_name='C'):
        super().__init__()
        par = chord_name_parser(chord_name)
        # bass
        if par['bass_name']:
            bass = Note(par['bass_name'])
            self._notes = [bass - Interval('P8')]
            self._br357t = ['B']
        else:
            self._notes = []
            self._br357t = []
        # r357
        root = Note(par['root_name'])
        mode = Mode(par['root_name'] + ' ' + CHORD_TYPE_TO_SCALE_TYPE[par['chord_type']])
        mode_notes = mode.get_notes()
        mode_steps = CHORD_TYPE_TO_DEGREES[par['chord_type']]
        self._notes.extend([mode_notes[step] for step in mode_steps])
        self._br357t.extend('R')
        self._br357t.extend([f'{step + 1}' for step in mode_steps[1:]])
        # tensions
        if par['tension_type']:
            tension_names = tension_type_parser(par['tension_type'])
            tension_intervals = [TENSION_NAME_TO_INTERVAL_NAME[tension_name] for tension_name in tension_names]
            tensions = [root + Interval(interval) for interval in tension_intervals]
            self._notes.extend(tensions)
            self._br357t.extend(tension_names)

    def set_notes(self, notes):
        self._notes = notes
        # and `self._br357t` to be finished
        return self

    def get_type(self):
        intervals = [note2-note1 for note1, note2 in zip(self._notes[:-1], self._notes[1:])]
        deltas = [str(interval.get_delta_note()) for interval in intervals]
        deltas = ''.join(deltas)
        seventh_chord_type = INTERVAL_NAME_TO_CHORD_TYPE[deltas[:3]]

        ninth = sum(intervals[:4], Interval('P1'))
        ninth = INTERVAL_NAME_TO_TENSION_NAME[str(ninth)]
        eleventh = sum(intervals[:5], Interval('P1'))
        eleventh = INTERVAL_NAME_TO_TENSION_NAME[str(eleventh)]
        thirteenth = sum(intervals[:6], Interval('P1'))
        thirteenth = INTERVAL_NAME_TO_TENSION_NAME[str(thirteenth)]

        return seventh_chord_type + f'({ninth}, {eleventh}, {thirteenth})'

    def get_name(self):
        chord_type = self.get_type()
        return f'{self._notes[0]._get_name_without_group()}{chord_type}'