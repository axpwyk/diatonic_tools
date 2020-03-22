import re
from consts import *


''' note_name, interval_name, scale_name, alternated_note, chord_name, tension_type parsers '''


# for `Note`
def note_name_parser(note_name):
    # examples: 'C#3', 'Bb1', 'Fbb3', etc.
    search_obj = re.search(r'(?P<note_name>[ABCDEFG])(?P<accidental_str>[b#]*)(?P<group_str>-?\d+)?', note_name)
    return search_obj.groupdict()


# for `Interval`
def interval_name_parser(interval_name):
    # examples: 'm2', 'M3', 'P4', etc.
    search_obj = re.search(r'(?P<neg_str>-)?(?P<interval_type>[dmPMA])(?P<degree_str>[\d]+)', interval_name)
    return search_obj.groupdict()


# for `DiatonicScale`
def scale_name_parser(scale_name):
    # examples: 'C Ionian', 'Bb Dorian', 'Ionian(#5)', 'Lydian(b6)', 'Phrygian(#3)', 'Aeolian(#3, #7)', etc.
    search_obj = re.search(r'(?P<tonic_name>[ABCDEFG][b#]*-?\d*) ?(?P<scale_type>\w+) ?(?P<alternated_note>(\([^ac-z]*\)))?', scale_name)
    return search_obj.groupdict()


# for `AlternatedDiatonicScale`
def alternated_note_parser(alternated_note):
    # examples: '(b3)', '(b3, b7)', '(#5)', etc.
    return re.findall(r'[#b]+\d', alternated_note)


# for `Chord`
def chord_name_parser(chord_name):
    # examples: 'CM7', 'Dm7(9, 11, 13)', 'Bm7-5/F', etc.
    search_obj = re.search(r'(?P<root_name>[ABCDEFG][b#]*)(?P<chord_type>\w*[-+]?\d?)(?P<tension_type>(\([^ac-z]*\)))?(/(?P<bass_name>[ABCDEFG][b#]*))?', chord_name)
    return search_obj.groupdict()


def tension_type_parser(tension_type):
    # examples: '(9)', '(b9, #11)', '(9, 11, 13)', '(9, 13)', etc.
    return re.findall(r'[#b]*\d{1,2}', tension_type)


''' fancy music theory classes '''


class Note(object):
    def __init__(self, note_name='C0'):
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

        self._message = ''

    def __repr__(self):
        return self.get_name()

    def __sub__(self, other):
        if isinstance(other, Note):
            step1 = NATURAL_NOTES.index(self._note) + self._group * len(NATURAL_NOTES)
            step2 = NATURAL_NOTES.index(other._note) + other._group * len(NATURAL_NOTES)
            return Interval().set_vector(abs(self) - abs(other), step1 - step2)
        if isinstance(other, Interval):
            return self + (-other)
        else:
            raise TypeError('ClassError: `Note` could only subtract a `Note` or an `Interval`!')

    def __add__(self, other):
        if isinstance(other, Interval):
            delta_note = other._delta_note
            delta_step = other._delta_step
            step = NATURAL_NOTES.index(self._note) + delta_step
            note = NATURAL_NOTES[step % len(NATURAL_NOTES)]
            group = self._group + step // len(NATURAL_NOTES)
            accidental = abs(self) + delta_note - note - len(NOTE_NAMES) * group
            return Note().set_vector(note, accidental, group)
        else:
            raise TypeError('ClassError: `Note` could only add an `Interval`!')

    def __abs__(self):
        return self._note + self._accidental + self._group * len(NOTE_NAMES)

    def set_vector(self, note=None, accidental=None, group=None):
        if note:
            self._note = note
        if accidental:
            self._accidental = accidental
        if group:
            self._group = group
        return self

    def get_vector(self):
        return self._note, self._accidental, self._group

    def get_name(self, show_group=True):
        if show_group:
            return NOTE_NAMES[self._note] + (self._accidental * '#' if self._accidental > 0 else -self._accidental * 'b') + f'{self._group}'
        else:
            return NOTE_NAMES[self._note] + (self._accidental * '#' if self._accidental > 0 else -self._accidental * 'b')

    def add_sharp(self):
        self._accidental += 1
        return self

    def add_flat(self):
        self._accidental -= 1
        return self

    def add_accidental(self, n):
        self._accidental += n

    def add_oct(self):
        self._group += 1
        return self

    def sub_oct(self):
        self._group -= 1
        return self

    def set_message(self, message):
        self._message = message
        return self

    def get_message(self):
        return self._message


class Interval(object):
    def __init__(self, interval_name='P1'):
        par = interval_name_parser(interval_name)
        np = -1 if par['neg_str'] else 1
        type = par['interval_type']
        degree = eval(par['degree_str'])
        delta_step = degree - 1
        delta_note = [INTERVAL_TYPES_k[delta_step % len(NATURAL_NOTES)] for INTERVAL_TYPES_k in INTERVAL_TYPES].index(type)
        delta_note = delta_note + delta_step // len(NATURAL_NOTES) * len(NOTE_NAMES)
        self._delta_note, self._delta_step = np * delta_note, np * delta_step

    def __repr__(self):
        return self.get_name()

    def __add__(self, other):
        if isinstance(other, Note):
            return other + self
        elif isinstance(other, Interval):
            return Interval().set_vector(self._delta_note + other._delta_note, self._delta_step + other._delta_step)
        else:
            raise TypeError('ClassError: `Interval` could only add a `Note` or an `Interval`!')

    def __sub__(self, other):
        if isinstance(other, Interval):
            return Interval().set_vector(self._delta_note - other._delta_note, self._delta_step - other._delta_step)
        else:
            raise TypeError('ClassError: `Interval` could only subtract an `Interval`!')

    def __neg__(self):
        return Interval().set_vector(-self._delta_note, -self._delta_step)

    def __abs__(self):
        return self.get_vector()[0]

    def set_vector(self, delta_note=None, delta_step=None):
        if delta_note:
            self._delta_note = delta_note
        if delta_step:
            self._delta_step = delta_step
        return self

    def get_vector(self):
        return self._delta_note, self._delta_step

    def get_name(self):
        type = INTERVAL_TYPES[abs(self._delta_note) % len(NOTE_NAMES)][abs(self._delta_step) % len(NATURAL_NOTES)]
        degree = f'{abs(self._delta_step)+1}'
        return type + degree if self._delta_step >= 0 else '-' + type + degree


class DiatonicScale(object):
    def __init__(self, scale_name='C Ionian'):
        # parsing `scale_name`, and get `tonic_name` and `scale_type`
        par1 = scale_name_parser(scale_name)
        tonic_name_ = par1['tonic_name']
        scale_type = par1['scale_type']

        # parsing `tonic_name`, get `note_name`, `accidental_str` and `group_str` (unused)
        par2 = note_name_parser(tonic_name_)
        tonic_name = par2['note_name']
        accidentals_in_tonic_name = 0
        accidentals_in_tonic_name += par2['accidental_str'].count('#')
        accidentals_in_tonic_name -= par2['accidental_str'].count('b')
        tonic_name_enc = TONIC_NOTE_ENCODER[tonic_name]
        scale_type_enc = SCALE_TYPE_ENCODER[scale_type]
        self._accidentals = tonic_name_enc + 7 * accidentals_in_tonic_name + scale_type_enc
        self._tonic_degree = ['F', 'C', 'G', 'D', 'A', 'E', 'B'].index(tonic_name)

        # get meta notes
        self._get_meta_notes()

    def _get_meta_notes(self):
        # put accidental(s) on nature notes
        self._meta_notes = [Note('F0'), Note('C0'), Note('G0'), Note('D0'), Note('A0'), Note('E0'), Note('B0')]
        for k in range(0, self._accidentals) if self._accidentals>0 else range(self._accidentals, 0):
            self._meta_notes[k%7] = self._meta_notes[k%7].add_sharp() if self._accidentals>0 else self._meta_notes[k%7].add_flat()

    def __repr__(self):
        note_names = [note.get_name() for note in self.get_notes()]
        return '[' + ''.join([name+', ' for name in note_names[:-1]]) + note_names[-1] + ']'

    def __getitem__(self, item):
        return self.get_notes()[item]

    def __abs__(self):
        return [abs(note) for note in self.get_notes()]

    def set_tonic(self, tonic_name):
        par2 = note_name_parser(tonic_name)
        self._tonic_degree = ['F', 'C', 'G', 'D', 'A', 'E', 'B'].index(par2['note_name'])
        return self

    def get_notes(self):
        # generate real notes of current scale
        nn = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
        notes = [self._meta_notes[self._tonic_degree]]
        notes[0].set_message(f'{nn[0]}')
        for k in range(1, 7):
            next_note = self._meta_notes[(self._tonic_degree+2*k)%7]
            notes.append(next_note if abs(next_note)>abs(notes[-1]) else next_note + Interval('P8'))
            notes[-1].set_message(f'{nn[k]}')
        return notes

    def get_name(self, type_only=False):
        tonic_name_ = self.get_notes()[0].get_name(show_group=False)
        par2 = note_name_parser(tonic_name_)
        tonic_name = par2['note_name']
        accidentals_in_tonic_name = 0
        accidentals_in_tonic_name += par2['accidental_str'].count('#')
        accidentals_in_tonic_name -= par2['accidental_str'].count('b')
        tonic_name_enc = TONIC_NOTE_ENCODER[tonic_name]
        scale_type_enc = self._accidentals - tonic_name_enc - 7 * accidentals_in_tonic_name
        scale_type = SCALE_TYPE_DECODER[scale_type_enc + 3]
        if type_only:
            return scale_type
        else:
            return tonic_name_ + ' ' + scale_type

    def add_sharp(self, n=1):
        self._accidentals += n
        self._get_meta_notes()
        return self

    def add_flat(self, n=1):
        self._accidentals -= n
        self._get_meta_notes()
        return self


class AlteredDiatonicScale(DiatonicScale):
    def __init__(self, scale_name):
        par = scale_name_parser(scale_name)

        if par['alternated_note']:
            base_scale_type = par['scale_type']
            alternated_note = alternated_note_parser(par['alternated_note'])
            accidentals = []
            degrees = []
            for note in alternated_note:
                sharps = note.count('#')
                flats = note.count('b')
                accidentals.append(sharps - flats)
                degrees.append(eval(note[-1]) - 1)

            super().__init__(par['tonic_name']+ ' '+base_scale_type)
            for a, d in zip(accidentals, degrees):
                self._meta_notes[(self._tonic_degree+d*2)%7].add_accidental(a)

        else:
            super().__init__(scale_name)
            # print('If not error, this class now behaves like `DiatonicScale`.')

    def add_sharp(self, n=1):
        super().add_sharp(n)
        print('Warning! Accidentals lost. `AlternatedDiatonicScale` -> `DiatonicScale`.')

    def add_flat(self, n=1):
        super().add_flat(n)
        print('Warning! Accidentals lost. `AlternatedDiatonicScale` -> `DiatonicScale`.')

    def get_name(self, type_only=False):
        # TODO: return a simplified name, e.g. C Ionian(#4) -> C Lydian; C Ionian(b6, b7) -> C Aeolian(#3), etc.
        pass


class Chord(object):
    def __init__(self, chord_name='C'):

        self._bass = []
        self._body = []
        self._tensions = []

        par = chord_name_parser(chord_name)

        # bass note
        if par['bass_name']:
            self._bass = [Note(par['bass_name']) - Interval('P8')]
            self._bass[0].set_message('B')

        # r357 notes
        root = Note(par['root_name'])
        scale = AlteredDiatonicScale(par['root_name'] + ' ' + CHORD_TYPE_TO_SCALE_TYPE[par['chord_type']])
        scale_notes = scale.get_notes()
        degrees = CHORD_TYPE_TO_DEGREES[par['chord_type']]
        self._body.extend([scale_notes[deg].set_message(f'{deg+1}') for deg in degrees])
        self._body[0].set_message('R')

        # tension notes
        if par['tension_type']:
            tension_names = tension_type_parser(par['tension_type'])
            tension_intervals = [TENSION_NAME_TO_INTERVAL_NAME[tension_name] for tension_name in tension_names]
            tensions = [root + Interval(interval) for interval in tension_intervals]
            self._tensions.extend(tensions)
            _ = [tension.set_message(f'{tension_names[k]}') for k, tension in enumerate(self._tensions)]

    def __repr__(self):
        note_names = [note.get_name() for note in self.get_notes() if note is not None]
        return '[' + ''.join([name+', ' for name in note_names[:-1]]) + note_names[-1] + ']'

    def __getitem__(self, item):
        return self.get_notes()[item]

    def __abs__(self):
        if self._bass:
            return [abs(note) for note in self.get_notes()]
        else:
            return [abs(note) for note in self.get_notes()[1:]]

    def set_notes(self, bass=None, body=None, tensions=None):
        if bass:
            self._bass = [bass]
        if body:
            self._body = body
        if tensions:
            self._tensions = tensions
        return self

    def get_notes(self):
        return self._bass + self._body + self._tensions

    def get_type(self):
        intervals = [note2-note1 for note1, note2 in zip(self._body[:-1], self._body[1:])]
        deltas = [str(abs(interval)) for interval in intervals]
        deltas = ''.join(deltas)
        body_type = INTERVAL_NAME_TO_CHORD_TYPE[deltas]

        tension_to_root_intervals = [t-self._body[0] for t in self._tensions]
        tension_names = [INTERVAL_NAME_TO_TENSION_NAME[str(i)] for i in tension_to_root_intervals]

        if self._bass[0]:
            if self._tensions == []:
                return body_type + '/' + self._bass[0].get_name(show_group=False)
            else:
                return body_type + \
                       '(' + ''.join([tension_name+', ' for tension_name in tension_names[:-1]]) + tension_names[-1] + ')' + \
                       self._bass[0].get_name(show_group=False)
        else:
            if self._tensions == []:
                return body_type
            else:
                return body_type + \
                       '(' + ''.join([tension_name+', ' for tension_name in tension_names[:-1]]) + tension_names[-1] + ')'

    def get_name(self):
        chord_type = self.get_type()
        return f'{self._body[0].get_name(show_group=False)}{chord_type}'


''' other exciting functions '''


def circular_permutation_with_repetition(n, ns):
    import numpy as np

    # gcd of n_1, n_2, ..., n_K
    p = ns[0]
    for k in range(len(ns)-1):
        p = np.gcd(p, ns[k+1])

    # ds = {d: d|p}
    ds = []
    for d in range(1, p+1):
        if p % d == 0:
            ds.append(d)

    # euler totient function
    def _phi(n):
        ret = 0
        for k in range(n):
            if np.gcd(k, n) == 1:
                ret += 1
        return ret

    # factorial of n
    def _f(n):
        if n == 1:
            return n
        else:
            return n*_f(n-1)

    # circular permutation with repetition
    tmp = np.sum([_phi(d)*_f(n//d)//np.prod([_f(n_k//d) for n_k in ns]) for d in ds])//n

    return tmp
