import numpy as np
import scipy.fftpack.basic as sfb
import scipy.signal as ss
from theories import *
SF = 44100
BD = 16


# ns: number of samples
# nt: number of seconds


def triple_to_frequency(triple):
    nn = triple_to_note_number(triple)
    # A4 concerto pitch == nn57 == 440Hz
    return 440*(T**(nn-57))


def triple_to_wav_mono(wavetable, triple, nt, amp):
    """ generate a ndarray from `triple` given lasting time `nt` (>=0.0s) and amplitude `amp` (0.0-1.0) """
    # consts
    wt_length = len(wavetable)
    freq = triple_to_frequency(triple)
    ns = int(SF*nt)
    # linear interpolation
    step_size = wt_length * freq / SF
    poses = [step_size*k % wt_length for k in range(ns)]
    xs_left = [int(pos) for pos in poses]
    xs_right = [(x+1) % wt_length for x in xs_left]
    deltas_left = np.array(poses) - np.array(xs_left)
    deltas_right = np.array(xs_right) - np.array(poses)
    values_left = wavetable[xs_left]
    values_right = wavetable[xs_right]
    values = values_left*deltas_right + values_right*deltas_left

    return amp * values


def triples_to_wav_mono(wavetable, triples, nt, amp):
    wavs = [triple_to_wav_mono(wavetable, triple, nt, amp) for triple in triples]
    return np.sum(wavs, axis=0)


def add_vibrato(wav, f, amp_min=0.5, amp_max=1.0):
    ns = len(wav)/SF
    t = np.linspace(0, ns, len(wav))
    y = np.sin(2*np.pi*f*t)/2*(amp_max-amp_min) + (amp_min+amp_max)/2
    return y * wav


def add_reverb_m2s(wav, ir, decay=0.0):
    ir_new = ir#np.zeros_like(ir)
    #ir_new[0] = np.exp(-decay*np.arange(ir.shape[1])) * ir[0]
    #ir_new[1] = np.exp(-decay*np.arange(ir.shape[1])) * ir[1]
    print(ir)
    return np.stack([ss.fftconvolve(wav, ir_new[:, 0]), ss.fftconvolve(wav, ir_new[:, 1])], axis=0)
