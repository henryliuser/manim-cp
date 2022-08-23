from manim import *
from core import *
from common import *


class p3(Scene):
    def construct(self):
        output = Text("Output the number of unique enclosures of cows.",
                      color=GREEN, font_size=40)
        cons = Text("Constraints:", color=RED)
        cow_num = Tex("Number of cows: $0 < n \leq 2500$")
        x_bound = Tex("$0 \leq x \leq 10^9 = $ 1 billion")
        y_bound = Tex("$0 \leq y \leq 10^9 = $ 1 billion")
        unique = Text("No cows share x coordinates or y coordinates.",
                      weight=BOLD, font_size=34)

        output.shift(UP*3)
        cons.shift(UP*1)
        x_bound.shift(DOWN*1)
        y_bound.shift(DOWN*2)
        unique.shift(DOWN*3.5)
        VGroup(output, cons, cow_num, x_bound, y_bound, unique).scale(.7)

        # Competitors were tasked with writing a program that
        self.wait(2)

        # outputs the number of unique enclosures of cows, 
        # given their positions.
        self.play(Create(output), run_time=1.5)
        self.wait(2)

        # the list of up to 2500 cows is provided with
        self.play(Create(cons))
        self.play(Create(cow_num))
        self.wait(1)

        # integer xy-coordinates between 0 and 1 billion, or 10^9
        self.play(Create(x_bound))
        self.play(Create(y_bound))
        self.wait(1)

        # with each x coordinate and each y coordinate being unique
        # from each other.
        self.play(Create(unique))
        self.wait(3)
