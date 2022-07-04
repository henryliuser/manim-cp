from core import *
from manim import *
from common import *

class p13(Scene):
    def construct(self):
        # Beat 13: [Show return trip repeating while ticking timer]
        ax = NumberLine(
            x_range=[0, 9],
            length=10,
            color=BLUE,
            include_numbers=True
        )
        ant = Ant(ax=ax)
        coords = [(3, 2, 0), (5, 4, 0), (7, 1, 1), (8, 6, 1)]
        portals = createPortals(coords, ax)

        self.play(Create(ax))
        self.play(Create(ant.mob))
        self.add_foreground_mobject(ant.mob)
        self.play(*[FadeIn(p.mob) for p in portals])
        portal_arcs(self, portals)
        label = Tex('$t_r$ = return time')
        label.shift(UP)
        self.play(FadeIn(label, rate_func=there_and_back_with_pause, run_time=1.5))

        simulate(self, ant, portals, ax, run_time=.5, indi=False,
                 t=-1, steps=7)
        t = Timer(label='$t_r = $')
        t.mob.move_to(portals[2].mobs.entrance)
        t.mob.shift(DOWN*.7)
        self.play(FadeIn(t.mob))
        simulate(self, ant, portals, ax, run_time=.5, indi=False,
                 t=t, steps=8, start_pos=-1)
        self.play(*t.light())
        self.play(*t.fade())

        simulate(self, ant, portals, ax, run_time=.5, indi=False,
                 t=-1, steps=2, start_pos=-1)

        t = Timer(label='$t_r = $')
        t.mob.move_to(portals[2].mobs.entrance)
        t.mob.shift(DOWN*.7)
        self.play(FadeIn(t.mob))
        simulate(self, ant, portals, ax, run_time=.5, indi=False,
                 t=t, steps=8, start_pos=-1)

        self.play(*t.light())




