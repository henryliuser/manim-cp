from core import *
from manim import *
from common import *
from random import randint, choice


class p15(Scene):
    def construct(self):
        # beat 15: [Count return trip, put cost by entrance,
        # show return trip spanning multiple entrances,
        # smoosh costs in between while using line segments to indicate adding distance]
        ax = NumberLine(
            x_range=[0, 20],
            length=10,
            color=BLUE,
            z_index=-3,
            stroke_width=3
        )
        ant = Ant(ax=ax)
        coords = [(7, 3, 1), (10, 2, 1), (13, 8, 1), (15, 12, 1), (19, 5, 1)]
        portals = createPortals(coords, ax)
        self.play(FadeIn(ax))
        self.play(Create(ant.mob))
        self.add_foreground_mobject(ant.mob)
        self.play(*[FadeIn(p.mob) for p in portals])
        portal_arcs(self, portals)
        # simulate(self, ant, portals, ax, indi=False, run_time=1/60,
        #          steps=7, t=-1)

        # t = Timer(label='$t_r = $')
        # t.mob.move_to(portals[0].mobs.entrance)
        # t.mob.shift(DOWN*.7)
        # self.play(FadeIn(t.mob))
        # simulate(self, ant, portals, ax, run_time=.5, indi=False,
        #          t=t, steps=4, start_pos=-1)
        # t.mob.generate_target()
        # t.mob.target.move_to(portals[0].mobs.entrance).shift(UP*.45)
        # t.mob.target.scale(.5)
        # self.play(MoveToTarget(t.mob))
        d = portal_map(portals)
        while ant.props.pos != 12:
            simulate(self, ant, portals, ax, indi=False, run_time=.5,
                     steps=1, t=-1, start_pos=-1)
            x = ant.props.pos
            if x in d and d[x][1].props.open and len(d[x][0]) > 1:
                return_trip(self, ant, portals, ax)
        self.wait(1)
