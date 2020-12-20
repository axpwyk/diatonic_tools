import os; os.chdir('../..')
from audio import *
from scipy.io.wavfile import write

scale_name = 'C4 C-mode'
ds = DiatonicScale(scale_name)

wavs = []
for _ in range(20):
    wavs.extend([note_to_wav_mono(wt_sine, note, 0.1, 0.78) for note in ds.get_notes() + [ds[0].add_group(1)]])
    ds.add_accidental(1)
wav = np.concatenate(wavs)

# write(f'12-TET_5-tone_diatonic_scale_{scale_name.replace(" ", "_")}.wav', SF, wav)
write(f'12-TET_5-tone_diatonic_scales.wav', SF, wav)
