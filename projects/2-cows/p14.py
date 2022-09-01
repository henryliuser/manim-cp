from manim import *
from core import *
from common import *


class p14(Scene):
    def construct(self):
        cow_num = Tex("Number of cows $= n \leq 2500$")
        x_bound = Tex("$0 \leq x \leq 10^9 = $ 1 billion")
        y_bound = Tex("$0 \leq y \leq 10^9 = $ 1 billion").shift(DOWN)
        bounds = VGroup(x_bound, y_bound)
        before = Tex("Before: up to $(10^9)^4 = 10^{36}$ rectangles")
        after = Tex(
            r"After: up to $(2500)^4 \approx 4 \times 10^{13} =$ 40 trillion rectangles")
        difference = Tex(
            r"$\frac{10^{36}}{4 * 10^{13}} \approx 2.5 \times 10^{22} =$ 25 sextillion times faster")

        bounds.shift(UP*3 + LEFT*3.5)
        cow_num.shift(UP*2.5 + RIGHT*3.5)

        before.shift(DOWN*0)
        after.shift(DOWN*1)
        difference.shift(DOWN*2)

        self.wait(2)
        self.play(Create(bounds))
        self.wait(1)
        self.play(Create(cow_num))
        self.wait(1)


        self.play(Create(before), run_time=2)
        self.wait(3)
        self.play(Create(after), run_time=3)
        self.wait(7)
        self.play(Create(difference), run_time=2)
        self.wait(3)
        self.play(FadeOut(VGroup(*all_vmobs_in(self))))

