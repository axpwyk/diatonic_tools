import os; os.chdir('../..')
from instruments import *

tnz = Tonnetz([], enharmonic=True, title='Tonnetz', center_note=Note('C'), n_x=11, n_y=11)
tnz.plot()
plt.savefig('outputs/tonnetz_11_11.svg', bbox_inches='tight')
