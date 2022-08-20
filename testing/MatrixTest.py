from manim import *
from core import *

class TestMatrix(Scene):
    def construct(self):
        n, m = 10, 10
        mtx = [[Dot() for _ in range(m)] for _ in range(n)]
        grid = Grid(mtx)
        self.play(Create(grid.mob))
        self.play(grid[1][0].anim_highlight(RED))

        self.play(Create(grid.sub_grid(4, 5, 2, 1)))

        self.wait(3)

        self.wait(1)

