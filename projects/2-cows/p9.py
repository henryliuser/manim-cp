from manim import *
from core import *
from common import *


class p9(Scene):
    def construct(self):
        cows = [(9, 1), (6, 16), (0, 7), (4, 19)]
        grid = make_grid(cows)
        self.play(FadeIn(grid.mob))
        rects = unwrap_rects(grid)[1100:1106]
        go_through_rects(rects, grid, self, rt=1/2)
        self.wait(1)