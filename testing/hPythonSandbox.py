from core import *

class actually_funny(Scene):
    def construct(self):
        @cursed.namespace
        def eq():
            x = 5
            vg = VGroup( Rectangle(), Circle() )
            self.play( Create(MathTex("123")) )
            print((x + 1) * 3)
            y = 2 + x - 10 * 2

        self.play( Create(eq.vg.to_edge(UP)) )
        self.play( Create(Mono(rf"{eq.x, eq.y, [*all_vmobs_in(eq)]}").to_edge(DOWN)) )
        self.wait()

