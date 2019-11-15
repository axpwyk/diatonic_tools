from theories import *

''' 计算两个音符的音程差 '''

print('----------计算两个音符的音程差----------')

note1 = Note().from_name('G1')
note2 = Note().from_name('C1')
print(f'{note1} - {note2} = {note1 - note2}')
note1 = Note().from_name('D1')
note2 = Note().from_name('G1')
print(f'{note1} - {note2} = {note1 - note2}')
note1 = Note().from_name('G#1')
note2 = Note().from_name('C1')
print(f'{note1} - {note2} = {note1 - note2}')
note1 = Note().from_name('C#2')
note2 = Note().from_name('C1')
print(f'{note1} - {note2} = {note1 - note2}')

''' 计算两个音程的和与差 '''

print('----------计算两个音程的和与差----------')

interval1 = Interval().from_name('m3')
interval2 = Interval().from_name('M3')
print(f'{interval1} + {interval2} = {interval1 + interval2}')
interval1 = Interval().from_name('d4')
interval2 = Interval().from_name('A5')
print(f'{interval1} + {interval2} = {interval1 + interval2}')
interval1 = Interval().from_name('A8')
interval2 = Interval().from_name('A4')
print(f'{interval1} - {interval2} = {interval1 - interval2}')
interval1 = Interval().from_name('M9')
interval2 = Interval().from_name('M2')
print(f'{interval1} - {interval2} = {interval1 - interval2}')

''' 计算音符与音程的和差 '''

print('----------计算音符与音程的和差----------')

note = Note().from_name('G#1')
interval = Interval().from_name('M3')
print(f'{note} + {interval} = {note + interval}')
note = Note().from_name('G#1')
interval = Interval().from_name('P5')
print(f'{note} + {interval} = {note + interval}')
note = Note().from_name('G#1')
interval = Interval().from_name('m7')
print(f'{note} + {interval} = {note + interval}')
note = Note().from_name('G#1')
interval1 = Interval().from_name('M9')
interval2 = Interval().from_name('m9')
print(f'{note} + {interval1} - {interval2} = {note + interval1 - interval2}')
note = Note().from_name('C####3')
interval = Interval().from_name('-P8')
print(f'{note} + {interval} = {note + interval}')
