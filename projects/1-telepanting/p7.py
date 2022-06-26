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
        t = Timer()
        coords = [(3, 2, 0),(6, 5, 1),(7, 4, 0),(8, 1, 1)]
        portals = createPortals(coords, ax)

        self.play(Create(ax))
        self.play(Create(ant.mob))
        self.add_foreground_mobject(ant.mob)
        for p in portals:
            self.play(FadeIn(p.mob))
        self.play(*[x.show_arc() for x in portals])
        self.play(*[x.fade_arc() for x in portals])

        while ant.props.pos != 9:
            self.play(*t.tick(), *ant.move(self, portals))