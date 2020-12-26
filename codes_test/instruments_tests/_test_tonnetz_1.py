import os; os.chdir('../..')
from instruments import *

tnz = Tonnetz(Chord('G7-5'), enharmonic=True, title='G7-5', center_note=Note('C'))
tnz.plot()
