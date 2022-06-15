from manim import *
from utils import *
from colors import *

# all ABW structures will optionally take a scene
class Array(VGroup):
    class Element:
        def __init__(self, scene, **kwargs):
            self.scene = scene
            mp = {
                "value"         : None,
                "outline_color" : BLUE,
                "value_color"   : WHITE,
                "cell_color"    : BLACK,
                "height"        : 1,
                "width"         : 1,
            }
            initWithDefaults(self, mp, **kwargs)

        def __setattr__(self, key, value):
            self.__dict__[key] = value
            if key == 'value':
                # self.scene.play()  # play the interpolate anim
                pass

        def highlight(self, col):
            self.cell_color = col
            # self.scene.play(self.)

    def __init__(self, A, **kwargs):
        super().__init__(**kwargs)
        N = len(A)
        idxs = {}
        outline_color = BLUE
        stroke_width = 5
        color = WHITE
        width = height = 1
        tw = width * N
        hw = width / 2
        hh = height / 2
        left_element_offset = (width/2) - hw
        left_edge_offset = left_element_offset + hw

        # arr = [Array.Element(outline_color, color)]
        arr = []
        for _ in range(N):
            r = Rectangle(height=height, width=width)
            r.set_stroke(outline_color, stroke_width, 1)
            arr += [r]

            # r.set_fill()
        # arr = [Rectangle(height=1, width=1).set_stroke(BLUE, 5, 1) for _ in range(N)]

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
            b = Rectangle(width=width-0.06, height=height-0.06)
            b.set_stroke(LIGHT_ORANGE, 0.7, 0.7)
            b.set_fill(LIGHT_ORANGE, 0.7)
            b.move_to(t.get_center())
            self.backgrounds.add(b)

        self.add(self.backgrounds)
        self.elements.set_color(color)
        self.add(self.elements)
        self.move_to( ORIGIN - self.get_center() )

        toReg = {
            "N", "idxs", "width", "height", "stroke_width",
            "color", "outline_color", "arr",
        }
        self.props = Props(locals(), toReg)

    def __call__(self, i):  # exposes the i-th Array.Element
        pass

    def __getitem__(self, i):  # exposes the i-th Array.Element.value
        pass

