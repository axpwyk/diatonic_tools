from theories import *

''' 计算两个音符的音程差 '''

print('----------计算两个音符的音程差----------')

note1 = Note('G1')
note2 = Note('C1')
print(f'{note1} - {note2} = {note1 - note2}')
note1 = Note('D1')
note2 = Note('G1')
print(f'{note1} - {note2} = {note1 - note2}')
note1 = Note('G#1')
note2 = Note('C1')
print(f'{note1} - {note2} = {note1 - note2}')
note1 = Note('C#2')
note2 = Note('C1')
print(f'{note1} - {note2} = {note1 - note2}')

''' 计算两个音程的和与差 '''

print('----------计算两个音程的和与差----------')

interval1 = Interval('m3')
interval2 = Interval('M3')
print(f'{interval1} + {interval2} = {interval1 + interval2}')
interval1 = Interval('d4')
interval2 = Interval('A5')
print(f'{interval1} + {interval2} = {interval1 + interval2}')
interval1 = Interval('A8')
interval2 = Interval('A4')
print(f'{interval1} - {interval2} = {interval1 - interval2}')
interval1 = Interval('M9')
interval2 = Interval('M2')
print(f'{interval1} - {interval2} = {interval1 - interval2}')

''' 计算音符与音程的和差 '''

print('----------计算音符与音程的和差----------')

note = Note('G#1')
interval = Interval('M3')
print(f'{note} + {interval} = {note + interval}')
note = Note('G#1')
interval = Interval('P5')
print(f'{note} + {interval} = {note + interval}')
note = Note('G#1')
interval = Interval('m7')
print(f'{note} + {interval} = {note + interval}')
note = Note('G#1')
interval1 = Interval('M9')
interval2 = Interval('m9')
print(f'{note} + {interval1} - {interval2} = {note + interval1 - interval2}')
note = Note('C####3')
interval = Interval('-P8')
print(f'{note} + {interval} = {note + interval}')

''' 生成一个属七和弦 '''

notes = [Note('C1'), Note('C1')+Interval('M3'), Note('C1')+Interval('P5'), Note('C1')+Interval('m7')]
print(notes)
