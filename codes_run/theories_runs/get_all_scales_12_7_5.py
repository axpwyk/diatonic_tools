from theories import *
from itertools import combinations_with_replacement

accidentals = [''] + [f'#{k}' for k in range(1, 8)] + [f'b{k}' for k in range(1, 8)]

lydians = ['F Lydian']
for acc in combinations_with_replacement(accidentals, 8):
    cur_altered_notes = f"({', '.join([s for s in acc if s != ''])})"
    cur_scale_name = f'F Lydian{cur_altered_notes}'
    cur_ads = AlteredDiatonicScale(cur_scale_name).set_printoptions(ns=0)

    if not cur_ads.if_well_formed():
        continue

    distances = [cur_ads.distance_0(AlteredDiatonicScale(other_scale)) for other_scale in lydians]
    if 0 in distances:
        continue
    else:
        lydians.append(cur_scale_name)

print(lydians)
print(len(lydians))
