T = 2**(1/12)

sign = lambda x: 1 if x > 0 else 0 if x == 0 else -1

''' for Note '''

NATURAL_NOTES = [0, 2, 4, 5, 7, 9, 11]

NOTE_NAMES = ['C', '', 'D', '', 'E', 'F', '', 'G', '', 'A', '', 'B']

''' for Interval '''

INTERVAL_TYPES = [['P', 'd', '', '', '', '', 'A'],
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
                  ['d', '', '' ,'' ,'' ,'' ,'M']]

''' for Mode '''

IONIAN_INTERVALS = ['M2', 'M2', 'm2', 'M2', 'M2', 'M2', 'm2']

HMINOR_INTERVALS = ['M2', 'm2', 'M2', 'M2', 'm2', 'A2', 'm2']

MMINOR_INTERVALS = ['M2', 'm2', 'M2', 'M2', 'M2', 'M2', 'm2']

def list_shift(lst, t):
    return lst[t:] + lst[:t]

MODE_INTERVALS = {'Lydian': list_shift(IONIAN_INTERVALS, 4-1),
                  'Ionian': list_shift(IONIAN_INTERVALS, 1-1),
                  'Mixolydian': list_shift(IONIAN_INTERVALS, 5-1),
                  'Dorian': list_shift(IONIAN_INTERVALS, 2-1),
                  'Aeolian': list_shift(IONIAN_INTERVALS, 6-1),
                  'Phrygian': list_shift(IONIAN_INTERVALS, 3-1),
                  'Locrian': list_shift(IONIAN_INTERVALS, 7-1),
                  'HMinor': HMINOR_INTERVALS,
                  'MMinor': MMINOR_INTERVALS}

''' for Chord '''

CHORD_COLOR_CONSOLE = {'M7': 'red',
                        'M7+5': 'magenta',
                        '7': 'white',
                        'mM7': 'cyan',
                        'm7': 'blue',
                        'm7-5': 'cyan',
                        'dim7': 'green'}

# recognize chord type from intervals
INTERVAL_NAME_TO_CHORD_TYPE = {'44': 'aug',
                               '43': '',
                               '34': 'm',
                               '33': 'dim',
                               '443': 'M7+5',
                               '434': 'M7',
                               '433': '7',
                               '344': 'mM7',
                               '343': 'm7',
                               '334': 'm7-5',
                               '333': 'dim7',
                               '25': 'sus2',
                               '52': 'sus4',
                               '432': '6',
                               '4334': '9'}

CHORD_TYPE_TO_MODE_TYPE = {'aug': 'HMinor',
                           '': 'Ionian',
                           'm': 'Aeolian',
                           'dim': 'Locrian',
                           'M7+5': 'HMinor3',
                           'M7': 'Ionian',
                           '7': 'Mixolydian',
                           'mM7': 'HMinor',
                           'm7': 'Aeolian',
                           'm7-5': 'Locrian',
                           'dim7': 'HMinor7',
                           'sus2': 'Ionian',
                           'sus4': 'Ionian',
                           '6': 'Ionian',
                           '9': 'Mixolydian'}

CHORD_TYPE_TO_STEPS = {'aug': [0, 2, 4],
                       '': [0, 2, 4],
                       'm': [0, 2, 4],
                       'dim': [0, 2, 4],
                       'M7': [0, 2, 4, 6],
                       'M7+5': [0, 2, 4, 6],
                       '7': [0, 2, 4, 6],
                       'mM7': [0, 2, 4, 6],
                       'm7': [0, 2, 4, 6],
                       'm7-5': [0, 2, 4, 6],
                       'dim7': [0, 2, 4, 6],
                       'sus2': [0, 1, 4],
                       'sus4': [0, 3, 4],
                       '6': [0, 2, 4, 5],
                       '9': [0, 2, 4, 6, 1]}

TENSION_TYPE_TO_STEP = {'': [[], None],
                        '9': [[1], 0],
                        'b9': [[1], -1],
                        '#9': [[1], 1],
                        '11': [[3], 0],
                        '#11': [[3], 1],
                        '13': [[5], 0],
                        'b13': [[5], -1]}

''' for midi '''

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
