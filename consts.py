T = 2**(1/12)


def sign(x): return 1 if x > 0 else 0 if x == 0 else -1


''' for Note '''


NATURAL_NOTES = [0, 2, 4, 5, 7, 9, 11]

NOTE_NAMES = ['C', '', 'D', '', 'E', 'F', '', 'G', '', 'A', '', 'B']


''' for Interval '''


INTERVAL_TYPES = [['P', 'd', '', '', '', '', ''],
                  ['A', 'm', '', '', '', '', ''],
                  ['', 'M', 'd', '', '', '', ''],
                  ['', 'A', 'm', '', '', '', ''],
                  ['', '', 'M' ,'d' ,'' ,'' ,''],
                  ['', '', 'A' ,'P' ,'' ,'' ,''],
                  ['', '', '' ,'A' ,'d' ,'' ,''],
                  ['', '', '' ,'' ,'P' ,'d' ,''],
                  ['', '', '' ,'' ,'A' ,'m' ,''],
                  ['', '', '' ,'' ,'' ,'M' ,'d'],
                  ['', '', '' ,'' ,'' ,'A' ,'m'],
                  ['', '', '' ,'' ,'' ,'' ,'M']]


''' for DiatonicScale '''


# these two encoders are used to calculate number of accidentals
SCALE_TYPE_ENCODER = {'Locrian': -3, 'Phrygian': -2, 'Aeolian': -1, 'Dorian': 0, 'Mixolydian': 1, 'Ionian': 2, 'Lydian':3}

TONIC_NOTE_ENCODER = {'F': -3, 'C': -2, 'G': -1, 'D': 0, 'A': 1, 'E': 2, 'B': 3}

SCALE_TYPE_DECODER = ['Locrian', 'Phrygian', 'Aeolian', 'Dorian', 'Mixolydian', 'Ionian', 'Lydian']


''' for Chord '''


CHORD_TYPE_TO_SCALE_TYPE = {'aug': 'Ionian(#5)',
                            '': 'Ionian',
                            '-5': 'Ionian(b5)',
                            'm': 'Aeolian',
                            'dim': 'Locrian',
                            'dim-3': 'Locrian(b3)',
                            'M7+5': 'Ionian(#5)',
                            'M7': 'Ionian',
                            '7+5': 'Mixolydian(#5)',
                            '7': 'Mixolydian',
                            '7-5': 'Mixolydian(b5)',
                            'mM7': 'Aeolian(#7)',
                            'm7': 'Aeolian',
                            'm7-5': 'Locrian',
                            'dim7': 'Locrian(b7)',
                            'm7-5-3': 'Locrian(b3)',
                            'sus2': 'Ionian',
                            'sus4': 'Ionian',
                            '6': 'Ionian',
                            'm6': 'Dorian',
                            '9': 'Mixolydian'}

CHORD_TYPE_TO_DEGREES = {'aug': [0, 2, 4],
                         '': [0, 2, 4],
                         '-5': [0, 2, 4],
                         'm': [0, 2, 4],
                         'dim': [0, 2, 4],
                         'dim-3': [0, 2, 4],
                         'M7+5': [0, 2, 4, 6],
                         'M7': [0, 2, 4, 6],
                         '7+5': [0, 2, 4, 6],
                         '7': [0, 2, 4, 6],
                         '7-5': [0, 2, 4, 6],
                         'mM7': [0, 2, 4, 6],
                         'm7': [0, 2, 4, 6],
                         'm7-5': [0, 2, 4, 6],
                         'dim7': [0, 2, 4, 6],
                         'm7-5-3': [0, 2, 4, 6],
                         'sus2': [0, 1, 4],
                         'sus4': [0, 3, 4],
                         '6': [0, 2, 4, 5],
                         'm6': [0, 2, 4, 5],
                         '9': [0, 2, 4, 6, 1]}

TENSION_NAME_TO_INTERVAL_NAME = {'b9': 'm9',
                            '9': 'M9',
                            '#9': 'A9',
                            '11': 'P11',
                            '#11': 'A11',
                            'b13': 'm13',
                            '13': 'M13'}

INTERVAL_NAME_TO_TENSION_NAME = {'m9': 'b9',
                            'M9': '9',
                            'A9': '#9',
                            'P11': '11',
                            'A11': '#11',
                            'm13': 'b13',
                            'M13': '13'}

# recognize chord type from intervals
INTERVAL_NAME_TO_CHORD_TYPE = {'44': 'aug',
                               '43': '',
                               '42': '-5',
                               '34': 'm',
                               '33': 'dim',
                               '24': 'dim-3',
                               '443': 'M7+5',
                               '434': 'M7',
                               '442': '7+5',
                               '433': '7',
                               '424': '7-5',
                               '344': 'mM7',
                               '343': 'm7',
                               '334': 'm7-5',
                               '333': 'dim7',
                               '244': 'm7-5-3',
                               '25': 'sus2',
                               '52': 'sus4',
                               '432': '6',
                               '342': 'm6',
                               '4334': '9'}

CHORD_TYPE_TO_COLOR = {'M7': 'red',
                       'M7+5': 'magenta',
                       '7': 'white',
                       'mM7': 'cyan',
                       'm7': 'blue',
                       'm7-5': 'cyan',
                       'dim7': 'green'}


''' for midi.py '''


# ADD2 MIDI mapping
ADD2_NOTE_NAMES = ['---', '---', '---', 'Ride 2 CCPos Shaft<->Tip', 'Ride 1 CCPos Shaft<->Tip', 'Snare CCPos Closed (Br)', 'Snare CCPos Op<->Sha', 'CC HiHat Shaft',
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
                   '---', '---', '---', '---', '---', '---', '---', '---']

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
