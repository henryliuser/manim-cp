from manim import *
from core import *
from common import *


class p20(Scene):
    def construct(self):
        cows = [(3, 1), (1, 2), (4, 0), (0, 3), (2, 4)]
        grid = make_grid(cows)
        grid.make_axes()
        grid.mob.shift(LEFT*2)
        mp = x2y(cows).shift(RIGHT*2).scale(.8)
        self.play(FadeIn(grid.mob))

        cl = CoordinateList()
        hs = HashSet()
        n5_alg(grid, self, cl,
               hs, rt=1/3, add=False, start=15, stop=20)
        self.wait(2)
        self.play(Create(mp))
        self.wait(1)
        n4_alg(grid, self, cl,
               hs, mp, add=False, start=15, stop=20)
        self.play(FadeOut(VGroup(mp, grid.mob)))