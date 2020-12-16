import re
from copy import copy
from consts import *


''' all kinds of parsers '''


# for `Note`
def note_name_parser(note_name):
    # `note_name` is a string, examples: 'C#3', 'Bb1', 'Fbb3', etc.
    pattern = r'(?P<note_name>[' + NOTE_NAMES_STR + r'])(?P<accidental_str>[b#]*)(?P<group_str>-?\d+)?'
    search_obj = re.search(pattern, note_name)
    return search_obj.groupdict()


# for `Interval`
def interval_name_parser(interval_name):
    # `interval_name` is a string, examples: 'm2', 'M3', 'P4', etc.
    search_obj = re.search(r'(?P<negative_str>-)?(?P<interval_type>[dmPMA]+)(?P<degree_str>[\d]+)', interval_name)
    return search_obj.groupdict()


# for `DiatonicScale`
def scale_name_parser(scale_name):
    # `scale_name` is a string, examples: 'C Ionian', 'D Ionian(#5)', 'E Aeolian(#3, #7)', etc.
    temp = scale_name
    for pat in ALTERNATIVE_NAMES.keys():
        temp = re.sub(pat, ALTERNATIVE_NAMES[pat], temp)
    pattern = r'(?P<tonic_name>[' + NOTE_NAMES_STR + r'][b#]*-?\d*) ?(?P<scale_type>[\w-]+) ?(?P<altered_note>(\([^ac-z]*\)))?'
    search_obj = re.search(pattern, temp)
    return search_obj.groupdict()


def scale_type_parser(scale_type):
    pass


# for `AlteredDiatonicScale`
def altered_note_parser(altered_note):
    # `altered note` is a string, examples: '(b3)', '(b3, b7)', '(#5)', etc.
    return re.findall(r'[#b]+\d+', altered_note)


# for `Chord` and `ChordEx`
def chord_name_parser(chord_name):
    # `chord_name` is a string, examples: 'CM7', 'Dm7(9, 11, 13)', 'Bm7-5/F', etc.
    pattern = r'(?P<root_name>[' + NOTE_NAMES_STR + '][b#]*)(?P<chord_type>\w*[-+]?\d?\w*)(?P<tension_type>(\([^ac-z]*\)))?(/(?P<bass_name>[ABCDEFG][b#]*))?'
    search_obj = re.search(pattern, chord_name)
    return search_obj.groupdict()


def tension_type_parser(tension_type):
    # `tension_type` is a string, examples: '(9)', '(b9, #11)', '(9, 11, 13)', '(9, 13)', etc.
    return re.findall(r'[#b]*\d+', tension_type)


''' fancy music theory classes '''


class Note(object):
    def __init__(self, note_name='C0', vector=(0, 0, 0)):
        if all([N==12, M==7]) :
            par = note_name_parser(note_name)

            # get relative midi encoding number, integer in [0, 11]
            self._nnrel = NOTE_NAMES.index(par['note_name'])

            # get accidentals, integer in (-\infty, \infty)
            accidental = 0
            accidental += par['accidental_str'].count('#')
            accidental -= par['accidental_str'].count('b')
            self._accidental = accidental

            # get group number, integer in (-\infty, \infty)
            if par['group_str']:
                self._group = int(par['group_str'])
            else:
                self._group = 0

            # additional message (such as br357t for `Chord`, etc.)
            self._message = ''

        else:
            self._nnrel, self._accidental, self._group = vector

    def __repr__(self):
        return self.get_name()

    def __sub__(self, other):
        # `Note` - `Note` = `Interval`
        if isinstance(other, Note):
            step1 = NAMED_NOTES.index(self._nnrel) + self._group * M
            step2 = NAMED_NOTES.index(other._nnrel) + other._group * M
            return Interval().set_vector(abs(self) - abs(other), step1 - step2)
        # `Note` - `Interval` = `Note`
        if isinstance(other, Interval):
            return self + (-other)
        else:
            raise TypeError('ClassError: `Note` could only subtract a `Note` or an `Interval`!')

    def __add__(self, other):
        # `Note` + `Interval` = `Note`
        if isinstance(other, Interval):
            delta_nnabs = other._delta_nnabs
            delta_step = other._delta_step
            step = NAMED_NOTES.index(self._nnrel) + delta_step
            nnrel = NAMED_NOTES[step % M]
            group = self._group + step // M
            accidental = abs(self) + delta_nnabs - nnrel - N * group
            return Note().set_vector(nnrel, accidental, group).set_message(self.get_message())
        else:
            raise TypeError('ClassError: `Note` could only add an `Interval`!')

    def __abs__(self):
        # return absolute midi encoding number, integer in (-\infty, \infty), e.g.
        # (in 12-tone equal temperament, diatonic) 'Bb2' = (11, -1, 2) = 11-1+2*12 = 34
        return self._nnrel + self._accidental + self._group * N

    def set_vector(self, nnrel=None, accidental=None, group=None):
        # set note vector (nnrel, accidental, group) manually
        if nnrel:
            if nnrel not in NAMED_NOTES:
                raise ValueError('Given `nnrel` is not a named note. Please consider to choose another one!')
            else:
                self._nnrel = nnrel
        if accidental:
            self._accidental = accidental
        if group:
            self._group = group
        return self

    def get_vector(self, return_group=True):
        if return_group:
            return self._nnrel, self._accidental, self._group
        else:
            return self._nnrel, self._accidental

    def get_name(self, show_group=True):
        # get name of `Note`, e.g. Note('C0').get_name() = 'C0', Note('C0').get_name(show_group=False) = 'C', etc.
        if show_group:
            return NOTE_NAMES[self._nnrel] + (self._accidental * '#' if self._accidental > 0 else -self._accidental * 'b') + f'{self._group}'
        else:
            return NOTE_NAMES[self._nnrel] + (self._accidental * '#' if self._accidental > 0 else -self._accidental * 'b')

    def get_frequency(self):
        nnabs = abs(self)
        # in 12-TET 7-tone diatonic scale:
        # A4 concerto pitch == nnabs57 == 440Hz
        # A3 cubase pitch == nnabs45 == 440Hz
        return 440 * (T ** (nnabs - 45))

    def add_sharp(self, n=1):
        self._accidental += n
        return self

    def add_flat(self, n=1):
        self._accidental -= n
        return self

    def add_accidental(self, n=0):
        # a combination of `add_sharp` and `add_flat` methods
        self._accidental += n

    def add_oct(self, n=1):
        self._group += n
        return self

    def sub_oct(self, n=1):
        self._group -= n
        return self

    def add_group(self, n=0):
        # a combination of `add_oct` and `sub_oct` methods
        self._group += n

    def set_message(self, message):
        # `message` is a string
        self._message = message
        return self

    def get_message(self):
        return self._message

    def get_enharmonic_note(self, direction='auto'):
        # change a note to its enharmonic note, e.g.
        # (in 12-tone equal temperament, diatonic scale) [C, _, D, _, E, F, _, G, _, A, _, B]
        # C#0 -> Db0; C##0 -> D0; D0 -> D0, etc.
        # (in 12-tone equal temperament, diatonic pentatonic scale) [C, _, D, _, E, _, _, G, _, A, _, _]
        # C#0 -> Db0; E#0 -> Gbb0; E##0 -> Gb0; E###0 -> G0; G0 -> G0, etc.
        # (in 19-tone equal temperament, diatonic scale) [C, _, _, D, _, _, E, _, F, _, _, G, _, _, A, _, _, B, _]
        # C#0 -> Dbb0; C##0 -> Db0; C###0 -> D0; D0 -> D0, etc.
        nnabs = abs(self)

        if direction == 'up':
            offset = 1
        elif direction == 'down':
            offset = -1
        elif direction == 'auto':
            offset = sign(self._accidental)
        else:
            raise ValueError(r"Illegal `direction`! Please choose one from 'up', 'down' or 'auto'!")

        idx = [self._nnrel == k for k in NAMED_NOTES].index(True)
        new_idx = idx + offset

        new_nnrel = NAMED_NOTES[new_idx % M]
        new_group = self._group + new_idx // M
        new_accidental = nnabs - new_nnrel - new_group * N

        return Note().set_vector(new_nnrel, new_accidental, new_group)


class Interval(object):
    def __init__(self, interval_name='P1', vector=(0, 0)):
        if all([N==12, M==7]):
            par = interval_name_parser(interval_name)

            # negative or positive
            sgn = -1 if par['negative_str'] else 1

            # get interval type 'd', 'm', 'P', 'M', or 'A'
            interval_type = par['interval_type']

            # get interval degree, positive integer
            degree = int(par['degree_str'])

            # sgn * (degree - 1) for calculating and indexing
            delta_step = sgn * (degree - 1)

            # calculate interval vector (delta_nnabs, delta_step)
            octs = (delta_step % M - delta_step) // M
            center = DELTA_STEP_TO_DELTA_NOTE_CENTER_X2[delta_step % M] - octs * 2 * N
            interval_class = '0347' if delta_step % M in [0, 3, 4, 7] else '1256'
            delta_nnabs_x2 = center + sgn * interval_type_to_delta_nnabs_x2(interval_type, interval_class)
            self._delta_nnabs, self._delta_step = delta_nnabs_x2 // 2, delta_step

        else:
            self._delta_nnabs, self._delta_step = vector

    def __repr__(self):
        if any([N!=12, M!=7]):
            return f'({self._delta_nnabs}, {self._delta_step})'
        else:
            return self.get_name()

    def __add__(self, other):
        # `Interval` + `Note` = `Note`
        if isinstance(other, Note):
            return other + self
        # `Interval` + `Interval` = `Interval`
        elif isinstance(other, Interval):
            return Interval().set_vector(self._delta_nnabs + other._delta_nnabs, self._delta_step + other._delta_step)
        else:
            raise TypeError('ClassError: `Interval` could only add a `Note` or an `Interval`!')

    def __sub__(self, other):
        # `Interval` - `Interval` = `Interval`
        if isinstance(other, Interval):
            return Interval().set_vector(self._delta_nnabs - other._delta_nnabs, self._delta_step - other._delta_step)
        else:
            raise TypeError('ClassError: `Interval` could only subtract an `Interval`!')

    def __neg__(self):
        return Interval().set_vector(-self._delta_nnabs, -self._delta_step)

    def __abs__(self):
        # absolute interval is `self._delta_nnabs`
        return self._delta_nnabs

    def set_vector(self, delta_nnabs=None, delta_step=None):
        # set interval vector (delta_nnabs, delta_step) manually
        if delta_nnabs:
            self._delta_nnabs = delta_nnabs
        if delta_step:
            self._delta_step = delta_step
        return self

    def get_vector(self):
        return self._delta_nnabs, self._delta_step

    def get_name(self):
        # get name of `Interval`, e.g. Interval('M2').get_name() = 'M2', etc.
        if any([N!=12, M!=7]): raise NotImplementedError('`Interval.get_name` method currently requires `N`=12, `M`=7!')

        sgn = 1 if self._delta_step >= 0 else -1
        octs = (self._delta_step % M - self._delta_step) // M
        center = DELTA_STEP_TO_DELTA_NOTE_CENTER_X2[self._delta_step % M] - octs * 2 * N

        delta_nnabs_x2 = sgn * (self._delta_nnabs * 2 - center)
        interval_class = '0347' if f'{self._delta_step % M}' in '0347' else '1256'

        interval_type = delta_nnabs_x2_to_interval_type(delta_nnabs_x2, interval_class)
        degree = f'{abs(self._delta_step) + 1}'

        return interval_type + degree if sgn >= 0 else '-' + interval_type + degree

    def normalize(self):
        octs = (self._delta_step % M - self._delta_step) // M
        self._delta_step = self._delta_step % M
        self._delta_nnabs = self._delta_nnabs + N * octs
        return self


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

        return ChordEx().set_notes(notes=body)

    def get_full_chord(self, step=0):
        l = len(self.get_notes())
        step = step % l
        notes = []
        for i in range(7):
            idx = (step+2*i)
            add_interval = sum([Interval('P8') for _ in range(idx//l)], Interval('P1'))
            notes.append(self[idx%l]+add_interval)

        return Chord().set_notes(body=notes[:4], tensions=notes[4:])

    def get_full_chord_ex(self, step=0):
        l = len(self.get_notes())
        step = step % l
        notes = []
        for i in range(7):
            idx = (step+2*i)
            add_interval = sum([Interval('P8') for _ in range(idx//l)], Interval('P1'))
            notes.append(self[idx%l]+add_interval)

        return ChordEx().set_notes(notes=notes)


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

    def get_name(self, top_k=1, type_only=False, return_class_idx=False):
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
        bools = [_is_isomorphic(interval_vector, iv) for iv in SCALE_INTERVAL_VECTOR_LIST]
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

        if type_only:
            names = [top_k_scale for tonic_name, top_k_scale in zip(tonic_names, top_k_scales)]
        else:
            names = [tonic_name + ' ' + top_k_scale for tonic_name, top_k_scale in zip(tonic_names, top_k_scales)]

        if return_class_idx:
            return names, idx
        else:
            return names

    def get_conventional_name(self):
        name = self.get_name(type_only=True)[0]
        if name in CONVENTIONAL_NAMES.keys():
            return CONVENTIONAL_NAMES[name]
        else:
            return []


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
            self._bass = [bass.set_message('B')]
        if body:
            self._body = body
            messages = ['R', '3', '5', '7']
            for i, note in enumerate(self._body):
                note.set_message(messages[i])
        if tensions:
            self._tensions = tensions
            for note in self._tensions:
                note.set_message(INTERVAL_NAME_TO_TENSION_NAME[str(note-self._body[0])])

        return self

    def get_notes(self, bass_on=True):
        if bass_on:
            return self._bass + self._body + self._tensions
        else:
            return self._body + self._tensions

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

    def get_scale(self, top_k=1, return_class_idx=False):
        ''' get least-order scale of current chord '''
        def _dist(l1, l2):
                return sum([abs(i-j) for i, j in zip(l1, l2)])

        def _lshift(l, k):
            return l[k:] + l[:k]

        def _is_equal(list_1, list_2):
            if len(list_1) != len(list_2): return False
            if _dist(list_1, list_2) < 1e-5: return True
            else: return False

        chord_notes = self.get_notes(bass_on=False)
        root_name = chord_notes[0].get_name(show_group=False)
        iv = [abs(n2-n1) for n1, n2 in zip(chord_notes[:-1], chord_notes[1:])]

        # find all root positions in 66 classes of current chord
        all_steps = [[(k*2)%7 for k in range(7) if _is_equal(_lshift(interval_vector, k)[:len(iv)], iv)] for interval_vector in CHORD_INTERVAL_VECTOR_LIST]

        all_scales = []
        all_indices = []
        num_class = 0
        for k, indices in enumerate(all_steps):
            if num_class >= top_k: break
            if indices:
                class_k = CLASS_LIST[k]
                step = len(class_k) // 7
                # from the least accidentals to the most accidentals, return top k nearest scales
                class_k_reshuffle = sum([[class_k[s+step*j] for j in range(7)] for s in range(step)], [])
                for idx in indices:
                    cur_scale_type = class_k_reshuffle[(idx*2)%7]
                    sharps_on_tonics = cur_scale_type.count('#1')
                    flats_on_tonics = cur_scale_type.count('b1')
                    new_root_name = root_name + '#'*flats_on_tonics + 'b'*sharps_on_tonics
                    cur_scale = AlteredDiatonicScale(new_root_name + ' ' + cur_scale_type)
                    all_scales.append(cur_scale)
                    all_indices.append(k)
                num_class += 1

        if return_class_idx:
            return all_scales, all_indices
        else:
            return all_scales

    def get_icd(self, note_name):
        ''' get in-chord degree of a note '''
        scales = self.get_scale(66)
        icds = []
        for scale in scales:
            scale_nvs = [note.get_vector(return_group=False) for note in scale]  # nvs = note vectors
            note = Note(note_name)
            note_nv = note.get_vector(return_group=False)
            if note_nv not in scale_nvs:
                icds.append((scale.get_name()[0], -1))
            else:
                icds.append((scale.get_name()[0], scale_nvs.index(note_nv) + 1))
        return icds[[x[1]!=-1 for x in icds].index(True)]


class ChordEx(object):
    def __init__(self):
        self._bass = None
        self._notes = []
        self._steps = []

    def __repr__(self):
        note_names = [note.get_name() for note in self.get_notes() if note is not None]
        return '[' + ''.join([name+', ' for name in note_names[:-1]]) + note_names[-1] + ']'

    def __getitem__(self, item):
        return self.get_notes()[item]

    def __abs__(self):
        return [abs(note) for note in self.get_notes()]

    def set_notes(self, bass=None, notes=None):
        if bass:
            self._bass = bass
        if notes:
            self._notes = notes
            intervals = [note - notes[0] for note in notes]
            delta_steps = [interval.get_vector()[1] for interval in intervals]
            for note, ds in zip(notes, delta_steps):
                self._steps.append(ds % 7 + 1)
        return self

    def get_notes(self, bass_on=True):
        if bass_on and self._bass is not None:
            return self._bass + self._notes
        else:
            return self._notes

    def get_name(self, type_only=False):
        intervals = [note - self._notes[0] for note in self._notes]
        intervals = [interval.normalize().get_name() for interval in intervals]

        # get bass type
        if self._bass:
            bass_type = '/' + self._bass[0].get_name(show_group=False)
        else:
            bass_type = ''

        # get body type
        if 3 in self._steps:
            third_idx = self._steps.index(3)
            third_type = INTERVAL_NAME_TO_CHORD_TYPE[intervals[third_idx]]
            if third_type not in ['m', 'M']:
                third_type_post, third_type = third_type, ''
            else:
                third_type_post = ''
        else:
            third_type, third_type_post = '', ''

        if 5 in self._steps:
            fifth_idx = self._steps.index(5)
            fifth_type = INTERVAL_NAME_TO_CHORD_TYPE[intervals[fifth_idx]]
            if fifth_type not in ['']:
                fifth_type_post, fifth_type = fifth_type, ''
            else:
                fifth_type_post = ''
        else:
            fifth_type, fifth_type_post = '', ''

        if 7 in self._steps:
            seventh_idx = self._steps.index(7)
            seventh_type = INTERVAL_NAME_TO_CHORD_TYPE[intervals[seventh_idx]]
        else:
            seventh_type = ''

        # get tension type
        tension_types = []
        for k in [2, 4, 6]:
            if k in self._steps:
                idx = self._steps.index(k)
                tension_types.append(INTERVAL_NAME_TO_CHORD_TYPE[intervals[idx]])

        # generate chord type
        body_type = third_type + fifth_type + seventh_type + fifth_type_post + third_type_post
        if tension_types:
            tension_type = '(' + ''.join([t + ', ' for t in tension_types[:-1]]) + tension_types[-1] + ')'
        else:
            tension_type = ''
        chord_type =  body_type + tension_type + bass_type
        if type_only:
            return chord_type
        else:
            return f'{self._notes[0].get_name(show_group=False)}{chord_type}'

    def get_scale(self, top_k=1, return_class_idx=False):
        ''' get least-order scale of current chord '''
        def _dist(l1, l2):
                return sum([abs(i-j) for i, j in zip(l1, l2)])

        def _lshift(l, k):
            return l[k:] + l[:k]

        def _is_equal(list_1, list_2):
            if len(list_1) != len(list_2): return False
            if _dist(list_1, list_2) < 1e-5: return True
            else: return False

        chord_notes = self.get_notes(bass_on=False)
        root_name = chord_notes[0].get_name(show_group=False)
        iv = [abs(n2-n1) for n1, n2 in zip(chord_notes[:-1], chord_notes[1:])]

        # find all root positions in 66 classes of current chord
        all_steps = [[(k*2)%7 for k in range(7) if _is_equal(_lshift(interval_vector, k)[:len(iv)], iv)] for interval_vector in CHORD_INTERVAL_VECTOR_LIST]

        all_scales = []
        all_indices = []
        num_class = 0
        for k, indices in enumerate(all_steps):
            if num_class >= top_k: break
            if indices:
                class_k = CLASS_LIST[k]
                step = len(class_k) // 7
                # from the least accidentals to the most accidentals, return top k nearest scales
                class_k_reshuffle = sum([[class_k[s+step*j] for j in range(7)] for s in range(step)], [])
                for idx in indices:
                    cur_scale_type = class_k_reshuffle[(idx*2)%7]
                    sharps_on_tonics = cur_scale_type.count('#1')
                    flats_on_tonics = cur_scale_type.count('b1')
                    new_root_name = root_name + '#'*flats_on_tonics + 'b'*sharps_on_tonics
                    cur_scale = AlteredDiatonicScale(new_root_name + ' ' + cur_scale_type)
                    all_scales.append(cur_scale)
                    all_indices.append(k)
                num_class += 1

        if return_class_idx:
            return all_scales, all_indices
        else:
            return all_scales

    def get_icd(self, note_name):
        ''' get in-chord degree of a note '''
        scales = self.get_scale(66)
        icds = []
        for scale in scales:
            scale_nvs = [note.get_vector(return_group=False) for note in scale]  # nvs = note vectors
            note = Note(note_name)
            note_nv = note.get_vector(return_group=False)
            if note_nv not in scale_nvs:
                icds.append((scale.get_name()[0], -1))
            else:
                icds.append((scale.get_name()[0], scale_nvs.index(note_nv) + 1))
        return icds[[x[1]!=-1 for x in icds].index(True)]


class ChordScale(AlteredDiatonicScale):
    def __init__(self, scale_name):
        super().__init__(scale_name)
        self._chord_notes = [0, 2, 4, 6]
        self._tension_notes = [k for k in range(7) if k not in self._chord_notes]

    def get_info(self):
        notes = self.get_notes()
        itvs = [n - notes[0] for n in notes]
        itvs_abs = [abs(i) for i in itvs]
        itvs_abs_mod = [i % 12 for i in itvs_abs]
        degs = [INTERVAL_NAME_TO_TENSION_NAME[str(i)] for i in itvs]
        labels = [''] * len(degs)
        fake_dom7 = False
        fake_m7 = False

        # add "[CN]" to every base chord note
        for i in self._chord_notes:
            labels[i] = '[CN]'

        # add "[TN]" to every tension note
        for i in self._tension_notes:
            labels[i] = '[TN]'

        # if it contains dom7 chord (include enharmonic equivalents)
        if all([na in itvs_abs_mod for na in [4, 10]]):
            # if it contains real dom7 chord
            if '3' in degs and 'b7' in degs:
                # half tone above base chord note, but available because of dom7 base chord
                for idx in range(1, len(itvs_abs)):
                    if any([itvs_abs[idx]-itvs_abs[j]==1 for j in self._chord_notes]):
                            labels[idx] = '[OK]'
                # avoid_type_0: tonic note in dom7 chord
                if 5 in itvs_abs_mod:
                    idx = itvs_abs_mod.index(5)
                    labels[idx] = '[A0]'
            # if it contains fake dom7 chord
            else:
                fake_dom7 = True
                # avoid_type_1: half tone above base chord note
                for idx in range(1, len(itvs_abs)):
                    if any([itvs_abs[idx] - itvs_abs[j] == 1 for j in self._chord_notes]):
                        labels[idx] = '[A1]'
                    # avoid_type_1: half tone below M7
                    if '7' in degs:
                        idx_M7 = degs.index('7')
                        if itvs_abs[idx_M7] - itvs_abs[idx] == 1:
                            labels[idx] = '[A1]'

        # if it contains m7 chord (include enharmonic equivalents)
        if all([na in itvs_abs_mod for na in [3, 10]]):
            # if it contains real m7 chord
            if 'b3' in degs and 'b7' in degs:
                # avoid_type_1: half tone above 7th chord note
                for idx in range(1, len(itvs_abs)):
                    if any([itvs_abs[idx] - itvs_abs[j] == 1 for j in self._chord_notes]):
                        labels[idx] = '[A1]'
                    # avoid_type_1: half tone below M7
                    if '7' in degs:
                        idx_M7 = degs.index('7')
                        if itvs_abs[idx_M7] - itvs_abs[idx] == 1:
                            labels[idx] = '[A1]'
            # if it contains fake m7 chord
            else:
                fake_m7 = True
                # avoid_type_1: half tone above 7th chord note
                for idx in range(1, len(itvs_abs)):
                    if any([itvs_abs[idx] - itvs_abs[j] == 1 for j in self._chord_notes]):
                        labels[idx] = '[A1]'
                    # avoid_type_1: half tone below M7
                    if '7' in degs:
                        idx_M7 = degs.index('7')
                        if itvs_abs[idx_M7] - itvs_abs[idx] == 1:
                            labels[idx] = '[A1]'

        if not (all([na in itvs_abs_mod for na in [4, 10]]) or all([na in itvs_abs_mod for na in [3, 10]])):
            # avoid_type_1: half tone above 7th chord note
            for idx in range(1, len(itvs_abs)):
                if any([itvs_abs[idx] - itvs_abs[j] == 1 for j in self._chord_notes]):
                    labels[idx] = '[A1]'
                # avoid_type_1: half tone below M7
                if '7' in degs:
                    idx_M7 = degs.index('7')
                    if itvs_abs[idx_M7] - itvs_abs[idx] == 1:
                        labels[idx] = '[A1]'

        long_list = ['x'] * 12
        for i, n in enumerate(itvs_abs_mod):
            long_list[n] = labels[i] + ' ' + degs[i]

        return labels, long_list, fake_dom7, fake_m7

    def get_color(self):
        notes = self.get_notes()
        color = '#'
        for i in self._chord_notes + self._tension_notes:
            if i == 0: continue

            color = color + f'{hex(abs(notes[i] - notes[0]))}'[2:]

        return color


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
