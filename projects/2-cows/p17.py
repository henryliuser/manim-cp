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

            VGroup(first, second, third).arrange(DOWN)
            second.align_to(first, LEFT)
            third.align_to(first, LEFT)

            second_sign = MathTex("\\times")
            third_sign = MathTex("=")

            second_sign.next_to(second, LEFT)
            third_sign.next_to(third, LEFT)

            second = VGroup(second_sign, second)
            third = VGroup(third_sign, third)

        VGroup( *all_vmobs_in(alg) ).center()
        self.wait(1)
        self.play(Create(alg.first))
        self.wait(3)
        self.play(Create(alg.second))
        self.wait(3)
        self.play(Create(alg.third))
        self.wait(1)
        