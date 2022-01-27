bad_num = 1
max_hts = 2
stable = [0, 3, 4, 7]
unstable = [1, 2, 5, 6, 8, 9, 10, 11]
note_list = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']

bad_1 = []
bad_2 = []

for n1prev in stable:
    for n1next in unstable:
        for n2prev in unstable:
            for n2next in stable:
                # print(f'{n1prev} -> {n1next} | {n2prev} -> {n2next}')
                bad_num_1 = 0
                bad_num_2 = 0
                for roll in range(12):
                    if (n1prev + roll) % 12 in stable and (n1next + roll) % 12 in unstable and (n2prev + roll) % 12 in unstable and (n2next + roll) % 12 in stable:
                        bad_num_1 = bad_num_1 + 1
                    elif (n1prev + roll) % 12 in unstable and (n1next + roll) % 12 in stable and (n2prev + roll) % 12 in stable and (n2next + roll) % 12 in unstable:
                        bad_num_2 = bad_num_2 + 1

                if bad_num_1 == bad_num and abs(n1prev - n1next) <= max_hts and abs(n2prev-n2next) <= max_hts:
                    bad_1.append([note_list[n1prev], note_list[n1next], note_list[n2prev], note_list[n2next]])
                if bad_num_2 == bad_num and abs(n1prev - n1next) <= max_hts and abs(n2prev-n2next) <= max_hts:
                    bad_2.append([note_list[n1prev], note_list[n1next], note_list[n2prev], note_list[n2next]])

print(len(bad_1), bad_1)
print(len(bad_2), bad_2)
