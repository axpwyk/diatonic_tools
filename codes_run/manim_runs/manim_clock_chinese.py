#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys; sys.path.append(r'E:\Codes\__synced__\diatonic_tools')
import os; os.chdir('../..')
from manim import *
from theories import *

# global constants
R = 2
O = np.array((0, 0, 0))
C = np.cos(PI/2) + 1j*np.sin(PI/2)
omega = np.cos(-PI/6) + 1j*np.sin(-PI/6)
positions = [R*C*omega**k for k in range(12)]
pos_ticks = [np.array((np.real(position), np.imag(position), 0)) for position in positions]
texts = [r'C/B$\sharp$', r'C$\sharp$/D$\flat$', 'D', r'D$\sharp$/E$\flat$',
         r'E/F$\flat$', r'F/E$\sharp$', r'F$\sharp$/G$\flat$', 'G',
         r'G$\sharp$/A$\flat$', 'A', r'A$\sharp$/B$\flat$', r'B/C$\flat$']
sounds = [f'audio_runs/{k//12}_{k%12}.wav' for k in range(0, 24)] + [f'audio_runs/-1_11.wav']


class Head(Scene):
    def construct(self):
        text = TextMobject(r'本视频会按照以下严格的逻辑体系研究各种十二平均律下的七声音阶\\'
                            r'\phantom{!}\\'
                            r'\begin{itemize}'
                            r'\item 从十二个音中任选七个不重复的音组成\emph{七声音阶}'
                            r'\item \emph{音阶结构}指音阶的整体构型，与音程有关而与主音的选择无关'
                            r'\item 同一\emph{类}音阶具有相同的音阶结构'
                            r'\item 一个类包含七种音阶(从不同主音开始)'
                            r'\item 以Diatonic类音阶为核心'
                            r'\item 定义音阶结构之间的\emph{结构距离函数}($d$)'
                            r'\item 定义某一音阶到Diatonic类的距离为其\emph{阶数}(Order)'
                            r'\item 按照阶数递增的方式一劳永逸地对所有可能的七声音阶进行分类'
                            r'\end{itemize}').scale(0.65)
        self.wait(0.5)
        self.play(Write(text))
        self.wait(9.5)
        self.play(FadeOut(text))


class DiatonicScales(Scene):
    def construct(self):
        global R, O, C, omega, positions, pos_ticks, texts, sounds

        ''' generate constants and mobjects '''

        # clock face
        title = TextMobject('Diatonic类音阶(第0类·第0阶)').move_to(UP-np.array((0, 0.5, 0))).scale(0.8)
        circle = Circle(radius=R, color=WHITE).flip(LEFT).rotate(PI/2)
        center_point = Point()
        ticks = VGroup(*[Line(pos*0.95, pos) for pos in pos_ticks])
        names = VGroup(*[TextMobject(text).move_to(pos_tick*1.3).scale(0.5) for text, pos_tick in zip(texts, pos_ticks)])
        hands = VGroup(*[Line(O, pos*0.65, color=WHITE).set_opacity(0) for i, pos in enumerate(pos_ticks)])
        nums = VGroup(*[TextMobject(str(k)).move_to(pos_tick*0.8).scale(0.5) for k, pos_tick in enumerate(pos_ticks)])
        clock = VGroup(circle, ticks, names, hands, nums)
        sub1 = TextMobject('Diatonic类音阶可以通过连续的纯五度(+7)产生').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)
        sub2 = TextMobject('以上是全部的7种Diatonic类音阶').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)
        p5seq = [(5+7*k)%12 for k in range(7)]

        ''' make animation '''

        # create clock
        self.play(FadeInFromDown(title))
        self.play(ShowCreation(circle), FadeIn(ticks), Write(names), Write(nums))
        self.play(FadeInFromDown(sub1))
        self.wait(1)
        self.add(hands[p5seq[0]].set_opacity(1))
        self.add_sound(sounds[p5seq[0]], gain=-12)
        self.wait(1)
        for k in p5seq[1:]:
            self.wait(1)
            self.add(hands[k].set_opacity(1))
            self.add_sound(sounds[k], gain=-12)
            tmp = hands[k].copy().set_color(GRAY)
            self.play(Rotating(tmp, radians=7*PI/6, about_point=ORIGIN, run_time=1))
            tmp.set_opacity(0)
        self.wait(2)
        self.play(FadeOut(sub1))

        # def play diatonic scales function
        def play(scale_name, replay_on_c=True):
            # generate scales and note pitches
            scale = DiatonicScale(scale_name)
            c_scale = DiatonicScale('C'+' '+scale.get_name(type_only=True))
            notes = [note for note in abs(scale)]
            c_notes = [note for note in abs(c_scale)]
            tonic = notes[0]%12
            c_tonic = c_notes[0]%12

            # generate text mobjects
            def _scale_text(scale):
                scale_text = (
                    scale[0].get_name_old(show_group=False).replace('b', r'$\flat$').replace('#', r'$\sharp$') + ' ',
                    scale.get_name_old(type_only=True).replace('b', r'$\flat$').replace('#', r'$\sharp$'),
                    ' | ',
                    *[scale[k].get_name_old(show_group=False).replace('b', r'$\flat$').replace('#', r'$\sharp$') + '\t' for k in range(7)],
                    '({})'.format(scale[0].get_name_old(show_group=False).replace('b', r'$\flat$').replace('#', r'$\sharp$'))
                )
                print(scale_text)
                scale_text = TextMobject(*scale_text).scale(0.8)
                scale_text.move_to(DOWN+np.array((0, 0.5, 0)))
                return scale_text

            scale_text = _scale_text(scale)
            scale_text[0].set_color(BLUE)
            scale_text[3].set_color(BLUE)
            scale_text[-1].set_color(BLUE)

            # highlight tonic note (blue)
            self.play(FadeToColor(hands[(tonic)%12], BLUE), FadeInFromDown(scale_text))

            # play the scale with highlight color orange
            def _play(notes, offset, scale_text):
                # note 1
                hands[(notes[0]+offset)%12].set_color(ORANGE)
                scale_text[3].set_color(ORANGE)
                self.add_sound(sounds[notes[0]], gain=-12)
                self.wait(0.5)
                hands[(notes[0]+offset)%12].set_color(BLUE)
                scale_text[3].set_color(BLUE)
                # note 2-6
                for idx, i in enumerate(notes[1:]):
                    hands[(i+offset)%12].set_color(ORANGE)
                    scale_text[idx+4].set_color(ORANGE)
                    self.add_sound(sounds[i], gain=-12)
                    self.wait(0.5)
                    hands[(i+offset)%12].set_color(WHITE)
                    scale_text[idx+4].set_color(WHITE)
                # note 7
                hands[(notes[0]+offset)%12].set_color(ORANGE)
                scale_text[-1].set_color(ORANGE)
                self.add_sound(sounds[notes[0]+12], gain=-12)
                self.wait(0.5)
                hands[(notes[0]+offset)%12].set_color(BLUE)
                scale_text[-1].set_color(BLUE)

            _play(notes, 0, scale_text)
            self.wait(0.5)

            if replay_on_c:
                # generate new text mobjects
                c_scale_text = _scale_text(c_scale)
                c_scale_text[0].set_color(BLUE)
                c_scale_text[3].set_color(BLUE)
                c_scale_text[-1].set_color(BLUE)
                # rotate and play scale from c
                offset = notes[0]%12 if notes[0]%12 <= 6 else (notes[0]%12)-12
                ang = offset*PI/6
                original_scale_text = scale_text.copy()
                self.add_sound('audio_runs/rotate_1.wav', gain=-12)
                self.play(Rotate(hands, ang), Transform(scale_text, c_scale_text))
                self.wait(0.5)
                _play(c_notes, offset, scale_text)
                self.wait(0.5)
                self.add_sound('audio_runs/rotate_1.wav', gain=-12)
                self.play(Rotate(hands, -ang), Transform(scale_text, original_scale_text))

            # de-highlight tonic note
            self.play(FadeToColor(hands[(tonic)%12], WHITE), FadeOut(scale_text))

        play('F Lydian')
        play('C Ionian', False)
        play('G Mixolydian')
        play('D Dorian')
        play('A Aeolian')
        play('E Phrygian')
        play('B Locrian')
        self.play(FadeInFromDown(sub2))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(clock), FadeOut(sub2))


class In1(Scene):
    def construct(self):
        text = TextMobject(r'接下来定义音阶结构之间的\emph{结构距离函数}($d$)\\并给出一个实际计算的例子').scale(0.8)
        self.wait(0.5)
        self.play(Write(text))
        self.wait(2.5)
        self.play(FadeOut(text))


class StructualDistance(Scene):
    def construct(self):
        global R, O, C, omega, positions, pos_ticks, texts, sounds

        ''' generate constants and mobjects'''

        # clock face
        title = TextMobject('音阶结构之间的结构距离函数($d$)').move_to(UP-np.array((0, 0.5, 0))).scale(0.8)
        circle = Circle(radius=R, color=WHITE).flip(LEFT).rotate(PI/2)
        center_point = Point()
        ticks = VGroup(*[Line(pos*0.95, pos) for pos in pos_ticks])
        ticks2 = VGroup(*[Line(pos*0.95, pos) for pos in pos_ticks])
        names = VGroup(*[TextMobject(text).move_to(pos_tick*1.3).scale(0.5) for text, pos_tick in zip(texts, pos_ticks)])
        hands1 = VGroup(*[Line(O, pos*0.65, color=WHITE).set_opacity(0) for i, pos in enumerate(pos_ticks)])
        for k in [note%12 for note in abs(AlteredDiatonicScale('C Lydian(#2, #3)'))]:
            hands1[k].set_opacity(1).set_color(BLUE).set_stroke(width=5)
        hands2 = VGroup(*[Line(O, pos*0.65, color=WHITE).set_opacity(0) for i, pos in enumerate(pos_ticks)])
        for k in [note%12 for note in abs(AlteredDiatonicScale('C Lydian(#5, #6)'))]:
            hands2[k].set_opacity(1).set_color(ORANGE).set_stroke(width=2.5)
        nums = VGroup(*[TextMobject(str(k)).move_to(pos_tick*0.8).scale(0.5) for k, pos_tick in enumerate(pos_ticks)])
        clock = VGroup(circle, ticks, names, hands1, hands2, nums)
        sub1 = TextMobject('假设表上某七个指针构成音阶 A', tex_to_color_map={'A': BLUE}).move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)
        sub2 = TextMobject('再假设另外七个指针构成音阶 B', tex_to_color_map={'B': ORANGE}).move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)
        sub3 = TextMobject(r"$d$(A, B)=``当允许任意旋转时，A, B 相差的最少半音变化次数''",
                           tex_to_color_map={'A': BLUE, 'B': ORANGE}).move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)
        ds = np.zeros((12,), np.int)
        sub4 = TextMobject(
            r'$d$(A, B)=$\min$(',
            *[f'{d}, ' for d in ds[:-1]],
            f'{ds[-1]}',
            ')',
            tex_to_color_map={'A': BLUE, 'B': ORANGE}
        ).move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)

        ''' make animation '''

        self.play(FadeInFromDown(title))
        self.play(ShowCreation(circle), FadeIn(ticks), Write(names), Write(nums))

        self.play(FadeIn(hands1))
        self.play(FadeInFromDown(sub1))
        self.wait(3)
        self.play(FadeOut(sub1))

        self.play(FadeIn(hands2))
        self.play(FadeInFromDown(sub2))
        self.wait(3)
        self.play(FadeOut(sub2))

        self.play(FadeInFromDown(sub3))
        self.wait(6)
        self.play(FadeOut(sub3))

        def move_and_count(src_hands, tgt_hands, k):
            for src_hand, tgt_hand in zip(src_hands, tgt_hands):
                ht = tgt_hand - src_hand
                ang = -ht * PI / 6
                self.add_sound('audio_runs/rotate_2.wav', gain=-12)
                self.play(Rotating(hands2[(src_hand+k)%12], radians=ang, about_point=ORIGIN, run_time=0.5))
                ds[k] = ds[k] + abs(ht)
                sub4_new = TextMobject(
                    r'$d$(A, B)=$\min$(',
                    *[f'{d}, ' for d in ds[:-1]],
                    f'{ds[-1]}',
                    ')',
                    tex_to_color_map={'A': BLUE, 'B': ORANGE}
                ).move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)
                self.play(Transform(sub4, sub4_new, run_time=0))

            self.wait(0.5)

            for src_hand, tgt_hand in zip(reversed(src_hands), reversed(tgt_hands)):
                ht = tgt_hand - src_hand
                ang = -ht * PI / 6
                self.play(Rotating(hands2[(src_hand+k)%12], radians=-ang, about_point=ORIGIN, run_time=0.5))

        # [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1]  # 0
        # [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1]  # 0
        #
        # [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1]  # 1
        # [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1]  # 1
        #
        # [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1]  # 2
        # [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0]  # 2
        #
        # [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1]  # 3
        # [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1]  # 3
        #
        # [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1]  # 4
        # [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0]  # 4
        #
        # [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1]  # 5
        # [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1]  # 5
        #
        # [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1]  # 6
        # [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0]  # 6
        #
        # [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1]  # 7
        # [0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1]  # 7
        #
        # [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1]  # 8
        # [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0]  # 8
        #
        # [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1]  # 9
        # [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1]  # 9
        #
        # [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1]  # 10
        # [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # 10
        #
        # [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1]  # 11
        # [1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]  # 11

        self.play(FadeInFromDown(sub4))
        move_and_count([2, 4, 8, 10], [3, 5, 7, 9], 0)  # 0
        self.add_sound('audio_runs/rotate_1.wav', gain=-12)
        self.play(Rotate(hands2, PI/6))
        move_and_count([1, 7, 9, 10], [0, 6, 7, 9], 1)  # 1
        self.add_sound('audio_runs/rotate_1.wav', gain=-12)
        self.play(Rotate(hands2, PI/6))
        move_and_count([2, 4, 8, 10], [3, 5, 7, 11], 2)  # 2
        self.add_sound('audio_runs/rotate_1.wav', gain=-12)
        self.play(Rotate(hands2, PI/6))
        move_and_count([1, 7, 8], [0, 6, 7], 3)  # 3
        self.add_sound('audio_runs/rotate_1.wav', gain=-12)
        self.play(Rotate(hands2, PI/6))
        move_and_count([2, 4, 8, 10], [3, 5, 9, 11], 4)  # 4
        self.add_sound('audio_runs/rotate_1.wav', gain=-12)
        self.play(Rotate(hands2, PI/6))
        move_and_count([1], [0], 5)  # 5
        self.add_sound('audio_runs/rotate_1.wav', gain=-12)
        self.play(Rotate(hands2, PI/6))
        move_and_count([2, 4, 5, 6, 8, 10], [3, 5, 6, 7, 9, 11], 6)  # 6
        self.add_sound('audio_runs/rotate_1.wav', gain=-12)
        self.play(Rotate(hands2, PI/6))
        move_and_count([1, 4, 5], [0, 5, 6], 7)  # 7
        self.add_sound('audio_runs/rotate_1.wav', gain=-12)
        self.play(Rotate(hands2, PI/6))
        move_and_count([0, 2, 4, 8, 10], [-1, 0, 5, 7, 9], 8)  # 8
        self.add_sound('audio_runs/rotate_1.wav', gain=-12)
        self.play(Rotate(hands2, PI/6))
        move_and_count([1, 2, 3, 5], [0, 3, 5, 6], 9)  # 9
        self.add_sound('audio_runs/rotate_1.wav', gain=-12)
        self.play(Rotate(hands2, PI/6))
        move_and_count([0, 1, 2, 4, 8, 10], [-1, 0, 3, 5, 7, 9], 10)  # 10
        self.add_sound('audio_runs/rotate_1.wav', gain=-12)
        self.play(Rotate(hands2, PI/6))
        move_and_count([1, 3, 5], [3, 5, 6], 11)  # 11
        self.wait(2)
        sub4_new = TextMobject(r'$d$(A, B)=1',
                               tex_to_color_map={'A': BLUE, 'B': ORANGE, '1': YELLOW}).move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)
        self.play(Transform(sub4, sub4_new))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(clock), FadeOut(sub4))


''' order 1 '''


class In2(Scene):
    def construct(self):
        text = TextMobject(r'到Diatonic类音阶的结构距离为1的类属于第1阶。第1阶包含7个类：'
                           r'\begin{enumerate}'
                           r'\item Lydian($\sharp$2)类音阶。它包含了 Ukrainian Dorian 音阶、和声小调音阶、HMP5B (Phrygian Dominant) 等音阶'
                           r'\item Lydian($\sharp$3)类音阶（本视频略过）'
                           r'\item Lydian($\sharp$5)类音阶。它包含了 Altered 音阶、Acoustic (Lydian Dominant) 音阶、旋律小调(Minor Major)音阶、旋律大调(Major Minor)音阶、Half Diminished 等音阶'
                           r'\item Lydian($\sharp$6)类音阶。它包含了 Minor Neapolitan (Harmonic Phrygian) 等音阶'
                           r'\item Lydian($\flat$2)类音阶（本视频略过）'
                           r'\item Lydian($\flat$3)类音阶。它包含了和声大调等音阶'
                           r'\item Lydian($\flat$6)类音阶（本视频略过）'
                           r'\end{enumerate}').scale(0.65)
        self.wait(0.5)
        self.play(Write(text))
        self.wait(7.5)
        self.play(FadeOut(text))


class LydianS2(Scene):
    def construct(self):
        global R, O, C, omega, positions, pos_ticks, texts, sounds

        ''' generate constants and mobjects '''

        # clock face
        title = TextMobject(r'Lydian($\sharp$2)类音阶(第1类·第1阶)').move_to(UP-np.array((0, 0.5, 0))).scale(0.8)  # changed
        circle = Circle(radius=R, color=WHITE).flip(LEFT).rotate(PI/2)
        center_point = Point()
        ticks = VGroup(*[Line(pos*0.95, pos) for pos in pos_ticks])
        names = VGroup(*[TextMobject(text).move_to(pos_tick*1.3).scale(0.5) for text, pos_tick in zip(texts, pos_ticks)])
        hands = VGroup(*[Line(O, pos*0.65, color=WHITE).set_opacity(0) for i, pos in enumerate(pos_ticks)])
        nums = VGroup(*[TextMobject(str(k)).move_to(pos_tick*0.8).scale(0.5) for k, pos_tick in enumerate(pos_ticks)])
        clock = VGroup(circle, ticks, names, hands, nums)
        sub1 = TextMobject(r'Lydian($\sharp$2)类音阶可以通过Diatonic类音阶升高一个音产生').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        sub2 = TextMobject(r'以上是全部的7种Lydian($\sharp$2)类音阶').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        tonic_names = 'FCGDAEB'
        scale_types = [r'Lydian(#2)', r'Ionian(#5)', r'Mixolydian(#1)', r'Dorian(#4)', r'Aeolian(#7)', r'Phrygian(#3)', r'Locrian(#6)']  # changed
        scale_types_alt = [r'Lydian($\sharp$2)', r'Ionian($\sharp$5)', r'Mixolydian($\sharp$1)', r'Dorian($\sharp$4) (Ukrainian Dorian)',
                           r'Aeolian($\sharp$7) (和声小调)', r'Phrygian($\sharp$3) (HMP5B)', r'Locrian($\sharp$6)']  # changed
        diatonic_seq = [5, 7, 9, 11, 0, 2, 4]
        main_seq = diatonic_seq[:1] + [diatonic_seq[1]+1] + diatonic_seq[2:]  # changed
        print(main_seq)

        ''' make animation '''

        # create clock
        self.play(FadeInFromDown(title))
        self.play(ShowCreation(circle), FadeIn(ticks), Write(names), Write(nums))
        self.play(FadeInFromDown(sub1))
        self.wait(1)
        for k in diatonic_seq:
            self.play(ShowCreation(hands[k].set_opacity(1)), run_time=0.1)
        self.wait(1)

        # add accidentals
        sub1_new = TextMobject('F Lydian').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        self.play(Transform(sub1, sub1_new))
        tmp = hands[diatonic_seq[1]].copy().set_opacity(1)  # changed
        self.play(FadeToColor(tmp, YELLOW))
        hands[diatonic_seq[1]].set_opacity(0)  # changed
        self.add_sound('audio_runs/rotate_2.wav', gain=-12)
        self.play(Rotating(tmp, radians=-PI/6, about_point=ORIGIN, run_time=0.5))  # changed
        self.play(FadeToColor(tmp, WHITE))
        tmp.set_opacity(0)
        self.add(hands[main_seq[1]].set_opacity(1))  # changed
        sub1_new = TextMobject('F Lydian($\sharp$2)').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        self.play(Transform(sub1, sub1_new))

        self.wait(2)
        self.play(FadeOut(sub1))

        # def play altered diatonic scales function
        def play(tonic_name, scale_type, scale_type_alt, replay_on_c=True):
            # generate scales and note pitches
            # warning: when tonic_name = 'G', tonic may equal 'G#'
            scale = AlteredDiatonicScale(tonic_name + ' ' + scale_type)
            c_scale = AlteredDiatonicScale('C'+' '+scale_type)
            notes = [note for note in abs(scale)]
            c_notes = [note for note in abs(c_scale)]
            tonic = notes[0]%12
            c_tonic = c_notes[0]%12
            real_tonic = abs(Note(tonic_name))%12

            # generate text mobjects
            def _scale_text(scale, tonic_name, scale_type_alt):
                scale_text = (
                    tonic_name.replace('b', r'$\flat$').replace('#', r'$\sharp$')+' ',
                    scale_type_alt.replace('b', r'$\flat$').replace('#', r'$\sharp$'),
                    ' | ',
                    *[scale[k].get_name_old(show_group=False).replace('b', r'$\flat$').replace('#', r'$\sharp$') + '\t' for k in range(7)],
                    '({})'.format(scale[0].get_name_old(show_group=False).replace('b', r'$\flat$').replace('#', r'$\sharp$'))
                )
                print(scale_text)
                scale_text = TextMobject(*scale_text).scale(0.8)
                scale_text.move_to(DOWN+np.array((0, 0.5, 0)))
                return scale_text

            scale_text = _scale_text(scale, tonic_name, scale_type_alt)
            scale_text[0].set_color(BLUE)
            if real_tonic in main_seq:
                scale_text[3].set_color(BLUE)
                scale_text[-1].set_color(BLUE)

            # highlight tonic note (blue)
            if real_tonic in main_seq:
                self.play(FadeToColor(hands[real_tonic], BLUE), FadeInFromDown(scale_text))
            else:
                hands[real_tonic].set_opacity(0.5)
                self.play(FadeToColor(hands[real_tonic].set_opacity(0.5), BLUE), FadeInFromDown(scale_text))

            # play the scale with highlight color orange
            def _play(notes, offset, scale_text):
                # note 1
                hands[(notes[0]+offset)%12].set_color(ORANGE)
                scale_text[3].set_color(ORANGE)
                self.add_sound(sounds[notes[0]], gain=-12)
                self.wait(0.5)
                if real_tonic in main_seq:
                    hands[(notes[0]+offset)%12].set_color(BLUE)
                    scale_text[3].set_color(BLUE)
                else:
                    hands[(notes[0]+offset)%12].set_color(WHITE)
                    scale_text[3].set_color(WHITE)
                # note 2-6
                for idx, i in enumerate(notes[1:]):
                    hands[(i+offset)%12].set_color(ORANGE)
                    scale_text[idx+4].set_color(ORANGE)
                    self.add_sound(sounds[i], gain=-12)
                    self.wait(0.5)
                    hands[(i+offset)%12].set_color(WHITE)
                    scale_text[idx+4].set_color(WHITE)
                # note 7
                hands[(notes[0]+offset)%12].set_color(ORANGE)
                scale_text[-1].set_color(ORANGE)
                self.add_sound(sounds[notes[0]+12], gain=-12)
                self.wait(0.5)
                if real_tonic in main_seq:
                    hands[(notes[0]+offset)%12].set_color(BLUE)
                    scale_text[-1].set_color(BLUE)
                else:
                    hands[(notes[0]+offset)%12].set_color(WHITE)
                    scale_text[-1].set_color(WHITE)

            _play(notes, 0, scale_text)
            self.wait(0.5)

            if replay_on_c:
                # generate new text mobjects
                c_scale_text = _scale_text(c_scale, 'C', scale_type_alt)
                c_scale_text[0].set_color(BLUE)
                if real_tonic in main_seq:
                    c_scale_text[3].set_color(BLUE)
                    c_scale_text[-1].set_color(BLUE)
                # rotate and play scale from c
                offset = real_tonic if notes[0]%12 <= 6 else real_tonic-12
                ang = offset*PI/6
                original_scale_text = scale_text.copy()
                self.add_sound('audio_runs/rotate_1.wav', gain=-12)
                self.play(Rotate(hands, ang), Transform(scale_text, c_scale_text))
                self.wait(0.5)
                _play(c_notes, offset, scale_text)
                self.wait(0.5)
                self.add_sound('audio_runs/rotate_1.wav', gain=-12)
                self.play(Rotate(hands, -ang), Transform(scale_text, original_scale_text))

            # de-highlight tonic note
            if real_tonic in main_seq:
                self.play(FadeToColor(hands[real_tonic], WHITE), FadeOut(scale_text))
            else:
                self.play(FadeToColor(hands[real_tonic], WHITE), FadeOut(scale_text))
                hands[real_tonic].set_opacity(0)

        for k in range(7):
            choice = True if k != 1 else False
            play(tonic_names[k], scale_types[k], scale_types_alt[k], choice)

        self.play(FadeInFromDown(sub2))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(clock), FadeOut(sub2))


# class LydianS3(Scene):
#     def construct(self):
#         text = TextMobject(r'Lydian($\sharp$3)类音阶(第2类·第1阶)\\不常见，暂时略过').scale(0.8)
#         self.play(Write(text))
#         self.wait(2)
#         self.play(FadeOut(text))


class LydianS5(Scene):
    def construct(self):
        global R, O, C, omega, positions, pos_ticks, texts, sounds

        ''' generate constants and mobjects '''

        # clock face
        title = TextMobject(r'Lydian($\sharp$5)类音阶(第3类·第1阶)').move_to(UP-np.array((0, 0.5, 0))).scale(0.8)  # changed
        circle = Circle(radius=R, color=WHITE).flip(LEFT).rotate(PI/2)
        center_point = Point()
        ticks = VGroup(*[Line(pos*0.95, pos) for pos in pos_ticks])
        names = VGroup(*[TextMobject(text).move_to(pos_tick*1.3).scale(0.5) for text, pos_tick in zip(texts, pos_ticks)])
        hands = VGroup(*[Line(O, pos*0.65, color=WHITE).set_opacity(0) for i, pos in enumerate(pos_ticks)])
        nums = VGroup(*[TextMobject(str(k)).move_to(pos_tick*0.8).scale(0.5) for k, pos_tick in enumerate(pos_ticks)])
        clock = VGroup(circle, ticks, names, hands, nums)
        sub1 = TextMobject(r'Lydian($\sharp$5)类音阶可以通过Diatonic类音阶升高或降低一个音产生').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        sub2 = TextMobject(r'以上是全部的7种Lydian($\sharp$5)类音阶').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        tonic_names = 'FCGDAEB'
        scale_types = [r'Lydian(#5)', r'Ionian(#1)', r'Mixolydian(#4)', r'Dorian(#7)', r'Aeolian(#3)', r'Phrygian(#6)', r'Locrian(#2)']  # changed
        scale_types_alt = [r'Lydian($\sharp$5)', r'Ionian($\sharp$1) (Altered)', r'Mixolydian($\sharp$4) (Acoustic)', r'Dorian($\sharp$7) (旋律小调)',
                           r'Aeolian($\sharp$3) (旋律大调)', r'Phrygian($\sharp$6)', r'Locrian($\sharp$2) (Half Diminished)']  # changed
        diatonic_seq = [5, 7, 9, 11, 0, 2, 4]
        main_seq = diatonic_seq[:4] + [diatonic_seq[4]+1] + diatonic_seq[5:]  # changed
        print(main_seq)

        ''' make animation '''

        # create clock
        self.play(FadeInFromDown(title))
        self.play(ShowCreation(circle), FadeIn(ticks), Write(names), Write(nums))
        self.play(FadeInFromDown(sub1))
        self.wait(1)
        for k in diatonic_seq:
            self.play(ShowCreation(hands[k].set_opacity(1)), run_time=0.1)
        self.wait(1)

        # add accidentals
        sub1_new = TextMobject('F Lydian').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        self.play(Transform(sub1, sub1_new))
        tmp = hands[diatonic_seq[4]].copy().set_opacity(1)  # changed
        self.play(FadeToColor(tmp, YELLOW))
        hands[diatonic_seq[4]].set_opacity(0)  # changed
        self.add_sound('audio_runs/rotate_2.wav', gain=-12)
        self.play(Rotating(tmp, radians=-PI/6, about_point=ORIGIN, run_time=0.5))  # changed
        self.play(FadeToColor(tmp, WHITE))
        tmp.set_opacity(0)
        self.add(hands[main_seq[4]].set_opacity(1))  # changed
        sub1_new = TextMobject('F Lydian($\sharp$5)').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        self.play(Transform(sub1, sub1_new))

        self.wait(2)
        self.play(FadeOut(sub1))

        # def play altered diatonic scales function
        def play(tonic_name, scale_type, scale_type_alt, replay_on_c=True):
            # generate scales and note pitches
            # warning: when tonic_name = 'G', tonic may equal 'G#'
            scale = AlteredDiatonicScale(tonic_name + ' ' + scale_type)
            c_scale = AlteredDiatonicScale('C'+' '+scale_type)
            notes = [note for note in abs(scale)]
            c_notes = [note for note in abs(c_scale)]
            tonic = notes[0]%12
            c_tonic = c_notes[0]%12
            real_tonic = abs(Note(tonic_name))%12

            # generate text mobjects
            def _scale_text(scale, tonic_name, scale_type_alt):
                scale_text = (
                    tonic_name.replace('b', r'$\flat$').replace('#', r'$\sharp$')+' ',
                    scale_type_alt.replace('b', r'$\flat$').replace('#', r'$\sharp$'),
                    ' | ',
                    *[scale[k].get_name_old(show_group=False).replace('b', r'$\flat$').replace('#', r'$\sharp$') + '\t' for k in range(7)],
                    '({})'.format(scale[0].get_name_old(show_group=False).replace('b', r'$\flat$').replace('#', r'$\sharp$'))
                )
                print(scale_text)
                scale_text = TextMobject(*scale_text).scale(0.8)
                scale_text.move_to(DOWN+np.array((0, 0.5, 0)))
                return scale_text

            scale_text = _scale_text(scale, tonic_name, scale_type_alt)
            scale_text[0].set_color(BLUE)
            if real_tonic in main_seq:
                scale_text[3].set_color(BLUE)
                scale_text[-1].set_color(BLUE)

            # highlight tonic note (blue)
            if real_tonic in main_seq:
                self.play(FadeToColor(hands[real_tonic], BLUE), FadeInFromDown(scale_text))
            else:
                hands[real_tonic].set_opacity(0.5)
                self.play(FadeToColor(hands[real_tonic].set_opacity(0.5), BLUE), FadeInFromDown(scale_text))

            # play the scale with highlight color orange
            def _play(notes, offset, scale_text):
                # note 1
                hands[(notes[0]+offset)%12].set_color(ORANGE)
                scale_text[3].set_color(ORANGE)
                self.add_sound(sounds[notes[0]], gain=-12)
                self.wait(0.5)
                if real_tonic in main_seq:
                    hands[(notes[0]+offset)%12].set_color(BLUE)
                    scale_text[3].set_color(BLUE)
                else:
                    hands[(notes[0]+offset)%12].set_color(WHITE)
                    scale_text[3].set_color(WHITE)
                # note 2-6
                for idx, i in enumerate(notes[1:]):
                    hands[(i+offset)%12].set_color(ORANGE)
                    scale_text[idx+4].set_color(ORANGE)
                    self.add_sound(sounds[i], gain=-12)
                    self.wait(0.5)
                    hands[(i+offset)%12].set_color(WHITE)
                    scale_text[idx+4].set_color(WHITE)
                # note 7
                hands[(notes[0]+offset)%12].set_color(ORANGE)
                scale_text[-1].set_color(ORANGE)
                self.add_sound(sounds[notes[0]+12], gain=-12)
                self.wait(0.5)
                if real_tonic in main_seq:
                    hands[(notes[0]+offset)%12].set_color(BLUE)
                    scale_text[-1].set_color(BLUE)
                else:
                    hands[(notes[0]+offset)%12].set_color(WHITE)
                    scale_text[-1].set_color(WHITE)

            _play(notes, 0, scale_text)
            self.wait(0.5)

            if replay_on_c:
                # generate new text mobjects
                c_scale_text = _scale_text(c_scale, 'C', scale_type_alt)
                c_scale_text[0].set_color(BLUE)
                if real_tonic in main_seq:
                    c_scale_text[3].set_color(BLUE)
                    c_scale_text[-1].set_color(BLUE)
                # rotate and play scale from c
                offset = real_tonic if notes[0]%12 <= 6 else real_tonic-12
                ang = offset*PI/6
                original_scale_text = scale_text.copy()
                self.add_sound('audio_runs/rotate_1.wav', gain=-12)
                self.play(Rotate(hands, ang), Transform(scale_text, c_scale_text))
                self.wait(0.5)
                _play(c_notes, offset, scale_text)
                self.wait(0.5)
                self.add_sound('audio_runs/rotate_1.wav', gain=-12)
                self.play(Rotate(hands, -ang), Transform(scale_text, original_scale_text))

            # de-highlight tonic note
            if real_tonic in main_seq:
                self.play(FadeToColor(hands[real_tonic], WHITE), FadeOut(scale_text))
            else:
                self.play(FadeToColor(hands[real_tonic], WHITE), FadeOut(scale_text))
                hands[real_tonic].set_opacity(0)

        for k in range(7):
            choice = True if k != 1 else False
            play(tonic_names[k], scale_types[k], scale_types_alt[k], choice)

        self.play(FadeInFromDown(sub2))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(clock), FadeOut(sub2))
        extra_note = TextMobject(r'关于Lydian($\sharp$5)类音阶还有一些要提及的东西 \\'
                                 r'\phantom{!} \\'
                                 r'X Lydian($\sharp$5) = X$\sharp$ Phrygian($\flat$1) \\'
                                 r'X$\flat$ Ionian($\sharp$1) (Altered) = X Locrian($\flat$4) \\'
                                 r'X Mixolydian($\sharp$4) (Acoustic) = X Lydian($\flat$7) \\'
                                 r'X Dorian($\sharp$7) (旋律小调) = X Ionian($\flat$3) \\'
                                 r'X Aeolian($\sharp$3) (旋律大调) = X Mixolydian($\flat$6) \\'
                                 r'X Phrygian($\sharp$6) = X Dorian($\flat$2) \\'
                                 r'X Locrian($\sharp$2) (Half Diminished) = X Aeolian($\flat$5)').scale(0.8)
        self.play(Write(extra_note))
        self.wait(4)
        self.play(FadeOut(extra_note))


class LydianS6(Scene):
    def construct(self):
        global R, O, C, omega, positions, pos_ticks, texts, sounds

        ''' generate constants and mobjects '''

        # clock face
        title = TextMobject(r'Lydian($\sharp$6)类音阶(第4类·第1阶)').move_to(UP-np.array((0, 0.5, 0))).scale(0.8)  # changed
        circle = Circle(radius=R, color=WHITE).flip(LEFT).rotate(PI/2)
        center_point = Point()
        ticks = VGroup(*[Line(pos*0.95, pos) for pos in pos_ticks])
        names = VGroup(*[TextMobject(text).move_to(pos_tick*1.3).scale(0.5) for text, pos_tick in zip(texts, pos_ticks)])
        hands = VGroup(*[Line(O, pos*0.65, color=WHITE).set_opacity(0) for i, pos in enumerate(pos_ticks)])
        nums = VGroup(*[TextMobject(str(k)).move_to(pos_tick*0.8).scale(0.5) for k, pos_tick in enumerate(pos_ticks)])
        clock = VGroup(circle, ticks, names, hands, nums)
        sub1 = TextMobject(r'Lydian($\sharp$6)类音阶可以通过Diatonic类音阶升高一个音产生').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        sub2 = TextMobject(r'以上是全部的7种Lydian($\sharp$6)类音阶').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        tonic_names = 'FCGDAEB'
        scale_types = [r'Lydian(#6)', r'Ionian(#2)', r'Mixolydian(#5)', r'Dorian(#1)', r'Aeolian(#4)', r'Phrygian(#7)', r'Locrian(#3)']  # changed
        scale_types_alt = [r'Lydian($\sharp$6)', r'Ionian($\sharp$2)', r'Mixolydian($\sharp$5)', r'Dorian($\sharp$1)',
                           r'Aeolian($\sharp$4)', r'Phrygian($\sharp$7) (Minor Neapolitan)', r'Locrian($\sharp$3)']  # changed
        diatonic_seq = [5, 7, 9, 11, 0, 2, 4]
        main_seq = diatonic_seq[:5] + [diatonic_seq[5]+1] + diatonic_seq[6:]  # changed
        print(main_seq)

        ''' make animation '''

        # create clock
        self.play(FadeInFromDown(title))
        self.play(ShowCreation(circle), FadeIn(ticks), Write(names), Write(nums))
        self.play(FadeInFromDown(sub1))
        self.wait(1)
        for k in diatonic_seq:
            self.play(ShowCreation(hands[k].set_opacity(1)), run_time=0.1)
        self.wait(1)

        # add accidentals
        sub1_new = TextMobject('F Lydian').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        self.play(Transform(sub1, sub1_new))
        tmp = hands[diatonic_seq[5]].copy().set_opacity(1)  # changed
        self.play(FadeToColor(tmp, YELLOW))
        hands[diatonic_seq[5]].set_opacity(0)  # changed
        self.add_sound('audio_runs/rotate_2.wav', gain=-12)
        self.play(Rotating(tmp, radians=-PI/6, about_point=ORIGIN, run_time=0.5))  # changed
        self.play(FadeToColor(tmp, WHITE))
        tmp.set_opacity(0)
        self.add(hands[main_seq[5]].set_opacity(1))  # changed
        sub1_new = TextMobject('F Lydian($\sharp$6)').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        self.play(Transform(sub1, sub1_new))

        self.wait(2)
        self.play(FadeOut(sub1))

        # def play altered diatonic scales function
        def play(tonic_name, scale_type, scale_type_alt, replay_on_c=True):
            # generate scales and note pitches
            # warning: when tonic_name = 'G', tonic may equal 'G#'
            scale = AlteredDiatonicScale(tonic_name + ' ' + scale_type)
            c_scale = AlteredDiatonicScale('C'+' '+scale_type)
            notes = [note for note in abs(scale)]
            c_notes = [note for note in abs(c_scale)]
            tonic = notes[0]%12
            c_tonic = c_notes[0]%12
            real_tonic = abs(Note(tonic_name))%12

            # generate text mobjects
            def _scale_text(scale, tonic_name, scale_type_alt):
                scale_text = (
                    tonic_name.replace('b', r'$\flat$').replace('#', r'$\sharp$')+' ',
                    scale_type_alt.replace('b', r'$\flat$').replace('#', r'$\sharp$'),
                    ' | ',
                    *[scale[k].get_name_old(show_group=False).replace('b', r'$\flat$').replace('#', r'$\sharp$') + '\t' for k in range(7)],
                    '({})'.format(scale[0].get_name_old(show_group=False).replace('b', r'$\flat$').replace('#', r'$\sharp$'))
                )
                print(scale_text)
                scale_text = TextMobject(*scale_text).scale(0.8)
                scale_text.move_to(DOWN+np.array((0, 0.5, 0)))
                return scale_text

            scale_text = _scale_text(scale, tonic_name, scale_type_alt)
            scale_text[0].set_color(BLUE)
            if real_tonic in main_seq:
                scale_text[3].set_color(BLUE)
                scale_text[-1].set_color(BLUE)

            # highlight tonic note (blue)
            if real_tonic in main_seq:
                self.play(FadeToColor(hands[real_tonic], BLUE), FadeInFromDown(scale_text))
            else:
                hands[real_tonic].set_opacity(0.5)
                self.play(FadeToColor(hands[real_tonic].set_opacity(0.5), BLUE), FadeInFromDown(scale_text))

            # play the scale with highlight color orange
            def _play(notes, offset, scale_text):
                # note 1
                hands[(notes[0]+offset)%12].set_color(ORANGE)
                scale_text[3].set_color(ORANGE)
                self.add_sound(sounds[notes[0]], gain=-12)
                self.wait(0.5)
                if real_tonic in main_seq:
                    hands[(notes[0]+offset)%12].set_color(BLUE)
                    scale_text[3].set_color(BLUE)
                else:
                    hands[(notes[0]+offset)%12].set_color(WHITE)
                    scale_text[3].set_color(WHITE)
                # note 2-6
                for idx, i in enumerate(notes[1:]):
                    hands[(i+offset)%12].set_color(ORANGE)
                    scale_text[idx+4].set_color(ORANGE)
                    self.add_sound(sounds[i], gain=-12)
                    self.wait(0.5)
                    hands[(i+offset)%12].set_color(WHITE)
                    scale_text[idx+4].set_color(WHITE)
                # note 7
                hands[(notes[0]+offset)%12].set_color(ORANGE)
                scale_text[-1].set_color(ORANGE)
                self.add_sound(sounds[notes[0]+12], gain=-12)
                self.wait(0.5)
                if real_tonic in main_seq:
                    hands[(notes[0]+offset)%12].set_color(BLUE)
                    scale_text[-1].set_color(BLUE)
                else:
                    hands[(notes[0]+offset)%12].set_color(WHITE)
                    scale_text[-1].set_color(WHITE)

            _play(notes, 0, scale_text)
            self.wait(0.5)

            if replay_on_c:
                # generate new text mobjects
                c_scale_text = _scale_text(c_scale, 'C', scale_type_alt)
                c_scale_text[0].set_color(BLUE)
                if real_tonic in main_seq:
                    c_scale_text[3].set_color(BLUE)
                    c_scale_text[-1].set_color(BLUE)
                # rotate and play scale from c
                offset = real_tonic if notes[0]%12 <= 6 else real_tonic-12
                ang = offset*PI/6
                original_scale_text = scale_text.copy()
                self.add_sound('audio_runs/rotate_1.wav', gain=-12)
                self.play(Rotate(hands, ang), Transform(scale_text, c_scale_text))
                self.wait(0.5)
                _play(c_notes, offset, scale_text)
                self.wait(0.5)
                self.add_sound('audio_runs/rotate_1.wav', gain=-12)
                self.play(Rotate(hands, -ang), Transform(scale_text, original_scale_text))

            # de-highlight tonic note
            if real_tonic in main_seq:
                self.play(FadeToColor(hands[real_tonic], WHITE), FadeOut(scale_text))
            else:
                self.play(FadeToColor(hands[real_tonic], WHITE), FadeOut(scale_text))
                hands[real_tonic].set_opacity(0)

        for k in range(7):
            choice = True if k != 1 else False
            play(tonic_names[k], scale_types[k], scale_types_alt[k], choice)

        self.play(FadeInFromDown(sub2))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(clock), FadeOut(sub2))


# class LydianF2(Scene):
#     def construct(self):
#         text = TextMobject(r'Lydian($\flat$2)类音阶(第5类·第1阶)\\不常见，暂时略过').scale(0.8)
#         self.play(Write(text))
#         self.wait(2)
#         self.play(FadeOut(text))


class LydianF3(Scene):
    def construct(self):
        global R, O, C, omega, positions, pos_ticks, texts, sounds

        ''' generate constants and mobjects '''

        # clock face
        title = TextMobject(r'Lydian($\flat$3)类音阶(第6类·第1阶)').move_to(UP-np.array((0, 0.5, 0))).scale(0.8)  # changed
        circle = Circle(radius=R, color=WHITE).flip(LEFT).rotate(PI/2)
        center_point = Point()
        ticks = VGroup(*[Line(pos*0.95, pos) for pos in pos_ticks])
        names = VGroup(*[TextMobject(text).move_to(pos_tick*1.3).scale(0.5) for text, pos_tick in zip(texts, pos_ticks)])
        hands = VGroup(*[Line(O, pos*0.65, color=WHITE).set_opacity(0) for i, pos in enumerate(pos_ticks)])
        nums = VGroup(*[TextMobject(str(k)).move_to(pos_tick*0.8).scale(0.5) for k, pos_tick in enumerate(pos_ticks)])
        clock = VGroup(circle, ticks, names, hands, nums)
        sub1 = TextMobject(r'Lydian($\flat$3)音阶可以通过Diatonic类音阶降低一个音产生').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        sub2 = TextMobject(r'以上是全部的7种Lydian($\flat$3)类音阶').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        tonic_names = 'FCGDAEB'
        scale_types = [r'Lydian(b3)', r'Ionian(b6)', r'Mixolydian(b2)', r'Dorian(b5)', r'Aeolian(b1)', r'Phrygian(b4)', r'Locrian(b7)']  # changed
        scale_types_alt = [r'Lydian($\flat$3)', r'Ionian($\flat$6) (和声大调)', r'Mixolydian($\flat$2)', r'Dorian($\flat$5)',
                           r'Aeolian($\flat$1)', r'Phrygian($\flat$4)', r'Locrian($\flat$7)']  # changed
        diatonic_seq = [5, 7, 9, 11, 0, 2, 4]
        main_seq = diatonic_seq[:2] + [diatonic_seq[2]-1] + diatonic_seq[3:]  # changed
        print(main_seq)

        ''' make animation '''

        # create clock
        self.play(FadeInFromDown(title))
        self.play(ShowCreation(circle), FadeIn(ticks), Write(names), Write(nums))
        self.play(FadeInFromDown(sub1))
        self.wait(1)
        for k in diatonic_seq:
            self.play(ShowCreation(hands[k].set_opacity(1)), run_time=0.1)
        self.wait(1)

        # add accidentals
        sub1_new = TextMobject('F Lydian').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        self.play(Transform(sub1, sub1_new))
        tmp = hands[diatonic_seq[2]].copy().set_opacity(1)  # changed
        self.play(FadeToColor(tmp, YELLOW))
        hands[diatonic_seq[2]].set_opacity(0)  # changed
        self.add_sound('audio_runs/rotate_2.wav', gain=-12)
        self.play(Rotating(tmp, radians=PI/6, about_point=ORIGIN, run_time=0.5))  # changed
        self.play(FadeToColor(tmp, WHITE))
        tmp.set_opacity(0)
        self.add(hands[main_seq[2]].set_opacity(1))  # changed
        sub1_new = TextMobject(r'F Lydian($\flat$3)').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        self.play(Transform(sub1, sub1_new))

        self.wait(2)
        self.play(FadeOut(sub1))

        # def play altered diatonic scales function
        def play(tonic_name, scale_type, scale_type_alt, replay_on_c=True):
            # generate scales and note pitches
            # warning: when tonic_name = 'G', tonic may equal 'G#'
            scale = AlteredDiatonicScale(tonic_name + ' ' + scale_type)
            c_scale = AlteredDiatonicScale('C'+' '+scale_type)
            notes = [note for note in abs(scale)]
            c_notes = [note for note in abs(c_scale)]
            tonic = notes[0]%12
            c_tonic = c_notes[0]%12
            real_tonic = abs(Note(tonic_name))%12

            # generate text mobjects
            def _scale_text(scale, tonic_name, scale_type_alt):
                scale_text = (
                    tonic_name.replace('b', r'$\flat$').replace('#', r'$\sharp$')+' ',
                    scale_type_alt.replace('b', r'$\flat$').replace('#', r'$\sharp$'),
                    ' | ',
                    *[scale[k].get_name_old(show_group=False).replace('b', r'$\flat$').replace('#', r'$\sharp$') + '\t' for k in range(7)],
                    '({})'.format(scale[0].get_name_old(show_group=False).replace('b', r'$\flat$').replace('#', r'$\sharp$'))
                )
                print(scale_text)
                scale_text = TextMobject(*scale_text).scale(0.8)
                scale_text.move_to(DOWN+np.array((0, 0.5, 0)))
                return scale_text

            scale_text = _scale_text(scale, tonic_name, scale_type_alt)
            scale_text[0].set_color(BLUE)
            if real_tonic in main_seq:
                scale_text[3].set_color(BLUE)
                scale_text[-1].set_color(BLUE)

            # highlight tonic note (blue)
            if real_tonic in main_seq:
                self.play(FadeToColor(hands[real_tonic], BLUE), FadeInFromDown(scale_text))
            else:
                hands[real_tonic].set_opacity(0.5)
                self.play(FadeToColor(hands[real_tonic].set_opacity(0.5), BLUE), FadeInFromDown(scale_text))

            # play the scale with highlight color orange
            def _play(notes, offset, scale_text):
                # note 1
                hands[(notes[0]+offset)%12].set_color(ORANGE)
                scale_text[3].set_color(ORANGE)
                self.add_sound(sounds[notes[0]], gain=-12)
                self.wait(0.5)
                if real_tonic in main_seq:
                    hands[(notes[0]+offset)%12].set_color(BLUE)
                    scale_text[3].set_color(BLUE)
                else:
                    hands[(notes[0]+offset)%12].set_color(WHITE)
                    scale_text[3].set_color(WHITE)
                # note 2-6
                for idx, i in enumerate(notes[1:]):
                    hands[(i+offset)%12].set_color(ORANGE)
                    scale_text[idx+4].set_color(ORANGE)
                    self.add_sound(sounds[i], gain=-12)
                    self.wait(0.5)
                    hands[(i+offset)%12].set_color(WHITE)
                    scale_text[idx+4].set_color(WHITE)
                # note 7
                hands[(notes[0]+offset)%12].set_color(ORANGE)
                scale_text[-1].set_color(ORANGE)
                self.add_sound(sounds[notes[0]+12], gain=-12)
                self.wait(0.5)
                if real_tonic in main_seq:
                    hands[(notes[0]+offset)%12].set_color(BLUE)
                    scale_text[-1].set_color(BLUE)
                else:
                    hands[(notes[0]+offset)%12].set_color(WHITE)
                    scale_text[-1].set_color(WHITE)

            _play(notes, 0, scale_text)
            self.wait(0.5)

            if replay_on_c:
                # generate new text mobjects
                c_scale_text = _scale_text(c_scale, 'C', scale_type_alt)
                c_scale_text[0].set_color(BLUE)
                if real_tonic in main_seq:
                    c_scale_text[3].set_color(BLUE)
                    c_scale_text[-1].set_color(BLUE)
                # rotate and play scale from c
                offset = real_tonic if notes[0]%12 <= 6 else real_tonic-12
                ang = offset*PI/6
                original_scale_text = scale_text.copy()
                self.add_sound('audio_runs/rotate_1.wav', gain=-12)
                self.play(Rotate(hands, ang), Transform(scale_text, c_scale_text))
                self.wait(0.5)
                _play(c_notes, offset, scale_text)
                self.wait(0.5)
                self.add_sound('audio_runs/rotate_1.wav', gain=-12)
                self.play(Rotate(hands, -ang), Transform(scale_text, original_scale_text))

            # de-highlight tonic note
            if real_tonic in main_seq:
                self.play(FadeToColor(hands[real_tonic], WHITE), FadeOut(scale_text))
            else:
                self.play(FadeToColor(hands[real_tonic], WHITE), FadeOut(scale_text))
                hands[real_tonic].set_opacity(0)

        for k in range(7):
            choice = True if k != 1 else False
            play(tonic_names[k], scale_types[k], scale_types_alt[k], choice)

        self.play(FadeInFromDown(sub2))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(clock), FadeOut(sub2))


class LydianF6(Scene):
    def construct(self):
        global R, O, C, omega, positions, pos_ticks, texts, sounds

        ''' generate constants and mobjects '''

        # clock face
        title = TextMobject(r'Lydian($\flat$6)类音阶(第7类·第1阶)').move_to(UP-np.array((0, 0.5, 0))).scale(0.8)  # changed
        circle = Circle(radius=R, color=WHITE).flip(LEFT).rotate(PI/2)
        center_point = Point()
        ticks = VGroup(*[Line(pos*0.95, pos) for pos in pos_ticks])
        names = VGroup(*[TextMobject(text).move_to(pos_tick*1.3).scale(0.5) for text, pos_tick in zip(texts, pos_ticks)])
        hands = VGroup(*[Line(O, pos*0.65, color=WHITE).set_opacity(0) for i, pos in enumerate(pos_ticks)])
        nums = VGroup(*[TextMobject(str(k)).move_to(pos_tick*0.8).scale(0.5) for k, pos_tick in enumerate(pos_ticks)])
        clock = VGroup(circle, ticks, names, hands, nums)
        sub1 = TextMobject(r'Lydian($\flat$6)类音阶可以通过Diatonic类音阶降低一个音产生').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        sub2 = TextMobject(r'以上是全部的7种Lydian($\flat$6)类音阶').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        tonic_names = 'FCGDAEB'
        scale_types = [r'Lydian(b6)', r'Ionian(b2)', r'Mixolydian(b5)', r'Dorian(b1)', r'Aeolian(b4)', r'Phrygian(b7)', r'Locrian(b3)']  # changed
        scale_types_alt = [r'Lydian($\flat$6)', r'Ionian($\flat$2)', r'Mixolydian($\flat$5)', r'Dorian($\flat$1)',
                           r'Aeolian($\flat$4)', r'Phrygian($\flat$7)', r'Locrian($\flat$3)']  # changed
        diatonic_seq = [5, 7, 9, 11, 0, 2, 4]
        main_seq = diatonic_seq[:5] + [diatonic_seq[5]-1] + diatonic_seq[6:]  # changed
        print(main_seq)

        ''' make animation '''

        # create clock
        self.play(FadeInFromDown(title))
        self.play(ShowCreation(circle), FadeIn(ticks), Write(names), Write(nums))
        self.play(FadeInFromDown(sub1))
        self.wait(1)
        for k in diatonic_seq:
            self.play(ShowCreation(hands[k].set_opacity(1)), run_time=0.1)
        self.wait(1)

        # add accidentals
        sub1_new = TextMobject('F Lydian').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        self.play(Transform(sub1, sub1_new))
        tmp = hands[diatonic_seq[5]].copy().set_opacity(1)  # changed
        self.play(FadeToColor(tmp, YELLOW))
        hands[diatonic_seq[5]].set_opacity(0)  # changed
        self.add_sound('audio_runs/rotate_2.wav', gain=-12)
        self.play(Rotating(tmp, radians=PI/6, about_point=ORIGIN, run_time=0.5))  # changed
        self.play(FadeToColor(tmp, WHITE))
        tmp.set_opacity(0)
        self.add(hands[main_seq[5]].set_opacity(1))  # changed
        sub1_new = TextMobject(r'F Lydian($\flat$6)').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        self.play(Transform(sub1, sub1_new))

        self.wait(2)
        self.play(FadeOut(sub1))

        # def play altered diatonic scales function
        def play(tonic_name, scale_type, scale_type_alt, replay_on_c=True):
            # generate scales and note pitches
            # warning: when tonic_name = 'G', tonic may equal 'G#'
            scale = AlteredDiatonicScale(tonic_name + ' ' + scale_type)
            c_scale = AlteredDiatonicScale('C'+' '+scale_type)
            notes = [note for note in abs(scale)]
            c_notes = [note for note in abs(c_scale)]
            tonic = notes[0]%12
            c_tonic = c_notes[0]%12
            real_tonic = abs(Note(tonic_name))%12

            # generate text mobjects
            def _scale_text(scale, tonic_name, scale_type_alt):
                scale_text = (
                    tonic_name.replace('b', r'$\flat$').replace('#', r'$\sharp$')+' ',
                    scale_type_alt.replace('b', r'$\flat$').replace('#', r'$\sharp$'),
                    ' | ',
                    *[scale[k].get_name_old(show_group=False).replace('b', r'$\flat$').replace('#', r'$\sharp$') + '\t' for k in range(7)],
                    '({})'.format(scale[0].get_name_old(show_group=False).replace('b', r'$\flat$').replace('#', r'$\sharp$'))
                )
                print(scale_text)
                scale_text = TextMobject(*scale_text).scale(0.8)
                scale_text.move_to(DOWN+np.array((0, 0.5, 0)))
                return scale_text

            scale_text = _scale_text(scale, tonic_name, scale_type_alt)
            scale_text[0].set_color(BLUE)
            if real_tonic in main_seq:
                scale_text[3].set_color(BLUE)
                scale_text[-1].set_color(BLUE)

            # highlight tonic note (blue)
            if real_tonic in main_seq:
                self.play(FadeToColor(hands[real_tonic], BLUE), FadeInFromDown(scale_text))
            else:
                hands[real_tonic].set_opacity(0.5)
                self.play(FadeToColor(hands[real_tonic].set_opacity(0.5), BLUE), FadeInFromDown(scale_text))

            # play the scale with highlight color orange
            def _play(notes, offset, scale_text):
                # note 1
                hands[(notes[0]+offset)%12].set_color(ORANGE)
                scale_text[3].set_color(ORANGE)
                self.add_sound(sounds[notes[0]], gain=-12)
                self.wait(0.5)
                if real_tonic in main_seq:
                    hands[(notes[0]+offset)%12].set_color(BLUE)
                    scale_text[3].set_color(BLUE)
                else:
                    hands[(notes[0]+offset)%12].set_color(WHITE)
                    scale_text[3].set_color(WHITE)
                # note 2-6
                for idx, i in enumerate(notes[1:]):
                    hands[(i+offset)%12].set_color(ORANGE)
                    scale_text[idx+4].set_color(ORANGE)
                    self.add_sound(sounds[i], gain=-12)
                    self.wait(0.5)
                    hands[(i+offset)%12].set_color(WHITE)
                    scale_text[idx+4].set_color(WHITE)
                # note 7
                hands[(notes[0]+offset)%12].set_color(ORANGE)
                scale_text[-1].set_color(ORANGE)
                self.add_sound(sounds[notes[0]+12], gain=-12)
                self.wait(0.5)
                if real_tonic in main_seq:
                    hands[(notes[0]+offset)%12].set_color(BLUE)
                    scale_text[-1].set_color(BLUE)
                else:
                    hands[(notes[0]+offset)%12].set_color(WHITE)
                    scale_text[-1].set_color(WHITE)

            _play(notes, 0, scale_text)
            self.wait(0.5)

            if replay_on_c:
                # generate new text mobjects
                c_scale_text = _scale_text(c_scale, 'C', scale_type_alt)
                c_scale_text[0].set_color(BLUE)
                if real_tonic in main_seq:
                    c_scale_text[3].set_color(BLUE)
                    c_scale_text[-1].set_color(BLUE)
                # rotate and play scale from c
                offset = real_tonic if notes[0]%12 <= 6 else real_tonic-12
                ang = offset*PI/6
                original_scale_text = scale_text.copy()
                self.add_sound('audio_runs/rotate_1.wav', gain=-12)
                self.play(Rotate(hands, ang), Transform(scale_text, c_scale_text))
                self.wait(0.5)
                _play(c_notes, offset, scale_text)
                self.wait(0.5)
                self.add_sound('audio_runs/rotate_1.wav', gain=-12)
                self.play(Rotate(hands, -ang), Transform(scale_text, original_scale_text))

            # de-highlight tonic note
            if real_tonic in main_seq:
                self.play(FadeToColor(hands[real_tonic], WHITE), FadeOut(scale_text))
            else:
                self.play(FadeToColor(hands[real_tonic], WHITE), FadeOut(scale_text))
                hands[real_tonic].set_opacity(0)

        for k in range(7):
            choice = True if k != 1 else False
            play(tonic_names[k], scale_types[k], scale_types_alt[k], choice)

        self.play(FadeInFromDown(sub2))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(clock), FadeOut(sub2))


''' order 2 '''


class In3(Scene):
    def construct(self):
        text = TextMobject(r'到Diatonic类音阶的结构距离为2的类属于第2阶。第2阶包含15个类：'
                           r'\begin{enumerate}'
                           r'\item $\cdots$'
                           r'\item (第9类·第2阶) Lydian($\sharp$2,$\sharp$6)类音阶。它包含了 Hungarian Minor 音阶、Double Harmonic 等音阶'
                           r'\item $\cdots$'
                           r'\item (第16类·第2阶) Lydian($\sharp$5,$\sharp$6)类音阶。它包含了 Major Neapolitan (Melodic Phrygian) 等音阶'
                           r'\item $\cdots$'
                           r'\end{enumerate}').scale(0.65)
        self.wait(0.5)
        self.play(Write(text))
        self.wait(7.5)
        self.play(FadeOut(text))


class LydianS2S6(Scene):
    def construct(self):
        global R, O, C, omega, positions, pos_ticks, texts, sounds

        ''' generate constants and mobjects '''

        # clock face
        title = TextMobject(r'Lydian($\sharp$2,$\sharp$6)类音阶(第9类·第2阶)').move_to(UP-np.array((0, 0.5, 0))).scale(0.8)  # changed
        circle = Circle(radius=R, color=WHITE).flip(LEFT).rotate(PI/2)
        center_point = Point()
        ticks = VGroup(*[Line(pos*0.95, pos) for pos in pos_ticks])
        names = VGroup(*[TextMobject(text).move_to(pos_tick*1.3).scale(0.5) for text, pos_tick in zip(texts, pos_ticks)])
        hands = VGroup(*[Line(O, pos*0.65, color=WHITE).set_opacity(0) for i, pos in enumerate(pos_ticks)])
        nums = VGroup(*[TextMobject(str(k)).move_to(pos_tick*0.8).scale(0.5) for k, pos_tick in enumerate(pos_ticks)])
        clock = VGroup(circle, ticks, names, hands, nums)
        sub1 = TextMobject(r'Lydian($\sharp$2,$\sharp$6)类音阶可以通过Diatonic类音阶升高或降低两个音产生').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        sub2 = TextMobject(r'以上是全部的7种Lydian($\sharp$2,$\sharp$6)类音阶').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        tonic_names = 'FCGDAEB'
        scale_types = [r'Lydian(#2,#6)', r'Ionian(#2,#5)', r'Mixolydian(#1,#5)', r'Dorian(#1,#4)', r'Aeolian(#4,#7)', r'Phrygian(#3,#7)', r'Locrian(#3,#6)']  # changed
        scale_types_alt = [r'Lydian($\sharp$2,$\sharp$6)', r'Ionian($\sharp$2,$\sharp$5)', r'Mixolydian($\sharp$1,$\sharp$5)', r'Dorian($\sharp$1,$\sharp$4)',
                           r'Aeolian($\sharp$4,$\sharp$7) (Hungarian Minor)', r'Phrygian($\sharp$3,$\sharp$7) (Double Harmonic)', r'Locrian($\sharp$3,$\sharp$6)']  # changed
        diatonic_seq = [5, 7, 9, 11, 0, 2, 4]
        main_seq = diatonic_seq[:1] + [diatonic_seq[1]+1] + diatonic_seq[2:5] + [diatonic_seq[5]+1] + diatonic_seq[6:]  # changed
        print(main_seq)

        ''' make animation '''

        # create clock
        self.play(FadeInFromDown(title))
        self.play(ShowCreation(circle), FadeIn(ticks), Write(names), Write(nums))
        self.play(FadeInFromDown(sub1))
        self.wait(1)
        for k in diatonic_seq:
            self.play(ShowCreation(hands[k].set_opacity(1)), run_time=0.1)
        self.wait(1)

        # add accidentals
        sub1_new = TextMobject('F Lydian').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        self.play(Transform(sub1, sub1_new))
        tmp = hands[diatonic_seq[1]].copy().set_opacity(1)  # changed
        self.play(FadeToColor(tmp, YELLOW))
        hands[diatonic_seq[1]].set_opacity(0)  # changed
        self.add_sound('audio_runs/rotate_2.wav', gain=-12)
        self.play(Rotating(tmp, radians=-PI/6, about_point=ORIGIN, run_time=0.5))  # changed
        self.play(FadeToColor(tmp, WHITE))
        tmp.set_opacity(0)
        self.add(hands[main_seq[1]].set_opacity(1))  # changed
        sub1_new = TextMobject('F Lydian($\sharp$2)').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        self.play(Transform(sub1, sub1_new))

        tmp = hands[diatonic_seq[5]].copy().set_opacity(1)  # changed
        self.play(FadeToColor(tmp, YELLOW))
        hands[diatonic_seq[5]].set_opacity(0)  # changed
        self.add_sound('audio_runs/rotate_2.wav', gain=-12)
        self.play(Rotating(tmp, radians=-PI/6, about_point=ORIGIN, run_time=0.5))  # changed
        self.play(FadeToColor(tmp, WHITE))
        tmp.set_opacity(0)
        self.add(hands[main_seq[5]].set_opacity(1))  # changed
        sub1_new = TextMobject('F Lydian($\sharp$2,$\sharp$6)').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        self.play(Transform(sub1, sub1_new))

        self.wait(2)
        self.play(FadeOut(sub1))

        # def play altered diatonic scales function
        def play(tonic_name, scale_type, scale_type_alt, replay_on_c=True):
            # generate scales and note pitches
            # warning: when tonic_name = 'G', tonic may equal 'G#'
            scale = AlteredDiatonicScale(tonic_name + ' ' + scale_type)
            c_scale = AlteredDiatonicScale('C'+' '+scale_type)
            notes = [note for note in abs(scale)]
            c_notes = [note for note in abs(c_scale)]
            tonic = notes[0]%12
            c_tonic = c_notes[0]%12
            real_tonic = abs(Note(tonic_name))%12

            # generate text mobjects
            def _scale_text(scale, tonic_name, scale_type_alt):
                scale_text = (
                    tonic_name.replace('b', r'$\flat$').replace('#', r'$\sharp$')+' ',
                    scale_type_alt.replace('b', r'$\flat$').replace('#', r'$\sharp$').replace(r'u$\flat$l', 'ubl'),
                    ' | ',
                    *[scale[k].get_name_old(show_group=False).replace('b', r'$\flat$').replace('#', r'$\sharp$') + '\t' for k in range(7)],
                    '({})'.format(scale[0].get_name_old(show_group=False).replace('b', r'$\flat$').replace('#', r'$\sharp$'))
                )
                print(scale_text)
                scale_text = TextMobject(*scale_text).scale(0.8)
                scale_text.move_to(DOWN+np.array((0, 0.5, 0)))
                return scale_text

            scale_text = _scale_text(scale, tonic_name, scale_type_alt)
            scale_text[0].set_color(BLUE)
            if real_tonic in main_seq:
                scale_text[3].set_color(BLUE)
                scale_text[-1].set_color(BLUE)

            # highlight tonic note (blue)
            if real_tonic in main_seq:
                self.play(FadeToColor(hands[real_tonic], BLUE), FadeInFromDown(scale_text))
            else:
                hands[real_tonic].set_opacity(0.5)
                self.play(FadeToColor(hands[real_tonic].set_opacity(0.5), BLUE), FadeInFromDown(scale_text))

            # play the scale with highlight color orange
            def _play(notes, offset, scale_text):
                # note 1
                hands[(notes[0]+offset)%12].set_color(ORANGE)
                scale_text[3].set_color(ORANGE)
                self.add_sound(sounds[notes[0]], gain=-12)
                self.wait(0.5)
                if real_tonic in main_seq:
                    hands[(notes[0]+offset)%12].set_color(BLUE)
                    scale_text[3].set_color(BLUE)
                else:
                    hands[(notes[0]+offset)%12].set_color(WHITE)
                    scale_text[3].set_color(WHITE)
                # note 2-6
                for idx, i in enumerate(notes[1:]):
                    hands[(i+offset)%12].set_color(ORANGE)
                    scale_text[idx+4].set_color(ORANGE)
                    self.add_sound(sounds[i], gain=-12)
                    self.wait(0.5)
                    hands[(i+offset)%12].set_color(WHITE)
                    scale_text[idx+4].set_color(WHITE)
                # note 7
                hands[(notes[0]+offset)%12].set_color(ORANGE)
                scale_text[-1].set_color(ORANGE)
                self.add_sound(sounds[notes[0]+12], gain=-12)
                self.wait(0.5)
                if real_tonic in main_seq:
                    hands[(notes[0]+offset)%12].set_color(BLUE)
                    scale_text[-1].set_color(BLUE)
                else:
                    hands[(notes[0]+offset)%12].set_color(WHITE)
                    scale_text[-1].set_color(WHITE)

            _play(notes, 0, scale_text)
            self.wait(0.5)

            if replay_on_c:
                # generate new text mobjects
                c_scale_text = _scale_text(c_scale, 'C', scale_type_alt)
                c_scale_text[0].set_color(BLUE)
                if real_tonic in main_seq:
                    c_scale_text[3].set_color(BLUE)
                    c_scale_text[-1].set_color(BLUE)
                # rotate and play scale from c
                offset = real_tonic if notes[0]%12 <= 6 else real_tonic-12
                ang = offset*PI/6
                original_scale_text = scale_text.copy()
                self.add_sound('audio_runs/rotate_1.wav', gain=-12)
                self.play(Rotate(hands, ang), Transform(scale_text, c_scale_text))
                self.wait(0.5)
                _play(c_notes, offset, scale_text)
                self.wait(0.5)
                self.add_sound('audio_runs/rotate_1.wav', gain=-12)
                self.play(Rotate(hands, -ang), Transform(scale_text, original_scale_text))

            # de-highlight tonic note
            if real_tonic in main_seq:
                self.play(FadeToColor(hands[real_tonic], WHITE), FadeOut(scale_text))
            else:
                self.play(FadeToColor(hands[real_tonic], WHITE), FadeOut(scale_text))
                hands[real_tonic].set_opacity(0)

        for k in range(7):
            choice = True if k != 1 else False
            play(tonic_names[k], scale_types[k], scale_types_alt[k], choice)

        self.play(FadeInFromDown(sub2))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(clock), FadeOut(sub2))
        extra_note = TextMobject(r'关于Lydian($\sharp$2,$\sharp$6)类音阶还有一些要提及的东西 \\'
                                 r'\phantom{!} \\'
                                 r'$\vdots$ \\'
                                 r'X Aeolian($\sharp$4,$\sharp$7) (Hungarian Minor) = X Lydian($\flat$3,$\flat$6) \\'
                                 r'X Phrygian($\sharp$3,$\sharp$7) (Double Harmonic) = X Ionian($\flat$2,$\flat$6) \\'
                                 r'$\vdots$').scale(0.8)
        self.play(Write(extra_note))
        self.wait(4)
        self.play(FadeOut(extra_note))


class LydianS5S6(Scene):
    def construct(self):
        global R, O, C, omega, positions, pos_ticks, texts, sounds

        ''' generate constants and mobjects '''

        # clock face
        title = TextMobject(r'Lydian($\sharp$5,$\sharp$6)类音阶(第16类·第2阶)').move_to(UP-np.array((0, 0.5, 0))).scale(0.8)  # changed
        circle = Circle(radius=R, color=WHITE).flip(LEFT).rotate(PI/2)
        center_point = Point()
        ticks = VGroup(*[Line(pos*0.95, pos) for pos in pos_ticks])
        names = VGroup(*[TextMobject(text).move_to(pos_tick*1.3).scale(0.5) for text, pos_tick in zip(texts, pos_ticks)])
        hands = VGroup(*[Line(O, pos*0.65, color=WHITE).set_opacity(0) for i, pos in enumerate(pos_ticks)])
        nums = VGroup(*[TextMobject(str(k)).move_to(pos_tick*0.8).scale(0.5) for k, pos_tick in enumerate(pos_ticks)])
        clock = VGroup(circle, ticks, names, hands, nums)
        sub1 = TextMobject(r'Lydian($\sharp$5,$\sharp$6)类音阶可以通过Diatonic类音阶变化两个音产生').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        sub2 = TextMobject(r'以上是全部的7种Lydian($\sharp$5,$\sharp$6)类音阶').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        tonic_names = 'FCGDAEB'
        scale_types = [r'Lydian(#5,#6)', r'Ionian(#1,#2)', r'Mixolydian(#4,#5)', r'Dorian(#1,#7)', r'Aeolian(#3,#4)', r'Phrygian(#6,#7)', r'Locrian(#2,#3)']  # changed
        scale_types_alt = [r'Lydian($\sharp$5,$\sharp$6)', r'Ionian($\sharp$1,$\sharp$2)', r'Mixolydian($\sharp$4,$\sharp$5)', r'Dorian($\sharp$1,$\sharp$7)',
                           r'Aeolian($\sharp$3,$\sharp$4)', r'Phrygian($\sharp$6,$\sharp$7) (Major Neapolitan)', r'Locrian($\sharp$2,$\sharp$3)']  # changed
        diatonic_seq = [5, 7, 9, 11, 0, 2, 4]
        main_seq = diatonic_seq[:4] + [diatonic_seq[4]+1] + diatonic_seq[5:5] + [diatonic_seq[5]+1] + diatonic_seq[6:]  # changed
        print(main_seq)

        ''' make animation '''

        # create clock
        self.play(FadeInFromDown(title))
        self.play(ShowCreation(circle), FadeIn(ticks), Write(names), Write(nums))
        self.play(FadeInFromDown(sub1))
        self.wait(1)
        for k in diatonic_seq:
            self.play(ShowCreation(hands[k].set_opacity(1)), run_time=0.1)
        self.wait(1)

        # add accidentals
        sub1_new = TextMobject('F Lydian').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        self.play(Transform(sub1, sub1_new))
        tmp = hands[diatonic_seq[4]].copy().set_opacity(1)  # changed
        self.play(FadeToColor(tmp, YELLOW))
        hands[diatonic_seq[4]].set_opacity(0)  # changed
        self.add_sound('audio_runs/rotate_2.wav', gain=-12)
        self.play(Rotating(tmp, radians=-PI/6, about_point=ORIGIN, run_time=0.5))  # changed
        self.play(FadeToColor(tmp, WHITE))
        tmp.set_opacity(0)
        self.add(hands[main_seq[4]].set_opacity(1))  # changed
        sub1_new = TextMobject('F Lydian($\sharp$5)').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        self.play(Transform(sub1, sub1_new))

        tmp = hands[diatonic_seq[5]].copy().set_opacity(1)  # changed
        self.play(FadeToColor(tmp, YELLOW))
        hands[diatonic_seq[5]].set_opacity(0)  # changed
        self.add_sound('audio_runs/rotate_2.wav', gain=-12)
        self.play(Rotating(tmp, radians=-PI/6, about_point=ORIGIN, run_time=0.5))  # changed
        self.play(FadeToColor(tmp, WHITE))
        tmp.set_opacity(0)
        self.add(hands[main_seq[5]].set_opacity(1))  # changed
        sub1_new = TextMobject('F Lydian($\sharp$5,$\sharp$6)').move_to(DOWN+np.array((0, 0.5, 0))).scale(0.8)  # changed
        self.play(Transform(sub1, sub1_new))

        self.wait(2)
        self.play(FadeOut(sub1))

        # def play altered diatonic scales function
        def play(tonic_name, scale_type, scale_type_alt, replay_on_c=True):
            # generate scales and note pitches
            # warning: when tonic_name = 'G', tonic may equal 'G#'
            scale = AlteredDiatonicScale(tonic_name + ' ' + scale_type)
            c_scale = AlteredDiatonicScale('C'+' '+scale_type)
            notes = [note for note in abs(scale)]
            c_notes = [note for note in abs(c_scale)]
            tonic = notes[0]%12
            c_tonic = c_notes[0]%12
            real_tonic = abs(Note(tonic_name))%12

            # generate text mobjects
            def _scale_text(scale, tonic_name, scale_type_alt):
                scale_text = (
                    tonic_name.replace('b', r'$\flat$').replace('#', r'$\sharp$')+' ',
                    scale_type_alt.replace('b', r'$\flat$').replace('#', r'$\sharp$'),
                    ' | ',
                    *[scale[k].get_name_old(show_group=False).replace('b', r'$\flat$').replace('#', r'$\sharp$') + '\t' for k in range(7)],
                    '({})'.format(scale[0].get_name_old(show_group=False).replace('b', r'$\flat$').replace('#', r'$\sharp$'))
                )
                print(scale_text)
                scale_text = TextMobject(*scale_text).scale(0.8)
                scale_text.move_to(DOWN+np.array((0, 0.5, 0)))
                return scale_text

            scale_text = _scale_text(scale, tonic_name, scale_type_alt)
            scale_text[0].set_color(BLUE)
            if real_tonic in main_seq:
                scale_text[3].set_color(BLUE)
                scale_text[-1].set_color(BLUE)

            # highlight tonic note (blue)
            if real_tonic in main_seq:
                self.play(FadeToColor(hands[real_tonic], BLUE), FadeInFromDown(scale_text))
            else:
                hands[real_tonic].set_opacity(0.5)
                self.play(FadeToColor(hands[real_tonic].set_opacity(0.5), BLUE), FadeInFromDown(scale_text))

            # play the scale with highlight color orange
            def _play(notes, offset, scale_text):
                # note 1
                hands[(notes[0]+offset)%12].set_color(ORANGE)
                scale_text[3].set_color(ORANGE)
                self.add_sound(sounds[notes[0]], gain=-12)
                self.wait(0.5)
                if real_tonic in main_seq:
                    hands[(notes[0]+offset)%12].set_color(BLUE)
                    scale_text[3].set_color(BLUE)
                else:
                    hands[(notes[0]+offset)%12].set_color(WHITE)
                    scale_text[3].set_color(WHITE)
                # note 2-6
                for idx, i in enumerate(notes[1:]):
                    hands[(i+offset)%12].set_color(ORANGE)
                    scale_text[idx+4].set_color(ORANGE)
                    self.add_sound(sounds[i], gain=-12)
                    self.wait(0.5)
                    hands[(i+offset)%12].set_color(WHITE)
                    scale_text[idx+4].set_color(WHITE)
                # note 7
                hands[(notes[0]+offset)%12].set_color(ORANGE)
                scale_text[-1].set_color(ORANGE)
                self.add_sound(sounds[notes[0]+12], gain=-12)
                self.wait(0.5)
                if real_tonic in main_seq:
                    hands[(notes[0]+offset)%12].set_color(BLUE)
                    scale_text[-1].set_color(BLUE)
                else:
                    hands[(notes[0]+offset)%12].set_color(WHITE)
                    scale_text[-1].set_color(WHITE)

            _play(notes, 0, scale_text)
            self.wait(0.5)

            if replay_on_c:
                # generate new text mobjects
                c_scale_text = _scale_text(c_scale, 'C', scale_type_alt)
                c_scale_text[0].set_color(BLUE)
                if real_tonic in main_seq:
                    c_scale_text[3].set_color(BLUE)
                    c_scale_text[-1].set_color(BLUE)
                # rotate and play scale from c
                offset = real_tonic if notes[0]%12 <= 6 else real_tonic-12
                ang = offset*PI/6
                original_scale_text = scale_text.copy()
                self.add_sound('audio_runs/rotate_1.wav', gain=-12)
                self.play(Rotate(hands, ang), Transform(scale_text, c_scale_text))
                self.wait(0.5)
                _play(c_notes, offset, scale_text)
                self.wait(0.5)
                self.add_sound('audio_runs/rotate_1.wav', gain=-12)
                self.play(Rotate(hands, -ang), Transform(scale_text, original_scale_text))

            # de-highlight tonic note
            if real_tonic in main_seq:
                self.play(FadeToColor(hands[real_tonic], WHITE), FadeOut(scale_text))
            else:
                self.play(FadeToColor(hands[real_tonic], WHITE), FadeOut(scale_text))
                hands[real_tonic].set_opacity(0)

        for k in range(7):
            choice = True if k != 1 else False
            play(tonic_names[k], scale_types[k], scale_types_alt[k], choice)

        self.play(FadeInFromDown(sub2))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(clock), FadeOut(sub2))
        extra_note = TextMobject(r'关于Lydian($\sharp$5,$\sharp$6)类音阶还有一些要提及的东西 \\'
                                 r'\phantom{!} \\'
                                 r'$\vdots$ \\'
                                 r'X Phrygian($\sharp$6,$\sharp$7) (Major Neapolitan) = X Dorian($\sharp$7,$\flat$2) \\'
                                 r'$\vdots$').scale(0.8)
        extra_note_alt = TextMobject(r'关于Lydian($\sharp$5,$\sharp$6)类音阶还有一些要提及的东西 \\'
                                     r'\phantom{!} \\'
                                     r'$\vdots$ \\'
                                     r'X Phrygian($\sharp$6,$\sharp$7) (Major Neapolitan) = X Ionian($\flat$2,$\flat$3) \\'
                                     r'$\vdots$').scale(0.8)
        self.play(Write(extra_note))
        self.wait(4)
        self.play(Transform(extra_note, extra_note_alt))
        self.wait(4)
        self.play(FadeOut(extra_note))


class Ending(Scene):
    def construct(self):
        text = TextMobject(r'限于篇幅，视频中只列举了一些常用音阶 \\'
                           r'用排列组合可以算出全部的七声音阶有 66 类，最高 8 阶 \\'
                           r'从第 3 阶(第 23 类)开始，七声音阶的音程结构就已经很诡异了 \\'
                           r"曾经有一个属于第 3 阶的音阶``Enigmatic Scale''在人类历史上出现过 \\"
                           r"它作为配和声的挑战出现在某本杂志上，音程结构被故意设计地不和谐 \\").scale(0.65)
        self.wait(0.5)
        self.play(Write(text))
        self.wait(7.5)
        self.play(FadeOut(text))
        text = TextMobject('感谢观看')
        self.wait(0.5)
        self.play(Write(text))
        self.wait(4.5)
        self.play(FadeOut(text))
