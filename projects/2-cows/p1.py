from manim import *
from core import *
from common import *


class p1(Scene):
    def construct(self):
        fence_color = "#C4A484"
        cell_color = "#005400"
        outline_color = DARKER_GRAY

        # Farmer John is in charge of a herd of cows on a pasture.
        cows = [(0, 0), (2, 1), (1, 2)]
        grid = make_grid(cows, color=cell_color, outline_color=outline_color)
        grid.mob.shift(DOWN*.5)
        self.play(FadeIn(grid.mob))
        self.wait(3.5)

        # He plans to make a rectangular fence
        pg = grid.sub_grid(1, 1, 1, 1, color=fence_color)
        mins = minimal_enclosures(grid, cows)[:4] + [(1, 1, 1, 1)]
        self.play(FadeIn(pg))
        self.wait(.5)

        # enclosing some of his cows.
        for x, y in cows:
            self.play(ScaleInPlace(grid[x][y].mobs.val, 1.2,
                                   rate_func=there_and_back), run_time=.6)
        self.wait(.5)

        # He wants to know how many different subsets of cows he can possibly enclose,
        pg = go_through_rects(mins, grid, self, pg=pg,
                              rt=.5, color=fence_color)
        
        # provided he orients the fencing parallel to 
        pg.set_color(PURE_RED)
        self.play(Rotate(pg, 90*DEGREES))
        pg.set_color(fence_color)

        # the x and y axes
        self.play(Create(grid.make_axes()))
        self.play(FadeOut(pg))

        cl = CoordinateList()
        cl.mob.shift(UP*2.8 + LEFT*2)
        for x, y in sorted(cows, key=lambda x:x[1]):
            res = [ScaleInPlace(grid[x][y].mobs.val, 1.4,
                                   rate_func=there_and_back_with_pause)]
            res.extend(cl.AddFromAxes(y, x, grid))
            self.play(*res, run_time=1)
        
        self.wait(1)
