# built-in libs
import time
import itertools

# 3rd-party libs
import scipy.signal as ss

# project libs
from theories import *


''' ----------------------------------------------------------------------------------------- '''
''' ************************************ audio generation *********************************** '''
''' ----------------------------------------------------------------------------------------- '''


WT_SINE = np.sin(np.linspace(0, 2 * np.pi, 65536))
WT_SQUARE =ss.square(np.linspace(0, 2 * np.pi, 65536))
WT_SAWTOOTH = ss.sawtooth(np.linspace(0, 2 * np.pi, 65536), 1)
WT_TRIANGLE = ss.sawtooth(np.linspace(0, 2 * np.pi, 65536), 0.5)


def wave_generator(nnabs, wt=WT_TRIANGLE):
    wt_length = len(wt)
    freq = Note().from_nnabs(nnabs).get_frequency()
    tl = 2048 / SF
    amp = 0.75

    k = -1

    while(1):
        k = k + 1
        # linear interpolation
        n_samples = int(SF * tl)
        step_size = wt_length * freq / SF

        poses = step_size * np.arange(k * n_samples, (k + 1) * n_samples) % wt_length

        xs_left = np.floor(poses).astype('int')
        xs_right = (xs_left + 1) % wt_length
        deltas_left = poses - xs_left
        deltas_right = xs_right - poses
        values_left = wt[xs_left]
        values_right = wt[xs_right]

        values = values_left * deltas_right + values_right * deltas_left

        yield amp * values


class WavetableOscillator(object):
    def __init__(self, init_freq=440, init_amp=0.75, init_phase=0):
        self._freq = init_freq
        self._amp = init_amp
        self._phase = init_phase

        self._step = 0
        self._wt = WT_SAWTOOTH
        self._wt_length = len(self._wt)
        self._refresh_step_length()

    def __iter__(self):
        return self

    def __next__(self):
        pos = self._step * self._step_length + self._phase * self._wt_length / 360
        # pos_l = int(pos)
        # pos_r = pos_l + 1
        # intp_l = self._wt[pos_l % self._wt_length] * (pos_r - pos)
        # intp_r = self._wt[pos_r % self._wt_length] * (pos - pos_l)

        self._step = self._step + 1

        return self._wt[int(pos) % self._wt_length]  # self._amp * (intp_l + intp_r)

    def _refresh_step_length(self):
        self._step_length = self._wt_length * self._freq / SF

    def set_freq(self, freq):
        self._freq = float(freq)
        self._refresh_step_length()
        return self

    def set_amp(self, amp):
        self._amp = float(amp)
        return self

    def set_phase(self, phase):
        self._phase = float(phase)
        return self


class ADSREnvelope(object):
    """ modified from https://python.plainenglish.io/build-your-own-python-synthesizer-part-2-66396f6dad81"""
    def __init__(self, attack_time=0.05, decay_time=0.05, sustain_level=0.5, release_time=0.1):
        self._attack_time = attack_time
        self._decay_time = decay_time
        self._sustain_level = sustain_level
        self._release_time = release_time

        self._val = 0
        self._status = 1
        self._stepper = self._get_ads_stepper()

        self._scale = 1

    def _get_ads_stepper(self):
        steppers = []
        if self._attack_time > 0:
            steppers.append(itertools.count(start=self._val, step=(1 - self._val) / (self._attack_time * SF)))
        if self._decay_time > 0:
            steppers.append(itertools.count(start=1, step=-(1 - self._sustain_level) / (self._decay_time * SF)))
        while(1):
            l = len(steppers)
            if l > 0:
                val = next(steppers[0])
                if l == 2 and val > 1:
                    steppers.pop(0)
                    val = next(steppers[0])
                elif l == 1 and val < self._sustain_level:
                    steppers.pop(0)
                    val = self._sustain_level
            else:
                val = self._sustain_level
            yield val

    def _get_r_stepper(self):
        steppers = []
        if self._release_time > 0:
            release_step = - self._val / (self._release_time * SF)
            steppers.append(itertools.count(self._val, step=release_step))
        else:
            steppers.append(itertools.count(0, step=0))
        steppers.append(itertools.count(0, step=0))

        while(1):
            val = next(steppers[0])
            if val > 0:
                yield val
            else:
                yield next(steppers[1])

    def __iter__(self):
        return self

    def __next__(self):
        self._val = next(self._stepper)
        return self._val * self._scale

    def get_status(self):
        return self._status

    def set_status(self, status):
        if status == 1:
            self._status = 1
            self._stepper = self._get_ads_stepper()
            return self
        elif status == 0:
            self._status = 0
            self._stepper = self._get_r_stepper()
            return self
        else:
            return self

    def set_scale(self, scale):
        self._scale = scale
        return self


class PolySynthMono(object):
    def __init__(self, unison=3, detune_range=3, unison_mix=0.2):
        self._notes = {}
        self._oscs = {}
        self._adsrs = {}
        self._times = {}
        self._locks = {}

        # for unison
        self._unison = unison
        self._detune_range = detune_range
        self._unison_mix = unison_mix

        # for adsr
        self._adsr_values = [0.005, 0.05, 0.2, 0.2]

    def note_on(self, nnabs):
        self._notes[nnabs] = Note().from_nnabs(nnabs)

        freq = self._notes[nnabs].get_frequency()
        freqs = np.linspace(freq - self._detune_range, freq + self._detune_range, self._unison)
        self._oscs[nnabs] = [WavetableOscillator().set_freq(f) for f in freqs]

        scales = [1 - self._unison_mix if self._unison - 2 <= 2 * i <= self._unison else self._unison_mix for i in range(self._unison)]
        self._adsrs[nnabs] = [ADSREnvelope(*self._adsr_values).set_status(1).set_scale(scale) for scale in scales]

        self._times[nnabs] = time.time()
        self._locks[nnabs] = True

        return self

    def note_off(self, nnabs):
        if nnabs in self._notes.keys():
            for i in range(len(self._adsrs[nnabs])):
                self._adsrs[nnabs][i].set_status(0)
            self._times[nnabs] = time.time()
            self._locks[nnabs] = False

    def countdown_step(self):
        del_list = []
        for k, v in self._locks.items():
            if not v and time.time() - self._times[k] > self._adsr_values[-1]:
                del_list.append(k)

        for k in del_list:
            self._notes.pop(k)
            self._oscs.pop(k)
            self._adsrs.pop(k)
            self._times.pop(k)
            self._locks.pop(k)

        return self

    def get_samples(self):
        chunk_size = 64
        samples = np.zeros((chunk_size, ))

        if self._oscs:
            samples_tmp = []
            for k, v in self._oscs.items():
                samples_osc = [np.array([next(vi) for _ in range(chunk_size)]) for vi in v]
                samples_adsr = [np.array([next(vi) for _ in range(chunk_size)]) for vi in self._adsrs[k]]
                samples_tmp.append(np.sum([o * a for o, a in zip(samples_osc, samples_adsr)], axis=0))
            samples = np.sum(samples_tmp, axis=0)
            samples = samples / 8

        return samples


''' ----------------------------------------------------------------------------------------- '''
''' ********************************** audio visualization ********************************** '''
''' ----------------------------------------------------------------------------------------- '''


def draw_spectrum_mono(wav, sampling_frequency, window_samples=1024, time_step=0.002):
    N = np.max(np.shape(wav))
    N_secs = N/sampling_frequency
    stride = int(time_step*sampling_frequency)
    starting_poses = [k*stride for k in range(N//stride)]

    # t = np.linspace(-0.1, 0.1, window_samples)
    # delta = 0.01
    # gaussian_mask = 1/np.sqrt(2*np.pi*delta**2)*np.exp(-1/(2*delta**2)*np.power(t, 2))

    t = np.arange(window_samples)
    a0 = 0.35875
    a1 = 0.48829
    a2 = 0.14128
    a3 = 0.01168
    bh_mask = a0-a1*np.cos(2*np.pi*t/window_samples)+a2*np.cos(4*np.pi*t/window_samples)-a3*np.cos(6*np.pi*t/window_samples)

    pieces = np.array([bh_mask*wav[tick:tick+window_samples] for tick in starting_poses if tick+window_samples<N])
    # pieces_fft = [np.abs(np.fft.fftshift(np.fft.fft(piece))) for piece in pieces]
    pieces_fft = np.abs(np.fft.fftshift(np.fft.fft(pieces), axes=1))
    spectrum = np.transpose(np.array(pieces_fft))[window_samples//2:, :]

    return spectrum


''' ----------------------------------------------------------------------------------------- '''
''' *************************************** deprecated ************************************** '''
''' ----------------------------------------------------------------------------------------- '''


def note_to_wav_mono(wt, audio_note, tl, amp):
    """
        generate a ndarray from `audio_note`
        `wt`:   wavetable, 1 period
        `tl`:   lasting time, positive float, seconds
        `amp`:  amplitude, float in (0.0, 1.0)
    """
    # constants
    wt_length = len(wt)
    freq = audio_note.get_frequency()

    # linear interpolation
    n_samples = int(SF * tl)
    step_size = wt_length * freq / SF
    poses = [step_size*k % wt_length for k in range(n_samples)]

    xs_left = [int(pos) for pos in poses]
    xs_right = [(x+1) % wt_length for x in xs_left]
    deltas_left = np.array(poses) - np.array(xs_left)
    deltas_right = np.array(xs_right) - np.array(poses)
    values_left = wt[xs_left]
    values_right = wt[xs_right]

    values = values_left*deltas_right + values_right*deltas_left

    # envelope
    eps = 0.01
    values[:int(SF*eps)] = values[:int(SF*eps)] * np.linspace(0, 1, int(SF*eps))
    values[-int(SF*eps):] = values[-int(SF*eps):] * np.linspace(1, 0, int(SF*eps))

    return amp * values


def notes_to_wav_mono(wt, notes, tl, amp):
    wavs = [note_to_wav_mono(wt, note, tl, amp) for note in notes]
    return np.average(wavs, axis=0)


def add_vibrato(wav, f, amp_min=0.5, amp_max=1.0):
    ns = len(wav)/SF
    t = np.linspace(0, ns, len(wav))
    y = np.sin(2*np.pi*f*t)/2*(amp_max-amp_min) + (amp_min+amp_max)/2
    return y * wav


def add_reverb_m2s(wav, ir, decay=0.0):
    ir_new = ir#np.zeros_like(ir)
    #ir_new[0] = np.exp(-decay*np.arange(ir.shape[1])) * ir[0]
    #ir_new[1] = np.exp(-decay*np.arange(ir.shape[1])) * ir[1]
    return np.stack([ss.fftconvolve(wav, ir_new[:, 0]), ss.fftconvolve(wav, ir_new[:, 1])], axis=0)
