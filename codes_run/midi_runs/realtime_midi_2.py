import sys
sys.path.extend(['D:\\Codes\\__synced__\\diatonic_tools', 'D:\\Codes\\__synced__\\diatonic_tools\\exts', 'D:/Codes/__synced__/diatonic_tools'])

import mido
import pyaudio
from theories import *
from audio import PolySynthMono


def show_chord_name(notes, last_n_chr):
    print('\r', ''.join([' ' for _ in range(last_n_chr)]), end='\r', flush=True)
    if notes:
        # 计算缓存区音符五度重心位置
        note_inf, note_sup = get_polar(notes, enharmonic=True)[0]
        average_gidx = int((note_inf.get_gidx() + note_sup.get_gidx()) / 2)
        note_key_center = Note().add_gidx(average_gidx - 1)

        # 按照音高整理音符列表，并计算和弦名称

        for i in range(len(notes)):
            notes[i].get_enharmonic_note_by_key_center(note_key_center.get_name())
        notes.sort(key=lambda note: note.get_nnabs())
        p = ''.join([
            Chord().set_notes(body=notes).get_sorted_chord().get_name(),
            ' - ',
            f'[{", ".join([note.get_name() for note in notes])}]',
            ' - ',
            f'{[note.get_nnrel() for note in notes]}'
        ])
        print(p, end='', flush=True)
        return len(p)
    else:
        print('', end='', flush=True)
        return 0


port = mido.open_input()
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=SF, frames_per_buffer=64, output=True)

try:
    psm = PolySynthMono()
    chord_notes = []
    last_n_chr = 0
    while(1):
        # 处理 midi 输入数据
        for msg in port.iter_pending():
            if msg.type == 'note_on':
                psm.note_on(msg.note)
                chord_notes.append(Note().from_nnabs(msg.note))
                last_n_chr = show_chord_name(chord_notes, last_n_chr)
            elif msg.type == 'note_off':
                psm.note_off(msg.note)
                chord_notes.pop(chord_notes.index(msg.note))
                last_n_chr = show_chord_name(chord_notes, last_n_chr)
            else:
                continue

        # 倒计时，并删除未锁定且倒计时小于 0 的音符
        psm.countdown_step()

        # 从振荡器生成样本，写入音频流
        samples = psm.get_samples()
        samples = np.float32(samples).tobytes()
        stream.write(samples)

except KeyboardInterrupt as err:
    print('Stopping...')
    p.terminate()
