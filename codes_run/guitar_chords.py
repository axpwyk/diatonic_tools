from instruments import *

m7 = {
    'string_6': {
        'basic': [
            '575555',
            '577585',
            '575585',
            '5x5555',
            '575588',
            '577588',
            '577558',
            '575558'
        ],
        'jazz': [
            '5x555x'  # mxrrrx / mxiiix
        ],
        'other': [
            '5x5553'  # txmrli
        ]
    },

    'string_5': {
        'basic': [
            'xcecdc',
            'xcecdf',
        ],
        'jazz': [
            'xcacdx'
        ],
        'other': [
            'xcxedf'
        ]
    },

    'string_4': {
        'basic': [
            'xx7988',
            'xx7585'
        ],
        'other': [
            'xx7588'
        ]

    }

}

# m7 chord basic
basic_m7_1 = '575555'
basic_m7_2 = '577585'
basic_m7_3 = '575585'
basic_m7_4 = '5x5555'

# m7 chord jazz
jazz_m7_1 = '5x555x'

# m7 chord other
other_m7_1 = '5x5553'


Guitar().set_notes(Chord('Am7')).plot_all_chords(color_style='br357t', max_span=5)
plt.show()
