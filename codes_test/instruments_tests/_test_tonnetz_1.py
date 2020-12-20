import os; os.chdir('../..')
from instruments import *

tnz = Tonnetz(Chord('Em7(b11)'), enharmonic=True, title='Em7(b11)', center_note=Note('D'))
tnz.plot()
