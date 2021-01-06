import numpy as np
import scipy.signal as ss
from theories import *


wt_sine = np.sin(np.linspace(0, 2*np.pi, 65536))
wt_sawtooth = ss.sawtooth(np.linspace(0, 1, 65536), 1)


class AudioNote(Note):
    def __init__(self, note_name=f'{NAMED_STR_LIN[0]}0'):
        super().__init__(note_name=note_name)

        self._starting_tick = 0
        self._lasting_tick = 0
        self.xxx = 0

    def get_frequency(self):
        """
        (in [12, 7, 5] diatonic scale)
        A4 concerto pitch == nnabs57 == 440Hz
        A3 cubase pitch == nnabs45 == 440Hz

        :return: frequency of current note (float type)
        """
        return C3 * (T ** (int(self) - N * 3))


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


# def note_to_wav_mono(wavetable, note):
#     """ generate a ndarray from `note` given lasting time `tl` (>=0.0s) and amplitude `amp` (0.0-1.0) """
#     # consts
#     wt_length = len(wavetable)
#     freq = nn_to_frequency(note[2])
#     ns = int(SF*note[1])
#     # linear interpolation
#     step_size = wt_length * freq / SF
#     poses = [step_size*k % wt_length for k in range(ns)]
#     xs_left = [int(pos) for pos in poses]
#     xs_right = [(x+1) % wt_length for x in xs_left]
#     deltas_left = np.array(poses) - np.array(xs_left)
#     deltas_right = np.array(xs_right) - np.array(poses)
#     values_left = wavetable[xs_left]
#     values_right = wavetable[xs_right]
#     values = values_left*deltas_right + values_right*deltas_left
#
#     return note[3]/127.0 * values


# def sheet_to_wav_mono(wavetable, sheet):
#     total_time = max([note[0]+note[1] for note in sheet])
#     ns = int(total_time*SF)
#
#     values = np.zeros((ns, ))
#     for note in sheet:
#         # _tss: starting time in samples
#         _tss = int(note[0]*SF)
#         value = note_to_wav_mono(wavetable, note)
#         _ns = int(note[1]*SF)
#         print(_tss, _ns)
#         values[_tss:_tss+_ns] += value
#
#     return values


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
