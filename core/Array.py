from manim import *
from core.utils import *
from core.colors import *

# all ABW structures will optionally take a scene
class Array(VGroup):
    class Element(VGroup):
        def __init__(self, scene, *args, **kwargs):
            super().__init__(*args, **kwargs)  # hopefully this doesn't break shit
            self.scene = scene
            mp = {
                # mobs
                "border"        : None,
                "fill"          : None,
                "value"         : None,
                "value_repr"    : None,
                # props
                "outline_color" : BLUE,
                "value_color"   : WHITE,
                "cell_color"    : BLACK,
                "height"        : 1,
                "width"         : 1,
            }
            initWithDefaults(self, mp, **kwargs)
            self.add( self.border )  # VGroup.add(self, self.border)

        # def __setattr__(self, key, value):  # probably unneeded... not sure yet
        #     self.__dict__[key] = value
        #     if key == 'value':
        #         # self.scene.play()  # play the interpolate anim
        #         pass

        def set_val(self, val, **kwargs):  # func
            self.value = val
            new_tex = Tex( str(val) )
            self.scene.play()
            T = Tex()
            T.animate.set_tex_string()
            self.scene.play( self.value_repr.set_tex_ )

        def highlight(self, col):
            self.cell_color = col
            # self.scene.play( self.fill.animate.set_color() )

        def addToScene(self):
            # for mob in self.mobs:
            #     self.scene.add(mob)
            self.scene.add( self.fill )
            self.scene.add( self.border )
            self.scene.add( self.value )
            self.scene.add( self.value_repr )



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
        pass

