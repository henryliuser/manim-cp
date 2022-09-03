from manim import *
from core import *
from common import *


class p21(Scene):
    def construct(self):
        n4 = Tex("$n^4$ rectangles to check")
        cl = CoordinateList()
        hs = HashSet()

        cl.mob.shift(LEFT*3.5+DOWN*2)
        hs.mob.shift(UP).scale(1.4)
        hs.props.fs *= 1.4
        cows = [(3, 1), (1, 2), (4, 0), (0, 3), (2, 4)]
        
        self.wait(1)
        self.play(Create(n4))
        self.wait(1)
        self.play(FadeOut(n4))
        for y, x in cows[:4]:
            self.play(*cl.AddWithFade(x, y), run_time=.3)
        
        self.play(FadeIn(hs.mob))
        hs.put(cl.mob, self, iterate=cl.props.coords_mobs)
        self.wait(1)
        self.play(FadeOut(hs.mob))
        