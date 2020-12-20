import os; os.chdir('../..')
from audio import *
from scipy.io.wavfile import write

scale_name = 'A A-mode'
ds = DiatonicScale(scale_name).add_accidental(-26)
print(ds)
for i in range(26):
    ds.add_accidental(1)
    print(ds)

# wavs = [note_to_wav_mono(wt_sine, note, 1.0, 0.78) for note in ds.get_notes() + [ds[0].add_oct()]]
# wav = np.concatenate(wavs)
#
# write(f'97-TET_26-tone_diatonic_scale_{scale_name.replace(" ", "_")}.wav', SF, wav)
