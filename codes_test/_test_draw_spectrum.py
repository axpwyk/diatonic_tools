from scipy.io.wavfile import read
from audio import draw_spectrum_mono
from utils_im import *
import pathlib


def nl(x):
    y = 1/2*np.sin(np.pi*(x-1/2))+1/2
    return y


path = pathlib.Path(r'../wavs/test.wav')
print(path)

sf, wav = read(path)
wav = wav / 32768
print(wav.min(), wav.max())

spectrum_L = draw_spectrum_mono(wav[44100*12:44100*16, 0], sf, 2048)
spectrum_L = 0.1*np.log(spectrum_L)
spectrum_L = (spectrum_L-spectrum_L.min())/(spectrum_L.max()-spectrum_L.min())
for _ in range(0):
    spectrum_L = nl(spectrum_L)

print(spectrum_L.shape)
print(spectrum_L.min(), spectrum_L.max())

plt_add_image_2d(spectrum_L, show=False)
#plt.yscale('log')
# plt.savefig('my_first_spectrum.png')
plt.show()
