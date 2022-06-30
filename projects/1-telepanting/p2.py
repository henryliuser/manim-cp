from core.utils import *
from manim import *
from common import *

class p2(Scene):
    def construct(self):
        # Beat 4: [Pause, show small simulation]
        ax = NumberLine(
            x_range=[0, 5],
            length=10,
            color=BLUE,
            include_numbers=True
        )
        ant = Ant(ax=ax)
        coords = [(2, 1, 1), (4, 3, 1)]
        portals = createPortals(coords, ax)

        self.play(Create(ax))
        self.play(Create(ant.mob))
        self.add_foreground_mobject(ant.mob)
        for p in portals:
            self.play(FadeIn(p.mob))

        t = simulate(self, ant, portals, ax)
        self.play(*t.fade())