from manim import *
from core import *
from common import *


class p15(Scene):
    def construct(self):
        n = 5
        cows = gen_random_pasture(n, 30, 60)
        grid = make_grid(cows)
        grid.make_axes()


        self.play(FadeIn(grid.mob), run_time=.5)
        cows, grid = anim_compress(cows, grid, self, rt=.6)
        cows, grid = anim_compress(cows, grid, self, do_x=False, rt=.6)

        new_grid = make_grid(cows)
        new_grid.make_axes()
        new_grid.mob.shift(DOWN)

        self.play(Transform(grid.mob, new_grid.mob), run_time=.5)
        self.play(FadeOut(grid.mob), FadeIn(new_grid.mob), run_time=1/60)
        self.wait(1)

        grid = new_grid
        cl, hs = position()
        coords = (0, 0, 3, 3)
        pg = grid.sub_grid(*coords)

        self.play(FadeIn(pg))
        anims, rt = sweep(coords, grid, cl, rt=1/3)
        self.play(*anims, run_time=rt)
        self.wait(2)
        self.play(FadeIn(hs.mob))
        self.wait(3)
        mob, val = cl.pop(self)
        hs.put(mob, self)
        self.wait(3)
        self.play(FadeOut(pg), *grid.remove_highlights())

        
        n6_alg(grid, self, cl, hs, rt=1/10, start=0, end=10)
        self.play(FadeOut(hs.mob))
        n6_alg(grid, self, cl, hs, rt=1/60, start=10, end=200, add=False)
        
