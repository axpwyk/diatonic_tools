import os; os.chdir('../..')
from theories import *


def prints(ads):
    print('notes: ', ads)
    print('name: ', ads.get_name())
    print('nnabs_list: ', ads.get_nnabs_list())
    print('named_nnrel_list: ', ads.get_named_nnrel_list())
    print('nnrel_list: ', ads.get_nnrel_list())
    print('accidental_list: ', ads.get_accidental_list())
    print('register_list: ', ads.get_register_list())
    print('intervals_seq: ', ads.get_intervals_seq())
    print('intervals_cum: ', ads.get_intervals_cum())
    print('1st chord: ', ads.get_chord(0, M))
    print('4th chord: ', ads.get_chord(3, M))
    print('5th chord: ', ads.get_chord(4, M))
    print()


# ads = AlteredDiatonicScale('F Lydian(#5,#6)').set_printoptions(use_conventional_name=True)
# prints(ads)
#
# ads.set_scale_tonic_str('G')
# prints(ads)
#
# ads.set_scale_tonic_deg(1)
# prints(ads)
#
# ads.add_accidentals_for_all(1)
# prints(ads)
#
# ads.add_accidental(-2)
# prints(ads)

ads = AlteredDiatonicScale('F Lydian(b7)').set_printoptions(use_old_name=True)
print(ads.get_name())

for _ in range(6):
    ads.set_scale_tonic_deg(1)
    print(ads.get_name())
