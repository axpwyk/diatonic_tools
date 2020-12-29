import re
from copy import copy, deepcopy
from consts import *


''' ----------------------------------------------------------------------------------------- '''
''' ********************************** all kinds of parsers ********************************* '''
''' ----------------------------------------------------------------------------------------- '''


# for `Note`
def note_name_parser(note_name):
    # `note_name` is a string, examples: 'C#3', 'Bb1', 'Fbb3', etc.
    pattern = r'(?P<named_note_name>[' + NAMED_LIN_STR + r'])(?P<accidental_str>[b#]*)(?P<register_str>-?\d*)'
    search_obj = re.search(pattern, note_name)
    return search_obj.groupdict()


def note_name_to_note_vector(note_name):
    par = note_name_parser(note_name)

    named_note_name = par['named_note_name']
    accidental_str = par['accidental_str']
    register_str = par['register_str']

    # get relative note number, integer in [0, N]
    nnrel = NAME_STR_TO_NNREL[named_note_name]

    # get accidentals, integer in (-\infty, \infty)
    accidental = 0 + accidental_str.count('#') - accidental_str.count('b')

    # get register number, integer in (-\infty, \infty)
    if register_str:
        register = int(register_str)
    else:
        register = 0

    return nnrel, accidental, register


# for `Interval`
def interval_name_parser(interval_name):
    # `interval_name` is a string, examples: 'm2', 'M3', 'P4', etc.
    search_obj = re.search(r'(?P<negative_str>-{0,1})(?P<interval_type>[dmPMA]+)(?P<degree_str>[\d]+)', interval_name)
    return search_obj.groupdict()


def interval_name_to_interval_vector(interval_name):
    """
    when [N, G, S] == [12, 7, 5], will choose naming scheme automatically
    when [N, G, S] != [12, 7, 5], will use naming scheme 2

    :param interval_name: interval name, e.g. 'P1', 'M2', etc.
    """
    par = interval_name_parser(interval_name)

    # negative or positive (will add this at the end)
    sgn = -1 if par['negative_str'] else 1

    # get interval type .., 'dd', 'd', 'm', 'P', 'M', 'A', 'AA', ...
    interval_type = par['interval_type']

    # get interval degree, positive integer
    degree = int(par['degree_str'])

    # get `abs(delta_step)`
    delta_step = degree - 1

    # get naming scheme
    if all([N == 12, G == 7, S == 5]):
        ns = DELTA_STEP_TO_NS_12_7_5[delta_step % M]
    else:
        ns = 2

    # calculate `delta_group`
    if ns == 1:
        delta_group = interval_type.count('A') - interval_type.count('d')
    elif ns == 2:
        ds = interval_type.count('d')
        if ds > 0:
            delta_group = interval_type.count('A') - interval_type.count('m') - interval_type.count('d') + 1
        else:
            delta_group = interval_type.count('A') - interval_type.count('m')
    else:
        raise ValueError('No such naming scheme! Choose `ns` from [1, 2]!')

    # calculate `delta_nnabs`
    delta_step_rel = delta_step % M
    delta_register = delta_step // M

    named_nnrel = NAMED_LIN_NNREL[delta_step_rel]
    delta_nnabs = delta_group + named_nnrel + N * delta_register

    return sgn * delta_nnabs, sgn * delta_step


# for `DiatonicScale`
def scale_name_parser(scale_name):
    # `scale_name` is a string, examples: 'C C-mode', 'D C-mode(#5)', 'E A-mode(#3, #7)', etc.
    pattern = r'(?P<scale_tonic_name>[' + NAMED_LIN_STR + r'][b#]*-{0,1}\d*) ?(?P<scale_type>[\w-]+) ?(?P<altered_note>(\([^ac-z]*\)){0,1})'
    search_obj = re.search(pattern, scale_name)
    return search_obj.groupdict()


def scale_type_parser(scale_type):
    # `scale_type` is a string, examples: 'D-mode', 'E-mode', 'α-mode', etc.
    # in [12, 7, 5] diatonic scale, D-mode is Dorian, E-mode is Phrygian, etc.
    pattern = '(?P<mode_tonic_name>[' + NAMED_LIN_STR + '])(?=(-mode))'
    search_obj = re.search(pattern, scale_type)
    return search_obj.groupdict()


# for `AlteredDiatonicScale`
def altered_note_parser(altered_note):
    # `altered note` is a string, examples: '(b3)', '(b3, b7)', '(#5)', etc.
    return re.findall(r'[#b]+\d+', altered_note)


# for `Chord`
def chord_name_parser(chord_name):
    # `chord_name` is a string, examples: 'CM7', 'Dm7(9, 11, 13)', 'Bm7-5/F', etc.
    pattern = r'(?P<root_name>[' + \
              NAMED_LIN_STR + \
              '][b#]*)(?P<chord_type>\w*[-+]?\d?\w*)(?P<tension_type>(\([^ac-z]*\)){0,1})/?(?P<bass_name>([' + \
              NAMED_LIN_STR + '][b#]*){0,1})'
    search_obj = re.search(pattern, chord_name)
    return search_obj.groupdict()


def tension_type_parser(tension_type):
    # `tension_type` is a string, examples: '(9)', '(b9, #11)', '(9, 11, 13)', '(9, 13)', etc.
    return re.findall(r'[#b]*\d+', tension_type)


''' ----------------------------------------------------------------------------------------- '''
''' ************************** fancy music theory classes (general) ************************* '''
''' ----------------------------------------------------------------------------------------- '''


class Note(object):
    def __init__(self, note_name=f'{NAMED_LIN_STR[0]}0'):
        # get note vector
        self._nnrel, self._accidental, self._register = note_name_to_note_vector(note_name)

        # additional message dict
        self._message = dict()

    def __repr__(self):
        return self.get_name()

    def __sub__(self, other):
        # `Note` - `Note` = `Interval`
        if isinstance(other, Note):
            step1 = NAMED_LIN_NNREL.index(self._nnrel) + self._register * M
            step2 = NAMED_LIN_NNREL.index(other._nnrel) + other._register * M
            return Interval().set_vector(abs(self) - abs(other), step1 - step2)
        # `Note` - `Interval` = `Note`
        if isinstance(other, Interval):
            return self + (-other)
        else:
            raise TypeError('ClassError: `Note` can only subtract a `Note` or an `Interval`!')

    def __add__(self, other):
        # `Note` + `Interval` = `Note`
        if isinstance(other, Interval):
            delta_nnabs, delta_step = other.get_vector()
            new_step = NAMED_LIN_NNREL.index(self._nnrel) + delta_step
            new_nnrel = NAMED_LIN_NNREL[new_step % M]
            new_register = self._register + new_step // M
            new_accidental = abs(self) + delta_nnabs - new_nnrel - N * new_register
            return Note().set_vector(new_nnrel, new_accidental, new_register).set_message_dict(**self.get_message_dict())
        else:
            raise TypeError('ClassError: `Note` can only add an `Interval`!')

    def __abs__(self):
        """
        return absolute note number
        (in [12, 7, 5] diatonic scale) 'Bb2' = (11, -1, 2) = 11 + (-1) + 2 * 12 = 34

        :return: absolute note number, integer in (-\infty, \infty)
        """
        return self._nnrel + self._accidental + self._register * N

    def set_vector(self, nnrel=None, accidental=None, register=None):
        # set note vector (nnrel, accidental, register) manually
        if nnrel:
            if nnrel not in NAMED_LIN_NNREL:
                raise ValueError('Given `nnrel` do not correspond to a named note. Please choose another one!')
            else:
                self._nnrel = nnrel
        if accidental:
            self._accidental = accidental
        if register:
            self._register = register
        return self

    def get_vector(self, return_register=True):
        if return_register:
            return self._nnrel, self._accidental, self._register
        else:
            return self._nnrel, self._accidental

    def get_name(self, show_register=True):
        # get name of `Note`, e.g. Note('C0').get_name() = 'C0', Note('C0').get_name(show_register=False) = 'C', etc.
        if show_register:
            return NNREL_TO_NAME_STR[self._nnrel] + (self._accidental * '#' if self._accidental > 0 else -self._accidental * 'b') + f'{self._register}'
        else:
            return NNREL_TO_NAME_STR[self._nnrel] + (self._accidental * '#' if self._accidental > 0 else -self._accidental * 'b')

    def get_frequency(self):
        """
        (in [12, 7, 5] diatonic scale)
        A4 concerto pitch == nnabs57 == 440Hz
        A3 cubase pitch == nnabs45 == 440Hz

        :return: frequency of current note (float type)
        """
        return C3 * (T ** (abs(self) - N * 3))

    def add_accidental(self, n=0):
        # a combination of `add_sharp` and `add_flat` methods
        self._accidental += n
        return self

    def add_register(self, n=0):
        # a combination of `add_register` and `sub_register` methods
        self._register += n
        return self

    def set_message(self, **kwargs):
        self._message = {**self._message, **kwargs}
        return self

    def get_message(self, key):
        if key in self._message.keys():
            return self._message[key]
        else:
            return None

    def set_message_dict(self, **kwargs):
        self._message = {**kwargs}
        return self

    def get_message_dict(self):
        return self._message

    def get_enharmonic_note(self, direction='auto'):
        """
        change a note to its enharmonic note, e.g.

        (in [12, 7, 5] diatonic scale) [C, _, D, _, E, F, _, G, _, A, _, B]
        C#0 -> Db0; C##0 -> D0; D0 -> D0, etc.

        (in [12, 5, 4] diatonic scale) [C, _, D, _, E, _, _, G, _, A, _, _]
        C#0 -> Db0; E#0 -> Gbb0; E##0 -> Gb0; E###0 -> G0; G0 -> G0, etc.

        (in [19, 11, 8] diatonic scale) [C, _, _, D, _, _, E, _, F, _, _, G, _, _, A, _, _, B, _]
        C#0 -> Dbb0; C##0 -> Db0; C###0 -> D0; D0 -> D0, etc.

        :param direction: direction of delta step
        :return: enharmonic note (Note type)
        """
        nnabs = abs(self)

        if direction == 'up':
            offset = 1
        elif direction == 'down':
            offset = -1
        elif direction == 'auto':
            offset = sign(self._accidental)
        else:
            raise ValueError(r"Illegal `direction`! Please choose one from 'up', 'down' or 'auto'!")

        step = NAMED_LIN_NNREL.index(self._nnrel)
        new_step = step + offset

        new_nnrel = NAMED_LIN_NNREL[new_step % M]
        new_register = self._register + new_step // M
        new_accidental = nnabs - new_nnrel - new_register * N

        return Note().set_vector(new_nnrel, new_accidental, new_register)


class Interval(object):
    def __init__(self, interval_name='P1'):
        # get interval vector
        self._delta_nnabs, self._delta_step = interval_name_to_interval_vector(interval_name)

    def __repr__(self):
        return self.get_name()

    def __add__(self, other):
        # `Interval` + `Note` = `Note`
        if isinstance(other, Note):
            return other + self
        # `Interval` + `Interval` = `Interval`
        elif isinstance(other, Interval):
            return Interval().set_vector(self._delta_nnabs + other._delta_nnabs, self._delta_step + other._delta_step)
        else:
            raise TypeError('ClassError: `Interval` can only add a `Note` or an `Interval`!')

    def __sub__(self, other):
        # `Interval` - `Interval` = `Interval`
        if isinstance(other, Interval):
            return Interval().set_vector(self._delta_nnabs - other._delta_nnabs, self._delta_step - other._delta_step)
        else:
            raise TypeError('ClassError: `Interval` can only subtract an `Interval`!')

    def __mul__(self, other):
        if isinstance(other, int):
            return Interval().set_vector(self._delta_nnabs*other, self._delta_step*other)
        else:
            raise TypeError('ClassError: `Interval` can only multiply an integer!')

    def __rmul__(self, other):
        if isinstance(other, int):
            return Interval().set_vector(other*self._delta_nnabs, other*self._delta_step)
        else:
            raise TypeError('ClassError: `Interval` can only multiply an integer!')

    def __neg__(self):
        return Interval().set_vector(-self._delta_nnabs, -self._delta_step)

    def __abs__(self):
        sgn = sign(self._delta_step)
        return Interval().set_vector(sgn * self._delta_nnabs, sgn * self._delta_step)

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
        """
        it only exists 2 types of intervals that contain same number of named notes in diatonic scale

        we call the larger interval P (Perfect), and the smaller interval d (diminished):
        ... < ddd < dd < d < P < A < AA < AAA < ... (naming scheme 1, `ns`=1)

        we can also call the larger interval M (major), and the smaller interval m (minor):
        ... < dd < d < m < M < A < AA < AAA < ... (naming scheme 2, `ns`=2)

        * notice: '-M2' and 'M-2' are different, we will use the former one when `delta_step` < 0

        :return: interval name (type: str)
        """
        sgn = sign(self._delta_step)

        if sgn < 0:
            delta_nnabs = -self._delta_nnabs
            delta_step = -self._delta_step
        else:
            delta_nnabs = self._delta_nnabs
            delta_step = self._delta_step

        delta_step_rel = delta_step % M
        delta_register = delta_step // M

        named_nnrel = NAMED_LIN_NNREL[delta_step_rel]
        delta_group = delta_nnabs - N * delta_register - named_nnrel

        # get naming scheme
        if all([N == 12, G == 7, S == 5]):
            ns = DELTA_STEP_TO_NS_12_7_5[delta_step % M]
        else:
            ns = 2

        if ns == 1:
            if delta_group > 0:
                type = 'A' * delta_group
            elif delta_group == 0:
                type = 'P'
            else:
                type = 'd' * abs(delta_group)
        elif ns == 2:
            if delta_group > 0:
                type = 'A' * delta_group
            elif delta_group == 0:
                type = 'M'
            elif delta_group == -1:
                type = 'm'
            else:
                type = 'd' * (abs(delta_group) - 1)
        else:
            raise ValueError('No such naming scheme! Choose `ns` from [1, 2]!')

        return -sgn * '-' + type + f'{delta_step + 1}'

    def get_r357t(self):
        if not all([N==12, G==7, S==5]):
            raise ValueError('`Interval.get_r357t` method currently only works when [N, G, S] = [12, 7, 5]!')
        delta_nnabs, delta_step = self.get_vector()
        delta_nnrel = delta_nnabs % N
        delta_step_rel = delta_step % M
        accidentals = delta_nnrel - NAMED_LIN_NNREL[delta_step_rel]  # based on Ionian mode
        r357t = ('#' * accidentals if accidentals > 0 else 'b' * abs(accidentals)) + str(delta_step + 1)
        return 'R' if r357t == '1' else r357t

    def normalize(self):
        delta_group = self._delta_step // M
        self._delta_step = self._delta_step % M
        self._delta_nnabs = self._delta_nnabs - N * delta_group
        return self


class DiatonicScale(object):
    def __init__(self, scale_name=f'{NAMED_LIN_STR[0]} {NAMED_LIN_STR[0]}-mode'):
        """
        Create a note list, which has diatonic property in `N`-TET system
        `self._meta_notes` are the notes in sequence of generative order
        """

        # parse `scale_name`, get `tonic_name` and `scale_type`
        par1 = scale_name_parser(scale_name)
        scale_tonic_name = par1['scale_tonic_name']

        # parse `scale_tonic_name`
        st_nnrel, st_accidental, st_register = note_name_to_note_vector(scale_tonic_name)

        # change old scale type to new scale type, e.g. `Ionian` -> `C-mode`
        scale_type = par1['scale_type']
        if scale_type in SCALE_TYPE_OLD_TO_NEW.keys():
            scale_type = SCALE_TYPE_OLD_TO_NEW[scale_type]

        # parse `scale_type`, and get `mode_tonic_name`
        mode_tonic_name = scale_type_parser(scale_type)['mode_tonic_name']

        # parse `mode_tonic_name`
        mt_nnrel, mt_accidental, mt_register = note_name_to_note_vector(mode_tonic_name)

        # get number of accidentals
        st_step_gen = NAMED_GEN_NNREL.index(st_nnrel)
        mt_step_gen = NAMED_GEN_NNREL.index(mt_nnrel)
        accidentals = st_step_gen + M * st_accidental - mt_step_gen
        self._st_step_gen = st_step_gen
        self._accidentals = accidentals

        # get meta notes
        self._meta_notes = [Note(f'{s}{st_register}') for s in NAMED_GEN_STR]

        # put accidental(s) on meta notes
        # order of sharps: (in [12, 7, 5] diatonic scale) FCGDAEB
        # order of flats: (in [12, 7, 5] diatonic scale) BEADGCF
        for k in range(0, accidentals) if accidentals > 0 else range(accidentals, 0):
            if accidentals > 0:
                self._meta_notes[k % M].add_accidental(1)
            else:
                self._meta_notes[k % M].add_accidental(-1)

        self._refresh()

    def __repr__(self):
        note_names = [note.get_name() for note in self]
        return '[' + ''.join([name+', ' for name in note_names[:-1]]) + note_names[-1] + ']'

    def __getitem__(self, item):
        """
        a linear view of `self._meta_notes` (remember that `self._meta_notes` is of generative order)
        changes will affect `self._meta_notes`
        """
        notes = sorted(self._meta_notes, key=lambda m: abs(m))

        # find index of tonic note in `notes`
        notes_nnabs = [abs(note) for note in notes]
        st_step = notes_nnabs.index(abs(self._meta_notes[self._st_step_gen]))

        # roll `notes`, make tonic note the 1st element
        notes = notes[st_step:] + notes[:st_step]

        return notes[item]

    def __abs__(self):
        # return a list of absolute note numbers `nnabs` of current scale
        # e.g. (in [12, 7, 5] diatonic scale) [C0, D0, E0, F0, G0, A0, B0] = [0, 2, 4, 5, 7, 9, 11]
        return [abs(note) for note in self]

    def _refresh(self):
        # add registers
        notes_nnabs = [abs(note) for note in self]
        notes_nnabs_bool = [nnabs < notes_nnabs[0] for nnabs in notes_nnabs]
        if True in notes_nnabs_bool:
            st_step = notes_nnabs_bool.index(True)
            for note in self[st_step:]:
                note.add_register(1)

        # add degree message for every note
        for k, note in enumerate(self):
            note.set_message(degree=k)

    def set_tonic(self, scale_tonic_name):
        # the default scale tonic note is in inputting `scale_name`, e.g. `C Ionian` -> 'C'
        st_nnrel, _, _ = note_name_to_note_vector(scale_tonic_name)
        self._st_step_gen = NAMED_GEN_NNREL.index(st_nnrel)

        self._refresh()

        return self

    def get_name(self, type_only=False, old_name=False):
        # calculate current scale name using `self._meta_notes` and `self._tonic_step`
        scale_tonic_name = self[0].get_name(show_register=False)

        st_nnrel, st_accidental, st_register = note_name_to_note_vector(scale_tonic_name)

        st_step_gen = NAMED_GEN_NNREL.index(st_nnrel)
        mt_step_gen = st_step_gen + M * st_accidental - self._accidentals

        scale_type = NAMED_GEN_STR[mt_step_gen] + '-mode'

        if old_name and all([N==12, M==7]):
            scale_type = SCALE_TYPE_NEW_TO_OLD[scale_type]

        if type_only:
            return scale_type
        else:
            return scale_tonic_name + ' ' + scale_type

    def get_intervals_seq(self):
        # example of interval vector: [C, D, E, F, G, A, B] -> [M2, M2, m2, M2, M2, M2, m2]
        notes = [*self, self[0] + Interval().set_vector(N, M)]
        return [n2 - n1 for n1, n2 in zip(notes[:-1], notes[1:])]

    def get_intervals_cum(self):
        # example of interval vector: [C, D, E, F, G, A, B] -> [P1, M2, M3, P4, P5, M6, M7]
        return [note - self[0] for note in self]

    def add_accidental(self, n=0):
        r = (self._accidentals + (0 if n >= 0 else n), self._accidentals + (n if n >= 0 else 0))
        for k in range(*r):
            self._meta_notes[k % M].add_accidental(sign(n))
        self._accidentals += n
        return self

    def add_register(self, n=0):
        for note in self:
            note.add_register(n)

    def get_chord(self, root_degree=0, n_notes=4, n_step_length=2):
        root_degree = root_degree % M

        notes = []
        for i in range(n_notes):
            idx = root_degree + n_step_length * i
            notes.append(copy(self[idx % M]) if idx < M else copy(self[idx % M]).add_register(idx // M))

        return notes


class AlteredDiatonicScale(DiatonicScale):
    def __init__(self, scale_name):
        par = scale_name_parser(scale_name)

        scale_tonic_name = par['scale_tonic_name']
        base_scale_type = par['scale_type']

        super().__init__(scale_tonic_name + ' ' + base_scale_type)

        # get altered notes
        if par['altered_note']:
            altered_notes = altered_note_parser(par['altered_note'])

            accidentals = []
            altered_degrees = []
            for note in altered_notes:
                accidentals.append(note.count('#') - note.count('b'))
                altered_degrees.append(int(''.join([s for s in note if s.isdigit()])) - 1)

            # alter base scale
            for a, d in zip(accidentals, altered_degrees):
                self[d % M].add_accidental(a)

    # TODO: study of `N`-TET altered diatonic scale; how to get its name?
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
        interval_list = [itv.get_vector()[0] for itv in self.get_intervals_seq()]
        print(interval_list)
        bools = [_is_isomorphic(interval_list, il) for il in SCALE_INTERVAL_VECTOR_LIST]
        idx = bools.index(True)

        class_idx = CLASS_LIST[idx]
        step = len(class_idx) // 7

        # from the least accidentals to the most accidentals, return top k nearest scales
        class_idx_reshuffle = sum([[class_idx[s+step*k] for k in range(7)] for s in range(step)], [])

        indices = []
        k = 0
        while len(indices) < top_k and k < len(class_idx_reshuffle):
            il = [itv.get_vector()[0] for itv in AlteredDiatonicScale('C'+' '+class_idx_reshuffle[k]).get_intervals_seq()]
            if _is_equal(interval_list, il):
                indices.append(k)
            k += 1

        top_k_scales = [class_idx_reshuffle[i] for i in indices]
        top_k_scales = [_delete_comma(scale) for scale in top_k_scales]

        sharps_on_tonics = [scale_name.count('#1') for scale_name in top_k_scales]
        flats_on_tonics = [scale_name.count('b1') for scale_name in top_k_scales]
        tonic_names = [copy(self[0]).add_accidental(-sharps_on_tonic).add_accidental(flats_on_tonic).get_name(show_register=False)
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
        if name in ALTERED_SCALE_TYPE_NEW_TO_OLD.keys():
            return ALTERED_SCALE_TYPE_NEW_TO_OLD[name]
        else:
            return []


''' ----------------------------------------------------------------------------------------- '''
''' ******************** fancy music theory classes (special [12, 7, 5]) ******************** '''
''' ----------------------------------------------------------------------------------------- '''


# TODO: rewrite `Chord` class
class Chord(object):
    def __init__(self, chord_name='C'):
        self._bass = []
        self._body = []
        self._tensions = []

        par = chord_name_parser(chord_name)

        # bass note
        if par['bass_name']:
            self._bass = [Note(par['bass_name']) - Interval('P8')]
            self._bass[0].set_message(br357t='B')

        # r357 notes
        root = Note(par['root_name'])
        scale = AlteredDiatonicScale(par['root_name'] + ' ' + CHORD_TYPE_TO_SCALE_TYPE[par['chord_type']])
        steps = CHORD_TYPE_TO_STEPS[par['chord_type']]
        self._body.extend([scale[step] for step in steps])
        for note in self._body:
            itv = note - self._body[0]
            note.set_message(br357t=itv.get_r357t())

        # tension notes
        if par['tension_type']:
            tension_names = tension_type_parser(par['tension_type'])
            tension_intervals = [TENSION_NAME_TO_INTERVAL_NAME[tension_name] for tension_name in tension_names]
            tensions = [root + Interval(interval) for interval in tension_intervals]
            self._tensions.extend(tensions)
            _ = [tension.set_message(br357t=f'{tension_names[k]}') for k, tension in enumerate(self._tensions)]

    def __repr__(self):
        note_names = [note.get_name() for note in self.get_notes() if note is not None]
        return '[' + ''.join([name+', ' for name in note_names[:-1]]) + note_names[-1] + ']'

    def __getitem__(self, item):
        return self.get_notes()[item]

    def __abs__(self):
        return [abs(note) for note in self.get_notes()]

    def set_notes(self, bass=None, body=None, tensions=None):
        if bass:
            self._bass = [bass.set_message(br357t='B')]
        if body:
            self._body = body
            messages = ['R', '3', '5', '7']
            for i, note in enumerate(self._body):
                note.set_message(br357t=messages[i])
        if tensions:
            self._tensions = tensions
            for note in self._tensions:
                note.set_message(br357t=INTERVAL_NAME_TO_TENSION_NAME[str(note - self._body[0])])

        return self

    def get_notes(self, bass_on=True):
        if bass_on:
            return self._bass + self._body + self._tensions
        else:
            return self._body + self._tensions

    def get_name(self, type_only=False):
        # get bass type
        if self._bass:
            bass_type = '/' + self._bass[0].get_name(show_register=False)
        else:
            bass_type = ''

        # get body type
        intervals = [note2-note1 for note1, note2 in zip(self._body[:-1], self._body[1:])]
        interval_vector = ''.join([str(interval.get_vector()[0]) for interval in intervals])
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
            return f'{self._body[0].get_name(show_register=False)}{chord_type}'

    def get_scale(self, top_k=1, return_class_idx=False):
        """ get least-order scale of current chord """
        def _dist(l1, l2):
            return sum([abs(i-j) for i, j in zip(l1, l2)])

        def _lshift(lst, k):
            return lst[k:] + lst[:k]

        def _is_equal(list_1, list_2):
            if len(list_1) != len(list_2): return False
            if _dist(list_1, list_2) < 1e-5: return True
            else: return False

        chord_notes = self.get_notes(bass_on=False)
        root_name = chord_notes[0].get_name(show_register=False)
        itv_list = [(n2-n1).get_vector()[0] for n1, n2 in zip(chord_notes[:-1], chord_notes[1:])]

        # find all root positions in 66 classes of current chord
        all_steps = [[(k*2)%7 for k in range(7) if _is_equal(_lshift(interval_vector, k)[:len(itv_list)], itv_list)] for interval_vector in CHORD_INTERVAL_VECTOR_LIST]

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
        """ get in-chord degree of a note """
        scales = self.get_scale(66)
        icds = []
        for scale in scales:
            scale_nvs = [note.get_vector(return_register=False) for note in scale]  # nvs = note vectors
            note = Note(note_name)
            note_nv = note.get_vector(return_register=False)
            if note_nv not in scale_nvs:
                icds.append((scale.get_name()[0], -1))
            else:
                icds.append((scale.get_name()[0], scale_nvs.index(note_nv) + 1))
        return icds[[x[1]!=-1 for x in icds].index(True)]


# TODO: combine `ChordEx` class into `Chord` class
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
            bass_type = '/' + self._bass[0].get_name(show_register=False)
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
        chord_type = body_type + tension_type + bass_type
        if type_only:
            return chord_type
        else:
            return f'{self._notes[0].get_name(show_register=False)}{chord_type}'

    def get_scale(self, top_k=1, return_class_idx=False):
        """ get least-order scale of current chord """
        def _dist(l1, l2):
            return sum([abs(i-j) for i, j in zip(l1, l2)])

        def _lshift(lst, k):
            return lst[k:] + lst[:k]

        def _is_equal(list_1, list_2):
            if len(list_1) != len(list_2): return False
            if _dist(list_1, list_2) < 1e-5: return True
            else: return False

        chord_notes = self.get_notes(bass_on=False)
        root_name = chord_notes[0].get_name(show_register=False)
        itv_list = [(n2-n1).get_vector()[0] for n1, n2 in zip(chord_notes[:-1], chord_notes[1:])]

        # find all root positions in 66 classes of current chord
        all_steps = [[(k*2)%7 for k in range(7) if _is_equal(_lshift(interval_vector, k)[:len(itv_list)], itv_list)] for interval_vector in CHORD_INTERVAL_VECTOR_LIST]

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
        """ get in-chord degree of a note """
        scales = self.get_scale(66)
        icds = []
        for scale in scales:
            scale_nvs = [note.get_vector(return_register=False) for note in scale]  # nvs = note vectors
            note = Note(note_name)
            note_nv = note.get_vector(return_register=False)
            if note_nv not in scale_nvs:
                icds.append((scale.get_name()[0], -1))
            else:
                icds.append((scale.get_name()[0], scale_nvs.index(note_nv) + 1))
        return icds[[x[1]!=-1 for x in icds].index(True)]


# TODO: write avoid type back to note
class ChordScale(AlteredDiatonicScale):
    def __init__(self, scale_name):
        super().__init__(scale_name)
        self._chord_notes = [0, 2, 4, 6]
        self._tension_notes = [k for k in range(7) if k not in self._chord_notes]

    def get_info(self):
        itvs = [n - self[0] for n in self]
        itvs_abs = [i.get_vector()[0] for i in itvs]
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
                        idx_maj7 = degs.index('7')
                        if itvs_abs[idx_maj7] - itvs_abs[idx] == 1:
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
                        idx_maj7 = degs.index('7')
                        if itvs_abs[idx_maj7] - itvs_abs[idx] == 1:
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
                        idx_maj7 = degs.index('7')
                        if itvs_abs[idx_maj7] - itvs_abs[idx] == 1:
                            labels[idx] = '[A1]'

        if not (all([na in itvs_abs_mod for na in [4, 10]]) or all([na in itvs_abs_mod for na in [3, 10]])):
            # avoid_type_1: half tone above 7th chord note
            for idx in range(1, len(itvs_abs)):
                if any([itvs_abs[idx] - itvs_abs[j] == 1 for j in self._chord_notes]):
                    labels[idx] = '[A1]'
                # avoid_type_1: half tone below M7
                if '7' in degs:
                    idx_maj7 = degs.index('7')
                    if itvs_abs[idx_maj7] - itvs_abs[idx] == 1:
                        labels[idx] = '[A1]'

        long_list = ['x'] * 12
        for i, n in enumerate(itvs_abs_mod):
            long_list[n] = labels[i] + ' ' + degs[i]

        return labels, long_list, fake_dom7, fake_m7

    def get_color(self):
        color = '#'
        for i in self._chord_notes + self._tension_notes:
            if i == 0: continue

            itv = self[i] - self[0]
            color = color + f'{hex(itv.get_vector()[0])}'[2:]

        return color


''' ----------------------------------------------------------------------------------------- '''
''' ******************************** other exciting functions ******************************* '''
''' ----------------------------------------------------------------------------------------- '''


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
