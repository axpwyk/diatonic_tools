import numpy as np
import matplotlib.pyplot as plt
import colorsys as cs
from theories import *


''' matplotlib settings '''


# assign a style
plt.style.use('seaborn-pastel')
# assign a math font
plt.rc('mathtext', **{'fontset': 'cm'})
plt.rc('text', **{'usetex': False})
# assign a chinese font
plt.rc('font', **{'sans-serif': 'Consolas-with-Yahei'})
plt.rc('axes', **{'unicode_minus': False})


''' utils '''


def hex2oct(hex_string):
    search_obj = re.search(r'(?<=#)(?P<red>[\dabcdef]{2})(?P<green>[\dabcdef]{2})(?P<blue>[\dabcdef]{2})', hex_string)
    red = eval('0x'+search_obj['red'])
    green = eval('0x'+search_obj['green'])
    blue = eval('0x'+search_obj['blue'])
    return red/255, green/255, blue/255


def oct2hex(oct_list):
    red = oct_list[0] * 255
    green = oct_list[1] * 255
    blue = oct_list[2] * 255
    print(red, green, blue)
    digits = [str(k) for k in range(10)] + ['a', 'b', 'c', 'd', 'e', 'f']
    return '#'+f'{digits[int((red-red%16)//16)]}{digits[int(red%16)]}'+\
               f'{digits[int((green-green%16)//16)]}{digits[int(green%16)]}'+\
               f'{digits[int((blue-blue%16)//16)]}{digits[int(blue%16)]}'


def gradient1(t, color1, color2):
    c1 = hex2oct(color1)
    c2 = hex2oct(color2)
    return [[(1-s/(t-1))*c1[k]+s/(t-1)*c2[k] for k in range(3)] for s in range(t)]


def gradient2(t, color1, color2):
    c1 = cs.rgb_to_yiq(*hex2oct(color1))
    c2 = cs.rgb_to_yiq(*hex2oct(color2))
    return [cs.yiq_to_rgb(*[(1-s/(t-1))*c1[k]+s/(t-1)*c2[k] for k in range(3)]) for s in range(t)]


def gradient3(t, color1, color2):
    c1 = color1
    c2 = color2
    return [[(1-s/(t-1))*c1[k]+s/(t-1)*c2[k] for k in range(3)] for s in range(t)]


''' instrument modelling '''


class Guitar(object):
    def __init__(self, notes=None):
        # multiple notes on single string
        self._poly = True
        # default notes
        if notes:
            self._notes = notes
        else:
            self._notes = Chord('C').get_notes()
        # open string notes
        self._open_string_notes = np.array([16, 21, 26, 31, 35, 40])
        self._max_string = self._open_string_notes.shape[0]
        # fret notes
        self._max_fret = 25
        self._fretboard_notes = np.array([self._open_string_notes + i for i in range(0, self._max_fret)])
        # get note information
        self._get_note_information()
        # press
        self._press()

    def _get_note_information(self):
        # fix note names and br357t on fretboard
        self.fretboard_note_names = []
        self.fretboard_note_br357ts = []
        self.fretboard_note_degrees = []
        for fret in self._fretboard_notes:
            tmp_names = []
            tmp_br357ts = []
            tmp_degrees = []
            for note in fret:
                idx_bool = np.array([abs(x)%12 for x in self._notes])==note%12
                if any(idx_bool):
                    idx = np.where(np.array([abs(x)%12 for x in self._notes])==note%12)[0][0]
                    tmp_names.append(self._notes[idx].get_name(show_group=False)+f'{note//12}')
                    tmp_br357ts.append(self._notes[idx].get_message())
                    tmp_degrees.append(idx)
                else: tmp_names.append(''); tmp_br357ts.append(''); tmp_degrees.append(-1)
            self.fretboard_note_names.append(tmp_names)
            self.fretboard_note_br357ts.append(tmp_br357ts)
            self.fretboard_note_degrees.append(tmp_degrees)

    def _press(self):
        # pressed strings
        self.pressed = np.zeros((self._max_fret, self._max_string), np.bool)
        for note in self._notes:
            self.pressed[self._fretboard_notes % 12 == abs(note) % 12] = True

        if not self._poly:
            for k in range(self._max_string):
                string_k = self.pressed[:, k]
                idx = np.where(string_k)[0][0]+1
                self.pressed[idx:, k] = False

    def set_notes(self, notes):
        self._notes = notes
        self._get_note_information()
        self._press()
        return self

    def set_poly_on(self, bool):
        self._poly = bool
        return self

    def select(self, selection='x3201p'):
        for string in range(len(selection)):
            if selection[string] == 'p': pass
            elif selection[string] == 'x':
                self.pressed[:, string] = False
            else:
                self.pressed[:, string] = False
                self.pressed[eval('0x'+selection[string]), string] = True
        return self

    def plot1(self, fret_left=0, fret_right=4, ax=None, title=None):
        rotation = 0
        w_scale = 2
        fontsize = 20
        strings = np.arange(self._max_string)
        fret = w_scale * np.arange(0, self._max_fret)
        fingers = np.concatenate([[-1.0], fret[:-1]+fret[1:]]) / 2
        fret_interval = [fret_left, fret_right]

        # new figure
        w = fret[fret_interval[1]] - fret[fret_interval[0]] + 4
        h = strings[-1] - strings[0] + 2
        scale = 0.75
        if not ax:
            fig = plt.figure(figsize=(w*scale, h*scale), dpi=72)
            ax = plt.gca(aspect='equal')
        else:
            fig = plt.gcf()
            ax.set_aspect('equal')
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_axis_off()
        ax.margins(0.0)

        # add title
        if title:
            ax.text(0.5, 0.895, title, fontsize=fontsize*1.5, va='bottom', ha='center', transform=ax.transAxes)

        # plot position blocks
        for i in range(fret_interval[0]+1, fret_interval[1]+1):
            if i in range(12, self._max_fret, 12):
                rect = plt.Rectangle((fingers[i], strings[0]), fret[i]-fingers[i], strings[-1]-strings[0], color='gray', alpha=0.2)
                ax.add_patch(rect)
            elif i % 12 in [3, 5, 7, 9]:
                mid = (strings[-1]-strings[0])/2
                rect = plt.Rectangle((fingers[i], mid), fret[i]-fingers[i], mid, color='gray', alpha=0.2)
                ax.add_patch(rect)
            else: pass

        # plot frets
        ax.set_xlim(fret[fret_interval[0]]-1, fret[fret_interval[1]]+3)
        _ = [ax.plot((fret[i], fret[i]), (strings[0], strings[-1]), c='black', lw=2.0) for i in range(fret_interval[0], fret_interval[1]+1)]
        _ = [ax.annotate(fret[i]//w_scale, (fret[i], -0.5), rotation=rotation, fontsize=fontsize, color='blue', va='center', ha='center') for i in range(fret_interval[0], fret_interval[1]+1)[1:2]]

        # plot strings
        ax.set_ylim(strings[0]-1, strings[-1]+1)
        _ = [ax.plot((fret[fret_interval[0]], fret[fret_interval[1]]), (s, s), c='black', lw=1.0) for s in strings]

        # plot dots
        radius = 0.3
        colors = gradient1(len(self._notes), '#f6b0f0', '#f6deb0')
        for string in strings:

            sp = self.pressed[:, string]

            if any(sp):  # if there exists note on current string
                if self._poly:  # plot all notes
                    circ0 = [plt.Circle((fingers[0]+fret[fret_interval[0]], string), radius, fc='white', ec='black') for _ in range(1) if sp[0]]
                    circs = [plt.Circle((fingers[i+1], string), radius, fc='black', ec='black') for i, k in enumerate(sp[1:]) if k and fret_interval[0]<i+1<=fret_interval[1]]
                    _ = [ax.add_patch(c) for c in circ0 + circs]
                else:  # only plot top note
                    top_idx, = np.where(sp)
                    top_idx = top_idx[-1]
                    if top_idx == 0:
                        circ = plt.Circle((fingers[0]+fret[fret_interval[0]], string), radius, fc='white', ec='black')
                        ax.add_patch(circ)
                    elif fret_interval[0]<top_idx<=fret_interval[1]:
                        circ = plt.Circle((fingers[top_idx], string), radius, fc='black', ec='black')
                        ax.add_patch(circ)
                    else: pass

            else:  # if there isn't any note on current string, add a cross mark on open string position
                cross = [plt.Line2D((fingers[0]+fret[fret_interval[0]]-radius*np.sqrt(2)/2, fingers[0]+fret[fret_interval[0]]+radius*np.sqrt(2)/2),
                                    (string-radius*np.sqrt(2)/2, string+radius*np.sqrt(2)/2), c='black'),
                         plt.Line2D((fingers[0]+fret[fret_interval[0]]+radius*np.sqrt(2)/2, fingers[0]+fret[fret_interval[0]]-radius*np.sqrt(2)/2),
                                    (string-radius*np.sqrt(2)/2, string+radius*np.sqrt(2)/2), c='black')]
                ax.add_line(cross[0]); ax.add_line(cross[1])

        # add string texts (top notes)
        text_names = []
        text_br357ts = []
        text_degrees = []
        for string in strings:

            sp = self.pressed[:, string]

            top_idx, = np.where(sp)
            if sum(top_idx.shape)<=0:
                text_names.append('')
                text_br357ts.append('')
                text_degrees.append('')
                continue
            else:
                top_idx = top_idx[-1]
                text_names.append(self.fretboard_note_names[top_idx][string])
                text_br357ts.append(self.fretboard_note_br357ts[top_idx][string])
                text_degrees.append(self.fretboard_note_degrees[top_idx][string])

        _ = [ax.annotate(text.replace('b', r'$\flat$').replace('#', r'$\sharp$'), (fret[fret_interval[1]]+0.25, strings[i]), rotation=rotation,
                         fontsize=fontsize, va='center', ha='left', bbox=dict(facecolor=colors[0], alpha=0.0)) for i, text in enumerate(text_names)]
        _ = [ax.annotate(text.replace('b', r'$\flat$').replace('#', r'$\sharp$'), (fret[fret_interval[1]]+1.75, strings[i]), rotation=rotation,
                         fontsize=fontsize, va='center', ha='left', bbox=dict(facecolor=colors[-1], alpha=0.2)) for i, text in enumerate(text_br357ts)]

        # plt.savefig('debug.svg', bbox_inches='tight', pad_inches=0.0)
        # plt.close()

    def plot2(self, fret_left=0, fret_right=4, ax=None, title=None):
        rotation = 0
        w_scale = 2
        fontsize = 12
        strings = np.arange(self._max_string)
        fret = w_scale * np.arange(0, self._max_fret)
        fingers = np.concatenate([[-0.5], fret[:-1]+fret[1:]]) / 2
        fret_interval = [fret_left, fret_right]

        # new figure
        w = fret[fret_interval[1]] - fret[fret_interval[0]] + 2
        h = strings[-1] - strings[0] + 2.4
        scale = 0.75
        if not ax:
            fig = plt.figure(figsize=(w*scale, h*scale), dpi=72)
            ax = plt.gca(aspect='equal')
        else:
            fig = plt.gcf()
            ax.set_aspect('equal')
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_axis_off()
        ax.margins(0.0)

        # add title
        if title:
            ax.text(0.5, 0.895, title, fontsize=fontsize*1.5, va='bottom', ha='center', transform=ax.transAxes)

        # plot position blocks
        for i in range(fret_interval[0]+1, fret_interval[1]+1):
            if i in range(12, self._max_fret, 12):
                rect = plt.Rectangle((fingers[i], strings[0]), fret[i]-fingers[i], strings[-1]-strings[0], color='gray', alpha=0.2)
                ax.add_patch(rect)
            elif i % 12 in [3, 5, 7, 9]:
                mid = (strings[-1]-strings[0])/2
                rect = plt.Rectangle((fingers[i], mid), fret[i]-fingers[i], mid, color='gray', alpha=0.2)
                ax.add_patch(rect)
            else: pass

        # plot frets
        ax.set_xlim(fret[fret_interval[0]]-1, fret[fret_interval[1]]+1)
        _ = [ax.plot((fret[i], fret[i]), (strings[0], strings[-1]), c='black', lw=2.0) for i in range(fret_interval[0], fret_interval[1]+1)]
        _ = [ax.annotate(fret[i]//w_scale, (fret[i], -0.5), rotation=rotation, fontsize=fontsize, color='red', va='center', ha='center') for i in range(fret_interval[0], fret_interval[1]+1)]

        # plot strings
        ax.set_ylim(strings[0]-1.2, strings[-1]+1.2)
        _ = [ax.plot((fret[fret_interval[0]], fret[fret_interval[1]]), (s, s), c='black', lw=1.0) for s in strings]

        # plot texts
        radius = 0.15
        colors = gradient1(len(self._notes), '#f6b0f0', '#f6deb0')
        for string in strings:

            sp = self.pressed[:, string]

            if any(sp):  # if there exists note on current string
                if self._poly:  # plot all notes
                    _ = [ax.annotate(f'({self.fretboard_note_names[0][string]}, {self.fretboard_note_br357ts[0][string]})'.replace('b', r'$\flat$').replace('#', r'$\sharp$'),
                                     (fingers[0]+fret[fret_interval[0]], string), rotation=rotation, color='white', va='center', ha='center',
                                     fontsize=fontsize, bbox=dict(facecolor='#ee5511')) for _ in range(1) if sp[0]]
                    _ = [ax.annotate(f'({self.fretboard_note_names[i+1][string]}, {self.fretboard_note_br357ts[i+1][string]})'.replace('b', r'$\flat$').replace('#', r'$\sharp$'),
                                     (fingers[i+1], string), rotation=rotation, color='black', va='center', ha='center',
                                     fontsize=fontsize, bbox=dict(facecolor=colors[self.fretboard_note_degrees[i+1][string]])) for i, k in enumerate(sp[1:]) if k and fret_interval[0]<i+1<=fret_interval[1]]
                else:  # only plot top note
                    top_idx, = np.where(sp)
                    top_idx = top_idx[-1]
                    if top_idx == 0:
                        ax.annotate(f'({self.fretboard_note_names[0][string]}, {self.fretboard_note_br357ts[0][string]})'.replace('b', r'$\flat$').replace('#', r'$\sharp$'),
                                    (fingers[0]+fret[fret_interval[0]], string), rotation=rotation, va='center', ha='center',
                                    fontsize=fontsize, bbox=dict(facecolor='#ee5511'))
                    elif fret_interval[0]<top_idx<=fret_interval[1]:
                        ax.annotate(f'({self.fretboard_note_names[top_idx][string]}, {self.fretboard_note_br357ts[top_idx][string]})'.replace('b', r'$\flat$').replace('#', r'$\sharp$'),
                                    (fingers[top_idx], string), rotation=rotation, va='center', ha='center',
                                    fontsize=fontsize, bbox=dict(facecolor=colors[self.fretboard_note_degrees[top_idx][string]]))
                    else: pass

            else:  # if there isn't any note on current string, add a cross mark on open string position
                cross = [plt.Line2D((fingers[0]+fret[fret_interval[0]]-radius*np.sqrt(2)/2, fingers[0]+fret[fret_interval[0]]+radius*np.sqrt(2)/2),
                                    (string-radius*np.sqrt(2)/2, string+radius*np.sqrt(2)/2), c='black'),
                         plt.Line2D((fingers[0]+fret[fret_interval[0]]+radius*np.sqrt(2)/2, fingers[0]+fret[fret_interval[0]]-radius*np.sqrt(2)/2),
                                    (string-radius*np.sqrt(2)/2, string+radius*np.sqrt(2)/2), c='black')]
                ax.add_line(cross[0]); ax.add_line(cross[1])

        # fig.savefig('debug.svg', bbox_inches='tight', pad_inches=0.0)
        # plt.close()


class Piano(object):
    pass


class Clock(object):
    def __init__(self, notes):
        self._notes = notes

    def plot(self, title, tonic=None, margin_anno_type=None, colorize=None):
        import colorsys as cs

        radius = 5
        omega = np.cos(np.pi/6) - 1j*np.sin(np.pi/6)
        offset = (-omega)**3

        texts = ['C', r'C$\sharp$/D$\flat$', 'D', r'D$\sharp$/E$\flat$',
                 'E', 'F', r'F$\sharp$/G$\flat$', 'G',
                 r'G$\sharp$/A$\flat$', 'A', r'A$\sharp$/B$\flat$', 'B']
        for note in self._notes:
            texts[abs(note)%12] = note.get_name(show_group=False).replace('#', r'$\sharp$').replace('b', r'$\flat$') + f'({note.get_message()})'
        text_colors = [cs.hls_to_rgb(h, 0.5, 0.75) for h in np.linspace(0, 1.0, 12, endpoint=False)]
        text_colors = [text_color if k in [abs(x)%12 for x in self._notes] else 'gray' for k, text_color in enumerate(text_colors)]
        text_positions = [(1.4*radius*np.real(omega**k*offset), 1.4*radius*np.imag(omega**k*offset)) for k in range(12)]

        hand_colors = [[0.5, 0.5, 0.5]] * 12
        msgs = [note.get_message() for note in self._notes]
        if 'R' in msgs: root_pos = abs(self._notes[msgs.index('R')]) % 12
        else: root_pos = -1
        if 'B' in msgs: bass_pos = abs(self._notes[msgs.index('B')]) % 12
        else: bass_pos = -1
        if tonic is not None: tonic_pos = tonic % 12
        else: tonic_pos = -1
        for i in range(12):
            if i in [root_pos, bass_pos, tonic_pos]:
                hand_colors[i] = [0.75*(i==root_pos), 0.75*(i==bass_pos), 0.75*(i==tonic_pos)]
        if colorize:
            for i in colorize:
                hand_colors[i] = 'red'


        ''' new figure '''


        fig, ax = plt.subplots(1, 1)
        fig.set_figwidth(4); fig.set_figheight(4)
        fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.0, hspace=0.0)
        ax.margins(0.0)
        ax.set_aspect('equal')
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlim(-1.8*radius, 1.8*radius)
        ax.set_ylim(-1.8*radius, 1.8*radius)


        ''' plotting '''


        ks1 = [abs(x) for x in self._notes]

        circ = plt.Circle((0, 0), radius, fc='none', ec='black', lw=2.0)
        hands = [plt.Line2D((0, 0.8*radius*np.real(omega**k*offset)), (0, 0.8*radius*np.imag(omega**k*offset)),
                        lw=1.5, c=hand_colors[k]) for k in range(12)]
        ticks = [plt.Line2D((0.95*radius*np.real(omega**k*offset), radius*np.real(omega**k*offset)), (0.95*radius*np.imag(omega**k*offset), radius*np.imag(omega**k*offset)),
                        lw=1, c='black') for k in range(12)]

        ax.add_patch(circ)
        _ = [ax.add_line(hand) for hand in [hands[k%12] for k in ks1]]
        _ = [ax.add_line(tick) for tick in [ticks[k] for k in range(12)]]
        _ = [ax.annotate(k, (1.1*radius*np.real(omega**k*offset), 1.1*radius*np.imag(omega**k*offset)), ha='center', va='center') for k in range(12)]
        _ = [ax.annotate(texts[k], text_positions[k], va='center', ha='center', bbox=dict(facecolor=text_colors[k], alpha=0.2, edgecolor=text_colors[k])) for k in range(12)]
        ks2 = ks1 + [12+ks1[0]]
        if margin_anno_type == 'degree':
            _ = [ax.annotate(f'{(k2-k1)*30}°', (np.real(0.65*radius*omega**(k1+(k2-k1)/2)*offset), np.imag(0.65*radius*omega**(k1+(k2-k1)/2)*offset)),
                             ha='center', va='center') for k1, k2 in zip(ks2[:-1], ks2[1:])]
        elif margin_anno_type == 'interval':
            notes_appended = self._notes + [self._notes[0]+Interval('P8')]
            _ = [ax.annotate(notes_appended[i+1]-notes_appended[i], (np.real(0.65*radius*omega**(k1+(k2-k1)/2)*offset), np.imag(0.65*radius*omega**(k1+(k2-k1)/2)*offset)),
                             ha='center', va='center') for i, (k1, k2) in enumerate(zip(ks2[:-1], ks2[1:]))]
        else: pass
        ax.text(0.05, 0.95, title, transform=ax.transAxes, ha='left', va='top', bbox=dict(facecolor='none', edgecolor='black'))


class ColorScheme(object):
    def __init__(self, notes):
        self._notes = notes

    def plot(self, title):
        h = np.linspace(0, 1, 12, endpoint=False)
        hs = [abs(t)%12 for t in self._notes]
        # save_name = ''
        l1 = 0.5; l2 = 0.25
        s1 = 0.95; s2 = 0.5

        n_colors = len(hs)
        n_gradients = 7

        colors = np.zeros((n_colors, n_gradients, 3), 'float')
        for i in range(n_colors):
            colors[i] = gradient3(n_gradients, cs.hls_to_rgb(h[hs[i]], l1, s1), cs.hls_to_rgb(h[hs[i]], l2, s2))


        ax = plt.gca()
        ax.margins(0.0)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_aspect('equal')

        x_margins = 0.5; w = 3
        y_margins = 1.5; h = 1
        h_text = 1
        ax.set_xlim(0, (x_margins+w)*n_gradients-x_margins)
        ax.set_ylim(0-h_text, (y_margins+h)*n_colors-y_margins+h_text)
        for i in range(n_colors):
            for j in range(n_gradients):
                rect = plt.Rectangle(((w+x_margins)*j, (h+y_margins)*i), w, h, color=colors[n_colors-i-1, j])
                ax.add_patch(rect)
                ax.annotate(oct2hex(colors[n_colors-i-1, j]), ((x_margins+w)*j+w/2, (y_margins+h)*i-h_text/2), va='center', ha='center')
        ax.annotate(f'{title} {[k*360//12 for k in hs]}',
                    (((x_margins+w)*n_gradients-x_margins)/2, (y_margins+h)*n_colors-y_margins+h_text/2), ha='center', va='center')
        # if not save_name:
        #     plt.savefig('debug.svg', bbox_inches='tight', pad_inches=0.0)
        # else:
        #     plt.savefig(save_name+'.svg', bbox_inches='tight', pad_inches=0.0)
