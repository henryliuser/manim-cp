from core import *
from manim import *
from common import *
from random import randint, choice


class p10(Scene):
    def construct(self):
        # beat 10: inductive arguments
        ax = NumberLine(
            x_range=[0, 8],
            length=30,
            color=BLUE,
        )
        bx = NumberLine(
            x_range=[0, 12],
            length=10,
            color=BLUE,
        )
        ant = Ant(ax=ax)
        port = [Portal(x=5, y=4, open=0, ax=ax, color=BLUE)]
        self.play(FadeIn(ax))
        self.play(Create(ant.mob))
        self.add_foreground_mobject(ant.mob)
        for p in port:
            self.play(FadeIn(p.mob))
        self.wait(3)

        # beat 11: [Show ant teleporting back, grow size of open portals or smth]
        coords = [(2, 1, 1), (4, 3, 1), (7, 6, 1), (9, 8, 1), (11, 5, 1)]
        portals = createPortals(coords, bx)
        for s in [4, 5]:
            simulate(self, ant, port, ax, run_time=1, indi=False,
                     t=-1, start_pos=2, steps=s)
        fade_ins = [FadeIn(p.mob) for p in portals]
        self.play(Transform(ax, bx), FadeOut(port[0].mob))
        self.play(*fade_ins)
        portal_arcs(self, portals, arrow=True)
        ant = Ant(pos=10, ax=bx)
        self.play(Create(ant.mob))
        self.play(*hlp(ant, portals))
        self.play(*ant.move(self, portals))
        ant.props.pos = 5
        self.play(portals[4].toggle(), ant.anim_pos())
        self.play(*hlp(ant, portals), run_time=2)
        self.play(*hp(portals[2:4]), run_time=2)
        simulate(self, ant, portals, bx, run_time=1 / 5, indi=False, t=-1,
                 start_pos=-1, steps=7)
        self.wait(1)

        # beat 12: [Briefly show chaos of number of possible states,
        # then collapse previous states to open]
        toggles = [(0, 3, 1, 2), (1,), (3, 1), (2,), (2, 1, 3, 0),
                   (1, 3, 2), (1, 3), (0, 1, 2), (3, 0), (1, 0, 2)]
        for tog in toggles:
            a = []
            for x in tog:
                a.append(portals[x].toggle(run_time=.4))
            self.play(*a)
        self.wait(1)
        self.play(*reset_portals(portals, coords))
        self.wait(1)
        
