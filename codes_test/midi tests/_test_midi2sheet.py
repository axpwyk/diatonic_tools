import mido
import sys
import midi

sys.stdout = open('log1.txt', 'w')

file = r'../../midi/test1.mid'
mid = mido.MidiFile(file)

for i, track in enumerate(mid.tracks):
    print(f'<HEAD OF TRACK {i}>')
    print(track)
    for msg in track:
        print(f'{i}:\t{msg}')
    print(f'<END OF TRACK {i}>\n')

sys.stdout.close()
sys.stdout = open('log2.txt', 'w')

sheet, _, _ =  midi.midi2sheet(file)
for i, msglist in enumerate(sheet):
    print(f'<HEAD OF TRACK {i}>')
    for msg in msglist:
        print(f'{i}:\t{msg}')
    print(f'<END OF TRACK {i}>\n')

sys.stdout.close()
