from manim import *
from core import *


class Test(Scene):
    def construct(self):
        A = Rectangle()
        self.play( Create(A) )

        A.align_

