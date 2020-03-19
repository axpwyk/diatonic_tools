import matplotlib.pyplot as plt
import numpy as np
import colorsys as cs
from theories import Chord
import re

plt.style.use('seaborn-pastel')
plt.rc('font', **{'sans-serif': 'Consolas-with-Yahei'})


def hex2oct(hex_string):
    search_obj = re.search(r'(?<=#)(?P<red>[\dabcdef]{2})(?P<green>[\dabcdef]{2})(?P<blue>[\dabcdef]{2})', hex_string)
    red = eval('0x'+search_obj['red'])
    green = eval('0x'+search_obj['green'])
    blue = eval('0x'+search_obj['blue'])
    return red/255, green/255, blue/255


def oct2hex(oct_list):
    red = oct_list[0] * 255
    green = oct_list[1] * 255
    blue = oct_list[2] * 255
    print(red, green, blue)
    digits = [str(k) for k in range(10)] + ['a', 'b', 'c', 'd', 'e', 'f']
    return '#'+f'{digits[int((red-red%16)//16)]}{digits[int(red%16)]}'+\
               f'{digits[int((green-green%16)//16)]}{digits[int(green%16)]}'+\
               f'{digits[int((blue-blue%16)//16)]}{digits[int(blue%16)]}'


def gradient1(t, color1, color2):
    c1 = hex2oct(color1)
    c2 = hex2oct(color2)
    return [[(1-s/(t-1))*c1[k]+s/(t-1)*c2[k] for k in range(3)] for s in range(t)]


def gradient2(t, color1, color2):
    c1 = color1
    c2 = color2
    return [[(1-s/(t-1))*c1[k]+s/(t-1)*c2[k] for k in range(3)] for s in range(t)]


h = np.linspace(0, 1, 12, endpoint=False)
chord_name = 'Ddim7'
hs = [abs(t)%12 for t in Chord(chord_name)[1:]]
save_name = ''
l1 = 0.5; l2 = 0.25
s1 = 0.95; s2 = 0.5

n_colors = len(hs)
n_gradients = 7

colors = np.zeros((n_colors, n_gradients, 3), 'float')
for i in range(n_colors):
    colors[i] = gradient2(n_gradients, cs.hls_to_rgb(h[hs[i]], l1, s1), cs.hls_to_rgb(h[hs[i]], l2, s2))


ax = plt.gca()
ax.margins(0.0)
ax.set_xticks([]); ax.set_yticks([])
ax.set_aspect('equal')

x_margins = 0.5; w = 3
y_margins = 1.5; h = 1
h_text = 1
ax.set_xlim(0, (x_margins+w)*n_gradients-x_margins)
ax.set_ylim(0-h_text, (y_margins+h)*n_colors-y_margins+h_text)
for i in range(n_colors):
    for j in range(n_gradients):
        rect = plt.Rectangle(((w+x_margins)*j, (h+y_margins)*i), w, h, color=colors[n_colors-i-1, j])
        ax.add_patch(rect)
        ax.annotate(oct2hex(colors[n_colors-i-1, j]), ((x_margins+w)*j+w/2, (y_margins+h)*i-h_text/2), va='center', ha='center')
ax.annotate(f'{chord_name} {[k*360//12 for k in hs]}',
            (((x_margins+w)*n_gradients-x_margins)/2, (y_margins+h)*n_colors-y_margins+h_text/2), ha='center', va='center')
if not save_name:
    plt.savefig('debug.svg', bbox_inches='tight', pad_inches=0.0)
else:
    plt.savefig(save_name+'.svg', bbox_inches='tight', pad_inches=0.0)
