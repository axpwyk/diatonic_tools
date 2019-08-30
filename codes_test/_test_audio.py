import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from audio import *

# 设置波表
t = np.linspace(0, np.pi, 65536)
wt = np.clip(np.tan(t), -1, 1)
# wt = read(r'..\wavetables\machine_learning_square_01.wav')[1]
plt.plot(wt)
plt.title('wavetable')
plt.show()

# 合成 wav
random_notes = np.random.randint(0, 12, (256, ))
random_groups = np.random.randint(3, 5, (256, ))
random_notes[random_notes==1] = 0
random_notes[random_notes==3] = 2
random_notes[random_notes==6] = 7
random_notes[random_notes==8] = 9
random_notes[random_notes==10] = 9
triples = [[random_notes[i], 0, random_groups[i]] for i in range(len(random_notes))]
wavs = [triple_to_wav_mono(wt, triples[i], 0.25, 0.8) for i in range(128)]
wav = np.concatenate(wavs)
wav = add_vibrato(wav, 7, 0.0, 1.0)
wavr = add_reverb_m2s(wav, read(r'..\irs\MINI_CAVES_E001_M2S.wav')[1], decay=0.0)
wavr[:, :len(wav)] += 5*wav
print(wavr.shape)

# 导出 wav
write(r'..\output\test.wav', SF, wavr.T/wavr.max())
