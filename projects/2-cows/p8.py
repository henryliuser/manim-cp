from manim import *
from core import *
from common import *


class p8(Scene):
    def construct(self):
        @cluster
        def alg():
            first = Tex("$0 \leq x \leq 10^9 = $ 1 billion")
            second = Tex("$0 \leq y \leq 10^9 = $ 1 billion")
            third = Tex("$(10^9)^2=10^{18}$ points")
            fourth = Tex("$(10^{18})^2=10^{36}$ pairs of points")
            fifth = Tex("$10^{36}$ possible rectangles")
            A = [first, second, third, fourth, fifth]
            vg = VGroup(*A)
            vg.arrange(DOWN)
            for x in A[1:]:
                x.align_to(first, LEFT)
            vg.move_to(center(TOP_LEFT, BOT_MID)).scale(.7)
        self.play(Create(alg.vg))

        div = split()
        self.play(FadeIn(div))

        dimens = [(2, 2), (3, 2.5), (1, 4), (5, 1), (4, 3.5), (2.5, 2), (1.5, 2.5)]
        vg = None
        for x, y in dimens:
            r = Rectangle(height=x, width=y).move_to(center(TOP_RIGHT, BOT_MID))
            tl = Dot().move_to(r.get_corner(UP + LEFT)).scale(1.3)
            br = Dot().move_to(r.get_corner(DOWN+RIGHT)).scale(1.3)


            nvg = VGroup(tl, br, r)
            if vg is None:
                self.play(Create(nvg))
                vg = nvg
            else:
                self.play(Transform(vg, nvg))

        self.play(FadeOut(vg))


        final = Tex(r"$\frac{10^{36}}{\text{10,000,000/second}} = 10^{21}$ years")
        final.move_to(center(TOP_RIGHT, BOT_MID))
        self.wait(7)
        self.play(Create(final))
        self.wait(4)
    