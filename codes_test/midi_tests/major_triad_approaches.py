from midi import *
from music21 import chord as ch


def note_generator(note_number, velocity_on=64, time1=0, time2=240):
    return dict(type='note', channel=0, note=note_number, velocity_on=velocity_on, velocity_off=64, lyric=None, time1=time1, time2=time2)


offsets = [-2, -1, 0, 1, 2]

msglist = []
counter = 0
for a in offsets:
    for b in offsets:
        for c in offsets:
            for d in offsets:
                t1 = counter*240*3
                t2 = t1 + 240
                n1 = 0 + 12*4
                n2 = 12 + 12*4
                n3 = 16 + 12*4
                n4 = 19 + 12*4
                msglist.append(note_generator(n1+a, time1=t1, time2=240))
                msglist.append(note_generator(n2+b, time1=t1, time2=240))
                msglist.append(note_generator(n3+c, time1=t1, time2=240))
                msglist.append(note_generator(n4+d, time1=t1, time2=240))
                tmp = ch.Chord([n1+a, n2+b, n3+c, n4+d])
                if not tmp.inversion():
                    msglist.append(dict(type='marker', text=f'{tmp.root().name} {tmp.commonName}', time=t1))
                else:
                    msglist.append(dict(type='marker', text=f'{tmp.root().name}/{tmp.bass().name} {tmp.commonName}', time=t1))
                msglist.append(note_generator(n1, time1=t2, time2=360))
                msglist.append(note_generator(n2, time1=t2, time2=360))
                msglist.append(note_generator(n3, time1=t2, time2=360))
                msglist.append(note_generator(n4, time1=t2, time2=360))
                counter = counter + 1

sheet2midi([msglist], 240, '../../output/major_triad_approaches.mid')
