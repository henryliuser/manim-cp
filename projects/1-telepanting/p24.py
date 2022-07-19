from manim import *
from common import *
from core import *

class p24(Scene):
    def construct(self):
        ax = NumberLine(
            x_range=[0, 20],
            length=10,
            color=BLUE,
            z_index=-3,
            stroke_width=3
        )
        ant = Ant(ax=ax)
        X = [7,10,13,15,19]
        Y = [3, 2, 8,12, 5]
        S = [1, 1, 1, 1, 1]
        coords = [(7, 3, 1), (10, 2, 1), (13, 8, 1), (15, 12, 1), (19, 5, 1)]
        portals = createPortals(coords, ax)
        self.play( FadeIn(ax), Create(ant.mob) )
        self.add_foreground_mobject(ant.mob)
        self.play( *[FadeIn(p.mob) for p in portals] )

        s1a = VGroup(*all_vmobs_in(self))
        s1b = s1a.copy().scale(0.75).to_edge(UP, buff=1)
        self.play( Transform(s1a, s1b) )

        A = Array(X)
        A.label = MathTex("A =").next_to(A.mob)
        A.mob.add(A.label)
        A.mob.to_corner(DOWN+LEFT, buff=1).shift(UP)
        PS = Array( [0] )
        PS.mob.move_to(A.mob).shift(DOWN)
        self.play( Create(A.mob), Create(PS.mob) )



        self.wait(3)




