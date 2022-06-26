from core.utils import *
from manim import *
from common import *

# [Draw number line, draw ant, move point, draw portals]
class p1(Scene):
    def construct(self):
        ax = NumberLine(
            x_range=[0, 7],
            length=10,
            color=BLUE,
            include_numbers=True
        )
        ant = Ant(ax=ax)
        t = Timer()
        coords = [(3, 2, 1), (5, 4, 1), (6, 1, 1)]
        portals = createPortals(coords, ax)

        self.play(Create(ax))
        self.play(Create(ant.mob))
        self.add_foreground_mobject(ant.mob)

        while ant.props.pos != ax.x_range[1]:
            self.play(*t.tick(), *ant.move(self, []))

        self.play(*t.reset(ant))

        order = [1, 0, 2]
        for i in order:
            self.play(FadeIn(portals[i].mob), run_time=.3)
        # self.play(FadeIn(*[p.mob for p in portals]))

        # beat2: [Blink portals, show ant teleportation and crossing, show toggling]

        # p = portals[0]
        # s = 2.2
        # self.play(ScaleInPlace(p.mobs.entrance, s),
        #           ScaleInPlace(p.mobs.opening, s))
        # self.play(p.toggle())
        # self.play(p.toggle())
        # self.play(ScaleInPlace(p.mobs.entrance, 1/s),
        #           ScaleInPlace(p.mobs.opening, 1/s))
        p = Portal(x=6.5, y=-1000, open=False, ax=ax,
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

        self.play(*[x.show_arc() for x in portals])
        self.play(*[x.show_arrow() for x in portals])
        self.bring_to_back(*[x.mobs.arc for x in portals])
        a = [x.fade_arc() for x in portals]
        a += [Indicate(x.mobs.entrance, run_time=.0001) for x in portals]
        self.play(*a)

        while ant.props.pos != ax.x_range[1]:
            self.play(*t.tick(), *ant.move(self, portals))

