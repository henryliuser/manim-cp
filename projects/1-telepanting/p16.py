from core import *
from manim import *
from common import *

# Add sample case (first line, then ant, then portals, then states, then show progression)
class p16(Scene):
    def construct(self):
        ax = NumberLine(
            x_range=[0, 9],
            length=10,
            color=BLUE,
            include_numbers=True
        )

        ant = Ant(ax=ax)
        x = [3, 6, 7, 8]
        y = [2, 5, 4, 1]
        s = [0, 1, 0, 1]
        N = len(x)
        s1 = VGroup(ant.mob, ax)
        coords = [ *map(tuple, zip(x,y,s)) ]
        portals = createPortals(coords, ax)

        self.play(Create(ax))
        self.play(Create(ant.mob))
        self.add_foreground_mobject(ant.mob)
        for p in portals:
            s1.add(p.mob)
            self.play(FadeIn(p.mob))

        s2 = s1.copy().scale(0.6).shift(3*UP)
        self.play( Transform(s1, s2) )

        X_label = Tex("X = ").to_edge(LEFT).shift(UP)
        Y_label = Tex("Y = ").to_edge(LEFT)
        S_label = Tex("S = ").to_edge(LEFT).shift(DOWN)
        labs = [X_label, Y_label, S_label]
        self.play( *map(Write, labs) )

