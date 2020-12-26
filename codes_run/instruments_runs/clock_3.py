from instruments import *
from pathlib import Path
import svgutils.compose as sc


''' svg generation '''


all_classes = []
with open('all_heptatonic_scale_classes.txt', 'r') as f:
    for line in f:
        all_classes.append(eval(line))
all_lydians = [cl[0] for cl in all_classes]


fig, axs = plt.subplots(11, 6)
fig.set_figheight(44)
fig.set_figwidth(24)
fig.subplots_adjust(0.0, 0.0, 1.0, 1.0, 0.0, 0.0)


for k, lydian in enumerate(all_lydians):
    scale = AlteredDiatonicScale('F' + lydian)
    print(f'{k:2d}  ' + lydian)
    print(scale)

    order = lydian.count('#') + lydian.count('b')
    i = k // 6
    j = k % 6

    c = Clock(scale)
    name = scale.get_name()[0]
    c.plot(name, abs(scale[0])%12, subtitle=f'Class {k} / Order {order}', ax=axs[i, j])
    # name.replace('#', '+').replace('b', '-')
    # plt.savefig(f'clocks/{k}_{name}.svg', bbox_inches='tight', pad_inches=0.1)
    # plt.close()
plt.savefig(f'outputs/test.svg', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.close()
