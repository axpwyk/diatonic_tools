all_heptatonic_scale_intervals = []
with open('all_heptatonic_scale_intervals.txt', 'r') as f:
    for line in f:
        all_heptatonic_scale_intervals.append(eval(line))
all_heptatonic_chord_intervals = [interval_vector_1 + interval_vector_2
                                  for interval_vector_1, interval_vector_2
                                  in zip(all_heptatonic_scale_intervals, all_heptatonic_scale_intervals)]
all_heptatonic_chord_intervals = [[intervals[i]+intervals[i+1] for i in range(0, 14, 2)] for intervals in all_heptatonic_chord_intervals]

with open('all_heptatonic_chord_intervals.txt', 'w') as f:
    for interval_vector in all_heptatonic_chord_intervals:
        f.write(f'{interval_vector}\n')
