from manim import *

# props:
# ant
# portal
# axis

class Main(Scene):
    def construct(s):
        sq = Square()
        sq.rotate(PI / 4)
        c = Circle()
        c.set_fill(PINK, opacity=0.5)
        sq.rotate(PI / 4)
        sq2 = Square()
        sq2.set_fill(BLUE, opacity=0.5)
        sq2.next_to(c, DOWN, buff=0.5)
        s.play( Transform(sq, c) )
        s.play( FadeIn(sq2) )

        # epilogue
        s.play( FadeOut(sq) )
        s.play( FadeOut(c) )
        s.play( FadeOut(sq2) )
