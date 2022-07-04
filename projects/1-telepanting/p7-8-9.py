from core import *
from manim import *
from common import *

class p7(Scene):
    def construct(self):
        # Beat 7: Add sample case (first line, then ant, then portals, then states, then show progression)
        ax = NumberLine(
            x_range=[0, 9],
            length=10,
            color=BLUE,
            include_numbers=True,
            line_to_number_buff=MED_LARGE_BUFF,
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

        self.play(*reset_portals(portals, coords))
        b = set([4, 8, 9, 13, 17, 21, 22, 23])
        # c = [4, 1, 5, 4, 4, 1, 1]
        # Beat 8: [Replay ant movement]
        # Beat 9: [Highlight open portals to the left]
        t = simulate(self, ant, portals, ax, run_time=.5, indi=False, steps=1)
        for x in range(22):
            run_time = .5
            simulate(self, ant, portals, ax, run_time=run_time,
                     indi=False, steps=1, t=t, start_pos=-1,
                     hl=True)
            if t.props.t in b:
                a = hlp(ant, portals, run_time=run_time)
                if a or not a:
                    self.play(*a)
        self.play(*t.fade())

        self.play(*reset_portals(portals, coords))

        # t = simulate(self, ant, portals, ax, run_time=.5, indi=False, steps=0)
        # waits = [2, 2]
        # steps = [4, 4]
        # for w, s in zip(waits, steps):
        #     self.wait(w)
        #     simulate(self, ant, portals, ax, run_time=.5, indi=False,
        #              steps=s, t=t)

