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
                Rectangle(height=.95, width=.95,
                          fill_color=my.cell_color,
                          stroke_opacity=0,
                          fill_opacity=0.7),

            "border" :
                Rectangle(height=my.height, width=my.width)
                    .set_stroke(BLUE, my.stroke_width, 1),

            "tex"    : Tex(my.value),
        }
        super().__init__(self.props, mobs, kwargs)

    def anim_set_val(self, val):
        self.props.value = val
        ti = self.mobs.tex
        tf = Tex( str(val) )
        tf.move_to(ti)
        self.mobs.tex = tf
        return Transform(ti, tf)

    def anim_highlight(self, col):
        f = self.mobs.fill
        self.props.cell_color = col
        return f.animate.set_color(col)

class Test(Scene):
    def construct(self):
        A = [Element() for _ in range(5)]
        for i in range(1, 5):
            A[i].mob.next_to(A[i-1].mob, buff=0)

        self.play( *[Create(x.mob,run_time=0.01) for x in A] )
        self.wait(1)
        self.play( A[2].anim_set_val(5) )
        self.wait(1)
        anim = [ A[i].anim_highlight(LIGHT_BROWN) for i in range(3) ]
        self.play( *anim )


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