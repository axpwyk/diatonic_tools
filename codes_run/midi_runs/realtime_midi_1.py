import sys
sys.path.extend(['D:\\Codes\\__synced__\\diatonic_tools', 'D:\\Codes\\__synced__\\diatonic_tools\\exts', 'D:/Codes/__synced__/diatonic_tools'])

import os
import math, itertools
import mido
import pyaudio
from theories import *
from audio import WavetableOscillator

port = mido.open_input()
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=SF, frames_per_buffer=1024, output=True)

notes = []
notes_buffer = [Note('C')] * 3
while(1):
    for msg in port.iter_pending():
        os.system('cls')
        if msg.type == 'note_on':
            # 计算缓存区音符五度重心位置
            note_inf, note_sup = get_polar(notes_buffer, enharmonic=True)[0]
            average_gidx = int((note_inf.get_gidx() + note_sup.get_gidx()) / 2)
            note_key_center = Note().add_gidx(average_gidx - 1)
            # print(f'polar_notes: ({note_inf, note_sup}) | center: {note_key_center.get_enharmonic_note_by_key_center("C").get_name()}')

            # 按照缓存区音符的重心位置计算当前音符名称，并把当前音符加入列表与缓存区
            current_note = Note().from_nnabs(msg.note, key_center=note_key_center.get_enharmonic_note_by_key_center('C').get_name() if notes else 'C')
            notes.append(current_note)
            notes_buffer.append(current_note)
            notes_buffer.pop(0)

            # 按照音高整理音符列表，并计算和弦名称
            notes.sort(key=lambda note: note.get_nnabs())
            print(Chord().set_notes(body=notes).get_sorted_chord().get_name(), ' - ', f'[{", ".join([note.get_name() for note in notes])}]', '-', f'{[note.get_nnrel() for note in notes]}')

            # 播放音频
            wo = WavetableOscillator()
            env = np.ones([1024, ])
            env[:128] = env[:128] * np.linspace(0, 1, 128)
            env[-128:] = env[-128:] * np.linspace(1, 0, 128)
            for itv in [Interval('P1'), Interval('M3'), Interval('P5'), Interval('P8')]:
                wo.set_freq((Note().from_nnabs(msg.note) + itv).get_frequency())
                chunk = np.array([next(wo) for k in range(1024)]) * env
                stream.write(chunk.astype(np.float32).tobytes())


        elif msg.type == 'note_off':
            # 查找 note_off 事件对应音符，将其从列表中移除
            idx = [note.get_nnabs() for note in notes].index(msg.note)
            notes.pop(idx)

            # 计算剩余音符组成的和弦名称
            print(Chord().set_notes(body=notes).get_sorted_chord().get_name(), ' - ', f'[{", ".join([note.get_name() for note in notes])}]', '-', f'{[note.get_nnrel() for note in notes]}')

        else:
            continue

# p.terminate()
