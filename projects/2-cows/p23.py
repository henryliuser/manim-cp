from manim import *
from core import *
from common import *


class p23(Scene):
    def construct(self):
        c1, c2 = BLUE, PURE_RED
        cows = [(3, 1), (1, 2), (4, 0), (0, 3), (2, 4)]
        grid = make_grid(cows)
        self.play(FadeIn(grid.mob))
        self.wait(8)
        rects = [(1, 0, 3, 3), (1, 0, 3, 2), (1, 1, 3, 2)]
        pg = go_through_rects(rects, grid, self, rt=1)

        rects = unwrap_rects(grid)[10:150:20]
        rects = shrinking_rects(rects, grid, cows)


        self.wait(1)
        pg = gtr_minimal(rects, grid, self, cows, rt=1/2,
                         pg=pg, col=c1, color=c2)
        pg.set_color(c1)
        self.play(FadeOut(pg), run_time=.5)

        rects = unwrap_rects(grid)
        pg = gtr_minimal(rects, grid, self, cows, rt=1/30,
                         pg=pg, col=c1, color=c2, 
                         always_wait=False, wt=1/2)
        self.play(FadeOut(pg), run_time=1/60)
        self.play(FadeOut(grid.mob))
        self.wait(1)
