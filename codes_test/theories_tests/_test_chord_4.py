from theories import *


def prints(c):
    # chord information
    c.set_printoptions(ns=0, show_register=False)
    print(f'chord: {c.get_name()}')
    print(str(c))
    # scale information
    for scale_name in c.get_scale(max_order=4, ns=2):
        scale = AlteredDiatonicScale(scale_name)
        scale.set_printoptions(show_register=False)
        print(f'{scale_name}: {str(scale)}')
    print()


# c = Chord('B 7(b9)')
# prints(c)
#
# c = Chord('C R.b3.5.b7')
# prints(c)
#
# c = Chord('D 7(#9)')
# prints(c)
#
# c = Chord('Fsus2/A')
# prints(c)
#
# c = Chord('Caug/F#')
# prints(c)

# prints(Chord('C R.b2.4.5.b6'))  # Miyakobushi Scale
# prints(Chord('C R.3.4.5.7'))  # Ryukyu Scale
# prints(Chord('C R.b3.4.5.b7'))  # Minor Pentatonic Scale

# prints(Chord('C R.3.7'))

prints(Chord('D R.3.5.6.9'))
prints(Chord('D R.b3.5.9.13'))
prints(Chord('E R.b2.4.5.b7'))
prints(Chord('C R.b3.4.b5.b7'))
