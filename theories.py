import re
from consts import *


# 用于解析音名、和弦名和调性名称的正则表达式
def note_name_parser(note_name):
    s = note_name
    search_obj = re.search(
        '(?P<name>[ABCDEFG])(?P<acci>[b#]*)(?P<group>-?\d*)', s)
    return search_obj.groupdict()


def chord_name_parser(chord_name):
    s = chord_name
    search_obj = re.search(
        '(?P<bass_name>[ABCDEFG][b#]*) *(?P<chord_type>\w*)(?P<additional>\([^ac-z]*\))*/?(?P<root_name>[ABCDEFG][b#]*)*', s)
    return search_obj.groupdict()


def tonality_parser(tonality):
    s = tonality
    search_obj = re.search('(?P<key_name>[ABCDEFG][b#]*) ?(?P<mode_name>\w+)', s)
    return search_obj.groupdict()


# 常用转换函数
def note_name_to_triple(note_name):
    """ 把音符名称（note_name）转换为三元组（triple）

    输入：
        note_name   音符名称 | python strings | 'Eb3', 'F#', 'G4', etc.

    输出：
        triple      三元组 | python list | [name, acci, group]

    备注：
        name        音名 | integer | range {0, 1, 2, 3, ..., 11}
        acci        变化 | integer | range {-1, 0, 1}
        group       音组 | integer | range {..., -1, 0, 1, 2, ...}
    """
    par = note_name_parser(note_name)
    name = NOTES.index(par['name'])

    acci = 0
    acci += par['acci'].count('#')
    acci -= par['acci'].count('b')

    if par['group']:
        group = eval(par['group'])
    else:
        group = -1
    return [name, acci, group]


def triple_to_note_name(triple):
    note_name = ''
    note_name += NOTES[triple[0]%12]

    if triple[1] > 0:
        note_name += '#'*triple[1]
    elif triple[1] < 0:
        note_name += 'b'*(-triple[1])
    else:
        pass

    if triple[2] >= 0:
        note_name += '{}'.format(triple[2])
    return note_name


def triples_to_note_names(triples):
    return [triple_to_note_name(t) for t in triples]


def triple_to_note_number(triple):
    # note_number represents for midi note number
    return triple[0] + triple[1] + triple[2]*12


def triples_to_note_numbers(triples):
    return [triple_to_note_number(t) for t in triples]


def chord_name_to_triples(chord_name='Cmaj7'):
    par = chord_name_parser(chord_name)
    bass_name = par['bass_name']
    chord_type = par['chord_type']
    scale_type = CHORD_TYPE_SCALES[chord_type]
    choose_list = CHORD_TYPE_CLST[chord_type]
    s = Tonality(bass_name+' '+scale_type)
    return s.chord(choose_list)[0]


# 音乐理论函数
def triple_add5(triple):
    # natural_attractor = [0, 2, 4, 5, 7, 9, 11]
    # diatonic 的特性是升号只在 7 加五度时出现在 4 上成为 #4
    target = triple[0] + 7
    if triple[0] == 11:
        return [target % 12 - 1, triple[1] + 1, triple[2] + target//12]
    else:
        return [target % 12, triple[1], triple[2] + target // 12]


def triple_sub5(triple):
    # natural_attractor = [0, 2, 4, 5, 7, 9, 11]
    # diatonic 的特性是降号只在 4 减五度时出现在 7 上成为 b7
    target = triple[0] - 7
    if triple[0] == 5:
        return [target % 12 + 1, triple[1] - 1, triple[2] - target // 12]
    else:
        return [target % 12, triple[1], triple[2] - target // 12]


class Tonality(object):
    def __init__(self, tonality='C Ionian'):
        par = tonality_parser(tonality)
        self.key = note_name_to_triple(par['key_name'])
        self.mode = MODES.index(par['mode_name'])
        self._build_scale()

    def _build_scale(self):
        if self.mode < 7:
            # 生成中心音，并按照 self.mode 进行向下和向上的五度相生
            self.scale = [self.key]
            for _ in range(self.mode):
                self.scale.insert(0, triple_sub5(self.scale[0]))
            for _ in range(6 - self.mode):
                self.scale.append(triple_add5(self.scale[-1]))
            # 音组归为 -1，排序使得主音在列表首位
            self.scale = [[s[0], s[1], -1] for s in self.scale]
            self.scale.sort()
            key7 = [0, 2, 4, 5, 7, 9, 11].index(self.key[0])
            self.scale = self.scale[key7:] + self.scale[:key7]

        else:
            # 以 Aeolian 为基础调式，后面添加临时升降号变为和声/旋律小调
            base_mode = 4
            self.scale = [self.key]
            for _ in range(base_mode):
                self.scale.insert(0, triple_sub5(self.scale[0]))
            for _ in range(6 - base_mode):
                self.scale.append(triple_add5(self.scale[-1]))
            # 音组归为 -1，排序使得主音在列表首位
            self.scale = [[s[0], s[1], -1] for s in self.scale]
            self.scale.sort()
            key7 = [0, 2, 4, 5, 7, 9, 11].index(self.key[0])
            self.scale = self.scale[key7:] + self.scale[:key7]
            # 添加临时升降号
            if self.mode == 7:
                self.scale[-1][1] += 1
            elif self.mode == 8:
                self.scale[-1][1] += 1
                self.scale[-2][1] += 1

    def add_sharp(self):
        pos = (self.mode * 3) % 7
        self.scale[pos][1] += 1
        self.key = self.scale[0]
        self.mode = (self.mode - 1) % 7

    def add_flat(self):
        pos = (3 + self.mode * 3) % 7
        self.scale[pos][1] -= 1
        self.key = self.scale[0]
        self.mode = (self.mode + 1) % 7

    def tonality(self):
        return triple_to_note_name(self.key) + ' ' + MODES[self.mode]

    def chord(self, choose_list, group=-1):
        # root 取值为 {0, 1, 2, 3, 4, 5, 6}，表示第几个音级作为根音
        chord = [self.scale[i] for i in choose_list]
        # 把 note number 找到（消去升降号）
        chord_nn = [t[0]+t[1] for t in chord]
        # 求差，推断和弦结构
        diff = [(chord_nn[i+1]-chord_nn[i]) % 12 for i in range(len(chord_nn)-1)]
        diff_s = ''
        for d in diff:
            diff_s += str(d)
        # 返回和弦 triples 和从 CHORDS 中得到的和弦结构名
        return chord, CHORDS[diff_s]
