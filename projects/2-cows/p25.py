from manim import *
from core import *
from common import *


class p25(Scene):
    def construct(self):
        first = Tex(
            r"$n^4$ rectangles to check $\leq 2500^4$ rectangles $\approx$ 40 trillion")
        first.shift(UP*.7)
        
        final = Tex(r"$\frac{\text{40 trillion}}{\text{10,000,000/second}} = 1$ month")
        
        greater = Tex("$> 2$ seconds").next_to(final).shift(UP*.1)

        vg = VGroup(final, greater)
        vg.center().shift(DOWN*.7)

        self.wait(1)
        self.play(Create(first), run_time=2)
        self.wait(1)
        self.play(Create(final))
        self.wait(7)
        self.play(Create(greater), run_time=.5)
        self.wait(7)
        vg.add(first)
        self.play(FadeOut(vg))
