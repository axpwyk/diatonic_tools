from theories import *

tendencies_all = {
    'b2': [-1, 2],
    'b6': [-1],
    'b3': [0],
    'b7': [+2],
    '4': [-2, -1, +2],
    '1': [0],
    '5': [0],
    '2': [-2, +1, +2],
    '6': [-2],
    '3': [0],
    '7': [+1],
    '#4': [-2, +1]
}
tendencies = [tendencies_all.get(k)[t] for k, t in zip(tendencies_all.keys(), [0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0])]
tendencies_from_key_center = tendencies[5:] + tendencies[:5]


def chord_tendency_list(key_center, chord):
    tendency_list = []
    for note in chord:
        offset = (note.get_span() - key_center.get_span()) % 12
        tendency_list.append(tendencies_from_key_center[offset])
    return tendency_list


def chord_tendency_value(key_center, chord):
    tl = chord_tendency_list(key_center, chord)
    return sum([1/abs(k) if abs(k)!=0 else 0 for k in tl])


def min_tendency_key_center(chord):
    tvs = []
    offset = -5
    for kc in [Note().add_gidx(i) for i in range(offset, offset + 12)]:
        tvs.append(chord_tendency_value(kc, chord))
    return Note().add_gidx(tvs.index(min(tvs)) + offset)


def random_major_chord(key_center):
    key_name = key_center.get_name(show_register=False)
    return DiatonicScale(f'{key_name} Ionian').get_chord(np.random.randint(0, 7), 7)


def max_tendency_major_chord(key_center):
    key_name = key_center.get_name(show_register=False)
    chds = [DiatonicScale(f'{key_name} Ionian').get_chord(i, 7) for i in range(7)]
    tvs = [chord_tendency_value(key_center, chd) for chd in chds]
    idx = tvs.index(max(tvs))
    return chds[idx]


chds = [DiatonicScale('C Ionian').get_chord(0, 7)]
kcs = [Note('C')]
for _ in range(100):
    prev_chord = chds[-1]
    next_kc = min_tendency_key_center(prev_chord)
    next_chord = random_major_chord(next_kc)
    chds.append(next_chord)
    kcs.append(next_kc)

chds = [Chord().set_notes(body=chd[:4], tension=chd[4:]) for chd in chds]
print(chds)
print(kcs)
