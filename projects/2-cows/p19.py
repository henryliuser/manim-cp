from manim import *
from core import *
from common import *


class p19(Scene):
    def construct(self):
        @cluster
        def dimension():
            A = [[None] for _ in range(5)]
            grid = Grid(A)
            self.play(FadeIn(grid.mob))
            self.wait(1)
            gmob = grid.mob
            bracket = MathTex("\\lbrace")
            bracket.width *= 2
            bracket.stretch_to_fit_height(height(grid.mob))
            bracket.scale(.9).next_to(grid.mob, LEFT)
            n = Tex("n").next_to(bracket, LEFT)
            tbracket = MathTex("\\lbrace").rotate(-90 *
                                                DEGREES).next_to(grid.mob, UP)
            tbracket.scale_to_fit_width(width(grid.mob))
            m = MathTex("1").next_to(tbracket, UP)

            self.play(FadeIn(tbracket), FadeIn(m), run_time=.5)
            self.play(FadeIn(bracket), FadeIn(n), run_time=.5)
            self.wait(1)

            anims, rt = sweep((0, 0, 4, 0), grid,
                            CoordinateList(), add=False, color=BLUE, rt=1/6)
            self.play(*anims, run_time=rt)
        
        vg = VGroup(*all_vmobs_in(dimension))
        self.wait(6)

        self.play(FadeOut(vg))

        eq = Tex(r"$n^5 \leq 2500^5 \approx 10^{16} = 10$ quadrillion")
        timeEq = Tex(r"$\frac{10^{16}}{\text{10,000,000/second}}$ = 30 years")


        eq.shift(UP*.5)
        timeEq.shift(DOWN)

        self.play(Create(eq))
        self.wait(5)
        self.play(Create(timeEq))
        self.wait(1)