from ast import literal_eval


''' ----------------------------------------------------------------------------------------- '''
''' *********************************** for `theories.py` *********************************** '''
''' ----------------------------------------------------------------------------------------- '''
''' NN = note number, ABS = absolute, REL = relative, NNREL/NNABS = int type                  '''
''' STR = str type, LST = list type, LIN = linear, GEN = generative                           '''
'''                                                                                           '''
''' * we call [index of `NAMED_NNREL_LIN`] `step`                                             '''
''' * we call [index of `NAMED_NNREL_GEN`] `span`                                             '''
''' * we call [index of a scale] or [number of notes contained in an interval] `degree`       '''
'''                                                                                           '''
''' * WARNING: Changing `S` will lead to different interval naming scheme                     '''
'''            A4 in [N, G, S] = [12, 7, 5] is P4 (M4) in [N, G, S] = [12, 7, 0]              '''
''' ----------------------------------------------------------------------------------------- '''


# most basic constants (generate named nnrels from starting point `S` using step length `G` modulo `N`)
N = 12  # int(input('N: '))  # `N`-tone equal temperament (`N`-TET)
G = 7   # int(input('G: '))  # generator (step length)
S = 5   # int(input('S: '))  # starter (starting point)

# most basic calculations
M = pow(G, -1, N)                            # number of tones in diatonic scale
T = 2 ** (1 / N)                             # ratio of semi-tone frequencies
C3 = 440 * (T ** (36 - 45))                  # frequency of C3
NGS = '.'.join([str(k) for k in [N, G, S]])  # NGS for dict indexing

# define named notes (basic notes) in linear order
NAMED_STR_LIN = {
    '12.7.5': 'CDEFGAB',
    '19.11.8': 'CDEFGAB',
    '12.7.0': 'cdeFgab',  # F == f#
    '19.11.0': 'cdeFgab',  # F == f#
    '12.5.4': 'CDEGA',
    '53.31.22': 'cCdDefFgGaAb',  # C == c#, D == d#, F == f#, G == g#, A == a#
    '97.56.0': str().join([chr(ord('A')+j) for j in range(M)]),  # 26-tone diatonic scale
}.get(NGS, str().join([chr(int('03B1', 16)+j) for j in range(M)]))

# relative note numbers (nnrels) in generative order, e.g. [5, 0, 7, 2, 9, 4, 11]
NAMED_NNREL_GEN = [(S + i * G) % N for i in range(M)]

# NAMED_NNREL_GEN.index(0)
SPAN_OFFSET = (-S * M) % N

# relative note numbers (nnrels) in linear order, e.g. [0, 2, 4, 5, 7, 9, 11]
NAMED_NNREL_LIN = sorted(NAMED_NNREL_GEN)

# nnrel/str convertors
NNREL_TO_STR = {nnrel: NAMED_STR_LIN[i] for i, nnrel in enumerate(NAMED_NNREL_LIN)}
STR_TO_NNREL = dict((v, k) for k, v in NNREL_TO_STR.items())

# change `NAMED_STR_LIN` into generative order, e.g. 'CDEFGAB' -> 'FCGDAEB'
NAMED_STR_GEN = ''.join([NNREL_TO_STR[k] for k in NAMED_NNREL_GEN])

# step length of M2 interval in generative sequence
M2_STEP_GEN = NAMED_NNREL_GEN.index(S + NAMED_NNREL_LIN[1])

# a reasonable step length of stacked notes in linear sequence (not good)
CHORD_STEP_LIN = [nnrel - NAMED_NNREL_LIN[0] for nnrel in NAMED_NNREL_LIN].index(G) // 2


''' ----------------------------------------------------------------------------------------- '''
''' ************************************ basic utilities ************************************ '''
''' ----------------------------------------------------------------------------------------- '''


# sign function
def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0


# make elements of a list `lst` unique
def unique(lst):
    out = []
    for e in lst:
        if e in out:
            continue
        else:
            out.append(e)
    return out


# return a sorted list, with `idx`-th element of original list at the beginning
def circular_sorted(lst, idx, key=lambda x: x):
    _out = sorted([(e, i) for i, e in enumerate(lst)], key=lambda x: key(x[0]))
    indices = sorted([(i, j) for j, (_, i) in enumerate(_out)], key=lambda x: x[0])

    out = [x[0] for x in _out]
    idx = indices[idx][1]

    return out[idx:] + out[:idx]


# return 2 closest divisors of n
def closest_divisors(n):
    smallers = []
    for i in range(1, int(n ** (1 / 2)) + 1):
        if n % i == 0:
            smallers.append(i)
    smaller = max(smallers)

    return smaller, n // smaller


# a handy length function
def length(a, b):
    return b - a


# a handy middle point function
def middle(a, b):
    return (a + b) / 2


# a handy if x \in [a, b) function
def within(x, a, b):
    return a <= x < b


''' ----------------------------------------------------------------------------------------- '''
''' ********************************** for `Interval` Class ********************************* '''
''' naming scheme 0: ..., dd, d, P, A, AA, ...                                                '''
''' naming scheme 1: ..., dd, d, m, M, A, AA, ...                                             '''
''' ----------------------------------------------------------------------------------------- '''


# convert delta step to naming scheme 0 or 1
DELTA_STEP_TO_NS = {
    '12.7.5': [0, 1, 1, 0, 0, 1, 1],
    '19.11.8': [0, 1, 1, 0, 0, 1, 1]
}


''' ----------------------------------------------------------------------------------------- '''
''' ******************************* for `DiatonicScale` Class ******************************* '''
''' naming scheme 0 (NS0): C-mode, D-mode, ...                                                '''
''' naming scheme 1 (NS1): Ionian, Dorian, ...                                                '''
''' ----------------------------------------------------------------------------------------- '''


# scale type converter, change naming scheme 0 to naming scheme 1, e.g. 'C-mode' -> 'Ionian'
SCALE_TYPE_NS0_TO_NS1 = {
    '12.7.5': {
        'F-mode': ['Lydian'],
        'C-mode': ['Ionian'],
        'G-mode': ['Mixolydian'],
        'D-mode': ['Dorian'],
        'A-mode': ['Aeolian'],
        'E-mode': ['Phrygian'],
        'B-mode': ['Locrian']
    },
    '19.11.8': {
        'F-mode': ['Lydian'],
        'C-mode': ['Ionian'],
        'G-mode': ['Mixolydian'],
        'D-mode': ['Dorian'],
        'A-mode': ['Aeolian'],
        'E-mode': ['Phrygian'],
        'B-mode': ['Locrian']
    }
}

# scale type converter, change naming scheme 1 to naming scheme 0, e.g. 'Ionian' -> 'C-mode'
SCALE_TYPE_NS1_TO_NS0 = dict((ngs, dict((v, k) for k, vs in d.items() for v in vs)) for ngs, d in SCALE_TYPE_NS0_TO_NS1.items())

# default diatonic scale ns
DEFAULT_DIATONIC_SCALE_NS = 1


''' ----------------------------------------------------------------------------------------- '''
''' **************************** for `AlteredDiatonicScale` Class *************************** '''
''' ----------------------------------------------------------------------------------------- '''
''' naming scheme 0 (NS0): E-mode(#3), F-mode(b7), ...                                        '''
''' naming scheme 1 (NS1): Phrygian(#3), Lydian(b7), ...                                      '''
''' naming scheme 2 (NS2): Phrygian Dominant, Lydian Dominant, ...                            '''
'''                                                                                           '''
''' Class xx: starting from Lydian, add sharp to every degree then flat iteratively           '''
'''           e.g. Lydian - [x]Lydian(#1) - Lydian(#2) - ... - [x]Lydian(#7) - [x]Lydian(b1)  '''
'''                Lydian(b2) - ... [x]Lydian(#1, #1) - Lydian(#1, #2) - ...                  '''
''' ----------------------------------------------------------------------------------------- '''


# altered scale type converter, change naming scheme 0 to naming scheme 2, e.g. 'E-mode(#3)' -> 'HmP5b'
SCALE_TYPE_NS0_TO_NS2 = {
    '12.7.5': {
        # Class 1
        'F-mode(#2)': ['Lydian(#2)'],  # name?
        'C-mode(#5)': ['Ionian Augmented'],
        'Gb-mode(#1)': ['Ultra Locrian'],
        'D-mode(#4)': ['Ukrainian Dorian'],
        'A-mode(#7)': ['Harmonic Minor'],
        'E-mode(#3)': ['Phrygian Dominant', 'HmP5b'],
        'B-mode(#6)': ['Locrian(#6)'],  # name?

        # Class 3
        'F-mode(#5)': ['Lydian Augmented'],
        'E#-mode(b1)': ['Lydian Augmented'],

        'Cb-mode(#1)': ['Altered Dominant', 'Super Locrian'],
        'B-mode(b4)': ['Super Locrian', 'Altered Dominant'],

        'G-mode(#4)': ['Acoustic', 'Lydian Dominant'],
        'F-mode(b7)': ['Lydian Dominant', 'Acoustic'],

        'D-mode(#7)': ['Melodic Minor', 'Minor Major'],
        'C-mode(b3)': ['Minor Major', 'Melodic Minor'],

        'A-mode(#3)': ['Aeolian Dominant', 'Melodic Major'],
        'G-mode(b6)': ['Melodic Major', 'Aeolian Dominant'],

        'E-mode(#6)': ['Phrygian(#6)'],  # name?
        'D-mode(b2)': ['Dorian(b2)'],  # name?

        'B-mode(#2)': ['Half Diminished'],
        'A-mode(b5)': ['Half Diminished'],

        # Class 4
        'E-mode(#7)': ['Minor Neapolitan'],

        # Class 6
        'C-mode(b6)': ['Harmonic Major'],
        'G-mode(b2)': ['HMP5b'],

        # Class 9
        'E-mode(#3, #7)': ['Double Harmonic', 'Gypsy Major'],
        'C-mode(b2, b6)': ['Gypsy Major', 'Double Harmonic'],

        'A-mode(#4, #7)': ['Hungarian Minor'],
        'F-mode(b3, b6)': ['Hungarian Minor'],

        # Class 16
        'E-mode(#6, #7)': ['Major Neapolitan'],
        'D-mode(b2, #7)': ['Major Neapolitan'],
        'C-mode(b2, b3)': ['Major Neapolitan'],

        # Class 33
        'F-mode(b2, #5, #6)': ['Enigmatic'],
        'E#-mode(b1, b2, #6)': ['Enigmatic'],
        'D#-mode(b1, bb2)': ['Enigmatic'],

        # Class 0
        'F-mode': ['Lydian'],
        'C-mode': ['Major', 'Ionian'],
        'G-mode': ['Mixolydian'],
        'D-mode': ['Dorian'],
        'A-mode': ['Minor', 'Aeolian'],
        'E-mode': ['Phrygian'],
        'B-mode': ['Locrian']
    },
    '19.11.8': {
        # Class 1
        'F-mode(#2)': ['Lydian(#2)'],  # name?
        'C-mode(#5)': ['Ionian Augmented'],
        'Gb-mode(#1)': ['Ultra Locrian'],
        'D-mode(#4)': ['Ukrainian Dorian'],
        'A-mode(#7)': ['Harmonic Minor'],
        'E-mode(#3)': ['Phrygian Dominant', 'HmP5b'],
        'B-mode(#6)': ['Locrian(#6)'],  # name?

        # Class 3
        'F-mode(#5)': ['Lydian Augmented'],
        'E#-mode(b1)': ['Lydian Augmented'],

        'Cb-mode(#1)': ['Altered Dominant', 'Super Locrian'],
        'B-mode(b4)': ['Super Locrian', 'Altered Dominant'],

        'G-mode(#4)': ['Acoustic', 'Lydian Dominant'],
        'F-mode(b7)': ['Lydian Dominant', 'Acoustic'],

        'D-mode(#7)': ['Melodic Minor', 'Minor Major'],
        'C-mode(b3)': ['Minor Major', 'Melodic Minor'],

        'A-mode(#3)': ['Aeolian Dominant', 'Melodic Major'],
        'G-mode(b6)': ['Melodic Major', 'Aeolian Dominant'],

        'E-mode(#6)': ['Phrygian(#6)'],  # name?
        'D-mode(b2)': ['Dorian(b2)'],  # name?

        'B-mode(#2)': ['Half Diminished'],
        'A-mode(b5)': ['Half Diminished'],

        # Class 4
        'E-mode(#7)': ['Minor Neapolitan'],

        # Class 6
        'C-mode(b6)': ['Harmonic Major'],
        'G-mode(b2)': ['HMP5b'],

        # Class 9
        'E-mode(#3, #7)': ['Double Harmonic', 'Gypsy Major'],
        'C-mode(b2, b6)': ['Gypsy Major', 'Double Harmonic'],

        'A-mode(#4, #7)': ['Hungarian Minor'],
        'F-mode(b3, b6)': ['Hungarian Minor'],

        # Class 16
        'E-mode(#6, #7)': ['Major Neapolitan'],
        'D-mode(b2, #7)': ['Major Neapolitan'],
        'C-mode(b2, b3)': ['Major Neapolitan'],

        # Class 33
        'F-mode(b2, #5, #6)': ['Enigmatic'],
        'E#-mode(b1, b2, #6)': ['Enigmatic'],
        'D#-mode(b1, bb2)': ['Enigmatic'],

        # Class 0
        'F-mode': ['Lydian'],
        'C-mode': ['Major', 'Ionian'],
        'G-mode': ['Mixolydian'],
        'D-mode': ['Dorian'],
        'A-mode': ['Minor', 'Aeolian'],
        'E-mode': ['Phrygian'],
        'B-mode': ['Locrian']
    }
}

# altered scale type converter, change naming scheme 2 to naming scheme 0, e.g. 'HmP5b' -> 'E-mode(#3)'
SCALE_TYPE_NS2_TO_NS0 = dict((ngs, dict((v, k) for k, vs in d.items() for v in vs)) for ngs, d in SCALE_TYPE_NS0_TO_NS2.items())

# default altered diatonic scale ns
DEFAULT_ALTERED_DIATONIC_SCALE_NS = 2


def scale_type_convertor(scale_type, ns_old, ns_new):
    if ns_old == 0 and ns_new == 1:
        mapping = SCALE_TYPE_NS0_TO_NS1.get(NGS, {})
        return mapping.get(scale_type, [scale_type])[0]
    elif ns_old == 1 and ns_new == 0:
        mapping = SCALE_TYPE_NS1_TO_NS0.get(NGS, {})
        return mapping.get(scale_type, scale_type)
    elif ns_old == 0 and ns_new == 2:
        mapping = SCALE_TYPE_NS0_TO_NS2.get(NGS, {})
        return mapping.get(scale_type, [scale_type])[0]
    elif ns_old == 2 and ns_new == 0:
        mapping = SCALE_TYPE_NS2_TO_NS0.get(NGS, {})
        return mapping.get(scale_type, scale_type)
    else:
        raise ValueError('[`ns_old`, `ns_new`] must be [0, 1], [1, 0], [0, 2] or [2, 0]!')


# all possible altered diatonic scale types
ALL_SCALE_TYPES = {
    '12.7.5': [
    # order 0
	'Lydian',
    # order 1
	'Lydian(#2)',
	'Lydian(#3)',
	'Lydian(#5)',
	'Lydian(#6)',
	'Lydian(b2)',
	'Lydian(b3)',
	'Lydian(b6)',
    # order 2
	'Lydian(#2, #3)',
	'Lydian(#2, #6)',
	'Lydian(#2, b6)',
	'Lydian(#2, b7)',
	'Lydian(#3, #6)',
	'Lydian(#3, b2)',
	'Lydian(#3, b6)',
	'Lydian(#3, b7)',
	'Lydian(#5, #6)',
	'Lydian(#5, b2)',
	'Lydian(#5, b3)',
	'Lydian(#6, b2)',
	'Lydian(#6, b3)',
	'Lydian(b2, b3)',
	'Lydian(b2, b6)',
    # order 3
	'Lydian(#2, #2, #3)',
	'Lydian(#2, #3, b6)',
	'Lydian(#2, #3, b7)',
	'Lydian(#2, b1, b7)',
	'Lydian(#2, b6, b7)',
	'Lydian(#3, #6, b2)',
	'Lydian(#3, b1, b7)',
	'Lydian(#3, b2, b6)',
	'Lydian(#3, b2, b7)',
	'Lydian(#3, b6, b7)',
	'Lydian(#5, #6, b2)',
	'Lydian(#5, #6, b3)',
	'Lydian(#5, b2, b3)',
	'Lydian(#6, b2, b3)',
	'Lydian(b2, b3, b3)',
    # order 4
	'Lydian(#2, #2, #3, b6)',
	'Lydian(#2, #2, #3, b7)',
	'Lydian(#2, #3, b1, b7)',
	'Lydian(#2, #3, b6, b7)',
	'Lydian(#2, b1, b6, b7)',
	'Lydian(#2, b6, b7, b7)',
	'Lydian(#3, b1, b2, b7)',
	'Lydian(#3, b1, b6, b7)',
	'Lydian(#3, b6, b7, b7)',
	'Lydian(#5, #6, b2, b3)',
	'Lydian(#5, b2, b3, b3)',
	'Lydian(#6, b2, b3, b3)',
    # order 5
	'Lydian(#2, #2, #3, b1, b7)',
	'Lydian(#2, #2, #3, b6, b7)',
	'Lydian(#2, #3, b1, b6, b7)',
	'Lydian(#2, #3, b6, b7, b7)',
	'Lydian(#2, b1, b6, b7, b7)',
	'Lydian(#3, b1, b2, b2, b7)',
	'Lydian(#3, b1, b6, b7, b7)',
	'Lydian(#5, #6, b2, b3, b3)',
    # order 6
	'Lydian(#2, #2, #3, b1, b6, b7)',
	'Lydian(#2, #2, #3, b6, b7, b7)',
	'Lydian(#2, #3, b1, b6, b7, b7)',
	'Lydian(#2, b1, b1, b6, b7, b7)',
	'Lydian(#3, b1, b1, b6, b7, b7)',
    # order 7
	'Lydian(#2, #2, #3, b1, b6, b7, b7)',
	'Lydian(#2, #3, b1, b1, b6, b7, b7)',
    # order 8
	'Lydian(#2, #2, #3, b1, b1, b6, b7, b7)'
]
}


''' ----------------------------------------------------------------------------------------- '''
''' *********************************** for `Chord` Class *********************************** '''
''' naming scheme 0 (NS0): 1.3.5.7, 1.b3.5.b7, ...                                            '''
''' naming scheme 1 (NS1): M7, m7, ...                                                        '''
''' ----------------------------------------------------------------------------------------- '''


# chord type converter, change naming scheme 0 to naming scheme 1, e.g. 'R.3.5.b7' -> '7'
CHORD_TYPE_NS0_TO_NS1 = {
    '12.7.5': {
        # 5**
        'R.4.#5.7': ['augM7sus4', 'M7+5sus4'],
        'R.4.5.7': ['M7sus4'],
        'R.4.5': ['sus4'],
        'R.#3.#5.7': ['M7+5sus4(!)'],
        'R.#3.5.7': ['M7sus4(!)'],
        # 4**
        'R.3.#5.7': ['augM7', 'M7+5'],
        'R.3.#5.b7': ['aug7', '7+5'],
        'R.3.#5': ['aug', '+5'],
        'R.3.5.7': ['M7', 'maj7'],
        'R.3.5.7.9': ['M9', 'maj9'],
        'R.3.5.b7.9': ['9'],
        'R.3.5.b7': ['7'],
        'R.3.5.6': ['6'],
        'R.5': ['5'],
        'R.3.5': ['', 'M'],
        'R.3.b5.7': ['M7-5'],
        'R.3.b5.b7': ['7-5'],
        'R.3.b5': ['-5'],
        # 3**
        'R.b3.#5.b7': ['m7+5'],
        'R.b3.5.7': ['mM7'],
        'R.b3.5.b7': ['m7'],
        'R.b3.5.bb7': ['m6(!)'],
        'R.b3.5.6': ['m6'],
        'R.b3.5': ['m'],
        'R.b3.b5.7': ['mM7-5'],
        'R.b3.b5.b7': ['m7-5'],
        'R.b3.b5.bb7': ['dim7', 'm6-5'],
        'R.b3.b5': ['dim'],
        # 2**
        'R.bb3.5.b7': ['7sus2(!)'],
        'R.bb3.b5.b7': ['7-5sus2(!)'],
        'R.bb3.b5.bb7': ['6-5sus2(!)'],
        'R.2.5.b7': ['7sus2'],
        'R.2.b5.b7': ['7-5sus2'],
        'R.2.b5.6': ['6-5sus2'],
        'R.2.5': ['sus2'],
        'R.2.b5': ['-5sus2'],
        # scales
        'R.2.3.5.6': ['Gong'],
        'R.2.4.5.6': ['Zhi'],
        'R.2.4.6.b7': ['Shang'],
        'R.b3.4.5.b7': ['Yu'],
        'R.b3.4.b6.b7': ['Jue'],
        'R.b2.4.5.b6': ['In', 'Miyakobushi'],
        'R.3.4.5.7': ['Ryukyu']
    },
    '19.11.8': {
        # 5**
        'R.4.#5.7': ['augM7sus4', 'M7+5sus4'],
        'R.4.5.7': ['M7sus4'],
        'R.4.5': ['sus4'],
        'R.#3.#5.7': ['M7+5sus4(!)'],
        'R.#3.5.7': ['M7sus4(!)'],
        # 4**
        'R.3.#5.7': ['augM7', 'M7+5'],
        'R.3.#5.b7': ['aug7', '7+5'],
        'R.3.#5': ['aug', '+5'],
        'R.3.5.7': ['M7', 'maj7'],
        'R.3.5.7.9': ['M9', 'maj9'],
        'R.3.5.b7.9': ['9'],
        'R.3.5.b7': ['7'],
        'R.3.5.6': ['6'],
        'R.5': ['5'],
        'R.3.5': ['', 'M'],
        'R.3.b5.7': ['M7-5'],
        'R.3.b5.b7': ['7-5'],
        'R.3.b5': ['-5'],
        # 3**
        'R.b3.#5.b7': ['m7+5'],
        'R.b3.5.7': ['mM7'],
        'R.b3.5.b7': ['m7'],
        'R.b3.5.bb7': ['m6(!)'],
        'R.b3.5.6': ['m6'],
        'R.b3.5': ['m'],
        'R.b3.b5.7': ['mM7-5'],
        'R.b3.b5.b7': ['m7-5'],
        'R.b3.b5.bb7': ['dim7', 'm6-5'],
        'R.b3.b5': ['dim'],
        # 2**
        'R.bb3.5.b7': ['7sus2(!)'],
        'R.bb3.b5.b7': ['7-5sus2(!)'],
        'R.bb3.b5.bb7': ['6-5sus2(!)'],
        'R.2.5.b7': ['7sus2'],
        'R.2.b5.b7': ['7-5sus2'],
        'R.2.b5.6': ['6-5sus2'],
        'R.2.5': ['sus2'],
        'R.2.b5': ['-5sus2'],
        # scales
        'R.2.3.5.6': ['Gong'],
        'R.2.4.5.6': ['Zhi'],
        'R.2.4.6.b7': ['Shang'],
        'R.b3.4.5.b7': ['Yu'],
        'R.b3.4.b6.b7': ['Jue'],
        'R.b2.4.5.b6': ['In', 'Miyakobushi'],
        'R.3.4.5.7': ['Ryukyu']
    }
}

# chord type converter, change naming scheme 1 to naming scheme 0, e.g. '7' -> 'R.3.5.b7'
CHORD_TYPE_NS1_TO_NS0 = dict((ngs, dict((v, k) for k, vs in d.items() for v in vs)) for ngs, d in CHORD_TYPE_NS0_TO_NS1.items())

# default chord ns
DEFAULT_CHORD_NS = 1


def chord_type_convertor(chord_type, ns_old, ns_new):
    if ns_old == 0 and ns_new == 1:
        mapping = CHORD_TYPE_NS0_TO_NS1.get(NGS, {})
        return mapping.get(chord_type, [chord_type])[0]
    elif ns_old == 1 and ns_new == 0:
        mapping = CHORD_TYPE_NS1_TO_NS0.get(NGS, {})
        return mapping.get(chord_type, chord_type)
    else:
        raise ValueError('[`ns_old`, `ns_new`] must be [0, 1] or [1, 0]!')


''' -----------------------------------------------------------------------------------------'''
''' ************************************* for `audio.py` ************************************'''
''' -----------------------------------------------------------------------------------------'''


# sampling frequency
SF = 48000

# bit depth
BD = 24


''' -----------------------------------------------------------------------------------------'''
''' ********************************* for `instruments.py` **********************************'''
''' -----------------------------------------------------------------------------------------'''


FIG_HEIGHT = 3

NOTE_FACE_COLORS_LR = ['#f6b0f0', '#f6deb0']
NOTE_EDGE_COLORS_LR = ['#222222', '#222222']
NOTE_TEXT_COLORS_LR = ['#000000', '#000000']

BR357T_FACE_COLORS = {'B': '#00ff00', 'R': '#ff0000', 'T': '#0000ff', 'CN': '#444444', None:'#000000'}
BR357T_EDGE_COLORS = {'B': '#222222', 'R': '#222222', 'T': '#222222', 'CN': '#222222', None:'#000000'}
BR357T_TEXT_COLORS = {'B': '#000000', 'R': '#ffffff', 'T': '#ffffff', 'CN': '#ffffff', None:'#000000'}

DEGREE_FACE_COLORS_LR = ['#ff0000', '#222222']
DEGREE_EDGE_COLORS_LR = ['#000000', '#000000']
DEGREE_TEXT_COLORS_LR = ['#ffffff', '#ffffff']

TDS_FACE_COLORS =  {'T': '#d5e8d4', 'D': '#f8cecc', 'S': '#fff2cc', None: '#000000'}
TDS_EDGE_COLORS = {'T': '#222222', 'D': '#222222', 'S': '#222222', None: '#000000'}
TDS_TEXT_COLORS = {'T': '#000000', 'D': '#000000', 'S': '#000000', None: '#000000'}

AVOID_FACE_COLORS = {'[CN]': 'limegreen', '[A1]': 'red', '[A0]': 'orange', '[A2]': 'gold', '[OK]': 'dodgerblue', '[TN]': 'slategrey', None: 'black'}
AVOID_EDGE_COLORS = {'[CN]': '#222222', '[A1]': '#222222', '[A0]': '#222222', '[A2]': '#222222', '[OK]': '#222222', '[TN]': '#222222', None: '#222222'}
AVOID_TEXT_COLORS = {'[CN]': '#000000', '[A1]': '#000000', '[A0]': '#000000', '[A2]': '#000000', '[OK]': '#000000', '[TN]': '#000000', None: '#000000'}

VELOCITY_COLORS_LR = ['#ef58c', '#1cc6b7']


''' -----------------------------------------------------------------------------------------'''
''' ************************************* for `midi.py` *************************************'''
''' -----------------------------------------------------------------------------------------'''


# ADD2 MIDI mapping
ADD2_NOTE_NAMES = [
    '---', '---', '---', 'Ride 2 CCPos Shaft<->Tip', 'Ride 1 CCPos Shaft<->Tip', 'Snare CCPos Closed (Br)', 'Snare CCPos Op<->Sha', 'CC HiHat Shaft',
    'CC HiHat Tip', 'CC HiHat Bell', '---', '---', '---', '---', '---', '---',
    '---', '---', '---', '---', '---', '---', '---', '---',
    '---', '---', 'Sweep: Short 1', '---', 'Sweep: Short 2', 'Sweep: No Accent', 'Sweep: Fast Bright Acc', 'Sweep: Slow Bright Acc',
    'Sweep: Fast Dark Acc', 'Sweep: Slow Dark Acc', 'Sweep: Mute (br)', 'Closed Soft Tap (br)', 'Kick', 'Snare RimShot', 'Snare Open Hit', 'Snare RimShot (dbl)',
    'Snare Open Hit (dbl)', 'Snare Shallow Rimshot', 'Snare SideStick', 'Snare Shallow Hit', 'Snare RimClick', 'Ride 1 Tip', 'Cymbal 1', 'Flex 1 Hit A',
    'HH Foot Close', 'HH Closed1 Tip', 'HH Closed1 Shaft', 'HH Closed2 Tip', 'HH Closed2 Shaft', 'HH Closed Bell', 'HH Open A', 'HH Open B',
    'HH Open C', 'HH Open D', 'HH Open Bell', 'HH Foot Splash', 'Ride 1 Tip', 'Ride 1 Bell', 'Ride 1 Shaft', 'Ride 1 Choke',
    '---', 'Tom 4 Open Hit', 'Tom 4 Rimshot', 'Tom 3 Open Hit', 'Tom 3 Rimshot', 'Tom 2 Open Hit', 'Tom 2 Rimshot', 'Tom 1 Open Hit',
    'Tom 1 Rimshot', 'Flex 1 Hit B', 'Flex 1 Hit C', 'Sticks', 'Flex 1 Hit D', 'Cymbal 1', 'Cymbal 1 Choke', 'Cymbal 2',
    'Cymbal 2 Choke', 'Cymbal 3', 'Cymbal 3 Choke', '---', 'Ride 2 Tip', 'Ride 2 Bell', 'Ride 2 Shaft', 'Ride 2 Choke',
    '---', 'Cymbal 4', 'Cymbal 4 Choke', 'Cymbal 5', 'Cymbal 5 Choke', 'Cymbal 6', 'Cymbal 6 Choke', '---',
    'Flex 2 Hit A', 'Flex 2 Hit B', 'Flex 2 Hit C', 'Flex 2 Hit D', 'Flex 3 Hit A', 'Flex 3 Hit B', 'Flex 3 Hit C', 'Flex 3 Hit D',
    '---', '---', '---', '---', '---', '---', '---', '---',
    '---', '---', '---', '---', '---', '---', '---', '---',
    '---', '---', '---', '---', '---', '---', '---', '---',
    '---', '---', '---', '---', '---', '---', '---', '---'
]

# TODO: AGTC MIDI mapping
AGTC_NOTE_NAMES = [''] * 128

# CC name list
CC_NAMES = [f'cc {cc}' for cc in range(128)]
use_vocaloid = False
if use_vocaloid:
    CC_NAMES[11] = 'DYN'
    CC_NAMES[17] = 'BRE'
    CC_NAMES[74] = 'BRI'
    CC_NAMES[18] = 'CLE'
    CC_NAMES[19] = 'GEN'
    CC_NAMES[5] = 'POR'
    CC_NAMES[80] = 'PBS'
    CC_NAMES[81] = 'XSY'
    CC_NAMES[82] = 'GWL'


''' -----------------------------------------------------------------------------------------'''
''' *************************************** Show Info ***************************************'''
''' -----------------------------------------------------------------------------------------'''


out_str_1 = f'{N}-TET | {M}-tone | step length: {G} | starting: {S}'
out_str_2 = 'named notes: ' + str().join([f'{nnrel}={name} ' for nnrel, name in NNREL_TO_STR.items()])
n_hyphens = max(len(out_str_1), len(out_str_2))
print('-' * n_hyphens)
print(out_str_1)
print(out_str_2)
print('-' * n_hyphens)
