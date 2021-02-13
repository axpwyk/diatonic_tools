from theories import *
from itertools import product
import pandas as pd

df = pd.DataFrame(columns=['root_movement', 'type_prev', 'type_next', 'mode_type', 'scale_type', 'mode', 'order', 'class'])

movements = {scale_type: [] for scale_type in ALL_SCALE_TYPES['12.7.5']}

for i, scale_type in enumerate(ALL_SCALE_TYPES['12.7.5']):
    cur_ads = AlteredDiatonicScale(f'F {scale_type}')
    for mode, deg in product([0, 4, 1, 5, 2, 6, 3], range(1, 7)):
        deg = (mode + deg) % 7

        chord1 = Chord().set_notes(body=cur_ads.get_chord(root_degree=mode, n_notes=4))
        chord2 = Chord().set_notes(body=cur_ads.get_chord(root_degree=deg, n_notes=4))

        cp = ChordProgression(chord1, chord2)
        root_movement, type_prev, type_next = cp.get_movement()

        collection = {
            'root_movement': root_movement,
            'type_prev': type_prev,
            'type_next': type_next,
            'scale_type': scale_type,
            'mode_type': AlteredDiatonicScale(f'F {scale_type}').set_scale_tonic_deg(mode).get_name(type_only=True)[0],
            'mode': 'FGABCDE'[mode],
            'order': cur_ads.get_order(),
            'class': i
        }

        df = df.append(collection, ignore_index=True)

df.to_csv('../../all_7th_chord_progressions_12_7_5.csv', index=False)
