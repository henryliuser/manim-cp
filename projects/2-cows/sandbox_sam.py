from manim import *
from core import *
from common import *

class sandbox_sam(Scene):
    def construct(self):


        # a = gen_random_pasture(2, 2, 2)
        # a = [(0, 1), (1, 0)]
        a = [(2, 3), (3, 2), (1, 1)]
        grid = make_grid(a)
        grid.make_axes()
        grid.mob.shift(DOWN)
        self.play(FadeIn(grid.mob))
        n = HashSet()
        n.mob.shift(RIGHT*5).shift(UP*2)
        self.play(FadeIn(n.mob))

        l = CoordinateList()
        l.mob.shift(UP*2.5).shift(LEFT*4)
        self.play(Create(l.mob), run_time=1/60)

        n5_alg(grid, self, l, n)
        self.wait(1)

