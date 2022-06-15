from manim import *

# prefix sum animation
def psumAnim(A):
    ps = [0]
    for x in A:
        ps += [ x + ps[-1] ]

    class Main(Scene):
        def construct(self):
            pass