from math import log
import matplotlib.pyplot as plt
from theories import Note


KEY_CENTER = 'C'
NOTES = [Note(KEY_CENTER).add_generator(k) for k in range(-5, 7)]
NOTES.sort(key=lambda x: x.get_nnabs() % 12)
NOTE_NAMES = [note.get_name(show_register=False) for note in NOTES]


def get_hs(bass_x, length=16):
    num = int(length / bass_x)
    xs = [bass_x * k for k in range(1, num+1)]
    freqs = [130.8127826502993 * x for x in xs]  # frequency of C3 = 130.8127826502993
    hts = [12 * log(x) / log(2) for x in xs]  # half tones in 12-TET
    hts_round = [round(ht) for ht in hts]
    cents = [ht / 12 * 1200 for ht in hts]
    cents_round = [ht / 12 * 1200 for ht in hts_round]
    cents_delta = [ht1 - ht2 for ht1, ht2 in zip(cents, cents_round)]
    note_names_round = [f'{NOTE_NAMES[ht%12]}{ht//12+3}' for ht in hts_round]
    return num, xs, freqs, hts, hts_round, cents, cents_round, cents_delta, note_names_round


colors = ['indianred', 'darkorange', 'gold', 'mediumseagreen', 'dodgerblue', 'royalblue', 'blueviolet']
length = 23
bass_xs = [pow(1.5, k) for k in range(7)]

for i, bass_x in enumerate(bass_xs):
    num, xs, freqs, hts, hts_round, cents, cents_round, cents_delta, note_names_round = get_hs(bass_x=bass_x, length=length)
    y = -0.5 * i
    # print(xs, '\n', freqs, '\n', hts, '\n', hts_round, '\n', cents, '\n', cents_round, '\n', cents_delta, '\n', note_names_round)
    plt.plot(xs, [y] * num, ':k', zorder=0)
    circs = [plt.Circle((x, y), 0.1, edgecolor='black', facecolor=colors[i % len(colors)], zorder=1) for x in xs]
    _ = [plt.gca().add_patch(circ) for circ in circs]
    _ = [plt.annotate(f'{nnr}(+{c:.0f})' if c > 0 else f'{nnr}({c:.0f})', (x + 0.1, y + 0.1), ha='left', va='center') for x, c, nnr in zip(xs, cents_delta, note_names_round)]
    _ = [plt.annotate(f'{freq:.2f} Hz', (x + 0.1, y - 0.1), ha='left', va='center') for x, freq in zip(xs, freqs)]

plt.gca().set_xlim(0.5, length + 1.5)
plt.gca().set_ylim(-(len(bass_xs)) * 0.5, 0.5)
plt.gca().set_aspect('equal')
plt.show()
