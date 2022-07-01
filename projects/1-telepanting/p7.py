from core import *
from manim import *
from common import *

# Add sample case (first line, then ant, then portals, then states, then show progression)
class p7(Scene):
    def construct(self):
        ax = NumberLine(
            x_range=[0, 9],
            length=10,
            color=BLUE,
            include_numbers=True
        )
        ant = Ant(ax=ax)
        coords = [(3, 2, 0),(6, 5, 1),(7, 4, 0),(8, 1, 1)]
        portals = createPortals(coords, ax)

        self.play(Create(ax))
        self.play(Create(ant.mob))
        self.add_foreground_mobject(ant.mob)
        for p in portals:
            self.play(FadeIn(p.mob))

        portal_arcs(self, portals)

        t = simulate(self, ant, portals, ax, run_time=.5, indi=False)

        self.play(*t.fade())

        b = [4, 8, 13, 17, 21, 22, 23]
        c = [5, 5, 4, 4, 1, 1]
        # Beat 8: [Replay ant movement]
        t = simulate(self, ant, portals, ax, run_time=.5, indi=False, steps=4)
        for x in c:
            simulate(self, ant, portals, ax, run_time=.5,
                     indi=False, steps=x, t=t, start_pos=-1)
            self.play(*hlp(ant, portals))