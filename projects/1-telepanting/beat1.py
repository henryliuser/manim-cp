from core.utils import *
from manim import *
from _common import *

# [Draw number line, draw point, move point, draw portals]
class beat1(Scene):
    ax = NumberLine(
        x_range=[0, 9],
        length=10,
        color=BLUE,
        include_numbers=True
    )
    ant = Ant(ax=ax)
