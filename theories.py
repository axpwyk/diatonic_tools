import re
from copy import copy
import numpy as np
from consts import *
from itertools import product


''' ----------------------------------------------------------------------------------------- '''
''' ********************************** all kinds of parsers ********************************* '''
''' ----------------------------------------------------------------------------------------- '''


# for `Note`
def note_name_parser(note_name):
    # `note_name` is a string, examples: 'C#3', 'Bb1', 'Fbb3', etc.
    pattern_1 = r'(?P<named_str>[' + NAMED_STR_LIN + r'])'
    pattern_2 = r'(?P<accidental_str>[b#]*)(?P<register_str>-?\d*)'

    pattern = pattern_1 + pattern_2

    search_obj = re.search(pattern, note_name)
    return search_obj.groupdict()


# for `Interval`
def interval_name_parser(interval_name):
    # `interval_name` is a string, examples: 'm2', 'M3', 'P4', etc.
    search_obj = re.search(r'(?P<negative_str>-{0,1})(?P<interval_type>[dmPMA]+)(?P<degree_str>[\d]+)', interval_name)
    return search_obj.groupdict()


# for `DiatonicScale`
def scale_name_parser(scale_name):
    # `scale_name` is a string, examples: 'C C-mode', 'D C-mode(b6)', 'E Phrygian(#3, #7)', etc.

    # basic patterns
    pattern_1 = r'(?P<scale_tonic_name>[' + NAMED_STR_LIN + r'][#b]*-{0,1}\d*) '
    pattern_2 = r'(?P<scale_type>[\w#b+-]*)'
    pattern_3 = r'(?P<altered_note>(\([^ac-z]*\)){0,1})'

    # first we should make sure that `scale_name` is written in new naming scheme
    scale_type = re.sub(pattern_1, '', scale_name)

    if scale_type in SCALE_TYPE_NS1_TO_NS0.keys():
        scale_type = SCALE_TYPE_NS1_TO_NS0[scale_type]
    elif scale_type in ALTERED_SCALE_TYPE_NS2_TO_NS0.keys():
        scale_type = ALTERED_SCALE_TYPE_NS2_TO_NS0[scale_type]
    else:
        pass

    scale_name = re.match(pattern_1, scale_name).group() + scale_type

    # parse `scale_name`
    pattern = pattern_1 + pattern_2 + pattern_3
    search_obj = re.search(pattern, scale_name)

    return search_obj.groupdict()


def scale_type_parser(scale_type):
    # `scale_type` is a string, examples: 'D-mode', 'E-mode', 'α-mode', etc.
    pattern = '(?P<mode_tonic_name>[' + NAMED_STR_LIN + r'][#b]*-{0,1}\d*)(?=(-mode))'
    search_obj = re.search(pattern, scale_type)
    return search_obj.groupdict()


# for `AlteredDiatonicScale`
def altered_note_parser(altered_note):
    # `altered note` is a string, examples: '(b3)', '(b3, b7)', '(#5)', etc.
    return re.findall(r'[#b]+\d+', altered_note)


# for `Chord`
def chord_name_parser(chord_name):
    # `chord_name` is a string, examples: 'CM7', 'Dm7(9, 11, 13)', 'Bm7-5/F', etc.

    # basic patterns
    pattern_1 = r'(?P<root_name>[' + NAMED_STR_LIN + r'][#b]*-{0,1}\d*) ?'
    pattern_2 = r'(?P<chord_type>[\w.#b+-]*)'
    pattern_3 = r'(?P<tension_type>(\([^ac-z]*\)){0,1})'
    pattern_4 = '/?(?P<bass_name>([' + NAMED_STR_LIN + r'][#b]*-{0,1}\d*){0,1})'

    # parse `scale_name`
    pattern = pattern_1 + pattern_2 + pattern_3 + pattern_4
    search_obj = re.search(pattern, chord_name)

    results = search_obj.groupdict()

    # make sure that `chord_type` is written in new naming scheme
    if NGSChecker():
        if results['chord_type'] in CHORD_TYPE_NS1_TO_NS0[NGS].keys():
            results['chord_type'] = CHORD_TYPE_NS1_TO_NS0[NGS][results['chord_type']]

    return results


def tension_type_parser(tension_type):
    # `tension_type` is a string, examples: '(9)', '(b9, #11)', '(9, 11, 13)', '(9, 13)', etc.
    return re.findall(r'[#b]*\d+', tension_type)


''' ----------------------------------------------------------------------------------------- '''
''' ************************** fancy music theory classes (general) ************************* '''
''' ----------------------------------------------------------------------------------------- '''


class Note(object):
    @staticmethod
    def note_name_to_note_vector(note_name):
        par = note_name_parser(note_name)

        named_str = par['named_str']
        accidental_str = par['accidental_str']
        register_str = par['register_str']

        # get named nnrel, integer in `NAMED_NNREL_LIN`
        named_nnrel = STR_TO_NNREL[named_str]

        # get number of accidentals, integer in (-\infty, \infty)
        accidental = 0 + accidental_str.count('#') - accidental_str.count('b')

        # get register number, integer in (-\infty, \infty)
        if register_str:
            register = int(register_str)
        else:
            register = 0

        return named_nnrel, accidental, register

    def __init__(self, note_name=f'{NAMED_STR_LIN[0]}0'):
        # get note vector
        self._named_nnrel, self._accidental, self._register = self.note_name_to_note_vector(note_name)

        # additional message dict
        self._message = dict()

    def __str__(self):
        return self.get_name()

    def __repr__(self):
        return f"Note('{self.get_name()}')"

    def __sub__(self, other):
        # `Note` - `Note` = `Interval`
        if isinstance(other, Note):
            step1 = NAMED_NNREL_LIN.index(self._named_nnrel) + self._register * M
            step2 = NAMED_NNREL_LIN.index(other._named_nnrel) + other._register * M
            return Interval().set_vector(int(self) - int(other), step1 - step2)
        # `Note` - `Interval` = `Note`
        if isinstance(other, Interval):
            return self + (-other)
        else:
            raise TypeError('`Note` can only subtract a `Note` or an `Interval`!')

    def __add__(self, other):
        # `Note` + `Interval` = `Note`
        if isinstance(other, Interval):
            delta_nnabs, delta_step = other.get_vector()
            new_step = NAMED_NNREL_LIN.index(self._named_nnrel) + delta_step
            new_named_nnrel = NAMED_NNREL_LIN[new_step % M]
            new_register = self._register + new_step // M
            new_accidental = int(self) + delta_nnabs - new_named_nnrel - N * new_register
            return Note().set_vector(new_named_nnrel, new_accidental, new_register).set_message_dict(**self.get_message_dict())
        else:
            raise TypeError('`Note` can only add an `Interval`!')

    def __int__(self):
        """
        return absolute note number
        (in [12, 7, 5] diatonic scale) 'Bb2' = (11, -1, 2) = 11 + (-1) + 2 * 12 = 34

        :return: absolute note number, integer in (-\infty, \infty)
        """
        return self._named_nnrel + self._accidental + self._register * N

    def __lt__(self, other):
        if isinstance(other, Note):
            return int(self) < int(other)
        elif isinstance(other, int) or isinstance(other, float):
            return int(self) < other
        elif isinstance(other, str):
            return int(self) < int(Note(other))
        else:
            raise TypeError('`Note` can only compare with `Note`, `int`, `float` or `str`!')

    def __le__(self, other):
        if isinstance(other, Note):
            return int(self) <= int(other)
        elif isinstance(other, int) or isinstance(other, float):
            return int(self) <= other
        elif isinstance(other, str):
            return int(self) <= int(Note(other))
        else:
            raise TypeError('`Note` can only compare with `Note`, `int`, `float` or `str`!')

    def __eq__(self, other):
        if isinstance(other, Note):
            return all(
                [
                    self._named_nnrel == other._named_nnrel,
                    self._accidental == other._accidental,
                    self._register == other._register
                ]
            )
        elif isinstance(other, int) or isinstance(other, float):
            return int(self) == other
        elif isinstance(other, str):
            tmp = Note(other)
            return all(
                [
                    self._named_nnrel == tmp._named_nnrel,
                    self._accidental == tmp._accidental,
                    self._register == tmp._register
                ]
            )
        else:
            raise TypeError('`Note` can only compare with `Note`, `int`, `float` or `str`!')

    def __ne__(self, other):
        if isinstance(other, Note):
            return any(
                [
                    self._named_nnrel != other._named_nnrel,
                    self._accidental != other._accidental,
                    self._register != other._register
                ]
            )
        elif isinstance(other, int) or isinstance(other, float):
            return int(self) != other
        elif isinstance(other, str):
            tmp = Note(other)
            return any(
                [
                    self._named_nnrel != tmp._named_nnrel,
                    self._accidental != tmp._accidental,
                    self._register != tmp._register
                ]
            )
        else:
            raise TypeError('`Note` can only compare with `Note`, `int`, `float` or `str`!')

    def __gt__(self, other):
        if isinstance(other, Note):
            return int(self) > int(other)
        elif isinstance(other, int) or isinstance(other, float):
            return int(self) > other
        elif isinstance(other, str):
            return int(self) > int(Note(other))
        else:
            raise TypeError('`Note` can only compare with `Note`, `int`, `float` or `str`!')

    def __ge__(self, other):
        if isinstance(other, Note):
            return int(self) >= int(other)
        elif isinstance(other, int) or isinstance(other, float):
            return int(self) >= other
        elif isinstance(other, str):
            return int(self) >= int(Note(other))
        else:
            raise TypeError('`Note` can only compare with `Note`, `int`, `float` or `str`!')

    def set_vector(self, named_nnrel=None, accidental=None, register=None):
        # set note vector (named_nnrel, accidental, register) manually
        if named_nnrel is not None:
            if named_nnrel not in NAMED_NNREL_LIN:
                raise ValueError('Given `named_nnrel` does not correspond to a named note. Please choose another one!')
            else:
                self._named_nnrel = named_nnrel
        if accidental is not None:
            self._accidental = accidental
        if register is not None:
            self._register = register
        return self

    def get_vector(self, return_register=True):
        if return_register:
            return self._named_nnrel, self._accidental, self._register
        else:
            return self._named_nnrel, self._accidental

    def get_nnabs(self):
        return int(self)

    def get_named_nnrel(self):
        return self._named_nnrel

    def get_nnrel(self):
        return self._named_nnrel + self._accidental

    def get_accidental(self):
        return self._accidental

    def get_register(self):
        return self._register

    def get_name(self, show_register=True):
        # get name of `Note`, e.g. Note('C0').get_name() = 'C0', Note('C0').get_name(show_register=False) = 'C', etc.
        if show_register:
            return NNREL_TO_STR[self._named_nnrel] + (self._accidental * '#' if self._accidental > 0 else -self._accidental * 'b') + f'{self._register}'
        else:
            return NNREL_TO_STR[self._named_nnrel] + (self._accidental * '#' if self._accidental > 0 else -self._accidental * 'b')

    def from_name(self, note_name):
        self._named_nnrel, self._accidental, self._register = self.note_name_to_note_vector(note_name)
        return self

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
        nnabs = int(self)

        if direction == 'up':
            offset = 1
        elif direction == 'down':
            offset = -1
        elif direction == 'auto':
            offset = sign(self._accidental)
        else:
            raise ValueError(r"Illegal `direction`! Please choose one from 'up', 'down' or 'auto'!")

        step = NAMED_NNREL_LIN.index(self._named_nnrel)
        new_step = step + offset

        new_named_nnrel = NAMED_NNREL_LIN[new_step % M]
        new_register = self._register + new_step // M
        new_accidental = nnabs - new_named_nnrel - new_register * N

        return Note().set_vector(new_named_nnrel, new_accidental, new_register)


class Interval(object):
    @staticmethod
    def interval_name_to_interval_vector(interval_name, ns=0):
        """
        when [N, G, S] == [12, 7, 5], will choose naming scheme according to `DELTA_STEP_TO_NS`
        when [N, G, S] != [12, 7, 5], will use naming scheme 2

        :param interval_name: interval name, e.g. 'P1', 'M2', etc.
        :param ns: interval naming scheme, 0 = auto, 1 = dPA, 2 = dmMA
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
        if ns == 0:
            if NGSChecker():
                ns = DELTA_STEP_TO_NS[NGS][delta_step % M]
            else:
                ns = 2
        else:
            pass

        # calculate `delta_group`
        if ns == 1:
            delta_group = interval_type.count('A') - interval_type.count('d')
        elif ns == 2:
            if 'd' in interval_type:
                delta_group = interval_type.count('A') - interval_type.count('m') - interval_type.count('d') - 1
            else:
                delta_group = interval_type.count('A') - interval_type.count('m')
        else:
            raise ValueError('No such naming scheme! Choose `ns` from [1, 2]!')

        # calculate `delta_nnabs`
        delta_step_rel = delta_step % M
        delta_register = delta_step // M

        named_nnrel = NAMED_NNREL_LIN[delta_step_rel]
        delta_nnabs = delta_group + named_nnrel + N * delta_register

        # get interval vector
        return sgn * delta_nnabs, sgn * delta_step

    @staticmethod
    def interval_vector_to_interval_name(delta_nnabs, delta_step, ns=0):
        """
        it only exists 2 types of intervals that contain same number of named notes in diatonic scale

        we call the larger interval P (Perfect), and the smaller interval d (diminished):
        ... < ddd < dd < d < P < A < AA < AAA < ... (naming scheme 1, `ns`=1)

        we can also call the larger interval M (major), and the smaller interval m (minor):
        ... < dd < d < m < M < A < AA < AAA < ... (naming scheme 2, `ns`=2)

        * notice: '-M2' and 'M-2' are different, we will use the former one when `delta_step` < 0

        :return: interval name (type: str)
        """
        sgn = sign(delta_step)

        if sgn < 0:
            delta_nnabs, delta_step = -delta_nnabs, -delta_step

        delta_step_rel = delta_step % M
        delta_register = delta_step // M

        named_nnrel = NAMED_NNREL_LIN[delta_step_rel]
        delta_group = delta_nnabs - N * delta_register - named_nnrel

        # get naming scheme
        if ns == 0:
            if NGSChecker():
                ns = DELTA_STEP_TO_NS[NGS][delta_step % M]
            else:
                ns = 2
        else:
            pass

        if ns == 1:
            if delta_group > 0:
                itv_type = 'A' * delta_group
            elif delta_group == 0:
                itv_type = 'P'
            else:
                itv_type = 'd' * abs(delta_group)
        elif ns == 2:
            if delta_group > 0:
                itv_type = 'A' * delta_group
            elif delta_group == 0:
                itv_type = 'M'
            elif delta_group == -1:
                itv_type = 'm'
            else:
                itv_type = 'd' * (abs(delta_group) - 1)
        else:
            raise ValueError('No such naming scheme! Choose `ns` from [1, 2]!')

        return -sgn * '-' + itv_type + f'{delta_step + 1}'

    def __init__(self, interval_name='P1'):
        self._delta_nnabs, self._delta_step = self.interval_name_to_interval_vector(interval_name)

    def __str__(self):
        return self.get_name()

    def __repr__(self):
        return f"Interval('{self.get_name()}')"

    def __add__(self, other):
        # `Interval` + `Note` = `Note`
        if isinstance(other, Note):
            return other + self
        # `Interval` + `Interval` = `Interval`
        elif isinstance(other, Interval):
            return Interval().set_vector(self._delta_nnabs + other._delta_nnabs, self._delta_step + other._delta_step)
        else:
            raise TypeError('`Interval` can only add a `Note` or an `Interval`!')

    def __sub__(self, other):
        # `Interval` - `Interval` = `Interval`
        if isinstance(other, Interval):
            return Interval().set_vector(self._delta_nnabs - other._delta_nnabs, self._delta_step - other._delta_step)
        else:
            raise TypeError('`Interval` can only subtract an `Interval`!')

    def __mul__(self, other):
        if isinstance(other, int):
            return Interval().set_vector(self._delta_nnabs*other, self._delta_step*other)
        else:
            raise TypeError('`Interval` can only multiply an integer!')

    def __rmul__(self, other):
        if isinstance(other, int):
            return Interval().set_vector(other*self._delta_nnabs, other*self._delta_step)
        else:
            raise TypeError('`Interval` can only multiply an integer!')

    def __neg__(self):
        return Interval().set_vector(-self._delta_nnabs, -self._delta_step)

    def __abs__(self):
        sgn = sign(self._delta_step)
        return Interval().set_vector(sgn * self._delta_nnabs, sgn * self._delta_step)

    def __int__(self):
        return self._delta_nnabs

    def __lt__(self, other):
        if isinstance(other, Interval):
            return self._delta_nnabs < other._delta_nnabs
        elif isinstance(other, int) or isinstance(other, float):
            return self._delta_nnabs < other
        elif isinstance(other, str):
            return self._delta_nnabs < int(Interval(other))
        else:
            raise TypeError('`Interval` can only compare with `Interval`, `int`, `float` or `str`!')

    def __le__(self, other):
        if isinstance(other, Interval):
            return self._delta_nnabs <= other._delta_nnabs
        elif isinstance(other, int) or isinstance(other, float):
            return self._delta_nnabs <= other
        elif isinstance(other, str):
            return self._delta_nnabs <= int(Interval(other))
        else:
            raise TypeError('`Interval` can only compare with `Interval`, `int`, `float` or `str`!')

    def __eq__(self, other):
        if isinstance(other, Interval):
            return all([self._delta_nnabs == other._delta_nnabs, self._delta_step == other._delta_step])
        elif isinstance(other, int) or isinstance(other, float):
            return self._delta_nnabs == other
        elif isinstance(other, str):
            tmp_delta_nnabs, tmp_delta_step = Interval(other).get_vector()
            return all([self._delta_nnabs == tmp_delta_nnabs, self._delta_step == tmp_delta_step])
        else:
            raise TypeError('`Interval` can only compare with `Interval`, `int`, `float` or `str`!')

    def __ne__(self, other):
        if isinstance(other, Interval):
            return all([self._delta_nnabs != other._delta_nnabs, self._delta_step != other._delta_step])
        elif isinstance(other, int) or isinstance(other, float):
            return self._delta_nnabs != other
        elif isinstance(other, str):
            tmp_delta_nnabs, tmp_delta_step = Interval(other).get_vector()
            return any([self._delta_nnabs != tmp_delta_nnabs, self._delta_step != tmp_delta_step])
        else:
            raise TypeError('`Interval` can only compare with `Interval`, `int`, `float` or `str`!')

    def __gt__(self, other):
        if isinstance(other, Interval):
            return self._delta_nnabs > other._delta_nnabs
        elif isinstance(other, int) or isinstance(other, float):
            return self._delta_nnabs > other
        elif isinstance(other, str):
            return self._delta_nnabs > int(Interval(other))
        else:
            raise TypeError('`Interval` can only compare with `Interval`, `int`, `float` or `str`!')

    def __ge__(self, other):
        if isinstance(other, Interval):
            return self._delta_nnabs >= other._delta_nnabs
        elif isinstance(other, int) or isinstance(other, float):
            return self._delta_nnabs >= other
        elif isinstance(other, str):
            return self._delta_nnabs >= int(Interval(other))
        else:
            raise TypeError('`Interval` can only compare with `Interval`, `int`, `float` or `str`!')

    def set_vector(self, delta_nnabs=None, delta_step=None):
        # set interval vector (delta_nnabs, delta_step) manually
        if delta_nnabs is not None:
            self._delta_nnabs = delta_nnabs
        if delta_step is not None:
            self._delta_step = delta_step
        return self

    def get_vector(self):
        return self._delta_nnabs, self._delta_step

    def get_delta_nnabs(self):
        return int(self)

    def get_delta_step(self):
        return self._delta_step

    def get_name(self):
        return self.interval_vector_to_interval_name(self._delta_nnabs, self._delta_step)

    def from_name(self, interval_name):
        self._delta_nnabs, self._delta_step = self.interval_name_to_interval_vector(interval_name)
        return self

    def get_r357t(self):
        # (when `NGS` == '12.7.5') P2 -> 2, d2 -> b2, A2 -> #2, etc.
        r357t = self.interval_vector_to_interval_name(self._delta_nnabs, self._delta_step, ns=1)
        r357t = r357t.replace('P', '').replace('d', 'b').replace('A', '#')
        r357t = 'R' if r357t == '1' else r357t

        return r357t

    def from_r357t(self, r357t):
        # this is similar to interval naming scheme 1, 'P' -> '', 'd' -> 'b', 'A' -> '#'
        if r357t in ['', 'R']:
            self._delta_nnabs, self._delta_step = 0, 0
            return self
        else:
            interval_name = 'P' + r357t.replace('b', 'd').replace('#', 'A')
            self._delta_nnabs, self._delta_step = self.interval_name_to_interval_vector(interval_name, ns=1)

        return self

    def normalize(self):
        delta_group = self._delta_step // M
        self._delta_step = self._delta_step % M
        self._delta_nnabs = self._delta_nnabs - N * delta_group
        return self


class DiatonicScale(object):
    def __init__(self, scale_name=f'{NAMED_STR_LIN[0]} {NAMED_STR_LIN[0]}-mode'):
        """
        Create a note list, which has diatonic property in `N`-TET system
        `self._meta_notes` are the notes in sequence of generative order
        `scale_name` should be ST MT-mode: ST = scale tonic, MT = mode tonic
        """

        # parse `scale_name`, get `scale_tonic_name` and `scale_type`
        par1 = scale_name_parser(scale_name)
        scale_tonic_name = par1['scale_tonic_name']
        scale_type = par1['scale_type']

        # parse `scale_tonic_name`
        st_named_nnrel, st_accidental, st_register = Note.note_name_to_note_vector(scale_tonic_name)

        # parse `scale_type`, and get `mode_tonic_name`
        mode_tonic_name = scale_type_parser(scale_type)['mode_tonic_name']

        # parse `mode_tonic_name`
        mt_named_nnrel, mt_accidental, mt_register = Note.note_name_to_note_vector(mode_tonic_name)

        # [!] get scale tonic index in `NAMED_GEN_NNREL` and number of accidentals
        st_step_gen = NAMED_NNREL_GEN.index(st_named_nnrel)
        mt_step_gen = NAMED_NNREL_GEN.index(mt_named_nnrel)
        accidentals = st_step_gen - mt_step_gen + M * (st_accidental + mt_accidental)
        self._st_step_gen = st_step_gen
        self._accidentals = accidentals

        # get meta notes (generative order)
        self._meta_notes = [Note(f'{s}{st_register}') for s in NAMED_STR_GEN]

        # put accidental(s) on meta notes
        for k in range(0, accidentals) if accidentals > 0 else range(accidentals, 0):
            if accidentals > 0:
                self._meta_notes[k % M].add_accidental(1)
            else:
                self._meta_notes[k % M].add_accidental(-1)

        self._refresh_register()
        self._refresh_messages()

        # print options initialization
        self._printoptions = dict(ns=0, show_register=False)

    def __getitem__(self, item):
        """
        a linear view of `self._meta_notes` (remember that `self._meta_notes` is of generative order)
        changes will affect `self._meta_notes`
        """
        return [self._meta_notes[(self._st_step_gen + M2_STEP_GEN * k) % M] for k in range(M)][item]

    def __str__(self):
        note_names = [note.get_name(self._printoptions['show_register']) for note in self]
        return '[' + ', '.join(note_names) + ']'

    def __repr__(self):
        return f"DiatonicScale('{self.get_name()}')"

    def _refresh_register(self, st_register=None):
        if st_register is None:
            st_register = self[0].get_register()
        else:
            self[0].set_vector(register=st_register)

        for note in self[1:]:
            if note.get_nnrel() < self[0].get_nnrel():
                note.set_vector(register=st_register + 1)
            else:
                note.set_vector(register=st_register)

    def _refresh_messages(self):
        # add degree message for every note
        for k, note in enumerate(self):
            note.set_message(degree=k)

    def get_nnabs_list(self):
        """
        return a list of absolute note numbers `nnabs` of current scale in linear order
        e.g. (in [12, 7, 5] diatonic scale) [C0, D0, E0, F0, G0, A0, B0] = [0, 2, 4, 5, 7, 9, 11]
        """
        return [int(note) for note in self]

    def get_named_nnrel_list(self):
        return [note.get_named_nnrel() for note in self]

    def get_nnrel_list(self):
        return [(note.get_named_nnrel() + note.get_accidental()) % N for note in self]

    def get_accidental_list(self):
        return [note.get_accidental() for note in self]

    def get_register_list(self):
        return [note.get_register() for note in self]

    def set_printoptions(self, ns=None, show_register=None):
        if ns is not None:
            if ns == 0:
                self._printoptions['ns'] = 0
            elif ns in [1, 2]:
                if NGSChecker():
                    self._printoptions['ns'] = ns
                else:
                    print(f'Naming scheme {ns} works properly only when NGS in {SPECIAL_NGS}!')
            else:
                raise ValueError(f'No naming scheme {ns}! Please choose from [0, 1, 2]!')

        if show_register is not None:
            self._printoptions['show_register'] = show_register

        return self

    def set_scale_tonic_str(self, scale_tonic_name):
        # the default scale tonic note is in inputting `scale_name`, e.g. `C# Ionian` -> 'C#'
        st_named_nnrel, _, st_register = Note.note_name_to_note_vector(scale_tonic_name)
        self._st_step_gen = NAMED_NNREL_GEN.index(st_named_nnrel)

        self._refresh_register(st_register)
        self._refresh_messages()

        return self

    def set_scale_tonic_deg(self, degree=0, st_register=0):
        # set `degree` note of current diatonic scale as new scale tonic note
        st_new_named_nnrel = self[degree % M].get_named_nnrel()

        self._st_step_gen = NAMED_NNREL_GEN.index(st_new_named_nnrel)

        self._refresh_register(st_register)
        self._refresh_messages()

        return self

    def get_name(self, type_only=False):
        # calculate current scale name using `self[0]` and `self._accidentals`
        if self._printoptions['show_register']:
            scale_tonic_name = self[0].get_name()
        else:
            scale_tonic_name = self[0].get_name(show_register=False)

        st_named_nnrel, st_accidental, st_register = Note.note_name_to_note_vector(scale_tonic_name)

        st_step_gen = NAMED_NNREL_GEN.index(st_named_nnrel)
        mt_step_gen = st_step_gen + M * st_accidental - self._accidentals

        scale_type = NAMED_STR_GEN[mt_step_gen] + '-mode'

        if self._printoptions['ns'] == 1:
            scale_type = SCALE_TYPE_NS0_TO_NS1[scale_type]

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

    def add_accidentals_for_all(self, n=0):
        for note in self._meta_notes:
            note.add_accidental(n)
        self._accidentals += M * n

        return self

    def add_register(self, n=0):
        for note in self._meta_notes:
            note.add_register(n)
        return self

    def get_chord(self, root_degree, n_notes, n_step_length=CHORD_STEP_LIN):
        """
        notice: this method will return copies of `self._meta_notes` elements
        """
        root_degree = root_degree % M

        notes = []
        for i in range(n_notes):
            idx = root_degree + n_step_length * i
            notes.append(copy(self[idx % M]) if idx < M else copy(self[idx % M]).add_register(idx // M))

        for note in notes:
            br357t = (note - notes[0]).get_r357t()
            note.set_message(br357t=br357t)

        return notes

    def get_chord_ex(self, degrees=(0, )):
        """
        notice: this method will return copies of `self._meta_notes` elements
        """
        notes = []
        for i, deg in enumerate(degrees):
            cur_note = copy(self[deg % M])
            if i == 0:
                notes.append(cur_note)
            else:
                if cur_note.get_nnrel() < notes[-1].get_nnrel():
                    cur_register = notes[-1].get_register() + 1
                else:
                    cur_register = notes[-1].get_register()

                notes.append(copy(cur_note).set_vector(register=cur_register))

        for note in notes:
            br357t = (note - notes[0]).get_r357t()
            note.set_message(br357t=br357t)

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

    def __repr__(self):
        return '\n'.join([f"AlteredDiatonicScale('{scale_name}')" for scale_name in self.get_name()])

    def distance(self, other, return_offsets=False):
        a = np.expand_dims(np.array(self.get_nnabs_list()), axis=-1)  # [M, 1]
        b = np.expand_dims(np.array(other.get_nnabs_list()), axis=-1)  # [M, 1]
        x = np.expand_dims(np.arange(N), axis=0)  # [1, N]

        ax = np.expand_dims(np.sort((a + x) % N, axis=0), axis=-1)  # [M, N, 1]
        bx = np.expand_dims(np.sort((b + x) % N, axis=0), axis=-2)  # [M, 1, N]

        ds = np.sum((N - np.abs(2 * np.abs(ax - bx) - N)) // 2, axis=0)  # [N, N]
        d = np.min(ds)

        if return_offsets:
            offsets = np.stack(np.where(ds == d), axis=-1)  # rotations of a and b (counterclockwise)
            return d, offsets
        else:
            return d

    def get_order(self):
        return self.distance(DiatonicScale())

    def get_name(self, type_only=False):
        """
        get all possible lowest-order names of current altered diatonic scale, e.g.

        scale_1 (`self`; ???)      -> [Cb, Db, Eb, F, G, Ab, Bb] (11, 1, 3, 5, 7, 8, 10)
        scale_2 (`ds`; C Ionian)   -> [C, D, E, F, G, A, B] (0, 2, 4, 5, 7, 9, 11)
        offset                     -> [2, 10]

        scale_1 + 2                -> [C#, D#, E#, F##, G##, A#, B#] (1, 3, 5, 7, 9, 10, 0)
        scale_2 + 10               -> [C(#*10), D(#*10), ..., B(#*10)] (10, 0, 2, 3, 5, 7, 9)
        a = (scale_1 + 2).min.idx  -> 6
        b = (scale_2 + 10).min.idx -> 1
        mode_tonic.idx             -> (0 - a) % M + b = 2
        mode_tonic                 -> [C, D, E, F, G, A, B][2] = E

        sorted(scale_1 + 2)        -> (0, 1, 3, 5, 7, 9, 10)
        sorted(scale_2 + 10)       -> (0, 2, 3, 5, 7, 9, 10)
        altered_notes              -> (0, -1, 0, 0, 0, 0, 0)
        mode_tonic_offset          -> b - mode_tonic.idx = -1
        scale_type                 -> E-mode(b1)

        scale_tonic                -> Cb, but (b1) in scale_type, so it's C
        scale_name                 -> C E-mode(b1)
        """

        ds = DiatonicScale()
        order, offsets = self.distance(ds, return_offsets=True)

        scale_names = []
        for offset in offsets:
            scale_1_nnrels_offset = [(nnrel + offset[0]) % N for nnrel in self.get_nnrel_list()]
            scale_2_nnrels_offset = [(nnrel + offset[1]) % N for nnrel in ds.get_nnrel_list()]

            # get mode tonic
            a = scale_1_nnrels_offset.index(min(scale_1_nnrels_offset))
            b = scale_2_nnrels_offset.index(min(scale_2_nnrels_offset))
            mode_tonic_idx = (0 - a + b) % M
            mode_tonic_name = NAMED_STR_LIN[mode_tonic_idx]

            # get altered notes
            scale_1_nnrels_offset.sort()
            scale_2_nnrels_offset.sort()
            mode_tonic_offset = (b - mode_tonic_idx) % M
            altered_notes = dict()
            for i, (nnrel_1, nnrel_2) in enumerate(zip(scale_1_nnrels_offset, scale_2_nnrels_offset)):
                if nnrel_1 - nnrel_2 != 0:
                    altered_notes[(i + mode_tonic_offset) % M + 1] = nnrel_pair_to_accidental(nnrel_2, nnrel_1)

            # filter out modes like 'Ionian(#4, b7)', because it's not in simplest form 'Lydian(b7)'
            if len(altered_notes) > order:
                continue

            # get scale type
            if 1 in altered_notes.keys():
                mode_tonic_name += '#' * -altered_notes[1] + 'b' * altered_notes[1]
            scale_type = f'{mode_tonic_name}-mode'

            # get altered notes
            if altered_notes.items():
                altered_notes = {k: altered_notes[k] for k in sorted(altered_notes)}
                altered_notes_str = []
                for i, (degree, accidental) in enumerate(altered_notes.items()):
                    altered_notes_str.append('#' * accidental + 'b' * -accidental + f'{degree}')
                altered_notes_str = '(' + ', '.join(altered_notes_str) + ')'
            else:
                altered_notes_str = ''

            if scale_type in SCALE_TYPE_NS0_TO_NS1.keys():
                scale_type_ns1 = SCALE_TYPE_NS0_TO_NS1[scale_type] + altered_notes_str
            else:
                scale_type_ns1 = scale_type + altered_notes_str

            if scale_type + altered_notes_str in ALTERED_SCALE_TYPE_NS0_TO_NS2.keys():
                scale_type_ns2 = ALTERED_SCALE_TYPE_NS0_TO_NS2[scale_type + altered_notes_str][0]
            else:
                if scale_type in SCALE_TYPE_NS0_TO_NS1.keys():
                    scale_type_ns2 = SCALE_TYPE_NS0_TO_NS1[scale_type] + altered_notes_str
                else:
                    scale_type_ns2 = scale_type + altered_notes_str

            if self._printoptions['ns'] == 1:
                scale_type_out = scale_type_ns1
            elif self._printoptions['ns'] == 2:
                scale_type_out = scale_type_ns2
            else:
                scale_type_out = scale_type + altered_notes_str

            # get scale tonic
            scale_tonic = copy(self[0])

            if self._printoptions['show_register']:
                scale_tonic_name = scale_tonic.get_name()
            else:
                scale_tonic_name = scale_tonic.get_name(show_register=False)

            # if `type_only`
            if type_only:
                scale_names.append(scale_type_out)
            else:
                scale_names.append(scale_tonic_name + ' ' + scale_type_out)

        return unique(scale_names)


class Chord(object):
    @staticmethod
    def chord_name_to_notes(chord_name):
        bass = []
        body = []
        tension = []

        par1 = chord_name_parser(chord_name)
        bass_name = par1['bass_name']
        root_name = par1['root_name']
        chord_type = par1['chord_type']
        tension_type = par1['tension_type']

        # bass note
        if bass_name:
            bass.append(Note(bass_name) - Interval().set_vector(N, M))
            bass[0].set_message(br357t='B')

        # r357 notes
        root = Note(root_name)
        intervals = [Interval().from_r357t(r357) for r357 in chord_type.split('.')]
        body.extend([root + interval for interval in intervals])
        for note, interval in zip(body, intervals):
            note.set_message(br357t=interval.get_r357t())

        # tension notes
        if tension_type:
            ts = tension_type_parser(tension_type)
            intervals = [Interval().from_r357t(t) for t in ts]
            tension.extend([root + interval for interval in intervals])
            for note, interval in zip(tension, intervals):
                note.set_message(br357t=interval.get_r357t())

        return bass, body, tension

    @staticmethod
    def notes_to_chord_type(bass, body, tension):
        # get bass type
        if bass:
            bass_type = '/' + bass[0].get_name(show_register=False)
        else:
            bass_type = ''

        # get body type
        intervals = [note - body[0] for note in body]
        r357s = [interval.get_r357t() for interval in intervals]
        body_type = '.'.join(r357s)

        # get tension type
        if tension:
            intervals = [note - body[0] for note in tension]
            ts = [interval.get_r357t() for interval in intervals]
            tension_type = '(' + ', '.join(ts) + ')'
        else:
            tension_type = ''

        return body_type, tension_type, bass_type

    def __init__(self, chord_name=f'{NAMED_STR_LIN[0]}0'):
        self._bass, self._body, self._tension = self.chord_name_to_notes(chord_name)

        # print options initialization
        self._printoptions = dict(ns=0, show_register=False)

    def __str__(self):
        bass_names = [note.get_name(self._printoptions['show_register']) for note in self._bass]
        body_names = [note.get_name(self._printoptions['show_register']) for note in self._body]
        tension_names = [note.get_name(self._printoptions['show_register']) for note in self._tension]

        str_1 = 'bass: [' + ', '.join(bass_names) + ']'
        str_2 = 'body: [' + ', '.join(body_names) + ']'
        str_3 = 'tension: [' + ', '.join(tension_names) + ']'

        return '\n'.join([str_1, str_2, str_3])

    def __repr__(self):
        return f"Chord('{self.get_name()}')"

    def __getitem__(self, item):
        return (self._bass + self._body + self._tension)[item]

    def __abs__(self):
        return [int(note) for note in self._bass + self._body + self._tension]

    def set_notes(self, bass=None, body=None, tension=None):
        if bass is not None:
            self._bass = [note.set_message(br357t='B') for note in bass if isinstance(note, Note)]

        if body is not None:
            self._body = [note for note in body if isinstance(note, Note)]
            for note in self._body:
                interval = note - self._body[0]
                note.set_message(br357t=interval.get_r357t())

        if tension is not None:
            self._tension = [note for note in tension if isinstance(note, Note)]
            for note in self._tension:
                interval = note - self._tension[0]
                note.set_message(br357t=interval.get_r357t())

        return self

    def get_notes(self, return_bass=True, tension_only=False):
        if tension_only:
            return self._tension

        if return_bass:
            return self._bass + self._body + self._tension
        else:
            return self._body + self._tension

    def set_printoptions(self, ns=None, show_register=None):
        if ns is not None:
            if ns == 0:
                self._printoptions['ns'] = 0
            elif ns in [1, ]:
                if NGSChecker():
                    self._printoptions['ns'] = ns
                else:
                    raise ValueError(f'Naming scheme {ns} works properly only when NGS in {SPECIAL_NGS}!')
            else:
                raise ValueError(f'No naming scheme {ns}! Please choose from [0, 1]!')

        if show_register is not None:
            self._printoptions['show_register'] = show_register

        return self

    def get_intervals_seq(self, use_bass=True):
        notes = self.get_notes(return_bass=use_bass)
        return [n2 - n1 for n1, n2 in zip(notes[:-1], notes[1:])]

    def get_intervals_cum(self, use_bass=True):
        return [note - self[0] for note in self.get_notes(return_bass=use_bass)]

    def get_name(self, type_only=False):
        body_type, tension_type, bass_type = self.notes_to_chord_type(self._bass, self._body, self._tension)

        if self._printoptions['ns'] == 1:
            if body_type in CHORD_TYPE_NS0_TO_NS1[NGS].keys():
                body_type = CHORD_TYPE_NS0_TO_NS1[NGS][body_type][0]

        chord_type = body_type + tension_type + bass_type

        if type_only:
            return chord_type
        else:
            if self._printoptions['ns'] == 1:
                whitespace = ''
            else:
                whitespace = ' '
            return f"{self._body[0].get_name(show_register=self._printoptions['show_register'])}{whitespace}{chord_type}"

    def get_scale(self, use_bass=True, max_order=2, ns=2):
        """
        get all possible background scale of current chord, e.g.

        EM9                  -> [E, G#, B, D#, F#]
        circular_sorted(EM9) -> [E, F#, G#, (A), B, (C), D#]
        unused_notes         -> [A, C]

        possible A note      -> [A, A#]
        possible C note      -> [C, C#, C##]

        possible background scales:

        [E, F#, G#, A, B, C, D#]
        [E, F#, G#, A, B, C#, D#]
        [E, F#, G#, A, B, C##, D#]
        [E, F#, G#, A#, B, C, D#]
        [E, F#, G#, A#, B, C#, D#]
        [E, F#, G#, A#, B, C##, D#]

        use `AlteredDiatonicScale` to get information about these scales
        """
        if use_bass:
            notes = self.get_notes(return_bass=True)
        else:
            notes = self.get_notes(return_bass=False)

        # when current chord is not well-formed, i.e. it contains same notes, raise an error
        if len(unique([note.get_nnrel() for note in notes])) < len(notes):
            raise ValueError( f'Current chord is not well-formed! Please make sure that notes are different from each other!')

        # get normalized notes, e.g. [E1, G#1, B1, D#2, F#2] -> [E0, F#0, G#0, B0, D#1]
        notes_sorted = circular_sorted(notes, 0, lambda x: x.get_nnrel())
        notes_normed = [copy(note).set_vector(register=0) for note in notes_sorted]
        for note in notes_normed:
            if note < notes_normed[0]:
                note.add_register(1)

        # get unused notes, e.g. [E0, F#0, G#0, (A0), B0, (C1), D#1] -> [A0, C1], and indices of their left note, e.g. A0 -> 2, C1 -> 4
        notes_named_nnrels = [note.get_named_nnrel() for note in notes_normed]
        notes_nnabs_closed = [int(note) for note in notes_normed] + [int(notes_normed[0]) + N]

        ds_name = f'{notes_normed[0].get_name(show_register=True)} {NAMED_STR_LIN[0]}-mode'
        all_notes = list(DiatonicScale(ds_name))

        unused_notes, indices, idx = [], [], -1
        for note in all_notes:
            if note.get_named_nnrel() in notes_named_nnrels:
                idx += 1
            else:
                unused_notes.append(note)
                indices.append(idx)

        # get accidental range of unused notes, e.g. A0: (0, 2); C1: (0, 3)
        accidental_ranges = []  # corresponds to `unused_names`
        for cur_note, idx in zip(unused_notes, indices):
            cur_nnabs = int(cur_note)
            accidental_ranges.append(range(notes_nnabs_closed[idx] - cur_nnabs + 1, notes_nnabs_closed[idx + 1] - cur_nnabs))

        # add accidentals to unused notes, put them into chord and get scale
        scale_names = []
        for accidentals in product(*accidental_ranges):
            cur_scale = notes_normed + [copy(note).add_accidental(accidental) for note, accidental in zip(unused_notes, accidentals)]
            cur_scale = circular_sorted(cur_scale, 0, key=lambda x: x.get_named_nnrel())

            cur_r357ts = [(note - cur_scale[0]).get_r357t() for note in cur_scale]
            altered_r357ts = [r357t for r357t in cur_r357ts]
            altered_notes = '(' + ', '.join(altered_r357ts) + ')'

            cur_scale_name = f'{str(notes_normed[0])} {NAMED_STR_LIN[0]}-mode{altered_notes}'

            cur_ads = AlteredDiatonicScale(cur_scale_name).set_printoptions(ns=ns)

            # filter out scales like [C, D, E, F, G, Ab, Bbbb] (Ab == Bbbb)
            if True in [itv <= 0 for itv in cur_ads.get_intervals_seq()]:
                continue

            # filter out order > `max_order` scales
            if cur_ads.get_order() > max_order:
                continue

            scale_names.extend(cur_ads.get_name())

        return unique(scale_names)


# TODO: write avoid type back to note
class ChordScale(AlteredDiatonicScale):
    def __init__(self, scale_name):
        super().__init__(scale_name)
        self._chord_notes = [0, 2, 4, 6]
        self._tension_notes = [k for k in range(7) if k not in self._chord_notes]

    def _get_avoid(self):
        pass

    def get_info(self):
        itvs = [n - self[0] for n in self]
        itvs_abs = [int(i) for i in itvs]
        itvs_abs_mod = [i % 12 for i in itvs_abs]
        degs = [i.get_r357t() for i in itvs]
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
            if i == 0:
                continue

            itv = self[i] - self[0]
            color = color + f'{hex(int(itv))}'[2:]

        return color


''' ----------------------------------------------------------------------------------------- '''
''' ******************************** other exciting functions ******************************* '''
''' ----------------------------------------------------------------------------------------- '''


def circular_permutation_with_repetition(n, ns):
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
