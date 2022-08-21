from manim import *
from core import *
from common import *

class sandbox_sam(Scene):
    def construct(self):


        a = gen_random_pasture(4, 4, 7)
        a = [(2, 3), (3, 2), (1, 1), (0, 5)]
        grid = make_grid(a)
        grid.mob.shift(DOWN)
        self.play(Create(grid.mob))
        self.play(Create(grid.make_axes()))
        n = HashSet()
        n.mob.shift(RIGHT*5).shift(UP*2)
        self.play(Create(n.mob))

        l = CoordinateList()
        l.mob.shift(UP*2.5).shift(LEFT*4)
        self.play(Create(l.mob))

        n5_alg(grid, self, l, n)
        self.wait(1)


