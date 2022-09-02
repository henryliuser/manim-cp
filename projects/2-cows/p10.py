from calendar import c
from manim import *
from core import *
from common import *


class p10(Scene):
    def construct(self):
        cows = [(0, 0), (1, 6), (3, 1)]
        grid = make_grid(cows)
        grid.mob.shift(DOWN)
        rects = [(0, 0, 3, 1), (0, 0, 3, 5), (0, 0, 3, 1)]
        rects.extend(rects[1:] + rects[1:])

        self.play(FadeIn(grid.mob))
        pg = go_through_rects(rects, grid, self, rt=1.5, wt=1/60)

        self.wait(5)
        axes = grid.make_axes()
        self.play(FadeOut(pg), Create(axes))

        cl = CoordinateList()
        cl.mob.shift(UP*2.5 + LEFT*2)

        for x, y in cows:
            self.play(*cl.AddFromAxes(y, x, grid))

        self.wait(1)
        self.play(*cl.sort())
        self.wait(1)
        for x in cl.index():
            self.play(x, run_time=.3)
        self.wait(1)

        all = VGroup(grid.mob, cl.mob)
        all.generate_target()
        all.target.shift(LEFT*2)
        self.play(MoveToTarget(all))

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
        self.wait(3)
        self.play(FadeOut(VGroup(*all_vmobs_in(self))))
        self.wait(1)


