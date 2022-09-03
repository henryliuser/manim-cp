from manim import *
from core import *
from common import *


class p25(Scene):
    def construct(self):
        first = Tex("number of cows $= n \\leq 2500$", font_size=30)
        second = Tex(
            r"$n^3$ $\leq 2500^3$ $\approx$ 16 billion")
        third = Tex(
            r"$\frac{\text{16 billion}}{\text{10,000,000/second}} = $")
        fourth = Tex(
            r"$n^3$ $\leq 2500^2$ $\approx$ 6 million")
        
        fifth = Tex(
            r"$\frac{\text{6 million}}{\text{10,000,000/second}} = $")
        
        A = [first, second, third, fourth, fifth]
        vg = VGroup(*A)

        vg.arrange(DOWN)
        for x in A[1:]:
            x.align_to(first, LEFT)


        first.shift(UP*.5)
        VGroup(fourth, fifth).shift(DOWN*.5)

        third2 = Tex("$30$ seconds", color=PURE_RED).next_to(third)
        fifth2 = Tex("$\\frac{1}{2}$ second", color=GREEN).next_to(fifth)

        vg.add(third2).add(fifth2)
        vg.center()

        third.add(third2)
        fifth.add(fifth2)

        cows = [(3, 1), (1, 2), (4, 0), (0, 3), (2, 4)]
        grid = make_grid(cows)
        self.play(FadeIn(grid.mob), run_time=.5)
        rects = unwrap_rects(grid)
        pg = go_through_rects(rects, grid, self, rt=1/60, wt=0)
        self.play(FadeOut(pg), run_time=1/60)
        self.play(FadeOut(grid.mob))
        
        self.play(Create(first))
        self.wait(1)
        self.play(Create(second))
        self.wait(1)
        self.play(Create(third))
        self.wait(1)
        self.play(Create(fourth))
        self.wait(1)
        self.play(Create(fifth))
        self.wait(2)
        self.play(FadeOut(vg))
        self.wait(1)


