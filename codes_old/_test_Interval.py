from theories import *

''' 计算一列音符两两之间的音程关系 '''

notes = ['C1', 'D1', 'E1', 'F1', 'G1', 'A1', 'B1', 'C2']
print(notes, '\n')
for n1 in notes:
    for n2 in notes:
        note1 = Note().from_name(n1)
        note2 = Note().from_name(n2)
        print(note2-note1, end='')
        if n1 == n2:
            print(f'({note1})', end='')
        print(' ', end='')
    print('\n')

''' 计算音程的和/差 '''

note1 = Note().from_name('C1')
note2 = Note().from_name('G1')
interval = note2 - note1
print(interval+interval)
print(interval-interval)

''' 从名称（字符串）生成音程 '''

print(Interval().from_name('m2') - Interval().from_name('m6'))
print(Interval().from_name('P5') + Interval().from_name('d4'))

''' 计算音符与音程的和/差 '''

print(Note().from_name('G1') + Interval().from_name('m3'))
print(Note().from_name('Db1') + Interval().from_name('P5'))
print(Interval().from_name('-P8') + Note().from_name('C#2'))
print(Note().from_name('C#2') - Interval().from_name('P8'))
print(Note().from_name('B#1') + Interval().from_name('M2'))

''' 生成一个和弦 '''

root = Note().from_name('G#')
M3 = Interval().from_name('M3')
m3 = Interval().from_name('m3')
print(f'[{root.get_note()}, {root.get_accidental()}, {root.get_group()}]')
print(M3, f'[{M3.get_delta_note()}, {M3.get_delta_step()}]')

dominant = [root, root+M3, root+M3+m3, root+M3+m3+m3]
print(dominant)
