from manim import *
from utils import *

class Array(VGroup):
    class Element: pass
    def __init__(self, A, **kwargs):
        super().__init__(**kwargs)
        N = len(A)
        idxs = {}
        outline_color = BLUE
        color = WHITE
        width = height = 1
        tw = width * N
        hw = width / 2
        hh = height / 2
        left_element_offset = (width/2) - hw
        left_edge_offset = left_element_offset + hw

        arr = [Rectangle(height=1, width=1) for _ in range(N)]

        # color the cells
        for rect in arr:
            rect.set_color(outline_color)

        # align the cells next to each other
        for i in range(1, N):
            arr[i].next_to(arr[i-1], RIGHT, buff=0)

        self.add(*arr)
        self.elements = VGroup()     # element tex objects
        self.backgrounds = VGroup()  #

        for i,v in enumerate(A):
            if v is not None:
                t = Tex(str(v))
            else:
                t = Tex('.', width=0, height=0, color=BLACK)
            t.move_to(i * RIGHT * width)
            self.elements.add(t)
            b = Rectangle(width=width-0.1, height=height-0.1)
            b.set_stroke(color=BLACK, opacity=0)
            b.move_to(t.get_center())
            self.backgrounds.add(b)

        self.add(self.backgrounds)
        self.elements.set_color(color)
        self.add(self.elements)
        self.move_to( ORIGIN - self.get_center() )

        toReg = {
            "N", "idxs", "width", "height",
            "color", "outline_color", "arr",
        }
        self.props = Props(locals(), toReg)

    def __call__(self, i):
        pass

    def __getitem__(self, i):
        pass
