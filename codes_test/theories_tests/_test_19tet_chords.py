import sys
sys.path.extend(['D:\\Codes\\__synced__\\diatonic_tools', 'D:\\Codes\\__synced__\\diatonic_tools\\exts', 'D:/Codes/__synced__/diatonic_tools'])

import time
import pyaudio
from theories import *
from audio import WavetableOscillator

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=SF, frames_per_buffer=1024, output=True)

chords = [
    Chord().set_notes(body=[Note('A3'), Note('D4'), Note('E4'), Note('B4')]),
    [],
    Chord().set_notes(body=[Note('F3'), Note('C4'), Note('E4'), Note('A4')]),
    [],
    Chord().set_notes(body=[Note('E3'), Note('C4'), Note('D4'), Note('G4')]),
    [],
    Chord().set_notes(body=[Note('D3'), Note('A3'), Note('E4'), Note('F4')]),
    Chord().set_notes(body=[Note('C3'), Note('G3'), Note('B3'), Note('E4')]),
    Chord().set_notes(body=[Note('B2'), Note('F3'), Note('G#3'), Note('D4')]),
    [],
    Chord().set_notes(body=[Note('C3'), Note('G3'), Note('A3'), Note('E4')]),
    [],
    Chord().set_notes(body=[Note('B2'), Note('F3'), Note('Ab3'), Note('D4')]),
    [],
    Chord().set_notes(body=[Note('C3'), Note('G3'), Note('A3'), Note('E4')]),
    [],
    Chord().set_notes(body=[Note('D3'), Note('F#3'), Note('A3'), Note('D4')]),
    [],
    Chord().set_notes(body=[Note('E3'), Note('G#3'), Note('B3'), Note('E4')]),
    []
]


def show_chord(chord):
    notes = []
    for note in chord:
        notes.append(note)

        # 按照音高整理音符列表，并计算和弦名称
        notes.sort(key=lambda note: note.get_nnabs())
        print(Chord().set_notes(body=notes).get_sorted_chord().get_name(), ' - ',
              f'[{", ".join([note.get_name() for note in notes])}]', '-', f'{[note.get_nnrel() for note in notes]}')

        # 播放音频
        wos = [WavetableOscillator().set_freq(note.get_frequency()) for note in notes]
        chunk_size = 22050
        env = np.ones([chunk_size, ])
        env[:256] = env[:256] * np.linspace(0, 1, 256)
        env[-4096:] = env[-4096:] * np.linspace(1, 0, 4096)

        chunk = sum([np.array([next(wo) for _ in range(chunk_size)]) for wo in wos]) / len(notes) * env
        stream.write(chunk.astype(np.float32).tobytes())


for chord in chords:
    show_chord(chord)
    if len(chord) == 0:
        time.sleep(2)
    print()

p.terminate()
