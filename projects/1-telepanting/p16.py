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

        N = 4
        ant = Ant(ax=ax)
        X = Array( [3, 6, 7, 8] )
        Y = Array( [2, 5, 4, 1] )
        S = Array( [0, 1, 0, 1] )

        s1 = VGroup(ant.mob, ax)
        coords = [ *zip(X.og,Y.og,S.og) ]
        portals = createPortals(coords, ax)

        self.play(Create(ax))
        self.play(Create(ant.mob))
        self.add_foreground_mobject(ant.mob)

        mp = portal_map(portals)
        for p in portals:
            s1.add(p.mob)
            self.play(FadeIn(p.mob))

        s2 = s1.copy().scale(0.8).shift(3*UP)
        self.play( Transform(s1, s2) )

        X.label = Mono("X = ").center().to_edge(LEFT).shift(1.2*UP)
        Y.label = Mono("Y = ").center().to_edge(LEFT)
        S.label = Mono("S = ").center().to_edge(LEFT).shift(1.2*DOWN)
        self.play( *[Write(o.label) for o in (X,Y,S) ] )

        for o in [X,Y,S]:
            o.mob.next_to(o.label, RIGHT)

        self.play( *[Create(o.mob) for o in (X,Y,S) ] )

        # TODO: after entrance becomes coupled with the dot and stuff, adjust
        for A in [X,Y,S]:
            for i in range(N):
                # portal object : {entrance, exit}
                pobj = mp[ A.og[i] ] if A != S else mp[ X.og[i] ]
                high = A[i].anim_highlight(LIGHT_BROWN, rate_func=there_and_back_with_pause)
                indi = Indicate(pobj, scale_factor=1.75)
                self.play( indi, high )

        self.wait(3)

        dp = Array( ['?'] * N )
        dp.mob.to_edge(RIGHT)
        dp.label = Mono("dp = ").next_to(dp.mob, LEFT)
        self.play( Write(dp.label), Create(dp.mob) )

        self.wait(3)

class p17(Scene):
    def construct(self):
        pass