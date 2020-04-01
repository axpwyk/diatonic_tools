import re
from copy import copy
from consts import *


''' all kinds of name parsers '''


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
    temp = scale_name
    for pat in ALTERNATIVE_NAME_SUBS.keys():
        temp = re.sub(pat, ALTERNATIVE_NAME_SUBS[pat], temp)
    search_obj = re.search(r'(?P<tonic_name>[ABCDEFG][b#]*-?\d*) ?(?P<scale_type>\w+) ?(?P<altered_note>(\([^ac-z]*\)))?', temp)
    return search_obj.groupdict()


# for `AlteredDiatonicScale`
def altered_note_parser(altered_note):
    # examples: '(b3)', '(b3, b7)', '(#5)', etc.
    return re.findall(r'[#b]+\d', altered_note)


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
        # get note midi encoding number (0, 11), integer
        self._nn = NOTE_NAMES.index(par['note_name'])
        # get accidentals (-\infty, \infty), integer
        accidental = 0
        accidental += par['accidental_str'].count('#')
        accidental -= par['accidental_str'].count('b')
        self._accidental = accidental
        # get group number (-\infty, \infty), integer
        if par['group_str']:
            self._group = eval(par['group_str'])
        else:
            self._group = 0
        # additional message (such as br357t for `Chord`, etc.)
        self._message = ''

    def __repr__(self):
        return self.get_name()

    def __sub__(self, other):
        # `Note` - `Note` = `Interval`
        if isinstance(other, Note):
            step1 = NATURAL_NNS.index(self._nn) + self._group * len(NATURAL_NNS)
            step2 = NATURAL_NNS.index(other._nn) + other._group * len(NATURAL_NNS)
            return Interval().set_vector(abs(self) - abs(other), step1 - step2)
        # `Note` - `Interval` = `Note`
        if isinstance(other, Interval):
            return self + (-other)
        else:
            raise TypeError('ClassError: `Note` could only subtract a `Note` or an `Interval`!')

    def __add__(self, other):
        # `Note` + `Interval` = `Note`
        if isinstance(other, Interval):
            delta_nn = other._delta_nn
            delta_step = other._delta_step
            step = NATURAL_NNS.index(self._nn) + delta_step
            nn = NATURAL_NNS[step % len(NATURAL_NNS)]
            group = self._group + step // len(NATURAL_NNS)
            accidental = abs(self) + delta_nn - nn - len(NOTE_NAMES) * group
            return Note().set_vector(nn, accidental, group)
        else:
            raise TypeError('ClassError: `Note` could only add an `Interval`!')

    def __abs__(self):
        # return absolute midi encoding number (-\infty, \infty), integer, e.g. 'Bb2' = (11, -1, 2) = 11-1+2*12 = 34
        return self._nn + self._accidental + self._group * len(NOTE_NAMES)

    def set_vector(self, nn=None, accidental=None, group=None):
        # set note vector (nn, accidental, group) manually
        if nn:
            self._nn = nn
        if accidental:
            self._accidental = accidental
        if group:
            self._group = group
        return self

    def get_vector(self):
        return self._nn, self._accidental, self._group

    def get_name(self, show_group=True):
        # get name of `Note`, e.g. Note('C0').get_name() = 'C0', Note('C0').get_name(show_group=False) = 'C', etc.
        if show_group:
            return NOTE_NAMES[self._nn] + (self._accidental * '#' if self._accidental > 0 else -self._accidental * 'b') + f'{self._group}'
        else:
            return NOTE_NAMES[self._nn] + (self._accidental * '#' if self._accidental > 0 else -self._accidental * 'b')

    def add_sharp(self, n=1):
        self._accidental += n
        return self

    def add_flat(self, n=1):
        self._accidental -= n
        return self

    def add_accidental(self, n=0):
        # a combination of multiple `add_sharp` or `add-flat` methods
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
        # positive or negative
        pn = -1 if par['neg_str'] else 1
        # get interval type 'd', 'm', 'M', or 'A'
        type = par['interval_type']
        # get interval degree, positive integer
        degree = eval(par['degree_str'])
        # degree-1 for calculating and indexing
        delta_step = degree - 1
        # calculate interval vector (delta_nn, delta_step)
        delta_nn = [INTERVAL_TYPES_k[delta_step % len(NATURAL_NNS)] for INTERVAL_TYPES_k in INTERVAL_TYPES].index(type)
        delta_nn = delta_nn + delta_step // len(NATURAL_NNS) * len(NOTE_NAMES)
        self._delta_nn, self._delta_step = pn * delta_nn, pn * delta_step

    def __repr__(self):
        return self.get_name()

    def __add__(self, other):
        # `Interval` + `Note` = `Note`
        if isinstance(other, Note):
            return other + self
        # `Interval` + `Interval` = `Interval`
        elif isinstance(other, Interval):
            return Interval().set_vector(self._delta_nn + other._delta_nn, self._delta_step + other._delta_step)
        else:
            raise TypeError('ClassError: `Interval` could only add a `Note` or an `Interval`!')

    def __sub__(self, other):
        # `Interval` - `Interval` = `Interval`
        if isinstance(other, Interval):
            return Interval().set_vector(self._delta_nn - other._delta_nn, self._delta_step - other._delta_step)
        else:
            raise TypeError('ClassError: `Interval` could only subtract an `Interval`!')

    def __neg__(self):
        return Interval().set_vector(-self._delta_nn, -self._delta_step)

    def __abs__(self):
        # absolute interval is `self._delta_nn`
        return self._delta_nn

    def set_vector(self, delta_nn=None, delta_step=None):
        # set interval vector (delta_nn, delta_step) manually
        if delta_nn:
            self._delta_nn = delta_nn
        if delta_step:
            self._delta_step = delta_step
        return self

    def get_vector(self):
        return self._delta_nn, self._delta_step

    def get_name(self):
        # get name of `Interval`, e.g. Interval('M2').get_name() = 'M2', etc.
        type = INTERVAL_TYPES[abs(self._delta_nn) % len(NOTE_NAMES)][abs(self._delta_step) % len(NATURAL_NNS)]
        degree = f'{abs(self._delta_step)+1}'
        return type + degree if self._delta_step >= 0 else '-' + type + degree


class DiatonicScale(object):
    def __init__(self, scale_name='C Ionian'):
        '''
            `DiatonicScale` is basically a list of `Note`s
            currently it only supports 12 equal temperament
            number of accidentals and tonic position can uniquely determine the scale
        '''
        # parsing `scale_name`, and get `tonic_name` and `scale_type`
        par1 = scale_name_parser(scale_name)
        tonic_name = par1['tonic_name']
        scale_type = par1['scale_type']

        # parsing `tonic_name`, get `note_name`, `accidental_str` and `group_str` (unused)
        par2 = note_name_parser(tonic_name)
        tonic_name = par2['note_name']
        accidentals_in_tonic_name = 0
        accidentals_in_tonic_name += par2['accidental_str'].count('#')
        accidentals_in_tonic_name -= par2['accidental_str'].count('b')
        tonic_name_enc = TONIC_NAME_ENCODER[tonic_name]
        scale_type_enc = SCALE_TYPE_ENCODER[scale_type]

        # get scale identifiers (number of accidentals and tonic position)
        self._accidentals = tonic_name_enc + 7 * accidentals_in_tonic_name + scale_type_enc
        self._tonic_idx = ['F', 'C', 'G', 'D', 'A', 'E', 'B'].index(tonic_name)

        # get meta notes
        self._meta_notes = [Note('F0'), Note('C0'), Note('G0'), Note('D0'), Note('A0'), Note('E0'), Note('B0')]

        # refresh accidentals
        # put accidental(s) on natural notes
        # order of sharps: FCGDAEB (-->)
        # order of flats: BEADGCF (<--)
        for k in range(0, self._accidentals) if self._accidentals>0 else range(self._accidentals, 0):
            self._meta_notes[k%7] = self._meta_notes[k%7].add_sharp() if self._accidentals>0 else self._meta_notes[k%7].add_flat()

    def __repr__(self):
        note_names = [note.get_name() for note in self.get_notes()]
        return '[' + ''.join([name+', ' for name in note_names[:-1]]) + note_names[-1] + ']'

    def __getitem__(self, item):
        return self.get_notes()[item]

    def __abs__(self):
        # return a list of absolute note midi encoding numbers of current scale
        # e.g. [C0, D0, E0, F0, G0, A0, B0] = [0, 2, 4, 5, 7, 9, 11]
        return [abs(note) for note in self.get_notes()]

    def set_tonic(self, tonic_name):
        # the default tonic is the key in inputting `scale_name`, e.g. `C Ionian` -> 'C'
        par2 = note_name_parser(tonic_name)
        self._tonic_idx = ['F', 'C', 'G', 'D', 'A', 'E', 'B'].index(par2['note_name'])
        return self

    def get_notes(self):
        # generate real notes of current scale from meta notes
        # e.g. meta notes [F, C, G, D, A, E, Bb] + tonic note A = A Phrygian [A, Bb, C, D, E, F, G]
        step_roman_names = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
        notes = [self._meta_notes[self._tonic_idx]]
        notes[0].set_message(f'{step_roman_names[0]}')
        for k in range(1, 7):
            next_note = self._meta_notes[(self._tonic_idx + 2 * k) % 7]
            notes.append(next_note if abs(next_note)>abs(notes[-1]) else next_note + Interval('P8'))
            notes[-1].set_message(f'{step_roman_names[k]}')
        return notes

    def get_name(self, type_only=False):
        # calculate current scale name using `self._meta_notes` and `self._tonic_idx`
        tonic_name_with_accidentals = self.get_notes()[0].get_name(show_group=False)
        par2 = note_name_parser(tonic_name_with_accidentals)
        tonic_name_without_accidentals = par2['note_name']
        accidentals_in_tonic_name = 0
        accidentals_in_tonic_name += par2['accidental_str'].count('#')
        accidentals_in_tonic_name -= par2['accidental_str'].count('b')
        tonic_name_enc = TONIC_NAME_ENCODER[tonic_name_without_accidentals]
        scale_type_enc = self._accidentals - tonic_name_enc - 7 * accidentals_in_tonic_name
        scale_type = SCALE_TYPE_DECODER[scale_type_enc + 3]
        if type_only:
            return scale_type
        else:
            return tonic_name_with_accidentals + ' ' + scale_type

    def get_interval_vector(self):
        # example of interval vector: [C, D, E, F, G, A, B] -> [M2, M2, m2, M2, M2, M2, m2] = [2, 2, 1, 2, 2, 2, 1]
        notes = abs(self)
        notes = notes + [notes[0]+12]
        return [n2-n1 for n1, n2 in zip(notes[:-1], notes[1:])]

    def add_sharp(self, n=1):
        for k in range(self._accidentals, self._accidentals+n):
            self._meta_notes[k%7].add_sharp()
        self._accidentals += n
        return self

    def add_flat(self, n=1):
        for k in range(self._accidentals-n, self._accidentals):
            self._meta_notes[k%7].add_flat()
        self._accidentals -= n
        return self

    def add_accidentals(self, n=0):
        r = (self._accidentals + (0 if n >= 0 else n), self._accidentals + (n if n >= 0 else 0))
        for k in range(*r):
            self._meta_notes[k%7].add_accidental(sign(n))
        self._accidentals += n
        return self

    def get_7th_chord(self, step=0):
        l = len(self.get_notes())
        step = step % l
        body = []
        for i in range(4):
            idx = (step+2*i)
            body.append(self[idx%l] if idx<l else self[idx%l]+Interval('P8'))
        return Chord().set_notes(body=body)

    def get_full_chord(self, step=0):
        l = len(self.get_notes())
        step = step % l
        notes = []
        for i in range(7):
            idx = (step+2*i)
            add_interval = sum([Interval('P8') for _ in range(idx//l)], Interval('P1'))
            notes.append(self[idx%l]+add_interval)
        return Chord().set_notes(body=notes[:4], tensions=notes[4:])


class AlteredDiatonicScale(DiatonicScale):
    def __init__(self, scale_name):
        par = scale_name_parser(scale_name)
        # get base `DiatonicScale` and alternated notes
        if par['altered_note']:
            base_scale_type = par['scale_type']
            altered_notes = altered_note_parser(par['altered_note'])
            accidentals = []
            alternated_steps = []
            for note in altered_notes:
                sharps = note.count('#')
                flats = note.count('b')
                accidentals.append(sharps - flats)
                alternated_steps.append(eval(note[-1]) - 1)
            # base scale initialization
            super().__init__(par['tonic_name']+ ' ' +base_scale_type)
            # alter base scale
            for a, s in zip(accidentals, alternated_steps):
                self._meta_notes[(self._tonic_idx + s * 2) % 7].add_accidental(a)
        # if no altered notes
        else:
            super().__init__(scale_name)

    def get_name(self, top_k=1, return_class=False):
        def _dist(l1, l2):
                return sum([abs(i-j) for i, j in zip(l1, l2)])

        def _is_isomorphic(list_1, list_2):
            # first we compare the length of two sequences
            if len(list_1) != len(list_2): return False

            # compare interval sequences
            def _l_shift(li, k):
                return li[k:] + li[:k]

            for i in range(len(list_1)):
                if _dist(_l_shift(list_1, i), list_2) < 1e-5:
                    return True
                else: pass

            return False

        def _is_equal(list_1, list_2):
            if len(list_1) != len(list_2): return False
            if _dist(list_1, list_2) < 1e-5: return True
            else: return False

        def _delete_comma(scale_type):
            no_comma = re.sub('\(,+', '(', scale_type)
            no_brackets = re.sub('\(\)', '', no_comma)
            return no_brackets

        # compare interval vector with saved files, find class number `idx`
        interval_vector = self.get_interval_vector()
        bools = [_is_isomorphic(interval_vector, iv) for iv in INTERVAL_VECTOR_LIST]
        idx = bools.index(True)

        class_idx = CLASS_LIST[idx]
        step = len(class_idx) // 7

        # from the least accidentals to the most accidentals, return top k nearest scales
        class_idx_reshuffle = sum([[class_idx[s+step*k] for k in range(7)] for s in range(step)], [])

        indices = []
        k = 0
        while(len(indices) < top_k and k < len(class_idx_reshuffle)):
            iv = AlteredDiatonicScale('C'+' '+class_idx_reshuffle[k]).get_interval_vector()
            if _is_equal(interval_vector, iv):
                indices.append(k)
            k += 1

        top_k_scales = [class_idx_reshuffle[i] for i in indices]
        top_k_scales = [_delete_comma(scale) for scale in top_k_scales]

        sharps_on_tonics = [scale_name.count('#1') for scale_name in top_k_scales]
        flats_on_tonics = [scale_name.count('b1') for scale_name in top_k_scales]
        tonic_names = [copy(self[0]).add_flat(sharps_on_tonic).add_sharp(flats_on_tonic).get_name(show_group=False)
                       for sharps_on_tonic, flats_on_tonic in zip(sharps_on_tonics, flats_on_tonics)]
        names = [tonic_name + ' ' + top_k_scale for tonic_name, top_k_scale in zip(tonic_names, top_k_scales)]

        # print(f'Class={idx}, Root={tonic_name}, Type={top_k_scales}')

        if return_class:
            return names, idx
        else:
            return names


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
        steps = CHORD_TYPE_TO_STEPS[par['chord_type']]
        self._body.extend([scale_notes[step].set_message(f'{step+1}') for step in steps])
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
        return [abs(note) for note in self.get_notes()]

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

    def get_name(self, type_only=False):
        # get bass type
        if self._bass:
            bass_type = '/' + self._bass[0].get_name(show_group=False)
        else:
            bass_type = ''

        # get body type
        intervals = [note2-note1 for note1, note2 in zip(self._body[:-1], self._body[1:])]
        interval_vector = ''.join([str(abs(interval)) for interval in intervals])
        body_type = INTERVAL_VECTOR_TO_CHORD_TYPE[interval_vector]

        # get tension type
        tension_to_root_intervals = [t-self._body[0] for t in self._tensions]
        tension_names = [INTERVAL_NAME_TO_TENSION_NAME[str(interval)] for interval in tension_to_root_intervals]
        if self._tensions:
            tension_type = '(' + ''.join([tension_name+', ' for tension_name in tension_names[:-1]]) + tension_names[-1] + ')'
        else:
            tension_type = ''

        chord_type = body_type + tension_type + bass_type
        if type_only:
            return chord_type
        else:
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
