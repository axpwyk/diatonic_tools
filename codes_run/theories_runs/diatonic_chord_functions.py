from theories import *

for mode in SCALE_TYPE_NS0_TO_NS2[NGS].keys():
    ads = AlteredDiatonicScale(f'C {mode}')
    chords_c, chords_t, chords_r = get_sorted_chords(ads)
    print(f'C {mode}', '\t', ads, '\t', '\t'.join([ch.get_name() for ch in chords_c]), '\t|\t', '\t'.join([ch.get_name() for ch in chords_t]), '\t|\t', '\t'.join([ch.get_name() for ch in chords_r]))

ads = AlteredDiatonicScale(f'C Aeolian(#7)')
chords_c, chords_t, chords_r = get_sorted_chords(ads)
print(f'{ads.get_name()[0]}', '\t', ads, '\t', '\t'.join([ch.get_name() for ch in chords_c]), '\t|\t', '\t'.join([ch.get_name() for ch in chords_t]), '\t|\t', '\t'.join([ch.get_name() for ch in chords_r]))

ads = AlteredDiatonicScale(f'C Ionian(b6)')
chords_c, chords_t, chords_r = get_sorted_chords(ads)
print(f'{ads.get_name()[0]}', '\t', ads, '\t', '\t'.join([ch.get_name() for ch in chords_c]), '\t|\t', '\t'.join([ch.get_name() for ch in chords_t]), '\t|\t', '\t'.join([ch.get_name() for ch in chords_r]))

ads = AlteredDiatonicScale(f'C Lydian(b7)')
chords_c, chords_t, chords_r = get_sorted_chords(ads)
print(f'{ads.get_name()[0]}', '\t', ads, '\t', '\t'.join([ch.get_name() for ch in chords_c]), '\t|\t', '\t'.join([ch.get_name() for ch in chords_t]), '\t|\t', '\t'.join([ch.get_name() for ch in chords_r]))
