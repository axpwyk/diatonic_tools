def sign(x): return 1 if x > 0 else 0 if x == 0 else -1


''' for `Note` Class '''


# alterable consts
N = 12  # `N`-tone equal temperament (`N`-TET)
L = 7  # step length of diatonic generator
S = 5  # starting point of diatonic generator

# some calculations
M = pow(L, -1, N)  # number of notes in `N`-TET `L`-tone diatonic scale
T = 2**(1/N)  # semi-tone

# define named notes (natural notes)
# symbols for named notes ('CDEFGAB' is convention for 12-TET 7-tone diatonic scale)
NOTE_NAMES_STR = 'CDEFGAB'
# NOTE_NAMES_STR = str().join([chr(int('03B1', 16)+j) for j in range(M)])
if len(NOTE_NAMES_STR) != M: raise ValueError('Number of symbols must equal to number of notes!')

# linear nnrels
# we call elements of `NAMED_NOTES` `nnrel`, index of `NAMED_NOTES` `step`, and index in a scale `degree`
NAMED_NOTES = sorted([(S+i*L)%N for i in range(M)])

# a list of length `N` where i-th position is its corresponding note name (if no name use '')
NOTE_NAMES = [''] * N
for i, j in enumerate(NAMED_NOTES): NOTE_NAMES[j] = NOTE_NAMES_STR[i]


''' for `Interval` Class '''


# currently it's only available for 12-TET 7-tone diatonic scale
# 0   3 - 4   7  (..., dd, d, P, A, AA, ...)
# |   |   |   |
# 1 - 2   5 - 6  (..., dd, d, m, (P), M, A, AA, ...)

# find center
DELTA_STEP_TO_DELTA_NOTE_CENTER_X2 = [0, 3, 7, 10, 14, 17, 21]


# find offsets
def delta_nnabs_x2_to_interval_type(delta_nnabs_x2, interval_class):
    if interval_class == '0347':
        if delta_nnabs_x2 < 0:
            return -delta_nnabs_x2 // 2 * 'd'
        elif delta_nnabs_x2 == 0:
            return 'P'
        else:
            return delta_nnabs_x2 // 2 * 'A'
    elif interval_class == '1256':
        if delta_nnabs_x2 < 0:
            return -delta_nnabs_x2 // 2 * 'd' if delta_nnabs_x2 < -1 else 'm'
        else:
            return delta_nnabs_x2 // 2 * 'A' if delta_nnabs_x2 > 1 else 'M'
    else:
        raise ValueError('No such type!')


def interval_type_to_delta_nnabs_x2(interval_type, interval_class):
    if interval_class == '0347':
        if interval_type == 'P':
            return 0
        else:
            ds = interval_type.count('d')
            As = interval_type.count('A')
            if any([ds, As]):
                return -2 * ds + 2 * As
            else:
                raise ValueError('No such interval type!')
    if interval_class == '1256':
        if interval_type in ['m', 'M']:
            return {'m': -1, 'M': 1}[interval_type]
        else:
            ds = interval_type.count('d')
            As = interval_type.count('A')
            if any([ds, As]) and not all([ds, As]):
                return (-1 - 2*ds)*(ds!=0) + (1 + 2*As)*(As!=0)
            else:
                raise ValueError('No such interval type!')
    else:
        raise ValueError('No such type!')


''' for `DiatonicScale` Class '''


# currently it's only available for 12-TET 7-tone diatonic scale
# these two encoders are used to calculate number of accidentals
SCALE_TYPE_ENCODER = {'Locrian': -3, 'Phrygian': -2, 'Aeolian': -1, 'Dorian': 0, 'Mixolydian': 1, 'Ionian': 2, 'Lydian':3}

TONIC_NAME_ENCODER = {'F': -3, 'C': -2, 'G': -1, 'D': 0, 'A': 1, 'E': 2, 'B': 3}

# for `get_name` method
SCALE_TYPE_DECODER = ['Locrian', 'Phrygian', 'Aeolian', 'Dorian', 'Mixolydian', 'Ionian', 'Lydian']


''' for `DiatonicScaleV2` Class '''





''' for `AlteredDiatonicScale` Class '''


# get interval vectors of all 66 classes (stacking 2nds)
SCALE_INTERVAL_VECTOR_LIST = []
with open('all_heptatonic_scale_intervals.txt', 'r') as f:
    for line in f:
        SCALE_INTERVAL_VECTOR_LIST.append(eval(line))

# get interval vectors of all 66 classes (stacking 3rds)
CHORD_INTERVAL_VECTOR_LIST = []
with open('all_heptatonic_chord_intervals.txt', 'r') as f:
    for line in f:
        CHORD_INTERVAL_VECTOR_LIST.append(eval(line))

# get names of all 66 classes
CLASS_LIST = []
with open('all_heptatonic_scale_classes.txt', 'r') as f:
    for line in f:
        CLASS_LIST.append(eval(line))

# alternative names
ALTERNATIVE_NAMES = {
    'Ukrainian Dorian': 'Dorian(#4)',
    'Harmonic Minor': 'Aeolian(#7)',
    'Phrygian Dominant': 'Phrygian(#3)',
    'HMP5B': 'Phrygian(#3)',
    'Altered': 'Locrian(b4)',
    'Acoustic': 'Lydian(b7)',
    'Lydian Dominant': 'Lydian(b7)',
    'Melodic Minor': 'Dorian(#7)',
    'Minor Major': 'Ionian(b3)',
    'Melodic Major': 'Mixolydian(b6)',
    'Major Minor': 'Aeolian(#3)',
    'Half Diminished': 'Locrian(#2)',
    'Minor Neapolitan': 'Phrygian(#7)',
    'Harmonic Phrygian': 'Phrygian(#7)',
    'Harmonic Major': 'Ionian(b6)',
    'Harmonic Lydian': 'Lydian(b6)',
    'Hungarian Minor': 'Aeolian(#4, #7)',
    'Double Harmonic': 'Phrygian(#3, #7)',
    'Major Neapolitan': 'Phrygian(#6, #7)',
    'Melodic Phrygian': 'Phrygian(#6, #7)',
    'Major': 'Ionian',  # keep these two at the end!!!
    'Minor': 'Aeolian'  # keep these two at the end!!!
}

# conventional names
CONVENTIONAL_NAMES = {
    # Class 1
    'Phrygian(#3)': ['Phrygian Dominant', 'HmP5b'],
    'Aeolian(#7)': ['Harmonic Minor'],
    'Dorian(#4)': ['Ukrainian Dorian'],
    'Mixolydian(#1)': ['Ultra Locrian'],

    # Class 3
    'Mixolydian(#4)': ['Lydian Dominant', 'Acoustic'],
    'Lydian(b7)': ['Lydian Dominant', 'Acoustic'],

    'Aeolian(#3)': ['Aeolian Dominant', 'Melodic Major'],
    'Mixolydian(b6)': ['Aeolian Dominant', 'Melodic Major'],

    'Ionian(#1)': ['Super Locrian', 'Altered Dominant'],
    'Locrian(b4)': ['Super Locrian', 'Altered Dominant'],

    'Dorian(#7)': ['Melodic Minor'],
    'Ionian(b3)': ['Melodic Minor'],

    'Locrian(#2)': ['Half Diminished'],
    'Aeolian(b5)': ['Half Diminished'],

    # Class 4
    'Phrygian(#7)': ['Minor Neapolitan'],

    # Class 6
    'Ionian(b6)': ['Harmonic Major'],
    'Mixolydian(b2)': ['HMP5b'],

    # Class 9
    'Phrygian(#3,#7)': ['Double Harmonic', 'Gypsy Major'],
    'Ionian(b2,b6)': ['Double Harmonic', 'Gypsy Major'],

    'Aeolian(#4,#7)': ['Hungarian Minor'],
    'Lydian(b3,b6)': ['Hungarian Minor'],

    # Class 16
    'Phrygian(#6,#7)': ['Major Neapolitan'],
    'Dorian(#7,b2)': ['Major Neapolitan'],
    'Ionian(b2,b3)': ['Major Neapolitan']
}


''' for `Chord` Class '''


CHORD_TYPE_TO_SCALE_TYPE_OLD = {
    'aug': 'Ionian(#5)',
    '': 'Ionian',
    '-5': 'Ionian(b5)',
    'm': 'Aeolian',
    'dim': 'Locrian',
    'dim-3': 'Locrian(b3)',
    'M7+5': 'Ionian(#5)',
    '7+5': 'Mixolydian(#5)',
    'M7': 'Ionian',
    '7': 'Mixolydian',
    '7-5': 'Mixolydian(b5)',
    'mM7': 'Aeolian(#7)',
    'm7': 'Aeolian',
    'm7-5': 'Locrian',
    'dim7': 'Locrian(b7)',
    'm7-5-3': 'Locrian(b3)',
    'dim7-3': 'Locrian(b7, b3)',  # b Dorian(#1)
    'sus2': 'Ionian',
    'sus4': 'Ionian',
    '6': 'Ionian',
    'm6': 'Dorian',
    '9': 'Mixolydian'
}

CHORD_TYPE_TO_SCALE_TYPE = {
    # 5**
    'M7+5sus4': 'Ionian(#5)',  # M7+5+3
    'M7sus4': 'Ionian',  # M7+3
    'sus4': 'Ionian',  # +3
    # 4**
    'augM7': 'Ionian(#5)',  # M7+5
    'aug7': 'Mixolydian(#5)',  # 7+5
    'aug': 'Ionian(#5)',  # +5
    'M7': 'Lydian',
    '9': 'Mixolydian',
    '7': 'Mixolydian',
    '6': 'Lydian',  # -7
    '': 'Lydian',
    'M7-5': 'Ionian(b5)',
    '7-5': 'Locrian(#3)',
    '-5': 'Ionian(b5)',
    # 3**
    'm7+5': 'Dorian(#5)',
    'mM7': 'Aeolian(#7)',
    'm7': 'Aeolian',
    'm6': 'Dorian',  # m-7
    'm': 'Aeolian',
    'mM7-5': 'Locrian(#7)',
    'm7-5': 'Locrian',
    'dim7': 'Locrian(b7)',  # m-7-5
    'dim': 'Locrian',  # m-5
    # 2**
    '7sus2': 'Mixolydian',  # 7-3
    '7-5sus2': 'Mixolydian(b5)',  # 7-5-3
    '6-5sus2': 'Mixolydian(b5)',  # -7-5-3
    'sus2': 'Mixolydian',  # -3
    '-5sus2': 'Mixolydian(b5)',  # -5-3
}

CHORD_TYPE_TO_STEPS_OLD = {
    'aug': [0, 2, 4],
    '': [0, 2, 4],
    '-5': [0, 2, 4],
    'm': [0, 2, 4],
    'dim': [0, 2, 4],
    'dim-3': [0, 2, 4],
    'M7+5': [0, 2, 4, 6],
    '7+5': [0, 2, 4, 6],
    'M7': [0, 2, 4, 6],
    '7': [0, 2, 4, 6],
    '7-5': [0, 2, 4, 6],
    'mM7': [0, 2, 4, 6],
    'm7': [0, 2, 4, 6],
    'm7-5': [0, 2, 4, 6],
    'dim7': [0, 2, 4, 6],
    'm7-5-3': [0, 2, 4, 6],
    'dim7-3': [0, 2, 4, 6],
    'sus2': [0, 1, 4],
    'sus4': [0, 3, 4],
    '6': [0, 2, 4, 5],
    'm6': [0, 2, 4, 5],
    '9': [0, 2, 4, 6, 1]
}

CHORD_TYPE_TO_STEPS = {
# 5**
    'M7+5sus4': [0, 3, 4, 6],  # M7+5+3
    'M7sus4': [0, 3, 4, 6],  # M7+3
    'sus4': [0, 3, 4],  # +3
    # 4**
    'augM7': [0, 2, 4, 6],  # M7+5
    'aug7': [0, 2, 4, 6],  # 7+5
    'aug': [0, 2, 4],  # +5
    'M7': [0, 2, 4, 6],
    '9': [0, 2, 4, 6, 1],
    '7': [0, 2, 4, 6],
    '6': [0, 2, 4, 5],  # -7
    '': [0, 2, 4],
    'M7-5': [0, 2, 4, 6],
    '7-5': [0, 2, 4, 6],
    '-5': [0, 2, 4],
    # 3**
    'm7+5': [0, 2, 4, 6],
    'mM7': [0, 2, 4, 6],
    'm7': [0, 2, 4, 6],
    'm6': [0, 2, 4, 5],  # m-7
    'm': [0, 2, 4],
    'mM7-5': [0, 2, 4, 6],
    'm7-5': [0, 2, 4, 6],
    'dim7': [0, 2, 4, 6],  # m-7-5
    'dim': [0, 2, 4],  # m-5
    # 2**
    '7sus2': [0, 1, 4, 6],  # 7-3
    '7-5sus2': [0, 1, 4, 6],  # 7-5-3
    '6-5sus2': [0, 1, 4, 5],  # -7-5-3
    'sus2': [0, 1, 4],  # -3
    '-5sus2': [0, 1, 4],  # -5-3
}

TENSION_NAME_TO_INTERVAL_NAME = {
    # Root
    'R': 'P1',
    # 9th
    'b9': 'm2',
    '9': 'M2',
    '#9': 'A2',
    '##9': 'AA2',
    # 3rd
    'bb3': 'd3',
    'b3': 'm3',
    '3': 'M3',
    '#3': 'A3',
    # 11th
    'bb11': 'dd4',
    'b11': 'd4',
    '11': 'P4',
    '#11': 'A4',
    '##11': 'AA4',
    # 5th
    'bb5': 'dd5',
    'b5': 'd5',
    '5': 'P5',
    '#5': 'A5',
    '##5': 'AA5',
    # 13th
    'bb13': 'd6',
    'b13': 'm6',
    '13': 'M6',
    '#13': 'A6',
    # 7th
    'bbb7': 'dd7',
    'bb7': 'd7',
    'b7': 'm7',
    '7': 'M7'
}

INTERVAL_NAME_TO_TENSION_NAME = dict((v, k) for k, v in TENSION_NAME_TO_INTERVAL_NAME.items())

# recognize chord type from intervals
INTERVAL_VECTOR_TO_CHORD_TYPE = {
    # 5**
    '533': 'M7+5sus4',  # M7+5+3
    '524': 'M7sus4',  # M7+3
    '52': 'sus4',  # +3
    # 4**
    '443': 'augM7',  # M7+5
    '442': 'aug7',  # 7+5
    '44': 'aug',  # +5
    '434': 'M7',
    '4334': '9',
    '433': '7',
    '432': '6',  # -7
    '43': '',
    '425': 'M7-5',
    '424': '7-5',
    '42': '-5',
    # 3**
    '352': 'm7+5',
    '344': 'mM7',
    '343': 'm7',
    '342': 'm6',  # m-7
    '34': 'm',
    '335': 'mM7-5',
    '334': 'm7-5',
    '333': 'dim7',  # m-7-5
    '33': 'dim',  # m-5
    # 2**
    '253': '7sus2',  # 7-3
    '244': '7-5sus2',  # 7-5-3
    '243': '6-5sus2',  # -7-5-3
    '25': 'sus2',  # -3
    '24': '-5sus2',  # -5-3
}

CHORD_TYPE_TO_CONSOLE_COLOR = {
    'M7+5': 'magenta',
    'M7': 'red',
    '7': 'white',
    'mM7': 'cyan',
    'm7': 'blue',
    'm7-5': 'cyan',
    'dim7': 'green'
}


''' for `ChordEx` Class '''


# for `ChordEx.get_name_ex()` method
INTERVAL_NAME_TO_CHORD_TYPE = {
    # 3rd
    'd3': '-3',
    'm3': 'm',
    'M3': '',
    'A3': '+3',
    # 5th
    'dd5': '--5',
    'd5': '-5',
    'P5': '',
    'A5': '+5',
    'AA5': '++5',
    # 7th
    'dd7': '--7',
    'd7': '-7',
    'm7': '7',
    'M7': 'M7',
    # 9th
    'm2': 'b9',
    'M2': '9',
    'A2': '#9',
    # 11th
    'd4': 'b11',
    'P4': '11',
    'A4': '#11',
    # 13th
    'd6': 'bb13',
    'm6': 'b13',
    'M6': '13',
    'A6': '#13'
}


''' for midi.py '''


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

# AGTC MIDI mapping
AGTC_NOTE_NAMES = [0]*128

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


''' for audio.py '''


# sampling frequency
SF = 48000

# bit depth
BD = 24


''' end of `const.py` '''


out_str_1 = f'{N}-TET | {M}-tone | step length: {L} | starting: {S}'
out_str_2 = 'named notes: ' + str().join([f'{ni}={NAMED_NOTES[i]} ' for i, ni in enumerate(NOTE_NAMES_STR)])
num_dash = max(len(out_str_1), len(out_str_2))
print('-'*num_dash)
print(out_str_1)
print(out_str_2)
print('-'*num_dash)
