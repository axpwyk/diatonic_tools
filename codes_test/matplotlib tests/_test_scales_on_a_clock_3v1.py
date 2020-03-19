import matplotlib.pyplot as plt
import numpy as np
from colorsys import hls_to_rgb
from theories import *


''' matplotlib settings '''


DPI = 150
FONTSIZE = DPI // 8
# assign a style
plt.style.use('seaborn-pastel')
# assign a math font
plt.rc('mathtext', **{'fontset': 'cm'})
plt.rc('text', **{'usetex': False})
# assign a chinese font
plt.rc('font', **{'sans-serif': 'Consolas-with-Yahei'})
plt.rc('axes', **{'unicode_minus': False})


''' consts '''


r = 5
omega = np.cos(np.pi/6) - 1j*np.sin(np.pi/6)
offset = (-omega)**3
colors = [hls_to_rgb(h, 0.5, 0.75) for h in np.linspace(0, 1.0, 7, endpoint=False)]
texts = ['[0]C', r'[1]C$\sharp$/D$\flat$', '[2]D', r'[3]D$\sharp$/E$\flat$',
         '[4]E', '[5]F', r'[6]F$\sharp$/G$\flat$', '[7]G',
         r'[8]G$\sharp$/A$\flat$', '[9]A', r'[10]A$\sharp$/B$\flat$', '[11]B']
text_positions = [(1.4*r*np.real(omega**k*offset), 1.4*r*np.imag(omega**k*offset)) for k in range(12)]


''' new figure '''


fig, axss = plt.subplots(2, 2)
fig.set_figwidth(8); fig.set_figheight(8)
fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.0, hspace=0.0)
for axs in axss:
    for ax in axs:
        ax.margins(0.0)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal')
        ax.set_xlim(-1.8*r, 1.8*r)
        ax.set_ylim(-1.8*r, 1.8*r)


''' define draw function '''


def draw(ax, scale, title):
    ks = [x%12 for x in abs(scale)]
    cs = ['gray']*12
    for i, k in enumerate(ks):
        cs[k] = colors[i]

    circ = plt.Circle((0, 0), r, fc='none', ec='black', lw=2.0)
    hands = [plt.Line2D((0, 0.8*r*np.real(omega**k*offset)), (0, 0.8*r*np.imag(omega**k*offset)),
                    lw=1, c='gray') for k in range(12)]
    ticks = [plt.Line2D((0.95*r*np.real(omega**k*offset), r*np.real(omega**k*offset)), (0.95*r*np.imag(omega**k*offset), r*np.imag(omega**k*offset)),
                    lw=1, c='black') for k in range(12)]
    for i, c in enumerate(cs):
        hands[i].set_color(c)

    ax.add_patch(circ)
    _ = [ax.add_line(hand) for hand in [hands[k] for k in ks]]
    _ = [ax.add_line(tick) for tick in [ticks[k] for k in range(12)]]
    _ = [ax.annotate(texts[k], text_positions[k], va='center', ha='center', bbox=dict(facecolor=cs[k], alpha=0.2, edgecolor=cs[k])) for k in range(12)]
    ks2 = abs(scale) + [12+k for k in abs(scale)]
    _ = [ax.annotate(f'{(k2-k1)*30}°', (np.real(0.65*r*omega**(k1+(k2-k1)/2)*offset), np.imag(0.65*r*omega**(k1+(k2-k1)/2)*offset)), ha='center', va='center') for k1, k2 in zip(ks2[:7], ks2[1:8])]
    ax.text(0.05, 0.95, title, transform=ax.transAxes, ha='left', va='top', bbox=dict(facecolor='none', edgecolor='black'))


''' draw clocks '''


# C Ionian
scale = DiatonicScale('C Ionian')
draw(axss[0, 0], scale, 'C Ionian')

# Eb Ionian
scale = DiatonicScale('Eb Ionian')
draw(axss[0, 1], scale, 'E$\\flat$ Ionian')

# C Lydian
scale = DiatonicScale('G Ionian')
draw(axss[1, 0], scale, 'C Lydian')

# C Harmonic Minor
scale = AlteredDiatonicScale('C Harmonic Major')
draw(axss[1, 1], scale, 'C Harmonic Major')

plt.savefig('scales_3vs1.svg', bbox_inches='tight', pad_inches=0.0)
