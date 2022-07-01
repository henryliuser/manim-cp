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

        # Beat 8: [Replay ant movement]
        simulate(self, ant, portals, ax, run_time=.5, indi=False, steps=9)

        rf= there_and_back
        a = [ScaleInPlace(x.mobs.entrance, 1.5, rate_func=rf) for x in portals[:2]]
        a += [ScaleInPlace(x.mobs.opening, 1.5, rate_func=rf) for x in portals[:2]]
        self.play(*a)