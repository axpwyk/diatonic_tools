import mido

mid = mido.MidiFile('midi/cyberpunk.mid')

for msg in mid.tracks[21]:
    print(msg)
