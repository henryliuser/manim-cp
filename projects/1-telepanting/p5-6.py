from core.utils import *
from manim import *
from common import *
from random import randint


class p3(Scene):
    def construct(self):
        # Beat 5: [Expand to large road, ant slowly progressing]
        size = 100
        ax = NumberLine(
            x_range=[0, size],
            length=size,
            color=BLUE,
            include_numbers=False
        )
        coords = [(2, 1, 0), (7, 3, 1), (9, 6, 1), (10, 8, 0), (13, 12, 0), (16, 14, 0), (18, 5, 1), (21, 17, 0),
                  (26, 11, 0), (29, 28, 0), (30, 19, 0), (31, 15, 1), (35, 22, 1), (42, 33, 0), (44, 36, 1), (46, 38,
                                                                                                              1),
                  (47, 32, 0), (55, 45, 0), (59, 48, 0), (60, 40, 1), (65, 25, 1), (67, 34, 0), (68, 64, 0),
                  (74, 24, 0), (78, 69, 1), (90, 81, 1), (91, 43, 1), (97, 61, 0)]
        # coords = []
        # b = set(range(size))
        # for x in range(2, size):
        #     if randint(0, 3) == 0:
        #         while 3:
        #             a = randint(1, x - 1)
        #             if a in b:
        #                 b.remove(a)
        #                 b.remove(x)
        #                 coords.append((x, a, randint(0, 1)))
        #                 break
        # raise OSError(coords)
        portals = createPortals(coords, ax)
        a = []
        for p in portals:
            a.append(VGroup(p.mobs.entrance, p.mobs.exit, p.mobs.opening))

        A = [ax, *a]

        self.play(Create(ax), run_time=.1)
        self.play(*[FadeIn(x) for x in a], run_time=.5)

        self.play(ScaleInPlace(VGroup(*A), 12 / size, run_time=3))
        stagger_arcs(self, portals, arrow=False)
        ant = Ant(ax=ax)
        self.play(Create(ant.mob))
        self.add_foreground_mobject(ant.mob)
        t = simulate(self, ant, portals, ax, run_time=1 / 3, indi=False,
                     steps=6, start_pos=-1)
        simulate(self, ant, portals, ax, run_time=1 / 10, indi=False,
                 steps=20, start_pos=-1, t=t)
        simulate(self, ant, portals, ax, run_time=1 / 60,
                 indi=False, start_pos=-1, t=t, steps=240)
        self.wait(1)
        # fade out in post
