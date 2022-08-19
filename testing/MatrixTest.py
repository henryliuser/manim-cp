from manim import *
from core import *

class TestMatrix(Scene):
    def construct(self):
        # a = 4.8
        # b = 5
        # line = Rectangle(height=a, width=a, stroke_width=10, color=RED)
        # box = Rectangle(height=b, stroke_width=10, width=b)
        #
        # self.play(Create(line))
        # self.play(Create(box))

        n, m = 20, 20
        mtx = [[Dot() for _ in range(m)] for _ in range(n)]
        grid = Grid(mtx)
        self.play(Create(grid.mob))
        self.play(grid[1][0].anim_highlight(RED))
        self.wait(3)
