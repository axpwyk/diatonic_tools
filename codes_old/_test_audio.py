from scipy.io.wavfile import read, write
from midi import *
from audio import *

# 设置波表
t = np.linspace(0, np.pi, 65536)
wt = np.clip(np.tan(t), -0.4, 0.4)
# wt = read(r'..\wavetables\machine_learning_square_01.wav')[1]
plt.plot(wt)
plt.title('wavetable')
plt.show()

# 合成 wav
sheet = midi_to_note_list(r'..\midi\magnet.mid')[2]
print(sheet)
sheet = [[ts-min([note[0] for note in sheet]), tl, nn, vel, ch] for [ts, tl, nn, vel, ch] in sheet]
print(sheet)
wav = sheet_to_wav_mono(wt, sheet)
# wav = add_vibrato(wav, 7, 0.0, 1.0)
wavr = add_reverb_m2s(wav, read(r'..\irs\MINI_CAVES_E001_M2S.wav')[1], decay=0.0)
wavr[:, :len(wav)] += 5*wav
print(wavr.shape)
print(wavr.min(), wavr.max())

# 导出 wav
write(r'..\output\test.wav', SF, wavr.T/wavr.max())
