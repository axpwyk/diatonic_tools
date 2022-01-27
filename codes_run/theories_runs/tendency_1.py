from theories import *

tonics = [Note('F'), Note('C'), Note('G'), Note('D'), Note('A'), Note('E')]
dominants = [Note('C'), Note('G'), Note('D'), Note('A'), Note('E'), Note('B')]

t0 = [t.get_name(show_register=False) for t in tonics]
d0 = [d.get_name(show_register=False) for d in dominants]

t_dict = {
    't0': t0,
    't+1': [(t + Interval('m2')).get_name(show_register=False) for t in tonics],
    't-1': [(t - Interval('m2')).get_name(show_register=False) for t in tonics],
    't+2': [(t + Interval('M2')).get_name(show_register=False) for t in tonics],
    't-2': [(t - Interval('M2')).get_name(show_register=False) for t in tonics]
}

d_dict = {
    'd0': d0,
    'd+1': [(d + Interval('m2')).get_name(show_register=False) for d in dominants],
    'd-1': [(d - Interval('m2')).get_name(show_register=False) for d in dominants],
    'd+2': [(d + Interval('M2')).get_name(show_register=False) for d in dominants],
    'd-2': [(d - Interval('M2')).get_name(show_register=False) for d in dominants]
}

tendencies = {k: [] for k in 'CDEFGAB'}
for note_name in 'CDEFGAB':
    for k, v in t_dict.items():
        if note_name in v:
            tendencies[note_name].append(k)
    for k, v in d_dict.items():
        if note_name in v:
            tendencies[note_name].append(k)

for k, v in tendencies.items():
    print(f'{k}: {v}')
