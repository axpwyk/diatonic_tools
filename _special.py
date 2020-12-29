from ast import literal_eval


''' ----------------------------------------------------------------------------------------- '''
''' ********************************** for `Interval` Class ********************************* '''
''' ----------------------------------------------------------------------------------------- '''


DELTA_STEP_TO_NS_12_7_5 = [1, 2, 2, 1, 1, 2, 2]


''' ----------------------------------------------------------------------------------------- '''
''' ******************************* for `DiatonicScale` Class ******************************* '''
''' ----------------------------------------------------------------------------------------- '''


# scale type converter, change old naming scheme to new naming scheme, e.g. Ionian -> C-mode
SCALE_TYPE_OLD_TO_NEW = {
    'Lydian': 'F-mode',
    'Ionian': 'C-mode',
    'Mixolydian': 'G-mode',
    'Dorian': 'D-mode',
    'Aeolian': 'A-mode',
    'Phrygian': 'E-mode',
    'Locrian': 'B-mode'
}

SCALE_TYPE_NEW_TO_OLD = dict((v, k) for k, v in SCALE_TYPE_OLD_TO_NEW.items())


''' ----------------------------------------------------------------------------------------- '''
''' **************************** for `AlteredDiatonicScale` Class *************************** '''
''' ----------------------------------------------------------------------------------------- '''


# get interval vectors of all 66 classes (stacking 2nds)
SCALE_INTERVAL_VECTOR_LIST = []
with open('all_heptatonic_scale_intervals.txt', 'r') as f:
    for line in f:
        SCALE_INTERVAL_VECTOR_LIST.append(literal_eval(line))

# get interval vectors of all 66 classes (stacking 3rds)
CHORD_INTERVAL_VECTOR_LIST = []
with open('all_heptatonic_chord_intervals.txt', 'r') as f:
    for line in f:
        CHORD_INTERVAL_VECTOR_LIST.append(literal_eval(line))

# get names of all 66 classes
CLASS_LIST = []
with open('all_heptatonic_scale_classes.txt', 'r') as f:
    for line in f:
        CLASS_LIST.append(literal_eval(line))

# alternative names
ALTERED_SCALE_TYPE_OLD_TO_NEW = {
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
ALTERED_SCALE_TYPE_NEW_TO_OLD = {
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


''' ----------------------------------------------------------------------------------------- '''
''' *********************************** for `Chord` Class *********************************** '''
''' ----------------------------------------------------------------------------------------- '''


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
    '5': 'Lydian',
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
    '5': [0, 4],
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

# TODO: use calculation, not dict
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


''' ----------------------------------------------------------------------------------------- '''
''' ********************************** for `ChordEx` Class ********************************** '''
''' ----------------------------------------------------------------------------------------- '''


# for `ChordEx.get_name_ex` method
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
