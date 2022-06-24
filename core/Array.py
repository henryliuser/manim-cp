from manim import *
from core import *

# all ABW structures will optionally take a scene
class Array(VGroup):
    class Element(VGroup):
        def __init__(self, **props):
            props = {
                "outline_color" : BLUE,
                "value_color"   : WHITE,
                "cell_color"    : BLACK,
                "height"        : 1,
                "width"         : 1,
                "stroke_width"  : 5,
                "value"         : None,
            }
            mobs = {

                "tex"    : Tex(),
                "border" :
                    Rectangle(height=1, width=1).set_stroke(BLUE, 5, 1),
                "fill"   :
                    Rectangle(height=.95, width=0.95).set_fill(BLACK, 0.7),
            }
            mobs = Namespace(mobs, props)
            super().__init__(mobs, props)


        # def __setattr__(self, key, value):  # probably unneeded... not sure yet
        #     self.__dict__[key] = value
        #     if key == 'value':
        #         # self.scene.play()  # play the interpolate anim
        #         pass

        def anim_set_val(self, val):
            self.mobs.value = val
            ti = self.mobs.tex
            tf = Tex( str(val) )
            self.mobs.tex = tf
            return Transform(ti, tf)

        def anim_highlight(self, col):
            f = self.mobs.fill
            self.cell_color = col
            return f.animate.set_color(col)

        # def slice(self, ):
        #     pass

        def add_to_scene(self, scene):
            for mob in self.mobs:
                scene.add(mob)

    def init(self, A, **kwargs):
        super().__init__(**kwargs)
        arr = []
        for x in A:
            e = Array.Element(value=x)
            arr += [e]

        mobs = {
            "arr" : arr,
        }
        props = {
            "N" : len(A),
        }
        initWithDefaults(self, mobs, props, **kwargs)



    def __init__(self, A, **kwargs):
        super().__init__(**kwargs)
        # BEGIN PROPS
        N = len(A)
        border_color = BLUE
        fill_color = BLACK
        highlight_color = LIGHT_ORANGE
        fill_opacity = 0.7
        stroke_width = 5
        color = WHITE
        width = height = 1
        # END PROPS

        tw = width * N
        hw = width / 2
        hh = height / 2
        left_element_offset = (width/2) - hw
        left_edge_offset = left_element_offset + hw

        arr = []
        for _ in range(N):
            # color the border
            b = Rectangle(height=height, width=width)
            b.set_stroke(border_color, stroke_width, 1)
            f = Rectangle(height=height-0.05, width=width-0.05)
            f.set_fill(fill_color, fill_opacity)
            # e = Array.Element(self.scene, b, f)
            # arr += [e]
            arr += [b]

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
            b.set_stroke(fill_color, 0.7, 0.7)
            b.set_fill(fill_color, 0.7)
            b.move_to(t.get_center())
            self.backgrounds.add(b)

        self.add(self.backgrounds)
        self.elements.set_color(color)
        self.add(self.elements)
        self.move_to( ORIGIN - self.get_center() )

        toReg = {
            "N", "idxs", "width", "height", "stroke_width",
            "color", "border_color", "arr",
        }
        self.props = Props(locals(), toReg)

    def __call__(self, i):  # exposes the i-th Array.Element
        pass

    def __getitem__(self, i):  # exposes the i-th Array.Element.value
        return self.arr[i]

