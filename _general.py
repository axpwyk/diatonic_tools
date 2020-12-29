def sign(x): return (x > 0) - (x < 0)


''' ----------------------------------------------------------------------------------------- '''
''' *********************************** for `theories.py` *********************************** '''
''' ----------------------------------------------------------------------------------------- '''
''' NN = note number                                                                          '''
''' LIN = linear, GEN = generative, ABS = absolute, REL = relative, STR = string, LST = list  '''
'''                                                                                           '''
''' * we call [index of `NAMED_LIN_NNREL`] `step`                                             '''
''' * we call [index of a scale] or [number of notes contained in an interval] `degree`       '''
'''                                                                                           '''
''' * WARNING: Changing `S` will lead to different interval naming scheme                     '''
'''            A4 in [N, G, S] = [12, 7, 5] is P4 (M4) in [N, G, S] = [12, 7, 0]              '''
''' ----------------------------------------------------------------------------------------- '''


# most basic constants (generate elements from starting point `S` using step length `G` modulo `N`)
N = 12  # `N`-tone equal temperament (`N`-TET)
G = 7 # generator (step length)
S = 5  # starter (starting point)

# most basic calculations
M = pow(G, -1, N)  # number of tones in diatonic scale
T = 2 ** (1 / N)  # ratio of semi-tone frequencies
C3 = 440 * (T ** (36 - 45))  # frequency of C3

# define named notes (natural notes) in linear order
NAMED_LIN_STR = 'CDEFGAB'                                                  # [12, 7, 5] diatonic scale
# NAMED_LIN_STR = 'CDEGA'                                                  # [12, 5, 4] diatonic scale
# NAMED_LIN_STR = str().join([chr(ord('A')+j) for j in range(M)])          # 97-TET 26-tone
# NAMED_LIN_STR = str().join([chr(int('03B1', 16)+j) for j in range(M)])   # `N`-TET `M`-tone
if len(NAMED_LIN_STR) != M: raise ValueError('Number of symbols must equal to number of notes!')

# relative note numbers in generative order, e.g. [5, 0, 7, 2, 9, 4, 11]
NAMED_GEN_NNREL = [(S + i * G) % N for i in range(M)]

# relative note numbers in linear order, e.g. [0, 2, 4, 5, 7, 9, 11]
NAMED_LIN_NNREL = sorted(NAMED_GEN_NNREL)

# nnrel/note name convertors
NNREL_TO_NAME_STR = {nnrel: NAMED_LIN_STR[i] for i, nnrel in enumerate(NAMED_LIN_NNREL)}
NAME_STR_TO_NNREL = dict((v, k) for k, v in NNREL_TO_NAME_STR.items())

# change `NAMED_LIN_STR` into generative order, e.g. 'CDEFGAB' -> 'FCGDAEB'
NAMED_GEN_STR = ''.join([NNREL_TO_NAME_STR[k] for k in NAMED_GEN_NNREL])


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


NOTE_COLORS = ['#f6b0f0', '#f6deb0']
NOTE_TEXT_COLORS = ['#000000', '#000000']

BR357T_COLORS = {
    None: '#000000',
    # Root
    'R': '#ff0000',
    # Bass
    'B': '#00ff00',
    # 9th
    'b9': '#0000ff',
    '9': '#0000ff',
    '#9': '#0000ff',
    '##9': '#0000ff',
    # 3rd
    'bb3': '#000000',
    'b3': '#000000',
    '3': '#000000',
    '#3': '#000000',
    # 11th
    'bb11': '#0000ff',
    'b11': '#0000ff',
    '11': '#0000ff',
    '#11': '#0000ff',
    '##11': '#0000ff',
    # 5th
    'bb5': '#000000',
    'b5': '#000000',
    '5': '#000000',
    '#5': '#000000',
    '##5': '#000000',
    # 13th
    'bb13': '#0000ff',
    'b13': '#0000ff',
    '13': '#0000ff',
    '#13': '#0000ff',
    # 7th
    'bbb7': '#000000',
    'bb7': '#000000',
    'b7': '#000000',
    '7': '#000000'
}
BR357T_TEXT_COLORS = {
    None: '#ffffff',
    # Root
    'R': '#ffffff',
    # Bass
    'B': '#000000',
    # 9th
    'b9': '#ffffff',
    '9': '#ffffff',
    '#9': '#ffffff',
    '##9': '#ffffff',
    # 3rd
    'bb3': '#ffffff',
    'b3': '#ffffff',
    '3': '#ffffff',
    '#3': '#ffffff',
    # 11th
    'bb11': '#ffffff',
    'b11': '#ffffff',
    '11': '#ffffff',
    '#11': '#ffffff',
    '##11': '#ffffff',
    # 5th
    'bb5': '#ffffff',
    'b5': '#ffffff',
    '5': '#ffffff',
    '#5': '#ffffff',
    '##5': '#ffffff',
    # 13th
    'bb13': '#ffffff',
    'b13': '#ffffff',
    '13': '#ffffff',
    '#13': '#ffffff',
    # 7th
    'bbb7': '#ffffff',
    'bb7': '#ffffff',
    'b7': '#ffffff',
    '7': '#ffffff'
}

DEGREE_COLORS = ['#ff0000', '#000000']
DEGREE_TEXT_COLORS = ['#ffffff', '#ffffff']

TDS_COLORS =  {'T': '#d5e8d4', 'D': '#f8cecc', 'S': '#fff2cc'}

CSTYPE_COLORS = {'[CN]': 'limegreen', '[A1]': 'red', '[A0]': 'orange', '[A2]': 'gold', '[OK]': 'dodgerblue', '[TN]': 'slategrey', None: 'black'}

VELOCITY_COLORS = [[0.94, 0.02, 0.55], [0.11, 0.78, 0.72]]


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


''' -----------------------------------------------------------------------------------------'''
''' *************************************** Show Info ***************************************'''
''' -----------------------------------------------------------------------------------------'''


out_str_1 = f'{N}-TET | {M}-tone | step length: {G} | starting: {S}'
out_str_2 = 'named notes: ' + str().join([f'{nnrel}={name} ' for nnrel, name in NNREL_TO_NAME_STR.items()])
n_hyphens = max(len(out_str_1), len(out_str_2))
print('-' * n_hyphens)
print(out_str_1)
print(out_str_2)
print('-' * n_hyphens)
