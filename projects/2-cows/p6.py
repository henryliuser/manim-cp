from manim import *
from core import *
from common import *


class p6(Scene):
    def construct(self):
        # Our next idea may be to simply try every possible rectanagle and
        # see how many unique enclosures we end up with.
        cows = [(0, 0), (1, 2)]
        grid = make_grid(cows)

        self.play(FadeIn(grid.mob))

        rects = unwrap_rects(grid)
        pg = go_through_rects(rects, grid, self)

        fades = [pg, grid.mob]
        self.play(*[FadeOut(x) for x in fades])

        # There are two glaring issues with this approach. 
        # First of all, to store the 
        # entire grid in memory would take 125,000,000 gigabytes of RAM.	
        cows = gen_random_pasture(20, 30, 60)
        
        grid = make_grid(cows)
        grid.make_axes()
        grid.mob.scale(10)
        self.play(FadeIn(grid.mob))
        self.play(ScaleInPlace(grid.mob, .1))

        self.wait(1)
        self.play(FadeOut(grid.mob))
