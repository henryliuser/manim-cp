from manim import *
from core import *
from common import *

class sandbox_sam(Scene):
    def construct(self):
        cows = [(0, 6), (11, 0), (2, 4), (5, 3)]
        grid = make_grid(cows)
        grid.make_axes()
        grid.mob.shift(DOWN + LEFT*2)
        self.play(FadeIn(grid.mob))

        cl = CoordinateList()
        cl.mob.shift(UP*2.5 + LEFT*6)

        for x, y in cows:
            self.play(*cl.AddFromAxes(y, x, grid))
        self.play(*cl.sort())
        self.wait(1)
        for x in cl.index():
            self.play(x, run_time=.3)
        self.wait(1)


        t, c = cl.anim_map()
        t.shift(RIGHT*4)
        self.play(*c)
        self.wait(1)

        anims = cl.fill_map(t[0])
        for x in anims:
            self.play(x)
        self.wait(1)


        new_cows, new_grid = anim_compress(cows, grid, self)
        self.play(FadeOut(t))

        self.play(*cl.sort(y=True))
        t, c = cl.anim_map(do_y=True)
        t.shift(RIGHT*4)
        self.play(*c)
        self.wait(1)


        anims = cl.fill_map(t[0], do_y=True)
        for x in anims:
            self.play(x, run_time=.5)
        self.wait(1)


        anim_compress(new_cows, new_grid, self, do_x=False)
        self.wait(1)

        # a = [(2, 3), (3, 2), (1, 1)]
        # grid = make_grid(a)
        # grid.make_axes()
        # grid.mob.shift(DOWN)
        # self.play(FadeIn(grid.mob))
        # n = HashSet()
        # n.mob.shift(RIGHT*5).shift(UP*2)
        # self.play(FadeIn(n.mob))

        # l = CoordinateList()
        # l.mob.shift(UP*2.5).shift(LEFT*4)
        # self.play(Create(l.mob), run_time=1/60)

        # n5_alg(grid, self, l, n)
        # self.wait(1)

