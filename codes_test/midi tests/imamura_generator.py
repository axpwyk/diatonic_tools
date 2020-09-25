from midi import *
import numpy as np
import skimage.io as si
import skimage.transform as st

tpb = 240
step = tpb//8


def generate_unit_note(time, note_number, velocity_on):
    return dict(type='note', channel=0, note=note_number, velocity_on=velocity_on, velocity_off=64, lyric=None, time1=time, time2=step)


img = si.imread('imamura.jpg', as_gray=True)
print(img.shape)
img = st.resize(img, [64, 64]) * 127
img = img.astype(np.uint8)
print(img.min(), img.max())
plt.imshow(img, cmap='gray')
plt.show()

msglist = []
for i in range(64):
    for j in range(64):
        if img[63-i, j] < 80:
            msglist.append(generate_unit_note(j*step, 36+i, img[63-i, j]))
sheet = [msglist]

sheet2midi(sheet, tpb, 'test.mid')

pr = Pianoroll(sheet, tpb)
pr.set_intervals(pr.get_tick_range_s(0), pr.get_note_range_sg(0))
pr.draw_pianoroll(aspect_note=8, type='piano')
pr.draw_notes()
plt.savefig('test_guitar_plot.svg')
