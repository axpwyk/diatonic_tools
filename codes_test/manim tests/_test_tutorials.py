#!/usr/bin/env python

from manimlib.imports import *


# To watch one of these scenes, run the following:
# python -m manim example_scenes.py SquareToCircle -pl
#
# Use the flat -l for a faster rendering at a lower
# quality.
# Use -s to skip to the end and just save the final frame
# Use the -p to have the animation (or image, if -s was
# used) pop up once done.
# Use -n <number> to skip ahead to the n'th animation of a scene.
# Use -r <number> to specify a resolution (for example, -r 1080
# for a 1920x1080 video)


class OpeningManimExample(Scene):
    def construct(self):
        title = TextMobject("This is some \\LaTeX")
        basel = TexMobject(
            "\\sum_{n=1}^\\infty "
            "\\frac{1}{n^2} = \\frac{\\pi^2}{6}"
        )
        VGroup(title, basel).arrange(DOWN)
        self.play(
            Write(title),
            FadeInFrom(basel, UP),
        )
        self.wait()

        transform_title = TextMobject("That was a transform")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*map(FadeOutAndShiftDown, basel)),
        )
        self.wait()

        grid = NumberPlane()
        grid_title = TextMobject("This is a grid")
        grid_title.scale(1.5)
        grid_title.move_to(transform_title)

        self.add(grid, grid_title)  # Make sure title is on top of grid
        self.play(
            FadeOut(title),
            FadeInFromDown(grid_title),
            ShowCreation(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()

        grid_transform_title = TextMobject(
            "That was a non-linear function \\\\"
            "applied to the grid"
        )
        grid_transform_title.move_to(grid_title, UL)
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.apply_function,
            lambda p: p + np.array([
                np.sin(p[1]),
                np.sin(p[0]),
                0,
            ]),
            run_time=3,
        )
        self.wait()
        self.play(
            Transform(grid_title, grid_transform_title)
        )
        self.wait()


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(ShowCreation(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


class WarpSquare(Scene):
    def construct(self):
        square = Square()
        self.play(ApplyPointwiseFunction(
            lambda point: complex_to_R3(np.exp(R3_to_complex(point))),
            square
        ))
        self.wait()


class WriteStuff(Scene):
    def construct(self):
        example_text = TextMobject(
            "This is a some text",
            tex_to_color_map={"text": YELLOW}
        )
        example_tex = TexMobject(
            "\\sum_{k=1}^\\infty {1 \\over k^2} = {\\pi^2 \\over 6}",
        )
        group = VGroup(example_text, example_tex)
        group.arrange(DOWN)
        group.set_width(FRAME_WIDTH - 2 * LARGE_BUFF)

        self.play(Write(example_text))
        self.play(Write(example_tex))
        self.wait()


class UpdatersExample(Scene):
    def construct(self):
        decimal = DecimalNumber(
            0,
            show_ellipsis=True,
            num_decimal_places=3,
            include_sign=True,
        )
        square = Square().to_edge(UP)

        decimal.add_updater(lambda d: d.next_to(square, RIGHT))
        decimal.add_updater(lambda d: d.set_value(square.get_center()[1]))
        self.add(square, decimal)
        self.play(
            square.to_edge, DOWN,
            rate_func=there_and_back,
            run_time=5,
        )
        self.wait()


class SimpleMmodN(Scene):
    def construct(self):
        circle,lines = self.get_m_mod_n_objects(3,60)
        self.play(FadeIn(VGroup(circle,lines)))

    def get_m_mod_n_objects(self,x,y):
        circle = Circle().set_height(FRAME_HEIGHT)
        circle.scale(0.85)
        lines = VGroup()
        for i in range(y):
            start_point = circle.point_from_proportion((i%y)/y)
            end_point = circle.point_from_proportion(((i*x)%y)/y)
            line = Line(start_point,end_point).set_stroke(width=1)
            lines.add(line)
        return [circle,lines]


class TangentVector(Scene):
    def construct(self):
        figure = Ellipse(color=RED).scale(2)
        dot = Dot()
        alpha = ValueTracker(0)
        vector = self.get_tangent_vector(alpha.get_value(),figure,scale=2)
        dot.add_updater(lambda m: m.move_to(vector.get_start()))
        self.play(
            ShowCreation(figure),
            GrowFromCenter(dot),
            GrowArrow(vector)
            )
        vector.add_updater(
            lambda m: m.become(
                    self.get_tangent_vector(alpha.get_value()%1,figure,scale=2)
                )
            )
        self.add(vector,dot)
        self.play(alpha.increment_value, 2, run_time=8, rate_func=linear)
        self.wait()

    def get_tangent_vector(self, proportion, curve, dx=0.001, scale=1):
        coord_i = curve.point_from_proportion(proportion)
        coord_f = curve.point_from_proportion(proportion + dx)
        reference_line = Line(coord_i,coord_f)
        unit_vector = reference_line.get_unit_vector() * scale
        vector = Arrow(coord_i, coord_i + unit_vector, buff=0)
        return vector


class D0t(Dot):
    CONFIG = {
        "fill_color": BLUE,
        "fill_opacity": 1,
        "stroke_color": RED,
        "stroke_width": 1.7,
    }


class ParabolaCreation(GraphScene):
    CONFIG = {
        "x_min": -6,
        "x_max": 6,
        "x_axis_width": 12,
        "y_axis_height": 7,
        "graph_origin": 3.5 * DOWN,
        "y_min": 0,
        "y_max": 7,
    }
    def construct(self):
        self.setup_axes()
        self.x_axis.remove(self.x_axis[1])
        self.y_axis.remove(self.y_axis[1])
        self.play(Write(self.axes))

        h = 0; k = 1; p = 1
        parabola_function = lambda x: ((x-h)**2)/(4*p) + k

        parabola_right = self.get_graph(
                parabola_function,
                x_min = 0,
                x_max = 5,
                color = BLUE
            )


        parabola_left = self.get_graph(
                parabola_function,
                x_min = 0,
                x_max = -5,
                color = BLUE
            )
        anim_kwargs = {"run_time":5,"rate_func":linear}
        self.move_dot_path(parabola_right,anim_kwargs)
        self.move_dot_path(parabola_left,anim_kwargs)

    def move_dot_path(self,parabola,anim_kwargs):
        h = 0; k = 1; p = 1
        parabola_copy = parabola.copy()
        focus = D0t(self.coords_to_point(0,2))
        dot_guide = D0t(self.coords_to_point(h,p))
        dot_d = D0t(self.coords_to_point(0,0))
        circle = Circle(radius=1).move_to(self.coords_to_point(h,p))
        line_f_d = DashedLine(focus.get_center(),dot_guide.get_center())
        line_d_d = DashedLine(dot_guide.get_center(),dot_d.get_center())


        group = VGroup(circle,line_f_d,line_d_d,dot_d)

        def update_group(group):
            c,f_d,d_d,d = group
            d.move_to(self.coords_to_point(dot_guide.get_center()[0],0))
            radius = get_norm(focus.get_center() - dot_guide.get_center())
            new_c = Circle(radius = radius)
            new_c.move_to(dot_guide)
            c.become(new_c)
            f_d.become(DashedLine(focus.get_center(),dot_guide.get_center()))
            d_d.become(DashedLine(dot_guide.get_center(),dot_d.get_center()))

        group.add_updater(update_group)

        self.play(
            FadeInFromLarge(circle,scale_factor=2),
            *[GrowFromCenter(mob) for mob in [line_f_d,line_d_d,dot_guide,dot_d,focus]],
            )
        self.add(
            group,
            focus,
            dot_guide,
            )
        self.wait()
        self.add(parabola)
        self.bring_to_back(parabola)
        self.bring_to_back(self.axes)
        self.play(
            MoveAlongPath(dot_guide,parabola_copy),
            ShowCreation(parabola),
            **anim_kwargs
            )
        group.clear_updaters()
        self.wait(1.2)
        self.play(FadeOut(VGroup(group,dot_guide,focus)))
