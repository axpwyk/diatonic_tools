import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from theories import *
from utils import *


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
    fig = plt.figure(figsize=(w, h), dpi=dpi, facecolor='white')
    fig.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=1.0, wspace=0.1, hspace=0.1)
    ax = fig.gca(aspect='equal')
    ax.set_axis_off()
    ax.margins(x=0.01, y=0.01)
    return fig, ax


''' ----------------------------------------------------------------------------------------- '''
''' ************************************ color utilities ************************************ '''
''' ----------------------------------------------------------------------------------------- '''


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
''' ******************************** basic instrument classes ******************************* '''
''' ----------------------------------------------------------------------------------------- '''


class _NoteList(object):
    def __init__(self):
        self._notes = []
        self._unique()

    def _unique(self):
        notes_unique = []
        for note in self._notes:
            notes_unique_nnrels = [note.get_nnrel() for note in notes_unique]
            if note.get_nnrel() not in notes_unique_nnrels:
                notes_unique.append(note)

        self._notes = notes_unique

    def set_notes(self, notes):
        self._notes = [note for note in notes if isinstance(note, Note)]
        self._unique()
        return self

    def add_notes(self, notes):
        self._notes = self._notes + [note for note in notes if isinstance(note, Note)]
        self._unique()
        return self

    def del_notes(self):
        self._notes = []
        return self

    def _get_note_text(self, text_style):
        if text_style == 'note':
            for note in self._notes:
                note.set_message(text=note.get_name())
        elif text_style in ['br357t', 'degree', 'avoid']:
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

        # prepare useful ndarrays
        open_string_nnabs = np.expand_dims(np.array([int(note) for note in open_string_notes]), axis=0)  # shape = [1, n_strings]
        fret_delta_nnabs = np.expand_dims(np.arange(0, max_fret + 1), axis=1)  # shape = [n_frets, 1]
        fretboard_nnabs = open_string_nnabs + fret_delta_nnabs  # shape = [n_frets, n_strings]

        # basic properties of this guitar instance
        self._modulo_on = modulo_on  # if ignore register of note
        self._max_fret = max_fret  # max fret number (starting from 0)
        self._max_string = len(open_string_notes)  # max string number (starting from 0, lowest string)
        self._open_string_notes = list(open_string_notes)  # save open string notes to instance attribute

        # open string nnabs and fretboard nnabs
        self._open_string_nnabs = open_string_nnabs
        self._fretboard_nnabs = fretboard_nnabs

        # w to h ratio of fretboard
        self._w_to_h_ratio = w_to_h_ratio

        # fret markers
        self._short_fret_markers = short_fret_markers
        self._long_fret_markers = long_fret_markers

    def _get_note_with_indices(self, selection):
        """
        get notes and their indices of fretboard matrix

        :param selection: str type, e.g. 'x32010'

        :return: note_list, indices_list, used_strings
        """
        note_list, indices_list, used_strings =  [], [], []

        # check every note in `self._notes`
        for i, note in enumerate(self._notes):
            # gather all matching notes on fretboard
            if self._modulo_on:
                indices = np.stack(np.where(self._fretboard_nnabs % N == int(note) % N), axis=-1)  # [?, 2]
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

    def auto_select(self, max_span=4, use_open_string=False, highest_bass_string=2, top_note=None, lowest_soprano_string=-3):
        """
        select pressed notes automatically

        :param max_span: int type, maximum span of frets
        :param use_open_string: bool type, will check open strings at first
        :param highest_bass_string: int type, highest string of bass note or root note
        :param top_note: str type, br357t of highest note
        :param lowest_soprano_string: int type, lowest string of top note

        :return: list of selections, e.g. ['x3201x', 'x32010', ...], and their corresponding frets
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

        # get all chord diagrams
        chord_diagrams = []
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
                chord_diagram = np.zeros_like(fretboard_bool, np.bool)
                for fret, string in zip(frets, s2f.keys()):
                    chord_diagram[fret, string] = True

                chord_diagrams.append(chord_diagram)
                fret_positions.append(fret_position)

        print(f'Number of all chord diagrams: {len(chord_diagrams)}')

        # get real chord_diagrams and fret_positions
        chord_diagrams_filt = []
        fret_positions_filt = []
        for chord_diagram, fret_position in zip(chord_diagrams, fret_positions):
            # filters
            fretboard_nnrel_used = copy(fretboard_nnrel)
            fretboard_nnrel_used[~chord_diagram] = -1
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
                chord_diagram[:, :string_low] = False

            # 2. highest strings contain top note
            if top_note is not None:
                if nnrel_high not in fretboard_nnrel_used_high:
                    continue
                else:
                    string_high = lowest_soprano_string + np.where(fretboard_nnrel_used_high == nnrel_high)[1].max()
                    fretboard_nnrel_used_slice[:, string_high+1:] = -1
                    chord_diagram[:, string_high+1:] = False

            # 3. contains all notes
            if not all([k in fretboard_nnrel_used_slice for k in br357t_to_nnrels.values()]):
                continue

            chord_diagrams_filt.append(chord_diagram)
            fret_positions_filt.append(fret_position)

        # convert chord diagrams to str
        chord_diagrams_string = []
        fret_positions_string = []
        for cs, fp in zip(chord_diagrams_filt, fret_positions_filt):
            used_indices = np.stack(np.where(cs), axis=-1)
            cs_str = ['x'] * n_strings
            for fret, string in used_indices:
                cs_str[string] = np.base_repr(fret, N+max_span)
            cs_str = ''.join(cs_str).lower()

            if cs_str not in chord_diagrams_string:
                chord_diagrams_string.append(cs_str)
                fret_positions_string.append(fp)
            else:
                idx = chord_diagrams_string.index(cs_str)
                chord_diagrams_string.pop(idx)
                fret_positions_string.pop(idx)
                chord_diagrams_string.append(cs_str)
                fret_positions_string.append(fp)

        return chord_diagrams_string, fret_positions_string

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
            ax_w_to_h_ratio = w / h
            fig, ax = get_figure(FIG_HEIGHT * ax_w_to_h_ratio, FIG_HEIGHT)

        # add title if provided
        if title:
            # ax.set_title(title)
            ax.text(x=0.5, y=0.895, s=title, va='bottom', ha='center', transform=ax.transAxes)

        # plot fret markers
        for i in range(fret_left + 1, fret_right + 1):
            if i % N in long_fret_markers:
                rect = plt.Rectangle(
                    xy=(coord_fingers[i], coord_strings[0]),
                    width=coord_frets[i] - coord_fingers[i],
                    height=coord_strings[-1] - coord_strings[0],
                    color='gray',
                    alpha=0.2,
                    zorder=0
                )
                ax.add_patch(rect)
            elif i % N in short_fret_markers:
                rect = plt.Rectangle(
                    xy=(coord_fingers[i], middle(coord_strings[0], coord_strings[-1])),
                    width=coord_frets[i] - coord_fingers[i],
                    height=middle(coord_strings[0], coord_strings[-1]),
                    color='gray',
                    alpha=0.2,
                    zorder=0
                )
                ax.add_patch(rect)
            else:
                pass

        # plot frets (vertical lines)
        ax.set_xlim(coord_frets[fret_left] - w_to_h_ratio, coord_frets[fret_right] + w_to_h_ratio)
        _ = [
            ax.plot(
                (coord_frets[i], coord_frets[i]),
                (coord_strings[0], coord_strings[-1]),
                c='black',
                lw=2.0,
                zorder=1
            ) for i in range(fret_left, fret_right + 1)
        ]
        _ = [
            ax.annotate(
                s=i,
                xy=(coord_frets[i], -0.5),
                rotation=text_rotation,
                color='black',
                va='center',
                ha='center') for i in range(fret_left, fret_right + 1)
        ]

        # plot strings (horizontal lines)
        ax.set_ylim(coord_strings[0] - 1, coord_strings[-1] + 1)
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
                    s=note.get_message('text') if color_style != 'note' else note.get_name(),
                    xy=(coord_fingers[0] + coord_frets[fret_left], coord_strings[string]),
                    rotation=text_rotation,
                    color='black',
                    va='center',
                    ha='center',
                    zorder=4
                )
            # other fret dots
            elif within(fret, fret_left + 1, fret_right + 1):
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
                    s=note.get_message('text') if color_style != 'note' else note.get_name(),
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

    def plots(self, max_span=4, selections=('pppppp'), fret_positions=(0), text_rotation=0, color_style='note', title=None):
        # figure properties
        n_diagrams = len(selections)
        n_w = int(np.sqrt(n_diagrams))
        n_h = n_diagrams // n_w + 1

        # new figure
        fig = plt.figure(facecolor='white')

        # add title to figure
        suptitle = ''
        if title is not None:
            suptitle += title + '\n'
        suptitle += f"Tuning: {' '.join([note.get_name() for note in self._open_string_notes])}\n"
        fig.text(0.5, 1, suptitle, va='bottom', ha='center')

        # plots
        spec = gridspec.GridSpec(ncols=n_w, nrows=n_h, figure=fig)

        ax_w_to_h_ratio = 1
        for i, (chord_diagram, fret_position) in enumerate(zip(selections, fret_positions)):
            ax = fig.add_subplot(spec[i // n_w, i % n_w])
            ax.margins(0.0, 0.0)
            ax.set_axis_off()
            ax.set_aspect('equal')
            left = fret_position - 1 if fret_position > 0 else 0
            right = fret_position + max_span - 1 if fret_position > 0 else fret_position + max_span
            self.plot(left, right, chord_diagram, text_rotation, color_style, ax, chord_diagram)

            if i == 0:
                ax_size = ax.get_window_extent().size
                ax_w_to_h_ratio = ax_size[0] / ax_size[1]

        # figure settings
        k = 0
        fig_w_to_h_ratio = ax_w_to_h_ratio * n_w / (n_h + k)
        fig.subplots_adjust(0.0, 0.0, 1.0, 1.0, 0.0, 0.0)
        fig.set_figwidth(n_w * FIG_HEIGHT * fig_w_to_h_ratio)
        fig.set_figheight((n_h + k) * FIG_HEIGHT)

    def plot_all_chords(self, max_span=4, use_open_string=False, highest_bass_string=2, top_note=None, lowest_soprano_string=3, text_rotation=0, color_style='note', title=None):
        selections, fret_positions = self.auto_select(max_span=max_span, use_open_string=use_open_string, highest_bass_string=highest_bass_string, top_note=top_note, lowest_soprano_string=lowest_soprano_string)
        # figure properties
        n_diagrams = len(selections)
        n_w = int(np.sqrt(n_diagrams))
        n_h = n_diagrams // n_w + 1

        # new figure
        fig = plt.figure(facecolor='white')

        # add title to figure
        suptitle = ''
        if title is not None:
            suptitle += title + '\n'
        suptitle += f"Tuning: {' '.join([note.get_name() for note in self._open_string_notes])}\n"
        suptitle += f'use_open_string={use_open_string}\n'
        suptitle += f'highest_bass_string={self._max_string-highest_bass_string}'
        if top_note is not None:
            suptitle += f'\ntop_note={top_note} | lowest_soprano_string={self._max_string-lowest_soprano_string}'
        fig.text(0.5, 1, suptitle, va='bottom', ha='center')

        # plots
        spec = gridspec.GridSpec(ncols=n_w, nrows=n_h, figure=fig)

        ax_w_to_h_ratio = 1
        for i, (chord_diagram, fret_position) in enumerate(zip(selections, fret_positions)):
            ax = fig.add_subplot(spec[i//n_w, i%n_w])
            ax.margins(0.0, 0.0)
            ax.set_axis_off()
            ax.set_aspect('equal')
            left = fret_position - 1 if fret_position > 0 else 0
            right = fret_position + max_span - 1 if fret_position > 0 else fret_position + max_span
            self.plot(left, right, chord_diagram, text_rotation, color_style, ax, chord_diagram)

            if i == 0:
                ax_size = ax.get_window_extent().size
                ax_w_to_h_ratio = ax_size[0] / ax_size[1]

        # figure settings
        k = 0
        fig_w_to_h_ratio = ax_w_to_h_ratio * n_w / (n_h + k)
        fig.subplots_adjust(0.0, 0.0, 1.0, 1.0, 0.0, 0.0)
        fig.set_figwidth(n_w * FIG_HEIGHT * fig_w_to_h_ratio)
        fig.set_figheight((n_h + k) * FIG_HEIGHT)


class Piano(_NoteList):
    def __init__(self):
        super().__init__()

    def _get_note_range(self):
        notes = [int(note) for note in self._notes]
        return min(notes), max(notes)

    def plot_old(self, note_range=None, color_style='note', ax=None, title=None):
        if NGS != '12.7.5':
            raise ValueError('`Piano.plot_old` works properly only when NGS == 12.7.5!')

        # get note colors
        self._get_note_color(color_style)

        # get note texts
        self._get_note_text(color_style)

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
        if note_range is None:
            note_range = self._get_note_range()

        keys_expand = 1
        height = 6
        paddings = 0.1
        x_lims = (_note2pos_mark(note_range[0] - keys_expand)[0] - paddings, _note2pos_mark(note_range[1] + keys_expand)[0] + paddings)
        y_lims = (0 - paddings, height + 0.4 + paddings)
        ax_w = length(*x_lims)
        ax_h = length(*y_lims)
        fig_w_to_h_ratio = ax_w / ax_h

        # new figure
        if not ax:
            fig, ax = get_figure(FIG_HEIGHT * fig_w_to_h_ratio , FIG_HEIGHT)

        # axes settings
        ax.set_xlim(*x_lims)
        ax.set_ylim(*y_lims)

        # add title
        if title:
            ax.set_title(title, y=0.95)

        # key patches
        rects = [
            plt.Rectangle(**_note2pos_rect(note))
            for note in range(note_range[0] - 1 - keys_expand, note_range[1] + 2 + keys_expand)
        ]
        _ = [ax.add_patch(rect) for rect in rects]

        # note patches
        circs = [
            plt.Circle(
                xy=_note2pos_mark(int(note)),
                radius=0.4,
                ls='-',
                lw=1,
                ec=note.get_message('edge_color'),
                fc=note.get_message('face_color'),
                zorder=3
            ) for note in self._notes
        ]
        _ = [ax.add_patch(circ) for circ in circs]

        # note texts
        _ = [
            ax.annotate(
                s=note.get_message('text'),
                xy=_note2pos_mark(int(note)),
                color=note.get_message('text_color'),
                ha='center',
                va='center',
                zorder=4
            ) for note in self._notes
        ]

    def plot(self, note_range=None, color_style='note', ax=None, title=None):
        # get note colors
        self._get_note_color(color_style)

        # get note texts
        self._get_note_text(color_style)

        # constants
        if note_range is None:
            note_range = self._get_note_range()

        height = 4
        paddings = 0.1
        x_lims = (note_range[0] - paddings, note_range[1] + 1 + paddings)
        y_lims = (0 - paddings, height + 0.2 + paddings)
        ax_w = length(*x_lims)
        ax_h = length(*y_lims)
        fig_w = ax_w + 2 * paddings
        fig_h = ax_h + 2 * paddings
        fig_w_to_h_ratio = fig_w / fig_h

        # new figure
        if ax is None:
            fig, ax = get_figure(FIG_HEIGHT * fig_w_to_h_ratio, FIG_HEIGHT)

        # add title
        if title is not None:
            ax.set_title(title, y=0.95)

        # set display range
        ax.set_xlim(*x_lims)
        ax.set_ylim(*y_lims)

        # key patches
        key_rects = [
            plt.Rectangle(
                xy=(x, 0),
                width=1,
                height=height,
                lw=1.2,
                edgecolor='black',
                facecolor='white' if x % N in NAMED_NNREL_LIN else 'gray'
            ) for x in range(note_range[0], note_range[1] + 1)
        ]
        _ = [ax.add_patch(key_rect) for key_rect in key_rects]

        # key texts
        _ = [
            ax.annotate(
                s=str(x),
                xy=(x + 1 / 2, height - 1 / 2),
                ha='center',
                va='center',
                color='black',
            ) for x in range(note_range[0], note_range[1] + 1)
        ]

        # note patches
        note_circs = [
            plt.Circle(
                xy=(int(note) + 1 / 2, 1 / 2),
                radius=1 / 3,
                edgecolor=note.get_message('edge_color'),
                facecolor=note.get_message('face_color')
            ) for note in self._notes
        ]
        _ = [ax.add_patch(note_circ) for note_circ in note_circs]

        # note texts
        _ = [
            ax.annotate(
                s=note.get_message('text'),
                xy=(int(note) + 1 / 2, 1 / 2),
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
            fig, ax = get_figure(2 * FIG_HEIGHT, 2 * FIG_HEIGHT)

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

    def plot(self, n_gradients=M, ax=None, title=None):
        h = np.linspace(0, 1, N, endpoint=False)
        hs = [int(t) % N for t in self._notes]

        l1 = 0.5
        l2 = 0.25
        s1 = 0.95
        s2 = 0.5

        n_colors = len(hs)

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

        x_lims = 0, (x_margins + w) * n_gradients - x_margins
        y_lims = 0 - h_text, (y_margins + h) * n_colors - y_margins + h_text
        ax_w = length(*x_lims)
        ax_h = length(*y_lims)
        fig_w_to_h_ratio = ax_w / ax_h

        if ax is None:
            fig, ax = get_figure(FIG_HEIGHT * ax_w / 6, FIG_HEIGHT * ax_h / 6)

        if title is not None:
            ax.set_title(title, y=0.95)

        ax.set_xlim(*x_lims)
        ax.set_ylim(*y_lims)

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


class GenLine(_NoteList):
    def __init__(self, notes_list):
        """
        plot notes on a line in generative order

        :param notes_list: list of `DiatonicScale`, `AlteredDiatonicScale`, `Chord`, `ChordScale` instances, or list of list of `Note` instances
        """
        super().__init__()
        self._notes_list = notes_list

    def plot(self, color_style='note', key_note=Note(), tds_on=True, ax=None, title=None):
        def _get_pos(notes):
            notes_named_nnrel = [note.get_named_nnrel() for note in notes]
            notes_accidental = [note.get_accidental() for note in notes]

            return [NAMED_NNREL_GEN.index(nnrel) + accidental * M for nnrel, accidental in zip(notes_named_nnrel, notes_accidental)]

        if ax is None:
            if_fig = True
            fig, ax = get_figure(1, 1)
        else:
            if_fig = False
            fig = plt.gcf()

        if title is not None:
            ax.set_title(title, y=1)

        # constants
        n_lines = len(self._notes_list)
        paddings = 0.2
        x_mins = []
        x_maxs = []
        y_lims = (-n_lines + 1 - paddings, 1 + paddings)

        # iterate over `self._notes_list`
        for i, notes in enumerate(self._notes_list):
            # set notes
            self.set_notes(notes)

            # get note colors
            self._get_note_color(color_style)

            # get note texts
            self._get_note_text(color_style)

            # constants
            xs = _get_pos(notes)
            x_mins.append(min(xs))
            x_maxs.append(max(xs))

            # get background notes
            notes_bg = [Note().set_vector(named_nnrel=NAMED_NNREL_GEN[x % M], accidental=x // M) for x in range(min(xs), max(xs) + 1)]

            for note in notes_bg:
                if NGS == '12.7.5' and tds_on:
                    tds = ['T', 'D', 'S'][int(note - key_note) % 3]
                    note.set_message(face_color=tds_colors(tds))
                else:
                    note.set_message(face_color='white')

            # plot notes_bg
            rects = [
                plt.Rectangle(
                    xy=(x, -i),
                    width=1,
                    height=1,
                    facecolor=note.get_message('face_color'),
                    edgecolor='black',
                    zorder=0
                ) for note, x in zip(notes_bg, range(min(xs), max(xs) + 1))
            ]
            _ = [ax.add_patch(rect) for rect in rects]
            _ = [
                ax.annotate(
                    s=note.get_name(show_register=False),
                    xy=(x + 1 / 2, -i + 1 / 2),
                    color='black',
                    va='center',
                    ha='center',
                    zorder=1
                ) for note, x in zip(notes_bg, range(min(xs), max(xs) + 1))
            ]

            # plot notes
            for note, x in zip(self._notes, xs):
                rect = plt.Rectangle(
                    xy=(x + 1 / 8, -i + 1 / 8),
                    width=3 / 4,
                    height=3 / 4,
                    facecolor=note.get_message('face_color'),
                    edgecolor=note.get_message('edge_color'),
                    zorder=3
                )
                ax.add_patch(rect)
                ax.annotate(
                    s=note.get_name(show_register=False) if color_style == 'note' else note.get_name(show_register=False) + f"\n{note.get_message('text')}",
                    xy=(x + 1 / 2, -i + 1 / 2),
                    color=note.get_message('text_color'),
                    va='center',
                    ha='center',
                    zorder=4
                )

        # tonality stuff
        if NGS in ['12.7.5', '19.11.8']:
            major_offset = -1
        else:
            major_offset = 0

        # add vertical lines % M
        for x in range(min(x_mins), max(x_maxs) + 2):
            if x % M == NAMED_NNREL_GEN.index(key_note.get_named_nnrel()) + major_offset:
                ax.plot((x, x), (-n_lines + 1, 1), 'b', lw=2, zorder=5.1)

        # add vertical lines % N
        for x in range(min(x_mins), max(x_maxs) + 2):
            if x % N == NAMED_NNREL_GEN.index(key_note.get_named_nnrel()) + major_offset:
                ax.plot((x, x), (-n_lines + 1, 1), '--r', zorder=5.2)

        # add names
        try:
            names = [notes.get_name()[0] if isinstance(notes.get_name(), list) else notes.get_name() for notes in self._notes_list]
        except:
            names = ['[' + ', '.join([note.get_name(show_register=False) for note in notes]) + ']' for notes in self._notes_list]

        text_width = max(len(name) for name in names) / 3.5

        _ = [
            ax.annotate(
                s=name,
                xy=(max(x_maxs) + 3 / 2, -i + 1 / 2),
                color='black',
                va='center',
                ha='left',
                zorder=6
            ) for i, name in enumerate(names)
        ]

        # constants
        x_lims = (min(x_mins) - paddings, max(x_maxs) + 1 + paddings + text_width)
        ax_w = length(*x_lims) + 2 * paddings + text_width
        ax_h = length(*y_lims) + 2 * paddings

        # set axes lims
        ax.set_xlim(*x_lims)
        ax.set_ylim(*y_lims)

        # set figure size
        if if_fig:
            fig.set_figwidth(FIG_HEIGHT * ax_w / 4)
            fig.set_figheight(FIG_HEIGHT * ax_h  / 4)


class Tonnetz(_NoteList):
    def __init__(self):
        super().__init__()

    def plot(self, n_x=7, n_y=7, enharmonic=True, upside_down=False, center_note=Note(), color_style='note', tds_on=True, ax=None, title=None):
        # get note colors
        self._get_note_color(color_style)

        # get note texts
        self._get_note_text(color_style)

        # constants
        itv_gen = (Note(NAMED_STR_GEN[1]) - Note(NAMED_STR_GEN[0])).normalize()
        itv_major = (Note(NAMED_STR_LIN[CHORD_STEP_LIN]) - Note(NAMED_STR_LIN[0])).normalize()
        itv_minor = itv_gen - itv_major

        step_x = 3
        step_y = 3 ** (1 / 2) * step_x / 2
        offset_x = step_x / 2

        x_max = step_x * (n_x - 1 - n_x // 2 + (n_y - 1 - n_y // 2) / 2 + 1)
        y_max = step_y * (n_y - 1 - n_y // 2 + 1)

        ax_w = 2 * x_max
        ax_h = 2 * y_max

        if ax is None:
            fig, ax = get_figure(FIG_HEIGHT * ax_w / 6, FIG_HEIGHT * ax_h / 6)

        if title is not None:
            ax.set_title(title, y=0.95)

        ax.set_xlim([-x_max, x_max])
        ax.set_ylim([-y_max, y_max])

        # get background notes
        if upside_down:
            notes_bg = np.array(
                [
                    [
                        center_note + kx * itv_gen + ky * itv_minor for kx in range(-(n_x // 2), n_x // 2 + 1)
                    ] for ky in range(-(n_y // 2), n_y // 2 + 1)
                ]
            ).reshape([-1])
        else:
            notes_bg = np.array(
                [
                    [
                        center_note + kx * itv_gen + ky * itv_major for kx in range(-(n_x // 2), n_x // 2 + 1)
                    ] for ky in range(-(n_y // 2), n_y // 2 + 1)
                ]
            ).reshape([-1])

        for note in notes_bg:
            if NGS == '12.7.5' and tds_on:
                tds = ['T', 'D', 'S'][int(note - center_note) % 3]
                note.set_message(face_color=tds_colors(tds))
            else:
                note.set_message(face_color='white')

        # get background note positions
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
                s = cur_note.get_name(show_register=False) if color_style == 'note' else cur_note.get_name(show_register=False) + f'\n{text}'
                ax.annotate(s, cur_xy, color=text_color, va='center', ha='center')
            else:
                ax.annotate(cur_note.get_name(show_register=False), cur_xy, color='black', va='center', ha='center')
