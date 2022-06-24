from manim import *
from core import *

# class Main(Scene):
#     def construct(self):
#         t1 = Tex('5asd')
#         t2 = Tex('asdqwpoe')
#         self.play( Indicate(t1) )
#         self.play(
#             Transform(t1, t2),
#             Indicate(t1),
#         )

class Element(ABWComponent):
    def __init__(self, **kwargs):
        props = {
            "outline_color" : BLUE,
            "value_color"   : WHITE,
            "cell_color"    : BLACK,
            "height"        : 1,
            "width"         : 1,
            "stroke_width"  : 5,
            "value"         : 0,
        }
        my = self.props = Namespace(props, kwargs)
        mobs =  {
            "fill"   :
                Rectangle(height=.95, width=0.95, color=my.cell_color)
                    .set_fill(my.cell_color, opacity=0.7),

            "border" :
                Rectangle(height=my.height, width=my.width)
                    .set_stroke(BLUE, my.stroke_width, 1),

            "tex"    : Tex(my.value),
        }
        super().__init__(props, mobs, kwargs)

class Test(Scene):
    def construct(self):
        e = Element(stroke_width=5)
        self.play( Create(e.mob), run_time=0.001 )
        self.wait(1)


# class MyFoo(ABWComponent):
#     def __init__(self, **kwargs):
#         props = {
#             "elo"  : 500,
#             "mmr"  : 2000,
#             "cf_rating" : 1500,
#         }
#         super().__init__(locals(), props, kwargs)
#         mobs = {
#             "asd"  : Tex('asd'),
#             "haha" : Integer(5),
#             "dot"  : Dot(),
#             "cfr"  : Tex(cf_rating)
#         }
#
#
#
# class Test(Scene):
#     def construct(self):
#         mf = MyFoo(
#             haha=Integer(6),
#         )
#         self.play( Create(mf.mob) )
#         self.play(Write( Tex(mf.props.elo) ))