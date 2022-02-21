import os; os.chdir('../..')
from audio import *
from scipy.io.wavfile import write

scale_name = 'α2 α-mode'
ds = DiatonicScale(scale_name)

wavs = [note_to_wav_mono(WT_SINE, note, 1.0, 0.78) for note in ds.get_notes() + [ds[0].add_group(1)]]
wav = np.concatenate(wavs)

write(f'41-TET_12-tone_diatonic_scale_{scale_name.replace(" ", "_")}.wav', SF, wav)
