from theories import *
from instruments import *
from time import ctime
from os import mkdir, path

# 使用 Guitar 类显示和弦图形
chdlst = ['Am', 'D']
chds = [chord_name_to_triples(chd) for chd in chdlst]

# scales = []
# tonality = 'C Ionian'
# s = Tonality(tonality)
# scales.append(s.scale)
# s = Tonality(tonality)
# s.add_sharp()
# scales.append(s.scale)

triples_lst = chds
print(triples_lst)
g = Guitar()
offsets = [0.4*(i-(len(triples_lst)-1)/2) for i in range(len(triples_lst))]
for i in range(len(triples_lst)):
    g.set_pressed_from_triples(triples_lst[i])
    g.draw_guitar(i/len(triples_lst), -1, 15, offsets[i])

# 输出
t = ctime()
t = t.replace(':', ' ').replace(' ', '_')
plt.savefig(path.join('../output', '{}_{}.svg'.format(t, chdlst)))
plt.clf()
plt.close()
