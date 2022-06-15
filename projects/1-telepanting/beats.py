from manim import *

rainbow = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
# Add sample case (first line, then ant, then portals, then states, then show progression)
class beat7(Scene):
    def construct(self):
        nl = NumberLine(
            x_range=[0, 9],
            length=10,
            color=BLUE,
            include_numbers=True
        )
        self.play(Create(nl))
