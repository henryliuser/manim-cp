from manim import *
from core import *
from common import *


class p9(Scene):
    def construct(self):
        cows = gen_random_pasture(4, 10, 10)
        grid = make_grid(cows)
        self.play(FadeIn(grid.mob))
        rects = unwrap_rects(grid)[:135]
        P(self)
        pg = go_through_rects(rects, grid, self, rt=1/12)
        P(self)
        self.play(FadeOut(pg))
        self.play(FadeOut(grid.mob))
        P(self)