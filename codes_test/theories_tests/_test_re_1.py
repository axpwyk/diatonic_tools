from consts import *
import re


# for `DiatonicScale`
def scale_name_parser(scale_name):
    # `scale_name` is a string, examples: 'C C-mode', 'D C-mode(b6)', 'E Phrygian(#3, #7)', etc.

    # basic patterns
    pattern_1 = r'(?P<scale_tonic_name>[' + NAMED_STR_LIN + r'][#b]*-{0,1}\d*) '
    pattern_2 = r'(?P<scale_type>[\w#b+-]*)'
    pattern_3 = r'(?P<altered_note>(\([^ac-z]*\)){0,1})'

    # first we should make sure that `scale_name` is written in new naming scheme
    scale_type = re.sub(pattern_1, '', scale_name)

    if scale_type in SCALE_TYPE_NS1_TO_NS0.keys():
        scale_type = SCALE_TYPE_NS1_TO_NS0[scale_type]
    elif scale_type in ALTERED_SCALE_TYPE_NS2_TO_NS0.keys():
        scale_type = ALTERED_SCALE_TYPE_NS2_TO_NS0[scale_type]
    else:
        pass

    scale_name = re.match(pattern_1, scale_name).group() + scale_type

    # parse `scale_name`
    pattern = pattern_1 + pattern_2 + pattern_3
    search_obj = re.search(pattern, scale_name)

    return search_obj.groupdict()


# for `Chord`
def chord_name_parser(chord_name):
    # `chord_name` is a string, examples: 'CM7', 'Dm7(9, 11, 13)', 'Bm7-5/F', etc.

    # basic patterns
    pattern_1 = r'(?P<root_name>[' + NAMED_STR_LIN + r'][#b]*-{0,1}\d*) ?'
    pattern_2 = r'(?P<chord_type>[\w.#b+-]*)'
    pattern_3 = r'(?P<tension_type>(\([^ac-z]*\)){0,1})'
    pattern_4 = '/?(?P<bass_name>([' + NAMED_STR_LIN + r'][#b]*-{0,1}\d*){0,1})'

    # parse `scale_name`
    pattern = pattern_1 + pattern_2 + pattern_3 + pattern_4
    search_obj = re.search(pattern, chord_name)

    results = search_obj.groupdict()

    # make sure that `chord_type` is written in new naming scheme
    if results['chord_type'] in CHORD_TYPE_NS1_TO_NS0[NGS].keys():
        results['chord_type'] = CHORD_TYPE_NS1_TO_NS0[NGS][results['chord_type']]

    return results


print(chord_name_parser('CM7(#11)/B#-1'))
