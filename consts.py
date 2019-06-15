NOTES = ['C', '', 'D', '', 'E', 'F', '', 'G', '', 'A', '', 'B']

MODES = ['Lydian', 'Ionian', 'Mixolydian', 'Dorian', 'Aeolian', 'Phrygian', 'Locrian',
         'HMinor', 'MMinor', 'HMinor3', 'HMinor7']

# 用于从 triple 辨认和弦
CHORDS = {'44': 'aug',
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
          '432': '6'
          }

# 用于控制台为和弦着色
CHORD_TYPE_COLORS = {'M7': 'red',
                     'M7+5': 'magenta',
                     '7': 'white',
                     'mM7': 'cyan',
                     'm7': 'blue',
                     'm7-5': 'cyan',
                     'dim7': 'green'}

# 用于构造和弦对应的音阶
CHORD_TYPE_SCALES = {'aug': 'HMinor',
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
                     '6': 'Ionian'}

# 用于从音阶构造和弦
CHORD_TYPE_CLST = {'aug': [0, 2, 4],
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
                   '6': [0, 2, 4, 5]}

# 半音音阶 triples
CHROMATIC = [[0, 0, -1],
             [0, 1, -1],
             [2, 0, -1],
             [2, 1, -1],
             [4, 0, -1],
             [5, 0, -1],
             [5, 1, -1],
             [7, 0, -1],
             [7, 1, -1],
             [9, 0, -1],
             [11, -1, -1],
             [11, 0, -1]]
