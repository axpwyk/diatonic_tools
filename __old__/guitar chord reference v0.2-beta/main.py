from instruments import *
from time import strftime
from pathlib import Path
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--low", default=-1, type=int)
parser.add_argument("--high", default=24, type=int)
parser.add_argument("--radius_offset", default=-1, type=int)
args = parser.parse_args()


if __name__ == '__main__':
    # using chord list
    chord_names = np.loadtxt('chords.txt', np.chararray, comments=None, ndmin=1)
    print(chord_names)
    chords = [Chord(chord_name) for chord_name in chord_names]

    # show chords
    print(chords)

    # Guitar class
    g = Guitar()
    N = len(chords)
    step = 0.4
    offsets = np.arange(-(N/2-1/2)*step, (N/2-1/2)*step+step, step)
    for i in range(N):
        g.set_notes(chords[i])
        g.draw_guitar(height=6, hue=0.01+0.075*i, low=args.low, high=args.high, finger_offset=offsets[i], radius_offset=args.radius_offset)

    # export
    chords_name_export = ''.join([chd+'_' for chd in chord_names[:-1]]+[chord_names[-1]])
    filename = f'{strftime("%Y%m%d_%H%M%S")}_{chords_name_export}.svg'
    filename = filename.replace('/', r'on')
    print(filename)
    plt.savefig(Path(r'./output')/filename)
    plt.close()
