from manim import *
from core import *
from common import *


class p17(Scene):
    def construct(self):
        tex = lambda s : Tex(r"\raggedright " + s)

        @cluster
        def alg():
            first = tex("$n^4$ rectangles")
            second = tex("$n^2$ points in each rectangle") 
            third = tex("$n^6$ points to check")
            fourth = tex("$2500^6$ points")
            fifth = tex("$2 \\times 10^{19}$ points")
            A = [first, second, third, fourth, fifth]

            VGroup(*A).arrange(DOWN)
            for x in A[1:]:
                x.align_to(first, LEFT)

            signs = []
            signs.append(MathTex("\\times"))
            signs.append(MathTex("="))
            signs.append(MathTex("\\leq"))
            signs.append(MathTex("\\approx"))

            for sign, x in zip(signs, A[1:]):
                sign.next_to(x, LEFT)
            
            second = VGroup(signs[0], second)
            third = VGroup(signs[1], third)
            fourth = VGroup(signs[2], fourth)
            fifth = VGroup(signs[3], fifth)

        vg = VGroup( *all_vmobs_in(alg) ).center()
        self.wait(1)
        self.play(Create(alg.first))
        self.wait(1)
        self.play(Create(alg.second))
        self.wait(3)
        self.play(Create(alg.third))
        self.wait(1)
        self.play(Create(alg.fourth))
        self.wait(1)
        self.play(Create(alg.fifth))
        self.wait(1)

        c = Circle(radius=0)
        c.shift(LEFT*3+UP*1.5)
        self.play(ScaleAndMove(vg, .6, c))

        self.wait(1)
        final = Tex(r"$\frac{2 \times 10^{19}}{\text{10,000,000/second}} = 63$ thousand years")
        final.shift(DOWN)
        self.play(Create(final), run_time=3)
        self.wait(1)

