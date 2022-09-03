from manim import *
from core import *
from common import *


class p18(Scene):
    def construct(self):
        cows = [(3, 1), (1, 2), (4, 0), (0, 3), (2, 4)]
        grid = make_grid(cows)
        grid.make_axes()
        cl, hs = position()
        grid.mob.shift(DOWN)

        self.play(FadeIn(grid.mob), FadeIn(hs.mob))
        n5_alg(grid, self, cl, hs, start=0, stop=10)
        n5_alg(grid, self, cl, hs, start=0, stop=20, rt=1/15)
        self.play(FadeOut(cl), FadeOut(hs))
        n5_alg(grid, self, cl, hs, start=20, rt=1/60, add=False)
