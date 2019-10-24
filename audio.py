import numpy as np
import scipy.fftpack.basic as sfb
import scipy.signal as ss
from theories import *
SF = 44100
BD = 16


# ns: number of samples


def triple_to_frequency(triple):
    nn = triple_to_note_number(triple)
    # A4 concerto pitch == nn57 == 440Hz
    return 440*(T**(nn-69))


def nn_to_frequency(nn):
    return 440*(T**(nn-69))


def triple_to_wav_mono(wavetable, triple, tl, amp):
    """ generate a ndarray from `triple` given lasting time `tl` (>=0.0s) and amplitude `amp` (0.0-1.0) """
    # consts
    wt_length = len(wavetable)
    freq = triple_to_frequency(triple)
    ns = int(SF*tl)
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


def triples_to_wav_mono(wavetable, triples, tl, amp):
    wavs = [triple_to_wav_mono(wavetable, triple, tl, amp) for triple in triples]
    return np.sum(wavs, axis=0)


def note_to_wav_mono(wavetable, note):
    """ generate a ndarray from `note` given lasting time `tl` (>=0.0s) and amplitude `amp` (0.0-1.0) """
    # consts
    wt_length = len(wavetable)
    freq = nn_to_frequency(note[2])
    ns = int(SF*note[1])
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

    return note[3]/127.0 * values


def sheet_to_wav_mono(wavetable, sheet):
    total_time = max([note[0]+note[1] for note in sheet])
    ns = int(total_time*SF)

    values = np.zeros((ns, ))
    for note in sheet:
        # _tss: starting time in samples
        _tss = int(note[0]*SF)
        value = note_to_wav_mono(wavetable, note)
        _ns = int(note[1]*SF)
        print(_tss, _ns)
        values[_tss:_tss+_ns] += value

    return values


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


def draw_spectrum_mono(wav, sampling_frequency, window_samples):
    N = np.max(np.shape(wav))
    N_secs = N/sampling_frequency
    stride = 16
    starting_poses = [k*stride for k in range(N//stride)]
    t = np.linspace(-1, 1, window_samples)
    delta = 0.02
    gaussian_mask = 1/np.sqrt(delta)*np.exp(-np.pi/delta*np.power(t, 2))
    pieces = [gaussian_mask*wav[tick:tick+window_samples] for tick in starting_poses if tick+window_samples<N]
    pieces_fft = [np.abs(np.fft.fftshift(np.fft.fft(piece))) for piece in pieces]
    return np.transpose(np.array(pieces_fft))[:window_samples//2, :]
