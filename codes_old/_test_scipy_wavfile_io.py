from scipy.io.wavfile import write
import numpy as np

s = np.power(2, 1/12)
t = np.linspace(0, 1, 44100)
beep1 = np.sin(2*np.pi*440*t)*np.exp(-t)
beep2 = np.sin(2*np.pi*440*s**4*t)*np.exp(-t)
beep3 = np.sin(2*np.pi*440*s**7*t)*np.exp(-t)
beep4 = np.sin(2*np.pi*440*s**11*t)*np.exp(-t)

write('beep.wav', 44100, np.average([beep1, beep2, beep3, beep4], axis=0))
