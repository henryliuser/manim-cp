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

class MyFoo(ABWComponent):
    def __init__(self, **kwargs):
        mobs = {
            "asd"  : Tex('asd'),
            "haha" : Integer(5),
            "dot"  : Dot(),
        }
        props = {
            "elo"  : 500,
            "mmr"  : 2000,
            "cf rating" : 1500,
        }
        super().__init__(mobs, props, kwargs)

class Test(Scene):
    def construct(self):
        mf = MyFoo(
            haha=Integer(6),

        )

        self.play( Create(mf.mob) )
        self.play(Write( Tex(mf.props.elo) ))