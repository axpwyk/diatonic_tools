from itertools import product
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import colorsys as cs

from theories import *
# from midi import *


''' ----------------------------------------------------------------------------------------- '''
''' ********************************** matplotlib settings ********************************** '''
''' ----------------------------------------------------------------------------------------- '''


# assign a style
plt.style.use('seaborn-pastel')
plt.rc('figure', **{'dpi': 72})

# assign a math font
plt.rc('mathtext', **{'fontset': 'cm'})
plt.rc('text', **{'usetex': False})

# assign a chinese-supporting font
plt.rc('font', **{'sans-serif': 'Consolas-with-Yahei', 'size': 16.0})
plt.rc('axes', **{'unicode_minus': False})


def get_figure(w, h, dpi=None):
    # figure settings
    fig = plt.figure(figsize=(w, h), dpi=dpi)
    fig.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=1.0, wspace=0.1, hspace=0.1)
    ax = fig.gca(aspect='equal')
    ax.set_axis_off()
    ax.margins(x=0.01, y=0.01)
    return fig, ax


''' ----------------------------------------------------------------------------------------- '''
''' ************************************ color utilities ************************************ '''
''' ----------------------------------------------------------------------------------------- '''


def hex2float(hex_color_string):
    search_obj = re.search(r'(?<=#)(?P<r>[\dabcdef]{2})(?P<g>[\dabcdef]{2})(?P<b>[\dabcdef]{2})', hex_color_string)
    return [int(search_obj[s], 16) / 255 for s in ['r', 'g', 'b']]


def float2hex(dec_color_list):
    return '#' + ''.join([f'{int(k * 255):02x}' for k in dec_color_list])


def rgb_shader(t, t_min=0, t_max=1, color1=(0.94, 0.02, 0.55), color2=(0.11, 0.78, 0.72)):
    """
    Linear interpolation between 2 colors `color1` and `color2`
    :param t: variable
    :param t_min: lower bound of variable `t`
    :param t_max: upper bound of variable `t`
    :param color1: hex or float color in RGB
    :param color2: hex or float color in RGB
    :return: float color in RGB
    """
    # proportion of `t`
    t = (t - t_min) / (t_max - t_min)
    # if input colors are hex strings, convert them to float triples
    if isinstance(color1, str):
        color1 = hex2float(color1)
    if isinstance(color2, str):
        color2 = hex2float(color2)
    # convert `color1` and `color2` to yiq space for better gradient visuals
    color1 = cs.rgb_to_yiq(*color1)
    color2 = cs.rgb_to_yiq(*color2)
    # return color at `t` using linear interpolation
    return cs.yiq_to_rgb(*[t * c2 + (1.00-t) * c1 for (c1, c2) in zip(color1, color2)])


def hsv_shader(t, t_min=0, t_max=1, color1=(0.00, 0.80, 0.75), color2=(1.00, 0.80, 0.75)):
    # proportion of `t`
    t = (t - t_min) / (t_max - t_min)
    # return color at `t` using linear interpolation
    return cs.hsv_to_rgb(*[t * c2 + (1.00-t) * c1 for (c1, c2) in zip(color1, color2)])


def cst_shader(t, t_min=0, t_max=1, color=(1.00, 0.00, 0.00)):
    return color


def note_colors(i, n_notes, mode='face'):
    if mode == 'face':
        colors_lr = NOTE_FACE_COLORS_LR
    elif mode == 'edge':
        colors_lr = NOTE_EDGE_COLORS_LR
    elif mode == 'text':
        colors_lr = NOTE_TEXT_COLORS_LR
    else:
        raise ValueError("No such mode! Please choose from ['face', 'edge', 'text']!")

    return rgb_shader(i * n_notes / (n_notes - 1), 0, n_notes, color1=colors_lr[0], color2=colors_lr[1])


def br357t_colors(br357t, step_length=CHORD_STEP_LIN, mode='face'):
    if mode == 'face':
        colors = BR357T_FACE_COLORS
    elif mode == 'edge':
        colors = BR357T_EDGE_COLORS
    elif mode == 'text':
        colors = BR357T_TEXT_COLORS
    else:
        raise ValueError("No such mode! Please choose from ['face', 'edge', 'text']!")

    if 'B' in br357t:
        return colors['B']
    elif 'R' in br357t:
        return colors['R']
    elif br357t == None:
        return colors[None]
    else:
        step = int(''.join([s for s in br357t if s.isdigit()])) - 1
        if step % M in range(0, M, step_length):
            return colors['CN']
        else:
            return colors['T']


def degree_colors(degree, n_notes, mode='face'):
    if mode == 'face':
        colors_lr = DEGREE_FACE_COLORS_LR
    elif mode == 'edge':
        colors_lr = DEGREE_EDGE_COLORS_LR
    elif mode == 'text':
        colors_lr = DEGREE_TEXT_COLORS_LR
    else:
        raise ValueError("No such mode! Please choose from ['face', 'edge', 'text']!")

    return rgb_shader(degree * n_notes / (n_notes - 1), 0, n_notes, color1=colors_lr[0], color2=colors_lr[1])


def tds_colors(tds, mode='face'):
    if mode == 'face':
        colors = TDS_FACE_COLORS
    elif mode == 'edge':
        colors = TDS_EDGE_COLORS
    elif mode == 'text':
        colors = TDS_TEXT_COLORS
    else:
        raise ValueError("No such mode! Please choose from ['face', 'edge', 'text']!")

    if 'T' in tds:
        return colors['T']
    elif 'D' in tds:
        return colors['D']
    elif 'S' in tds:
        return colors['S']
    else:
        return colors[None]


def avoid_colors(avoid, mode='face'):
    if mode == 'face':
        colors = AVOID_FACE_COLORS
    elif mode == 'edge':
        colors = AVOID_EDGE_COLORS
    elif mode == 'text':
        colors = AVOID_TEXT_COLORS
    else:
        raise ValueError("No such mode! Please choose from ['face', 'edge', 'text']!")

    if avoid == '[CN]':
        return colors['[CN]']
    elif avoid == '[A1]':
        return colors['[A1]']
    elif '[A0]' in avoid:
        return colors['[A0]']
    elif '[A2]' in avoid:
        return colors['[A2]']
    elif '[OK]' in avoid:
        return colors['[OK]']
    elif '[TN]' in avoid:
        return colors['[TN]']
    else:
        return colors[None]


''' ----------------------------------------------------------------------------------------- '''
''' ************************************ other utilities ************************************ '''
''' ----------------------------------------------------------------------------------------- '''


# a handy length function
def length(a, b):
    return b - a


# a handy middle point function
def middle(a, b):
    return (a + b) / 2


# a handy if x \in [a, b) function
def within(x, a, b):
    return a <= x < b


''' ----------------------------------------------------------------------------------------- '''
''' ******************************** basic instrument classes ******************************* '''
''' ----------------------------------------------------------------------------------------- '''


# TODO: review `instruments.py`
class _NoteList(object):
    def __init__(self):
        self._notes = []

    def set_notes(self, notes):
        self._notes = [note for note in notes if isinstance(note, Note)]
        return self

    def add_notes(self, notes):
        self._notes = self._notes + [note for note in notes if isinstance(note, Note)]
        return self

    def del_notes(self):
        self._notes = []
        return self

    def _get_note_text(self, text_style):
        if text_style in ['note', 'br357t', 'degree', 'avoid']:
            for note in self._notes:
                note.set_message(text=note.get_message(text_style))
        else:
            raise ValueError("No such text style! Please choose from ['note', 'br357t', 'degree', 'avoid']!")

    def _get_note_color(self, color_style):
        if color_style == 'note':
            for i, note in enumerate(self._notes):
                note.set_message(face_color=note_colors(i, len(self._notes), 'face'))
                note.set_message(edge_color=note_colors(i, len(self._notes), 'edge'))
                note.set_message(text_color=note_colors(i, len(self._notes), 'text'))
        elif color_style == 'br357t':
            for note in self._notes:
                note.set_message(face_color=br357t_colors(note.get_message('br357t'), CHORD_STEP_LIN, 'face'))
                note.set_message(edge_color=br357t_colors(note.get_message('br357t'), CHORD_STEP_LIN, 'edge'))
                note.set_message(text_color=br357t_colors(note.get_message('br357t'), CHORD_STEP_LIN, 'text'))
        elif color_style == 'degree':
            for i, note in enumerate(self._notes):
                note.set_message(face_color=degree_colors(note.get_message('degree'), len(self._notes), 'face'))
                note.set_message(edge_color=degree_colors(note.get_message('degree'), len(self._notes), 'edge'))
                note.set_message(text_color=degree_colors(note.get_message('degree'), len(self._notes), 'text'))
        elif color_style == 'avoid':
            for note in self._notes:
                note.set_message(face_color=avoid_colors(note.get_message('avoid'), 'face'))
                note.set_message(edge_color=avoid_colors(note.get_message('avoid'), 'edge'))
                note.set_message(text_color=avoid_colors(note.get_message('avoid'), 'text'))
        else:
            raise ValueError("No such color style! Please choose from ['note', 'br357t', 'degree', 'avoid']!")


class Guitar(_NoteList):
    def __init__(self, modulo_on=True, max_fret=24,
                 open_string_notes=(Note('E1'), Note('A1'), Note('D2'), Note('G2'), Note('B2'), Note('E3')),
                 w_to_h_ratio=2.0, short_fret_markers=(3, 5, 7, 9), long_fret_markers=(0, )):
        # set `self._notes`
        super().__init__()
        # basic properties of this guitar instance
        self._modulo_on = modulo_on  # ignore register of note
        self._max_fret = max_fret  # number of frets
        self._max_string = len(open_string_notes)  # number of strings
        # open string nnabs and fretboard nnabs
        self._open_string_notes = list(open_string_notes)
        self._open_string_nnabs = np.array([int(note) for note in open_string_notes])  # 1-d `np.ndarray`
        self._fretboard_nnabs = np.array([self._open_string_nnabs + i for i in range(0, max_fret + 1)])  # [frets, strings]
        # w to h ratio of fretboard
        self._w_to_h_ratio = w_to_h_ratio
        # fret markers
        self._short_fret_markers = short_fret_markers
        self._long_fret_markers = long_fret_markers

    def _get_note_with_indices(self, selection):
        """
        get notes and their indices of fretboard matrix

        :param selection: string, e.g. 'x32010'
        :return: note_list, indices_list, used_strings
        """
        note_list, indices_list, used_strings =  [], [], []

        # check every note in `self._notes`
        for i, note in enumerate(self._notes):
            # gather all matching notes on fretboard
            if self._modulo_on:
                indices = np.stack(np.where(self._fretboard_nnabs%N == int(note)%N), axis=-1)  # [?, 2]
            else:
                indices = np.stack(np.where(self._fretboard_nnabs == int(note)), axis=-1)  # [?, 2]

            # add these notes and their indices to list
            for cur_indices in indices:
                # only keep notes in selection
                cur_fret, cur_string = cur_indices
                if selection[cur_string] == 'p':  # all notes on this string
                    pass
                elif selection[cur_string] == 'x':  # no note on this string
                    continue
                else:  # selected note on this string
                    if int(selection[cur_string], self._max_fret) == cur_fret:
                        pass
                    else:  # if selected note is not on this string, skip
                        continue

                cur_note = copy(note)

                # change register of current note
                if self._modulo_on:
                    delta_register = (self._fretboard_nnabs[cur_fret, cur_string] - int(note)) // N
                    cur_note.add_register(delta_register)

                note_list.append(cur_note)
                indices_list.append(cur_indices)
                if cur_string not in used_strings:
                    used_strings.append(cur_string)

        return note_list, indices_list, used_strings

    def set_modulo_on(self, modulo_on=True):
        self._modulo_on = modulo_on
        return self

    def auto_select(self, max_span=4, use_open_string=False, highest_bass_string=2, top_note=None, lowest_soprano_string=3):
        """
        select pressed notes automatically
        :param max_span: maximal span of frets
        :param use_open_string: will check open strings at first
        :return: list of selections, e.g. ['x3201x', 'x32010', ...]
        """

        # find lowest note, B or R
        br357t_to_nnrels = {note.get_message('br357t'): int(note) % N for note in self._notes}

        if 'B' in br357t_to_nnrels.keys():
            nnrel_low = br357t_to_nnrels['B']
        elif 'R' in br357t_to_nnrels.keys():
            nnrel_low = br357t_to_nnrels['R']
        else:
            raise ValueError('Given notes do not contain B or R!')

        # find highest note, if `top_note` is given
        if top_note is not None:
            if top_note in br357t_to_nnrels.keys():
                nnrel_high = br357t_to_nnrels[top_note]
            else:
                raise ValueError('Given top note does not exist!')
        else:
            nnrel_high = None

        # useful expressions
        fretboard_nnrel = self._fretboard_nnabs[:N+max_span] % N
        fret_positions_range = range(0, N)
        n_strings = self._max_string

        # get all chord schemes
        chord_schemes = []
        fret_positions = []
        for fret_position in fret_positions_range:
            fretboard_bool = np.any([fretboard_nnrel == nnrel for _, nnrel in br357t_to_nnrels.items()], axis=0)
            if use_open_string and fret_position > 0:
                fretboard_bool[1:fret_position] = False
                fretboard_bool[fret_position+max_span:] = False
            else:
                fretboard_bool[0:fret_position] = False
                fretboard_bool[fret_position+max_span:] = False

            frets, strings = np.where(fretboard_bool)
            s2f = {k: [] for k in strings}
            for fret, string in zip(frets, strings):
                s2f[string].append(fret)

            for frets in product(*s2f.values()):
                chord_scheme = np.zeros_like(fretboard_bool, np.bool)
                for fret, string in zip(frets, s2f.keys()):
                    chord_scheme[fret, string] = True

                chord_schemes.append(chord_scheme)
                fret_positions.append(fret_position)

        print(f'All possible chord diagrams: {len(chord_schemes)}')

        # get real chord_schemes and fret_positions
        chord_schemes_filt = []
        fret_positions_filt = []
        for chord_scheme, fret_position in zip(chord_schemes, fret_positions):
            # filters
            fretboard_nnrel_used = copy(fretboard_nnrel)
            fretboard_nnrel_used[~chord_scheme] = -1
            if use_open_string and fret_position > 0:
                fretboard_nnrel_used_slice = np.concatenate(
                    [
                        fretboard_nnrel_used[0:1],
                        fretboard_nnrel_used[fret_position:fret_position+max_span]
                    ]
                )
            else:
                fretboard_nnrel_used_slice = fretboard_nnrel_used[fret_position:fret_position+max_span]
            fretboard_nnrel_used_low = fretboard_nnrel_used_slice[:, :highest_bass_string+1]
            fretboard_nnrel_used_high = fretboard_nnrel_used_slice[:, lowest_soprano_string:]

            # 1. lowest strings contain B or R
            if nnrel_low not in fretboard_nnrel_used_low:
                continue
            else:
                string_low = np.where(fretboard_nnrel_used_low == nnrel_low)[1].min()
                fretboard_nnrel_used_slice[:, :string_low] = -1
                chord_scheme[:, :string_low] = False

            # 2. highest strings contain top note
            if top_note is not None:
                if nnrel_high not in fretboard_nnrel_used_high:
                    continue
                else:
                    string_high = lowest_soprano_string + np.where(fretboard_nnrel_used_high == nnrel_high)[1].max()
                    fretboard_nnrel_used_slice[:, string_high+1:] = -1
                    chord_scheme[:, string_high+1:] = False

            # 3. contains all notes
            if not all([k in fretboard_nnrel_used_slice for k in br357t_to_nnrels.values()]):
                continue

            chord_schemes_filt.append(chord_scheme)
            fret_positions_filt.append(fret_position)

        # convert chord schemes to str
        chord_schemes_string = []
        fret_positions_string = []
        for cs, fp in zip(chord_schemes_filt, fret_positions_filt):
            used_indices = np.stack(np.where(cs), axis=-1)
            cs_str = ['x'] * n_strings
            for fret, string in used_indices:
                cs_str[string] = np.base_repr(fret, N+max_span)
            cs_str = ''.join(cs_str).lower()

            if cs_str not in chord_schemes_string:
                chord_schemes_string.append(cs_str)
                fret_positions_string.append(fp)
            else:
                idx = chord_schemes_string.index(cs_str)
                chord_schemes_string.pop(idx)
                fret_positions_string.pop(idx)
                chord_schemes_string.append(cs_str)
                fret_positions_string.append(fp)

        return chord_schemes_string, fret_positions_string

    def plot(self, fret_left=0, fret_right=N, selection='pppppp', text_rotation=0, color_style='note', ax=None, title=None):
        # get note colors
        self._get_note_color(color_style)

        # get note texts
        self._get_note_text(color_style)

        # gather instance attributes
        w_to_h_ratio = self._w_to_h_ratio
        max_string = self._max_string
        max_fret = self._max_fret
        short_fret_markers = self._short_fret_markers
        long_fret_markers = self._long_fret_markers

        # get coordinates
        coord_strings = np.arange(max_string)
        coord_frets = w_to_h_ratio * np.arange(0, max_fret)
        coord_fingers = np.concatenate([np.array([-w_to_h_ratio / 2, ]), coord_frets[:-1] + coord_frets[1:]]) / 2

        # new figure if axes is not provided
        if ax is None:
            w = coord_frets[fret_right] - coord_frets[fret_left] + 2 * w_to_h_ratio
            h = coord_strings[-1] - coord_strings[0] + 2
            scale = 0.75
            fig, ax = get_figure(w * scale, h * scale)

        # add title if provided
        if title:
            ax.text(x=0.5, y=0.895, s=title, va='bottom', ha='center', transform=ax.transAxes)

        # plot fret markers
        for i in range(fret_left+1, fret_right+1):
            if i % N in long_fret_markers:
                rect = plt.Rectangle(
                    xy=(coord_fingers[i], coord_strings[0]),
                    width=coord_frets[i]-coord_fingers[i],
                    height=coord_strings[-1]-coord_strings[0],
                    color='gray',
                    alpha=0.2,
                    zorder=0
                )
                ax.add_patch(rect)
            elif i % N in short_fret_markers:
                rect = plt.Rectangle(
                    xy=(coord_fingers[i], middle(coord_strings[0], coord_strings[-1])),
                    width=coord_frets[i]-coord_fingers[i],
                    height=middle(coord_strings[0], coord_strings[-1]),
                    color='gray',
                    alpha=0.2,
                    zorder=0
                )
                ax.add_patch(rect)
            else:
                pass

        # plot frets (vertical lines)
        ax.set_xlim(coord_frets[fret_left]-w_to_h_ratio, coord_frets[fret_right]+w_to_h_ratio)
        _ = [
            ax.plot(
                (coord_frets[i], coord_frets[i]),
                (coord_strings[0], coord_strings[-1]),
                c='black',
                lw=2.0,
                zorder=1
            ) for i in range(fret_left, fret_right+1)
        ]
        _ = [
            ax.annotate(
                s=i,
                xy=(coord_frets[i], -0.5),
                rotation=text_rotation,
                color='black',
                va='center',
                ha='center') for i in range(fret_left, fret_right+1)
        ]

        # plot strings (horizontal lines)
        ax.set_ylim(coord_strings[0]-1, coord_strings[-1]+1)
        _ = [
            ax.plot(
                (coord_frets[fret_left], coord_frets[fret_right]),
                (s, s),
                c='black',
                lw=1.0,
                zorder=2
            ) for s in coord_strings
        ]

        # plot dots and texts
        radius = 0.15 * w_to_h_ratio
        note_list, indices_list, used_strings = self._get_note_with_indices(selection)

        circs = []
        for note, indices in zip(note_list, indices_list):
            # unpack indices
            fret, string = indices
            # open string dots
            if fret == 0:
                circs.append(
                    plt.Circle(
                        xy=(coord_fingers[0] + coord_frets[fret_left], coord_strings[string]),
                        radius=radius,
                        fc='white',
                        ec=note.get_message('face_color'),
                        zorder=3
                    )
                )
                ax.annotate(
                    s=note.get_message('text'),
                    xy=(coord_fingers[0] + coord_frets[fret_left], coord_strings[string]),
                    rotation=text_rotation,
                    color='black',
                    va='center',
                    ha='center',
                    zorder=4
                )
            # other fret dots
            elif within(fret, fret_left+1, fret_right+1):
                circs.append(
                    plt.Circle(
                        xy=(coord_fingers[fret], coord_strings[string]),
                        radius=radius,
                        fc=note.get_message('face_color'),
                        ec=note.get_message('face_color'),
                        zorder=3
                    )
                )
                ax.annotate(
                    s=note.get_message('text'),
                    xy=(coord_fingers[fret], coord_strings[string]),
                    rotation=text_rotation,
                    color=note.get_message('text_color'),
                    va='center',
                    ha='center',
                    zorder=4
                )
            else:
                continue

        # plot crosses
        crosses = []
        for string in range(max_string):
            if string not in used_strings:
                crosses.extend(
                    [
                        plt.Line2D((coord_fingers[0] + coord_frets[fret_left] - radius * np.sqrt(2) / 2,
                                    coord_fingers[0] + coord_frets[fret_left] + radius * np.sqrt(2) / 2),
                                   (string - radius * np.sqrt(2) / 2, string + radius * np.sqrt(2) / 2), c='black'),
                        plt.Line2D((coord_fingers[0] + coord_frets[fret_left] + radius * np.sqrt(2) / 2,
                                    coord_fingers[0] + coord_frets[fret_left] - radius * np.sqrt(2) / 2),
                                   (string - radius * np.sqrt(2) / 2, string + radius * np.sqrt(2) / 2), c='black')
                    ]
                )
            else:
                pass

        _ = [ax.add_patch(circ) for circ in circs]
        _ = [ax.add_line(line) for line in crosses]

    def plots(self, max_span=4, selections=('pppppp'), fret_positions=(0), text_rotation=0, color_style='note', title=''):
        n_schemes = len(selections)
        n_w = int(np.sqrt(n_schemes))
        n_h = n_schemes // n_w + 1

        fig = plt.figure(figsize=(4 * n_w * (self._w_to_h_ratio * max_span) / len(self._open_string_nnabs), 4 * n_h), dpi=144)
        suptitle = f'{title}\nTuning: {" ".join([note.get_name() for note in self._open_string_notes])}\n'
        fig.suptitle(suptitle)
        fig.subplots_adjust(0.0, 0.0, 1.0, 1.0-1/(2*n_h), 0.0, 0.0)
        spec = gridspec.GridSpec(ncols=n_w, nrows=n_h, figure=fig)

        for i, (chord_scheme, fret_position) in enumerate(zip(selections, fret_positions)):
            ax = fig.add_subplot(spec[i//n_w, i%n_w])
            ax.margins(0.0, 0.0)
            ax.set_axis_off()
            ax.set_aspect('equal')
            left = fret_position - 1 if fret_position > 0 else 0
            right = fret_position + max_span - 1 if fret_position > 0 else fret_position + max_span
            self.plot(left, right, chord_scheme, text_rotation, color_style, ax, chord_scheme)

    def plot_all_chords(self, max_span=4, use_open_string=False, highest_bass_string=2, top_note=None, lowest_soprano_string=3, text_rotation=0, color_style='note', title=''):
        chord_schemes, fret_positions = self.auto_select(max_span=max_span, use_open_string=use_open_string, highest_bass_string=highest_bass_string, top_note=top_note, lowest_soprano_string=lowest_soprano_string)
        n_schemes = len(chord_schemes)
        n_w = int(np.sqrt(n_schemes))
        n_h = n_schemes // n_w + 1

        fig = plt.figure(figsize=(4 * n_w * (self._w_to_h_ratio * max_span) / len(self._open_string_nnabs), 4 * n_h), dpi=144)
        suptitle = f'{title}\nTuning: {" ".join([note.get_name() for note in self._open_string_notes])}\n'
        suptitle += f'use_open_string={use_open_string}\n'
        suptitle += f'highest_bass_string={self._max_string-highest_bass_string}'
        if top_note is not None:
            suptitle += f' | lowest_soprano_string={self._max_string-lowest_soprano_string} | top_note={top_note}'
        fig.suptitle(suptitle)
        fig.subplots_adjust(0.0, 0.0, 1.0, 1.0-1/(2*n_h), 0.0, 0.0)
        spec = gridspec.GridSpec(ncols=n_w, nrows=n_h, figure=fig)

        for i, (chord_scheme, fret_position) in enumerate(zip(chord_schemes, fret_positions)):
            ax = fig.add_subplot(spec[i//n_w, i%n_w])
            ax.margins(0.0, 0.0)
            ax.set_axis_off()
            ax.set_aspect('equal')
            left = fret_position - 1 if fret_position > 0 else 0
            right = fret_position + max_span - 1 if fret_position > 0 else fret_position + max_span
            self.plot(left, right, chord_scheme, text_rotation, color_style, ax, chord_scheme)


class Piano(_NoteList):
    def __init__(self):
        super().__init__()

    def _get_note_range(self):
        notes = [int(note) for note in self._notes]
        return min(notes), max(notes)

    def plot_old(self, note_range=None, color_style='note', ax=None, title=None):
        if not all([N==12, G==7, S==5]):
            raise ValueError('`Piano.plot_old` works properly only when [N, G, S] = [12, 7, 5]!')

        # get note colors
        self._get_note_color(color_style)

        # get note texts
        self._get_note_text(color_style)

        # get plot range
        if note_range is None:
            note_range = self._get_note_range()

        # note to position mappings
        def _note2pos_xy(note):
            group = note // 12
            note = note % 12
            if note in range(5):
                if note in [0, 2, 4]:
                    return 10.5 * group + 1.5 / 2 * note, 0
                else:
                    return 10.5 * group + 1.5 / 2 * (note + 1) - 0.5, 2.5
            else:
                if note in [5, 7, 9, 11]:
                    return 10.5 * group + 1.5 / 2 * (note + 1), 0
                else:
                    return 10.5 * group + 1.5 / 2 * (note + 2) - 0.5, 2.5

        def _note2pos_rect(note):
            if note % 12 in [0, 2, 4, 5, 7, 9, 11]:
                return dict(
                    xy=_note2pos_xy(note),
                    width=1.5,
                    height=6,
                    fc='white',
                    ec='black',
                    ls='-',
                    lw=2,
                    joinstyle='round',
                    zorder=1
                )
            else:
                return dict(
                    xy=_note2pos_xy(note),
                    width=1,
                    height=3.5,
                    fc='black',
                    ec='black',
                    ls='-',
                    lw=2,
                    joinstyle='round',
                    zorder=2
                )

        def _note2pos_mark(note):
            group = note // 12
            note = note % 12
            if note in range(5):
                x = 10.5 * group + 1.5 / 2 * (note + 1)
            else:
                x = 10.5 * group + 1.5 / 2 * (note + 2)
            if note in [0, 2, 4, 5, 7, 9, 11]:
                y = 0.75
            else:
                y = 3.25
            return x, y

        # constants
        keys_expand = 1
        w = _note2pos_xy(note_range[1] + keys_expand)[0] - _note2pos_xy(note_range[0] - keys_expand)[0]
        h = 6

        # new figure
        if not ax:
            scale = 0.75
            fig, ax = get_figure(w * scale , h * scale)

        # axes settings
        ax.set_xlim(_note2pos_mark(note_range[0]-keys_expand)[0], _note2pos_mark(note_range[1]+keys_expand)[0])
        ax.set_ylim(0, h)

        # add title
        if title:
            ax.text(0.5, 0.895, title, va='bottom', ha='center', transform=ax.transAxes)
            ax.set_ylim(0, h+1)

        # draw
        rects = [
            plt.Rectangle(**_note2pos_rect(note))
            for note in range(note_range[0]-1-keys_expand, note_range[1]+2+keys_expand)
        ]
        _ = [ax.add_patch(rect) for rect in rects]

        # add annotation
        circs = [
            plt.Circle(
                xy=_note2pos_mark(int(note)),
                radius=0.4,
                ls='-',
                lw=1,
                ec=note.get_message('face_color'),
                fc=note.get_message('face_color'),
                zorder=3
            ) for note in self._notes
        ]
        _ = [ax.add_patch(circ) for circ in circs]
        _ = [
            ax.annotate(
                s=note.get_message('text'),
                xy=_note2pos_mark(int(note)),
                color='white',
                ha='center',
                va='center',
                zorder=4
            ) for note in self._notes
        ]

    def plot(self, height=3, note_range=None, color_style='br357t', ax=None, title=None):
        # get note colors
        self._get_note_color(color_style)

        # get note texts
        self._get_note_text(color_style)

        if note_range is None:
            note_range = self._get_note_range()

        if ax is None:
            fig, ax = get_figure(length(*note_range) + 3, height, 72)

        if title is not None:
            ax.text(0.5, 0.895, title, va='bottom', ha='center', transform=ax.transAxes)

        # set display range
        ax.set_xlim(note_range[0] - 1, note_range[1] + 2)

        # key patches
        key_rects = [
            plt.Rectangle(
                xy=(x, 0),
                width=1,
                height=height,
                edgecolor='gray',
                facecolor='white' if x % N in NAMED_NNREL_LIN else 'black'
            ) for x in range(note_range[0], note_range[1] + 1)
        ]
        _ = [ax.add_patch(key_rect) for key_rect in key_rects]

        self._get_note_color(color_style)

        # note patches
        note_circs = [
            plt.Circle(
                xy=(int(note) + 1/2, 1/2),
                radius=1/3,
                edgecolor='none',
                facecolor=note.get_message('face_color')
            ) for note in self._notes
        ]
        _ = [ax.add_patch(note_circ) for note_circ in note_circs]

        # texts
        _ = [
            ax.annotate(
                s=note.get_message('text'),
                xy=(int(note) + 1/2, 1/2),
                ha='center',
                va='center',
                color=note.get_message('text_color')
            ) for note in self._notes
        ]


class Clock(_NoteList):
    def __init__(self):
        super().__init__()

    def plot(self, color_style='note', interval_anno_style=None, ax=None, title=None, subtitle=None):
        # get note colors and texts
        self._get_note_color(color_style)
        self._get_note_text(color_style)

        radius = 5
        omega = np.cos(2 * np.pi / N) - np.sin(2 * np.pi / N) * 1j
        offset = 1j

        texts = [''] * N
        for note in self._notes:
            if color_style != 'note':
                texts[int(note) % N] += note.get_name(show_register=False) + f"({note.get_message('text')})"
            else:
                texts[int(note) % N] += note.get_name(show_register=False)

        text_positions = [(1.4*radius*np.real(omega**k*offset), 1.4*radius*np.imag(omega**k*offset)) for k in range(N)]

        hand_colors = [[0.5, 0.5, 0.5]] * N
        for note in self._notes:
            hand_colors[int(note) % N] = note.get_message('face_color')

        ''' new figure '''

        if not ax:
            fig, ax = get_figure(5, 5, 72)

        ax.set_xlim(-(radius+4), radius+4)
        ax.set_ylim(-(radius+4), radius+4)

        ''' plotting '''

        nnabs_list_1 = [int(x) for x in self._notes]

        circ = plt.Circle((0, 0), radius, fc='none', ec='black', lw=2.0)
        hands = [
            plt.Line2D(
                xdata=(0, 0.8*radius*np.real(omega**k*offset)),
                ydata=(0, 0.8*radius*np.imag(omega**k*offset)),
                lw=1.5,
                c=hand_colors[k]
            ) for k in range(N)
        ]
        ticks = [
            plt.Line2D(
                xdata=(0.95*radius*np.real(omega**k*offset), radius*np.real(omega**k*offset)),
                ydata=(0.95*radius*np.imag(omega**k*offset), radius*np.imag(omega**k*offset)),
                lw=1,
                c='black'
            ) for k in range(N)
        ]

        ax.add_patch(circ)
        _ = [ax.add_line(hand) for hand in [hands[k % N] for k in nnabs_list_1]]
        _ = [ax.add_line(tick) for tick in [ticks[k] for k in range(N)]]
        _ = [
            ax.annotate(
                s=k,
                xy=(1.1*radius*np.real(omega**k*offset), 1.1*radius*np.imag(omega**k*offset)),
                ha='center',
                va='center') for k in range(N)
        ]
        _ = [
            ax.annotate(
                s=texts[k],
                xy=text_positions[k],
                va='center',
                ha='center',
                bbox=dict(facecolor=hand_colors[k], alpha=0.2, edgecolor=hand_colors[k])) for k in range(N)]

        nnabs_list_2 = nnabs_list_1 + [nnabs_list_1[0] + N]

        if interval_anno_style == 'degree':
            _ = [
                ax.annotate(
                    s=f'{(k2-k1)*(360/N)}°',
                    xy=(np.real(0.65*radius*omega**(k1+(k2-k1)/2)*offset), np.imag(0.65*radius*omega**(k1+(k2-k1)/2)*offset)),
                    ha='center',
                    va='center'
                ) for k1, k2 in zip(nnabs_list_2[:-1], nnabs_list_2[1:])
            ]
        elif interval_anno_style == 'interval':
            notes = self._notes + [self._notes[0] + Interval().set_vector(N, M)]
            _ = [
                ax.annotate(
                    s=str(notes[i+1]-notes[i]),
                    xy=(np.real(0.65*radius*omega**(k1+(k2-k1)/2)*offset), np.imag(0.65*radius*omega**(k1+(k2-k1)/2)*offset)),
                    ha='center',
                    va='center'
                ) for i, (k1, k2) in enumerate(zip(nnabs_list_2[:-1], nnabs_list_2[1:]))
            ]
        else:
            pass

        if title:
            ax.text(0.05, 0.95, title, transform=ax.transAxes, ha='left', va='top', bbox=dict(facecolor='none', edgecolor='black'))
            if subtitle:
                ax.text(0.95, 0.05, subtitle, transform=ax.transAxes, ha='right', va='bottom', bbox=dict(facecolor='none', edgecolor='black'))


class ColorScheme(_NoteList):
    def __init__(self):
        super().__init__()

    def plot(self, ax=None, title='ColorScheme'):
        h = np.linspace(0, 1, N, endpoint=False)
        hs = [int(t) % N for t in self._notes]

        l1 = 0.5
        l2 = 0.25
        s1 = 0.95
        s2 = 0.5

        n_colors = len(hs)
        n_gradients = M

        colors = np.zeros((n_colors, n_gradients, 3), 'float')

        def _rgb_gradient(n, c1, c2):
            out = []
            for i in range(n):
                out.append(rgb_shader(i * n / (n - 1), 0, n, c1, c2))
            return np.array(out)

        for i in range(n_colors):
            colors[i] = _rgb_gradient(n_gradients, cs.hls_to_rgb(h[hs[i]], l1, s1), cs.hls_to_rgb(h[hs[i]], l2, s2))

        x_margins = 0.5
        w = 3
        y_margins = 1.5
        h = 1

        h_text = 1

        x_min = 0
        x_max = (x_margins+w)*n_gradients-x_margins
        y_min = 0 - h_text
        y_max = (y_margins+h)*n_colors-y_margins+h_text

        if ax is None:
            fig, ax = get_figure((x_max - x_min)/2, (y_max - y_min)/2, 72)

        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

        for i in range(n_colors):
            for j in range(n_gradients):
                rect = plt.Rectangle(((w+x_margins)*j, (h+y_margins)*i), w, h, color=colors[n_colors-i-1, j])
                ax.add_patch(rect)
                ax.annotate(
                    s=float2hex(colors[n_colors - i - 1, j]),
                    xy=((x_margins + w) * j + w / 2, (y_margins + h) * i - h_text / 2),
                    va='center',
                    ha='center'
                )
        if title:
            ax.annotate(
                s=title + ' ' + ''.join([f'{k}/{N} ' for k in hs]),
                xy=(((x_margins+w)*n_gradients-x_margins)/2, (y_margins+h)*n_colors-y_margins+h_text/2),
                ha='center',
                va='center'
            )


class Tonnetz(_NoteList):
    def __init__(self):
        super().__init__()

    def plot(self, n_x=11, n_y=11, enharmonic=True, upside_down=False, center_note=Note(), color_style='note', tds_on=False, ax=None, title=None):
        # get note colors
        self._get_note_color(color_style)

        # get note texts
        self._get_note_text(color_style)

        if ax is None:
            fig, ax = get_figure(24, 24, 72)

        # get background notes
        itv_gen = (Note(NAMED_STR_GEN[1]) - Note(NAMED_STR_GEN[0])).normalize()
        itv_maj = (Note(NAMED_STR_LIN[CHORD_STEP_LIN]) - Note(NAMED_STR_LIN[0])).normalize()
        itv_min = itv_gen - itv_maj

        if upside_down:
            notes_bg = np.array(
                [
                    [
                        center_note + kx * itv_gen + ky * itv_min for kx in range(-(n_x // 2), n_x // 2 + 1)
                    ] for ky in range(-(n_y // 2), n_y // 2 + 1)
                ]
            ).reshape([-1])
        else:
            notes_bg = np.array(
                [
                    [
                        center_note + kx * itv_gen + ky * itv_maj for kx in range(-(n_x // 2), n_x // 2 + 1)
                    ] for ky in range(-(n_y // 2), n_y // 2 + 1)
                ]
            ).reshape([-1])

        for note in notes_bg:
            if all([N == 12, G == 7, S == 5]) and tds_on:
                tds = ['T', 'D', 'S'][int(note - center_note) % 3]
                note.set_message(face_color=tds_colors(tds))
            else:
                note.set_message(face_color='white')

        # get background note positions
        step_x = 3
        step_y = 3 ** (1 / 2) * step_x / 2
        offset_x = step_x / 2

        notes_bg_xy = np.array(
            [
                [
                    [0 + kx * step_x + ky * offset_x, ky * step_y]  for kx in range(-(n_x // 2), n_x // 2 + 1)
                ] for ky in range(-(n_y // 2), n_y // 2 + 1)
            ]
        ).reshape([-1, 2])

        # plot
        notes_nnrel = [int(note) % N for note in self._notes]
        notes_vec2 = [note.get_vector(return_register=False) for note in self._notes]

        for cur_note, cur_xy in zip(notes_bg, notes_bg_xy):
            circ = plt.Circle(cur_xy, step_x / 3, facecolor=cur_note.get_message('face_color'), edgecolor='black')
            ax.add_patch(circ)

            if enharmonic:
                if_chosen = int(cur_note) % N in notes_nnrel
            else:
                if_chosen = cur_note.get_vector(return_register=False) in notes_vec2

            if if_chosen:
                idx = notes_nnrel.index(int(cur_note) % N)
                text = self._notes[idx].get_message('text')
                face_color = self._notes[idx].get_message('face_color')
                edge_color = self._notes[idx].get_message('edge_color')
                text_color = self._notes[idx].get_message('text_color')

                circ = plt.Circle(cur_xy, step_x / 4, facecolor=face_color, edgecolor=edge_color)
                ax.add_patch(circ)
                s = cur_note.get_name(show_register=False) if color_style == 'note' else cur_note.get_name(show_register=False) + f'({text})'
                ax.annotate(s, cur_xy, color=text_color, va='center', ha='center')
            else:
                ax.annotate(cur_note.get_name(show_register=False), cur_xy, color='black', va='center', ha='center')

        x_max = step_x * (n_x - 1 - n_x // 2 + (n_y - 1 - n_y // 2) / 2 + 1)
        y_max = step_y * (n_y - 1 - n_y // 2 + 1)
        ax.set_xlim([-x_max, x_max])
        ax.set_ylim([-y_max, y_max])

        if title is not None:
            ax.set_title(title)


''' ----------------------------------------------------------------------------------------- '''
''' ****************************** advanced instrument classes ****************************** '''
''' ----------------------------------------------------------------------------------------- '''


# TODO: make `Pianoroll` works again
class Pianoroll(object):
    def __init__(self, sheet, ticks_per_beat):
        """ pianoroll initialization, extract messages of same kind from sheet """
        # [01] get data
        self._sheet = sheet
        self._ticks_per_beat = ticks_per_beat
        self._max_ticks = max_ticks(sheet)

        self._pianoroll_exists = False

        # [02] get notes
        self._get_notes()

        # [03] get set_tempos
        self._get_set_tempos()

        # [04] get time_signatures
        self._get_time_signatures()

        # [05] get control_changes
        self._get_control_changes()

        # [06] get pitchwheels
        self._get_pitchwheels()

        # [07] set_vector default intervals
        self._set_intervals()

        # [08] set_vector default track colors
        self._set_track_colors()

        # [09] get lyrics
        self._get_lyrics()

    def _get_notes(self):
        self._notes = [[msg for msg in msglist if msg['type'] == 'note'] for msglist in self._sheet]
        # sort by channels, not tracks
        self._notes_c = [[msg for msg in sum(self._sheet, []) if msg['type'] == 'note' and msg['channel'] == k] for k in range(16)]

    def _get_set_tempos(self):
        self._set_tempos = [msg for msg in sum(self._sheet, []) if msg['type'] == 'set_tempo']
        self._set_tempos.sort(key=lambda msg: msg['time'])

        if self._set_tempos == []:
            self._set_tempos.insert(0, dict(type='set_tempo', tempo=500000, time=0))

        tempos = [msg['tempo'] for msg in self._set_tempos]
        self._bpm_range = (round(tempo2bpm(max(tempos))), round(tempo2bpm(min(tempos))))
        if self._bpm_range[1]-self._bpm_range[0]<1e-2:
            self._bpm_is_const = True
        else:
            self._bpm_is_const = False

    def _get_time_signatures(self):
        self._time_signatures = [msg for msg in sum(self._sheet, []) if msg['type'] == 'time_signature']
        self._time_signatures.sort(key=lambda msg: msg['time'])

        if self._time_signatures == [] or self._time_signatures[0]['time'] > 0:
            self._time_signatures.insert(0, dict(type='time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))

    def _get_control_changes(self):
        self._control_changes = [[msg for msg in msglist if msg['type'] == 'control_change'] for msglist in self._sheet]
        _ = [msglist.sort(key=lambda msg: msg['time']) for msglist in self._control_changes]
        self._used_controls = [list({msg['control'] for msg in msglist}) for msglist in self._control_changes]

        print('used controls:')
        for k, msglist in enumerate(self._used_controls):
            print(f'msglist {k}: {msglist}')
        print('')

    def _get_pitchwheels(self):
        self._pitchwheels = [[msg for msg in msglist if msg['type'] == 'pitchwheel'] for msglist in self._sheet]
        _ = [msglist.sort(key=lambda msg: msg['time']) for msglist in self._pitchwheels]

    def _set_intervals(self):
        self._time_interval = None
        self._note_interval = None

    def _set_track_colors(self):
        n_track = len(self._sheet)
        self._track_colors = [hsv_shader(t, 0, n_track + 1) for t in range(n_track)]

    def _get_lyrics(self):
        self._lyrics = [[msg for msg in msglist if msg['type'] == 'lyrics'] for msglist in self._sheet]
        _ = [msglist.sort(key=lambda msg: msg['time']) for msglist in self._lyrics]

    # ---------------------------------------------------------------------------------------------------- #

    def use_default_intervals(self):
        self._time_interval = (0, max(self._max_ticks))
        self._note_interval = (48, 72)
        self._pianoroll_exists = False
        plt.clf()

    def set_intervals(self, time_interval=None, note_interval=None):
        if time_interval:
            if time_interval[0] > time_interval[1]:
                raise ValueError('`time_interval[0]` should not larger than `time_interval[1]`!')
            else:
                self._time_interval = time_interval
        if note_interval:
            if note_interval[0] > note_interval[1]:
                raise ValueError('`note_interval[0]` should not larger than `note_interval[1]`!')
            else:
                self._note_interval = note_interval

        self._pianoroll_exists = False
        plt.clf()

    def set_track_color(self, track, color):
        self._track_colors[track] = color

    def _set_whdpi(self, width, height, dpi):
        pass

    def _set_hadpi(self, height, aspect_note, dpi):
        pass

    def draw_pianoroll(self, height=8, aspect_note=4, dpi=72, splits_per_beat=4, type='piano'):
        """

        Draw pianoroll with meta information.

        * variable's name ending with 's' means it is a list (multi variables)
        * list variable's name ending with '0' means it may contain messages whose time is out of time_interval

        Some abbreviations:

        * note              -> note
        * set_tempo         -> st
        * time_signature    -> ts
        * control_change    -> cc
        * pitchwheel        -> pw

        """

        ''' [00] intervals check '''

        if self._time_interval == None or self._note_interval == None:
            raise ValueError('Please set_vector intervals at first. You can use `use_default_intervals()` or `set_intervals()` to finish this job.')
        else:
            self._pianoroll_exists = True
            plt.clf()

        ''' [01] pianoroll meta params '''

        bottom_lane_h = 5
        self._bottom_lane_h = bottom_lane_h
        top_lane_h = 3

        bottom = self._note_interval[0] - bottom_lane_h
        self._bottom = bottom
        top = self._note_interval[1] + top_lane_h

        aspect_keyboard = {'piano': 4, 'drum': 6, 'agtc': 6}[type]

        width = height * (aspect_keyboard + aspect_note * length(*self._time_interval) / self._ticks_per_beat) / (top - bottom)
        axis_ratio = (aspect_keyboard / aspect_note * self._ticks_per_beat + length(*self._time_interval)) / (aspect_keyboard + aspect_note * length(*self._time_interval) / self._ticks_per_beat)
        keyboard_width = aspect_keyboard * axis_ratio

        left = self._time_interval[0] - keyboard_width
        right = self._time_interval[1]

        fontsize = 49*height/(length(*self._note_interval) + bottom_lane_h + top_lane_h)
        self._fontsize = fontsize
        markersize = 25*height/(length(*self._note_interval) + bottom_lane_h + top_lane_h)
        self._markersize = markersize

        ''' [02] set_tempos parsing '''

        sts0 = [[msg['time'], msg['tempo']] for msg in self._set_tempos]
        k_left = len(sts0)-1- [pw[0] <= self._time_interval[0] for pw in sts0][::-1].index(True)
        k_right = len(sts0)-1- [pw[0] <= self._time_interval[1] for pw in sts0][::-1].index(True)
        sts = [[self._time_interval[0], sts0[k_left][1]]] + [pw for pw in sts0 if self._time_interval[0] < pw[0] < self._time_interval[1]] + [[self._time_interval[1], sts0[k_right][1]]]

        ''' [03] time_signatures parsing '''

        # put all time_signatures into a list and append an end to the list
        tss0 = [[msg['time'], msg['numerator'], msg['denominator']] for msg in self._time_signatures]
        tss0.append([self._time_interval[1], tss0[-1][1], tss0[-1][2]])
        tss = [ts for ts in tss0 if within(ts[0], *self._time_interval)]
        # get a list of ticks_per_beat corresponding to time_signatures (because tpb changes with ts denominator)
        tpbs0 = [4 * self._ticks_per_beat // ts[2] for ts in tss0]
        # calculate delta x of three types of vertical line: bar-line, beat-line and split-line
        # step1 and step2 are changing with time_signatures, so they become step1s and step2s
        # step1: bar-line | step2: beat-line | step3: split-line
        # step1[k] = 4*self.ticks_per_beat*(nu[k]/de[k])
        # step2[k] = 4*self.ticks_per_beat*(1/de[k])
        step1s = [tpb*tss0[i][1] for (i, tpb) in enumerate(tpbs0)]
        step2s = tpbs0
        step3 = self._ticks_per_beat // splits_per_beat
        # x1s0 = [range(stt_0, stt_1, step1s[0]), range(stt_1, stt_2, step1s[1]), ..., range(stt_n, self.time_interval[1], step1s[n])]
        # x1s0[n][k] is x of the k-th bar-line after n-th time_signature
        x1s0 = [list(range(tss0[k][0], tss0[k+1][0], step1s[k])) for k in range(len(step1s)-1)]
        x1s = [x1 for x1 in sum(x1s0, []) if within(x1, *self._time_interval)]
        x2s0 = [list(range(tss0[k][0], tss0[k+1][0], step2s[k])) for k in range(len(step2s)-1)]
        x2s = [x2 for x2 in sum(x2s0, []) if within(x2, *self._time_interval) and x2 not in x1s]
        x3s0 = [k * step3 for k in range(self._time_interval[0] // step3, self._time_interval[1] // step3 + 1)]
        x3s = [x3 for x3 in x3s0 if within(x3, *self._time_interval) and x3 not in x1s + x2s]
        # l1s0: bar labels with x coord | l2s0: beat labels with x coord
        l1s0 = list(enumerate(sum(x1s0, [])))
        l1s = [l1[0] for l1 in l1s0 if l1[1] in x1s]
        l2s0 = sum([[[j % tss0[i][1], x2] for (j, x2) in enumerate(x2s0_section)] for (i, x2s0_section) in enumerate(x2s0)], [])
        l2s = [l2[0] for l2 in l2s0 if l2[1] in x2s]

        # ---------------------------------------------------------------------------------------------------- #

        ''' [01] draw pianoroll '''

        # initializing
        fig, ax = get_figure(width, height, dpi)
        # the largest rectangle
        largest_rect = plt.Rectangle((left, bottom), right-left, top-bottom, facecolor='none', edgecolor='#555555', lw=0.75, joinstyle='round', zorder=7)
        ax.add_patch(largest_rect)
        # bottom lane rectangle
        bl_rect = plt.Rectangle((self._time_interval[0], bottom), length(*self._time_interval), bottom_lane_h, facecolor='#ddeeff', lw=0.0, zorder=0)
        self._bl_rect = bl_rect
        ax.add_patch(bl_rect)
        # main area rectangle
        main_rect = plt.Rectangle((self._time_interval[0], self._note_interval[0]), length(*self._time_interval), length(*self._note_interval), facecolor='#ddeeff', lw=0.0, zorder=0)
        self._main_rect = main_rect
        ax.add_patch(main_rect)
        # top lane rectangle
        tl_rect = plt.Rectangle((left, self._note_interval[1]), right - left, top_lane_h, facecolor='#ffffff', lw=0.0, zorder=0)
        ax.add_patch(tl_rect)
        # background keys
        white_notes = [note for note in range(*self._note_interval) if note % 12 in [0, 2, 4, 5, 7, 9, 11]]
        black_notes = [note for note in range(*self._note_interval) if note % 12 in [1, 3, 6, 8, 10]]
        white_bg_rects = [plt.Rectangle((self._time_interval[0], note), length(*self._time_interval), 1, facecolor='#ffffff', lw=0.0, zorder=1) for note in white_notes]
        black_bg_rects = [plt.Rectangle((self._time_interval[0], note), length(*self._time_interval), 1, facecolor='#ddcccc', lw=0.0, zorder=1) for note in black_notes]
        _ = [ax.add_patch(rect) for rect in white_bg_rects+black_bg_rects]
        # left bottom rectangle
        lb_rect = plt.Rectangle((left, bottom), keyboard_width, bottom_lane_h, facecolor='#ffffff', lw=0.0, zorder=4)
        ax.add_patch(lb_rect)
        if self._bpm_is_const:
            text = f'bpm\n{self._bpm_range[0]}\n\nvel\n0..127'
        else:
            text = f'bpm\n{self._bpm_range[0]}..{self._bpm_range[1]}\n\nvel\n0..127'
        plt.annotate(text, (left + keyboard_width / 2, bottom + bottom_lane_h / 2), color='#555555',
                     va='center', ha='center', fontsize=fontsize, zorder=4.1, clip_path=lb_rect)
        # keyboard
        white_kbd_rects = [plt.Rectangle((left, note), keyboard_width, 1, facecolor='#ffffff', lw=0.0, zorder=4) for note in white_notes]
        black_kbd_rects = [plt.Rectangle((left, note), keyboard_width, 1, facecolor='#222222', lw=0.0, zorder=4) for note in black_notes]
        _ = [ax.add_patch(rect) for rect in white_kbd_rects+black_kbd_rects]
        # split lines of keys
        _ = [plt.plot([left, self._time_interval[0]], [note, note], color='#222222', lw=0.5, solid_capstyle='butt', zorder=4.1) for note in range(*self._note_interval)]
        # text on keys
        _ = [plt.annotate(note2label(note, type=type), (left+keyboard_width//16, note+0.5), color='#555555', va='center', fontsize=fontsize, zorder=4.1,
                          clip_path=white_kbd_rects[k]) for (k, note) in enumerate(white_notes)]
        _ = [plt.annotate(note2label(note, type=type), (left+keyboard_width//16, note+0.5), color='#ffffff', va='center', fontsize=fontsize, zorder=4.1,
                          clip_path=black_kbd_rects[k]) for (k, note) in enumerate(black_notes)]
        # horizontal grid lines
        _ = [plt.plot(self._time_interval, [note, note], color='#999999', lw=0.5, solid_capstyle='butt', zorder=2) for note in range(self._note_interval[0] + 1, self._note_interval[1])]
        # vertical grid lines
        _ = [plt.plot([x, x], [bottom, self._note_interval[1]], color='#aaaaaa', lw=0.5, solid_capstyle='butt', zorder=2.1) for x in x3s]
        _ = [plt.plot([x, x], [bottom, self._note_interval[1]], color='#555555', lw=0.5, solid_capstyle='butt', zorder=2.1) for x in x2s]
        _ = [plt.plot([x, x], [bottom, self._note_interval[1]], color='#222222', lw=1.0, solid_capstyle='butt', zorder=2.1) for x in x1s]
        # horizontal split lines
        plt.plot(self._time_interval, [self._note_interval[0], self._note_interval[0]], color='#555555', lw=0.5, solid_capstyle='butt', zorder=6.1)
        plt.plot([left, self._time_interval[1]], [self._note_interval[1], self._note_interval[1]], color='#555555', lw=0.5, solid_capstyle='butt', zorder=6.1)
        plt.plot([left, self._time_interval[1]], [self._note_interval[1] + 1, self._note_interval[1] + 1], color='#555555', lw=0.5, solid_capstyle='butt', zorder=6.1)
        plt.plot([left, self._time_interval[1]], [self._note_interval[1] + 2, self._note_interval[1] + 2], color='#555555', lw=0.5, solid_capstyle='butt', zorder=6.1)
        # vertical split lines
        plt.plot([self._time_interval[0], self._time_interval[0]], [bottom, self._note_interval[1]], color='#555555', lw=0.5, solid_capstyle='butt', zorder=6)

        ''' [02] draw set_tempos '''

        if not self._bpm_is_const:
            def _bpm2vel(bpm):
                bpm_lower = self._bpm_range[0]
                bpm_upper = self._bpm_range[1]
                lam = (bpm_upper - bpm) / (bpm_upper - bpm_lower)
                return lam * (self._note_interval[0] - bottom_lane_h) + (1 - lam) * self._note_interval[0]
            sts_x = [st[0] for st in sts]
            sts_y = [_bpm2vel(tempo2bpm(st[1])) for st in sts]
            plot = plt.step(sts_x, sts_y, color='#ee5511', lw=1.0, solid_capstyle='butt', solid_joinstyle='bevel', where='post', zorder=2.9, label='tempo')
            _ = [p.set_clip_path(bl_rect) for p in plot]

        ''' [03] draw time_signatures '''

        # time_signature labels
        _ = [plt.annotate(f'{ts[1]}/{ts[2]}', (ts[0], self._note_interval[1] + 1.5), color='#555555', va='center', ha='center', fontsize=fontsize) for ts in tss]
        # bar labels
        _ = [plt.annotate(l1, (x1, self._note_interval[1] + 2.5), color='#555555', va='center', ha='center', fontsize=fontsize) for (x1, l1) in zip(x1s, l1s)]
        # beat labels
        _ = [plt.annotate(l2, (x2, self._note_interval[1] + 2.5), fontsize=fontsize * 3 / 4, color='#555555', va='center', ha='center') for (x2, l2) in zip(x2s, l2s)]

    def _draw_notes(self, track=0, shader=rgb_shader, type='piano', alpha=1.0, lyric=None):
        """ draw notes """

        ''' pianoroll checking '''

        if not self._pianoroll_exists:
            raise ValueError('You should draw a pianoroll first using `draw_pianoroll()` method!')

        ''' notes parsing '''

        # divide notes both in note_interval and time_interval into 3 parts: left, full and right
        notes0 = [note for note in self._notes[track] if within(note['note'], *self._note_interval)]
        notes = [note for note in notes0 if within(note['time1'], *self._time_interval) or within(note['time1'] + note['time2'], *self._time_interval)]
        notes_full = [note for note in notes if within(note['time1'], *self._time_interval) and within(note['time1'] + note['time2'], *self._time_interval)]
        notes_left = [note for note in notes if note['time1'] < self._time_interval[0] <= note['time1'] + note['time2']]
        notes_right = [note for note in notes if note['time1'] < self._time_interval[1] <= note['time1'] + note['time2']]
        notes_rearranged = notes_full + notes_left + notes_right
        # getting rectangles of notes for pianoroll
        notes_full_rects = [plt.Rectangle((note['time1'], note['note']), note['time2'], 1,
                                          color=shader(note['velocity_on'], 0, 127), joinstyle='round', lw=0.0, alpha=alpha, zorder=5+0.001*track) for note in notes_full]
        notes_left_rects = [plt.Rectangle((self._time_interval[0], note['note']), note['time2'] - self._time_interval[0] + note['time1'], 1,
                                          color=shader(note['velocity_on'], 0, 127), joinstyle='round', lw=0.0, alpha=alpha, zorder=5+0.001*track) for note in notes_left]
        notes_right_rects = [plt.Rectangle((note['time1'], note['note']), self._time_interval[1] - note['time1'], 1,
                                           color=shader(note['velocity_on'], 0, 127), joinstyle='round', lw=0.0, alpha=alpha, zorder=5+0.001*track) for note in notes_right]
        notes_rects = notes_full_rects + notes_left_rects + notes_right_rects

        ''' draw notes '''

        ax = plt.gca()
        _ = [ax.add_patch(rect) for rect in notes_rects]
        # note edge
        _ = [plt.plot([note['time1'], note['time1']+note['time2'], note['time1']+note['time2'], note['time1'], note['time1']],
                      [note['note'], note['note'], note['note']+1, note['note']+1, note['note']],
                      color='#123456', lw=0.5, solid_capstyle='round', alpha=alpha, zorder=5+0.001*(track+0.2)) for note in notes_full]
        _ = [plt.plot([self._time_interval[0], note['time1'] + note['time2'], note['time1'] + note['time2'], self._time_interval[0]],
                      [note['note'], note['note'], note['note']+1, note['note']+1],
                      color='#123456', lw=0.5, solid_capstyle='round', alpha=alpha, zorder=5+0.001*(track+0.2)) for note in notes_left]
        _ = [plt.plot([self._time_interval[1], note['time1'], note['time1'], self._time_interval[1]],
                      [note['note']+1, note['note']+1, note['note'], note['note']],
                      color='#123456', lw=0.5, solid_capstyle='round', alpha=alpha, zorder=5+0.001*(track+0.2)) for note in notes_right]
        # note label
        if type == 'lyric':
            _ = [plt.annotate(note['lyric'], (note['time1'] + self._ticks_per_beat // 16, note['note'] + 0.5),
                              color='#ffffff', va='center', fontsize=self._fontsize, alpha=alpha, zorder=5 + 0.001 * (track + 0.1),
                              clip_path=notes_rects[k]) for (k, note) in enumerate(notes_rearranged)]
        else:
            _ = [plt.annotate(note2label(note['note'], type=type, show_group=False), (note['time1'] + self._ticks_per_beat // 16, note['note'] + 0.5),
                              color='#ffffff', va='center', fontsize=self._fontsize, alpha=alpha, zorder=5 + 0.001 * (track + 0.1),
                              clip_path=notes_rects[k]) for (k, note) in enumerate(notes_rearranged)]
        # on-velocity
        notes_full_vels = [plt.Line2D([note['time1'], note['time1']], [self._bottom, self._bottom + note['velocity_on'] / 127 * self._bottom_lane_h],
                                      color=shader(note['velocity_on'], 0, 127), lw=1.0, solid_capstyle='butt', alpha=alpha, zorder=3+0.001*track,
                                      marker='x', markevery=[1], markersize=self._markersize, mew=1) for note in notes_full + notes_right]
        _ = [ax.add_line(vel) for vel in notes_full_vels]
        _ = [vel.set_clip_path(self._bl_rect) for vel in notes_full_vels]
        # lyric
        if lyric:
            _ = [plt.annotate(lyric[k], (note['time1']+self._ticks_per_beat//16, note['note']-0.5),
                            color='#555555', va='center', fontsize=self._fontsize*3/4, zorder=5+0.001*(track+0.1)) for (k, note) in enumerate(notes) if k<len(lyric)]

    def draw_notes(self, tracks=(0,), color_scheme='velocity', type='piano', alpha=1.0, lyric=None):
        if color_scheme == 'velocity':
            _ = [self._draw_notes(t, rgb_shader, type, alpha, lyric) for t in tracks]
        elif color_scheme == 'track':
            _ = [self._draw_notes(t, lambda x, x_min, x_max: cst_shader(x, x_min, x_max, self._track_colors[t]), type, alpha, lyric) for t in tracks]

    def draw_control_changes(self, track=0, controls=(64, ), plot_type='stair', alpha=1.0):
        """ draw control_changes """

        ''' pianoroll checking '''

        if not self._pianoroll_exists:
            raise ValueError('You should draw a pianoroll first using `draw_pianoroll()` method!')

        ''' control_changes parsing '''

        ccs0 = dict.fromkeys(controls, [])
        ccs = dict.fromkeys(controls, [])
        for control in controls:
            ccs0[control] = [[msg['time'], msg['value']] for msg in self._control_changes[track] if msg['control'] == control]
            # add default value
            ccs0[control].insert(0, [0, 0])
            k_left = len(ccs0[control])-1- [cc[0] <= self._time_interval[0] for cc in ccs0[control]][::-1].index(True)
            k_right = len(ccs0[control])-1- [cc[0] <= self._time_interval[1] for cc in ccs0[control]][::-1].index(True)
            ccs[control] = [[self._time_interval[0], ccs0[control][k_left][1]]] + \
                           [cc for cc in ccs0[control] if self._time_interval[0] < cc[0] < self._time_interval[1]] + \
                           [[self._time_interval[1], ccs0[control][k_right][1]]]

        ''' draw control_changes '''

        ccs_stts = dict.fromkeys(controls, [])
        ccs_values = dict.fromkeys(controls, [])
        for i, control in enumerate(controls):
            ccs_stts[control] = [cc[0] for cc in ccs[control]]
            ccs_values[control] = [cc[1] / 127 * length(*self._note_interval) + self._note_interval[0] for cc in ccs[control]]

            color1 = cs.rgb_to_hsv(*self._track_colors[track])
            color2 = [color1[0], color1[1]/10, color1[2]/10]
            color = hsv_shader(i, 0, len(controls), color1, color2)
            if plot_type == 'piecewise':
                plot = plt.plot(ccs_stts[control], ccs_values[control], color=color, alpha=alpha,
                                lw=0.75, ls='--', dash_capstyle='butt', dash_joinstyle='bevel', zorder=2.9+0.001*(track+0.1*control),
                                clip_path=self._main_rect, label=f'[track {track}] {CC_NAMES[control]}')
                _ = [p.set_clip_path(self._main_rect) for p in plot]
            elif plot_type == 'stair':
                plot = plt.step(ccs_stts[control], ccs_values[control], color=color, alpha=alpha,
                                lw=0.75, ls='--', dash_capstyle='butt', dash_joinstyle='bevel', zorder=2.9+0.001*(track+0.1*control),
                                where='post', clip_path=self._main_rect, label=f'[track {track}] {CC_NAMES[control]}')
                _ = [p.set_clip_path(self._main_rect) for p in plot]
            elif plot_type == 'stair_fill':
                plot = plt.fill_between(ccs_stts[control], ccs_values[control], self._note_interval[0],
                                        color=color, alpha=alpha, step='post', lw=0.75, linestyle='--',
                                        capstyle='butt', joinstyle='bevel', zorder=2.9+0.001*(track+0.1*control),
                                        clip_path=self._main_rect, label=f'[track {track}] {CC_NAMES[control]}')
                plot.set_clip_path(self._main_rect)
            else:
                pass

    def _draw_pitchwheels(self, track=0, shader=cst_shader, plot_type='stair', alpha=1.0):
        """ draw pitchwheels """

        ''' pianoroll checking '''

        if not self._pianoroll_exists:
            raise ValueError('You should draw a pianoroll first using `draw_pianoroll()` method!')

        ''' pitchwheels parsing '''

        pws0 = [[msg['time'], msg['pitch']] for msg in self._pitchwheels[track]]
        # add default value
        pws0.insert(0, [0, 0])
        k_left = len(pws0)-1- [pw[0] <= self._time_interval[0] for pw in pws0][::-1].index(True)
        k_right = len(pws0)-1- [pw[0] <= self._time_interval[1] for pw in pws0][::-1].index(True)
        pws = [[self._time_interval[0], pws0[k_left][1]]] + [pw for pw in pws0 if self._time_interval[0] < pw[0] < self._time_interval[1]] + [[self._time_interval[1], pws0[k_right][1]]]

        ''' draw pitchwheels '''

        pws_stts = [pw[0] for pw in pws]
        pws_pits = [pw[1] / 16384 * length(*self._note_interval) + middle(*self._note_interval) for pw in pws]
        if plot_type == 'piecewise':
            plot = plt.plot(pws_stts, pws_pits, color=shader(0), lw=1.0, solid_capstyle='butt', solid_joinstyle='bevel', alpha=alpha,
                            zorder=2.9+0.001*track, label=f'[track {track}] pitchwheel')
            _ = [p.set_clip_path(self._main_rect) for p in plot]
        elif plot_type == 'stair':
            plot = plt.step(pws_stts, pws_pits, color=shader(0), lw=1.0, solid_capstyle='butt', solid_joinstyle='bevel', alpha=alpha,
                            where='post', zorder=2.9+0.001*track, label=f'[track {track}] pitchwheel')
            _ = [p.set_clip_path(self._main_rect) for p in plot]
        elif plot_type == 'stair_fill':
            plot = plt.fill_between(pws_stts, pws_pits, middle(*self._note_interval),
                                    color=shader(0), lw=1.0, capstyle='butt', joinstyle='bevel', alpha=alpha, step='post',
                                    zorder=2.9+0.001*track, label=f'[track {track}] pitchwheel')
            plot.set_clip_path(self._main_rect)
        else: pass

    def draw_pitchwheels(self, tracks=(0,), plot_type='stair', alpha=1.0):
        _ = [self._draw_pitchwheels(t, lambda x: cst_shader(x, 0, 1, self._track_colors[t]), plot_type, alpha) for t in tracks]

    def show_legends(self):
        l = plt.legend(loc='lower right', fontsize=self._fontsize)
        l.set_zorder(20)

    def show_chords(self, times, chords):
        """ show chords """

        ''' pianoroll checking '''

        if not self._pianoroll_exists:
            raise ValueError('You should draw a pianoroll first using `draw_pianoroll()` method!')

        ''' chords parsing '''

        chords0 = list(zip(times, chords))

        ''' show chords '''

        chords = [chord for chord in chords0 if within(chord[0], *self._time_interval)]
        _ = [plt.annotate(chord[1], (chord[0], self._note_interval[1] + 0.5), color='#555555', va='center', ha='center', fontsize=self._fontsize) for chord in chords]

    # ---------------------------------------------------------------------------------------------------- #

    def save(self, savepath):
        plt.savefig(Path(savepath))
        plt.close()

    # ---------------------------------------------------------------------------------------------------- #

    def get_tick_range_s(self, track):
        # get tick range (single track)
        return 0, self._max_ticks[track]

    def get_tick_range_m(self, tracks):
        # get tick range (multiple track)
        return 0, max([self._max_ticks[track] for track in tracks])

    def get_tick_range_a(self):
        # get tick range (all tracks)
        return 0, max(self._max_ticks)

    def get_note_range_sg(self, track):
        # get note range (single track, global)
        notes = [note['note'] for note in self._notes[track]]
        note_min = min(notes) - 1 if notes != [] else 48
        note_max = max(notes) + 2 if notes != [] else 72
        return note_min, note_max

    def get_note_range_mg(self, tracks):
        # get note range (multiple track, global)
        ranges = [self.get_note_range_sg(track) for track in tracks]
        note_min = min([r[0] for r in ranges])
        note_max = max([r[1] for r in ranges])
        return note_min, note_max

    def get_note_range_sl(self, track):
        # get note range (single track, local)
        notes = [note['note'] for note in self._notes[track] if within(note['time1'], *self._time_interval) or within(note['time1'] + note['time2'], *self._time_interval)]
        note_min = min(notes) - 1 if notes != [] else 48
        note_max = max(notes) + 2 if notes != [] else 72
        return note_min, note_max

    def get_note_range_ml(self, tracks):
        # get note range (multiple track, local)
        ranges = [self.get_note_range_sl(track) for track in tracks]
        note_min = min([r[0] for r in ranges])
        note_max = max([r[1] for r in ranges])
        return note_min, note_max

    def get_used_controls(self, track):
        return self._used_controls[track]

    def get_set_tempos(self):
        return [[msg['time'], msg['tempo']] for msg in self._set_tempos]

    def get_key_frames(self, track, note=36, bpm=164, fps=60):
        time1s = [tick2second(msg['time1'], self._ticks_per_beat, bpm2tempo(bpm)) for msg in self._notes[track] if msg['note']==note]
        time2s = [tick2second(2*msg['time2'], self._ticks_per_beat, bpm2tempo(bpm)) for msg in self._notes[track] if msg['note']==note]
        time3s = [time1+time2 for time1, time2 in zip(time1s, time2s)]
        vels = [msg['velocity_on'] for msg in self._notes[track] if msg['note']==note]

        ons = [int(time1//(1/fps)) for time1 in time1s]
        ons.append(-1)
        offs = [int(time3//(1/fps)) for time3 in time3s]
        offs.append(-1)
        print(f'length: {len(ons)} | {ons}')
        print(f'length: {len(offs)} | {offs}')
        print(f'length: {len(vels)} | {vels}')

        return ons, offs, vels
