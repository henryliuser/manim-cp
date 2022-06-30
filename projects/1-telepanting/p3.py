from core.utils import *
from manim import *
from common import *
from random import randint

class p3(Scene):
    def construct(self):
        # Beat 5: [Expand to large road, ant slowly progressing]
        size = 30
        ax = NumberLine(
            x_range=[0, size],
            length=size,
            color=BLUE,
            include_numbers=False
        )
        ant = Ant(ax=ax)
        coords = []
        b = set(range(size))
        for x in range(2, size):
            if randint(0, 3) == 0:
                while 3:
                    a = randint(1, x - 1)
                    if a in b:
                        b.remove(a)
                        b.remove(x)
                        coords.append((x, a, randint(0, 1)))

                        break
        portals = createPortals(coords, ax)
        A = [ant.mob, ax, *[p.mob for p in portals]]

        self.play(Create(ax))
        self.play(Create(ant.mob))
        self.add_foreground_mobject(ant.mob)
        self.play(*[FadeIn(p.mob) for p in portals], run_time=.5)
        self.play(ScaleInPlace(VGroup(*A), 12/size, run_time=3))
        stagger_arcs(self, portals)
        simulate(self, ant, portals, ax, run_time=.1, indi=False)