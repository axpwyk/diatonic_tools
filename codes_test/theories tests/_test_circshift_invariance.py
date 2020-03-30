import numpy as np
import time


def is_isomophic(list_1, list_2):
    list_1_diff = np.diff(list_1, append=list_1[0])
    list_2_diff = np.diff(list_2, append=list_2[0])
    fft1 = np.fft.fft(list_1)
    fft11 = np.fft.fft(list_1_diff)
    fft2 = np.fft.fft(list_2)
    fft22 = np.fft.fft(list_2_diff)
    d1 = np.linalg.norm(np.abs(fft1)-np.abs(fft2))
    d2 = np.linalg.norm(np.abs(fft11)-np.abs(fft22))
    d = d1 + d2
    if d < 1e-5:
        return True
    else:
        return False


class Timer(object):
    def __init__(self):
        self._t = 0.0
        self._records = []

    def start(self):
        self._t = time.time()

    def record(self):
        self._records.append(time.time()-self._t)

    def reset(self):
        self._t = 0.0
        self._records = []

    def get(self):
        return self._records


timer = Timer()
timer.start()
a = [1,3,1,2,2,2,1]
b = [1,2,2,2,1,3,1]
print(is_isomophic(a, b))
timer.record()
print(timer.get())
