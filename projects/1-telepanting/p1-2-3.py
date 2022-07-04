from core.utils import *
from manim import *
from common import *

class p1(Scene):
    def construct(self):
        # Beat 1: [Draw number line, draw ant, move point, draw portals]
        ax = NumberLine(
            x_range=[0, 7],
            length=10,
            color=BLUE,
            include_numbers=True
        )
        ant = Ant(ax=ax)
        coords = [(3, 2, 1), (5, 4, 1), (6, 1, 1)]
        portals = createPortals(coords, ax)

        self.play(Create(ax))
        self.play(Create(ant.mob))
        self.add_foreground_mobject(ant.mob)

        t = simulate(self, ant, [], ax)
        self.wait(1)
        self.play(*t.fade())
        # self.play(*t.reset(ant))

        order = [1, 0, 2]
        for i in order:
            self.play(FadeIn(portals[i].mob), run_time=.3)

        # Beat 2: [Blink portals, show ant teleportation and crossing, show toggling]

        p = Portal(x=3.5, y=-1000, open=False, ax=ax,
                   color=TEAL, entrance_label='Open')
        p.mob.shift(UP*1.7)
        lStart = Tex('.', color=BLACK).move_to(p.mobs.entrance).shift(UP*.7)
        lOpen = Tex('Open', font_size=30).move_to(lStart)
        lClosed = Tex('Closed', font_size=30).move_to(lStart)
        s = 2.2
        l = VGroup(p.mobs.entrance, p.mobs.opening)
        l.scale(s)
        self.play(FadeIn(p.mobs.entrance, p.mobs.opening))
        self.play(Transform(lStart, lOpen), p.toggle())
        self.wait(1)
        self.play(Transform(lStart, lClosed), p.toggle())
        self.wait(1)
        self.play(ShrinkToCenter(VGroup(lStart, l)))

        portal_arcs(self, portals)

        # Beat 3: [Show ant progressing through a case]
        simulate(self, ant, portals, ax)
        self.wait(1)